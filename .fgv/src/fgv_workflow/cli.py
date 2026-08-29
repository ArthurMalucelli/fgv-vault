import argparse
import ctypes
import json
import os
from pathlib import Path
import secrets
import stat
import sys
from typing import Callable

from .adapters import stage_adapters
from .locking import vault_lock
from .transaction import apply_transaction, build_plan, run_state


def plan_for_runtime(
    *,
    runtime: str,
    vault_root: Path,
    source: Path,
    analysis_path: Path,
    class_date: str,
) -> dict:
    return build_plan(
        runtime=runtime,
        vault_root=vault_root,
        source=source,
        analysis_path=analysis_path,
        class_date=class_date,
    )


def refresh_state(
    vault_root: Path,
    *,
    as_of: str,
    check: bool = False,
    runner: Callable[[list[str]], int] | None = None,
) -> int:
    with vault_lock(vault_root):
        return run_state(vault_root, as_of, check=check, runner=runner)


def apply_plan(
    plan: dict,
    *,
    vault_root: Path,
    source: Path,
    analysis_path: Path,
    processor: str,
    as_of: str,
    state_runner: Callable[[list[str]], int] | None = None,
    fault_hook: Callable[[str], None] | None = None,
) -> dict:
    return apply_transaction(
        plan,
        vault_root=vault_root,
        source=source,
        analysis_path=analysis_path,
        processor=processor,
        as_of=as_of,
        state_runner=state_runner,
        fault_hook=fault_hook,
    )


def _absolute_lexical(path: Path) -> Path:
    return Path(os.path.abspath(os.fspath(path)))


def _secure_nofollow_flag() -> int:
    nofollow = getattr(os, "O_NOFOLLOW", None)
    if type(nofollow) is not int or nofollow == 0:
        raise RuntimeError("secure plan output requires O_NOFOLLOW support")
    required_dir_fd = (os.open, os.stat, os.mkdir, os.rmdir, os.unlink)
    if any(operation not in os.supports_dir_fd for operation in required_dir_fd):
        raise RuntimeError("secure plan output requires dir_fd support")
    if os.stat not in os.supports_follow_symlinks:
        raise RuntimeError("secure plan output requires nofollow stat support")
    return nofollow


def _open_directory_without_symlinks(path: Path) -> int:
    if not path.is_absolute():
        raise ValueError(f"output parent must be absolute: {path}")
    directory_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
    )
    nofollow = _secure_nofollow_flag()
    descriptor = os.open(path.anchor, directory_flags)
    try:
        if not stat.S_ISDIR(os.fstat(descriptor).st_mode):
            raise NotADirectoryError(f"output parent is not a directory: {path.anchor}")
        for component in path.parts[1:]:
            try:
                next_descriptor = os.open(
                    component,
                    directory_flags | nofollow,
                    dir_fd=descriptor,
                )
            except OSError as error:
                raise ValueError(
                    f"output parent must exist without symlink traversal: {path}"
                ) from error
            try:
                if not stat.S_ISDIR(os.fstat(next_descriptor).st_mode):
                    raise NotADirectoryError(
                        f"output parent is not a directory: {path}"
                    )
            except BaseException:
                os.close(next_descriptor)
                raise
            os.close(descriptor)
            descriptor = next_descriptor
        return descriptor
    except BaseException:
        os.close(descriptor)
        raise


def _publish_descriptor_exclusive(
    source_descriptor: int,
    parent_descriptor: int,
    destination_name: str,
) -> None:
    if sys.platform == "darwin":
        function_name = "fclonefileat"
        argument_types = (
            ctypes.c_int,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_uint,
        )
        arguments = (
            source_descriptor,
            parent_descriptor,
            os.fsencode(destination_name),
            0,
        )
    elif sys.platform.startswith("linux"):
        function_name = "linkat"
        argument_types = (
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
            ctypes.c_char_p,
            ctypes.c_int,
        )
        arguments = (
            -100,
            os.fsencode(f"/proc/self/fd/{source_descriptor}"),
            parent_descriptor,
            os.fsencode(destination_name),
            0x00000400,
        )
    else:
        raise RuntimeError("secure plan output requires descriptor publication")

    library = ctypes.CDLL(None, use_errno=True)
    try:
        publish = getattr(library, function_name)
    except AttributeError as error:
        raise RuntimeError(
            "secure plan output requires descriptor publication"
        ) from error
    publish.argtypes = argument_types
    publish.restype = ctypes.c_int
    ctypes.set_errno(0)
    result = publish(*arguments)
    if result != 0:
        error_number = ctypes.get_errno()
        raise OSError(
            error_number,
            os.strerror(error_number),
            destination_name,
        )


def _open_anonymous_plan_file(parent_descriptor: int, nofollow: int) -> int:
    if sys.platform.startswith("linux"):
        temporary = getattr(os, "O_TMPFILE", None)
        if type(temporary) is not int or temporary == 0:
            raise RuntimeError("secure plan output requires O_TMPFILE support")
        return os.open(
            ".",
            os.O_RDWR | temporary | getattr(os, "O_CLOEXEC", 0),
            0o600,
            dir_fd=parent_descriptor,
        )
    if sys.platform != "darwin":
        raise RuntimeError("secure plan output requires anonymous file support")

    staging_name = None
    for _attempt in range(128):
        candidate = f".fgv-plan-{secrets.token_hex(16)}.stage"
        try:
            os.mkdir(candidate, 0o700, dir_fd=parent_descriptor)
        except FileExistsError:
            continue
        staging_name = candidate
        break
    else:
        raise FileExistsError("could not reserve private plan staging")

    directory_flags = (
        os.O_RDONLY
        | getattr(os, "O_CLOEXEC", 0)
        | getattr(os, "O_DIRECTORY", 0)
        | nofollow
    )
    staging_descriptor: int | None = None
    payload_descriptor: int | None = None
    staging_exists = True
    payload_linked = False
    try:
        staging_descriptor = os.open(
            staging_name,
            directory_flags,
            dir_fd=parent_descriptor,
        )
        payload_descriptor = os.open(
            "payload",
            os.O_RDWR
            | os.O_CREAT
            | os.O_EXCL
            | getattr(os, "O_CLOEXEC", 0)
            | nofollow,
            0o600,
            dir_fd=staging_descriptor,
        )
        payload_linked = True
        os.unlink("payload", dir_fd=staging_descriptor)
        payload_linked = False
        os.rmdir(staging_name, dir_fd=parent_descriptor)
        staging_exists = False
        result = payload_descriptor
        payload_descriptor = None
        return result
    finally:
        if staging_exists:
            if staging_descriptor is not None and payload_linked:
                try:
                    os.unlink("payload", dir_fd=staging_descriptor)
                except OSError:
                    pass
                else:
                    payload_linked = False
            if not payload_linked:
                try:
                    os.rmdir(staging_name, dir_fd=parent_descriptor)
                except OSError:
                    pass
        if payload_descriptor is not None:
            os.close(payload_descriptor)
        if staging_descriptor is not None:
            os.close(staging_descriptor)


def _write_plan_output(
    output: Path,
    data: bytes,
    *,
    source: Path,
    analysis_path: Path,
) -> None:
    nofollow = _secure_nofollow_flag()
    output_path = _absolute_lexical(output)
    if not output_path.name:
        raise ValueError("plan output must name a file")
    output_canonical = output_path.resolve(strict=False)
    for label, protected in (("source", source), ("analysis", analysis_path)):
        protected_canonical = _absolute_lexical(protected).resolve(strict=True)
        if output_canonical == protected_canonical:
            raise ValueError(f"plan output must differ from {label}")

    parent_descriptor = _open_directory_without_symlinks(output_path.parent)
    output_descriptor: int | None = None
    try:
        try:
            os.stat(
                output_path.name,
                dir_fd=parent_descriptor,
                follow_symlinks=False,
            )
        except FileNotFoundError:
            pass
        else:
            raise FileExistsError(f"plan output already exists: {output_path}")

        output_descriptor = _open_anonymous_plan_file(
            parent_descriptor,
            nofollow,
        )

        opened = os.fstat(output_descriptor)
        if not stat.S_ISREG(opened.st_mode):
            raise IOError(f"temporary plan output is not a regular file: {output_path}")

        remaining = memoryview(data)
        while remaining:
            try:
                written = os.write(output_descriptor, remaining)
            except InterruptedError:
                continue
            if written <= 0:
                raise IOError(f"plan output write made no progress: {output_path}")
            remaining = remaining[written:]
        os.fsync(output_descriptor)

        _publish_descriptor_exclusive(
            output_descriptor,
            parent_descriptor,
            output_path.name,
        )
        os.fsync(parent_descriptor)
    finally:
        if output_descriptor is not None:
            os.close(output_descriptor)
        os.close(parent_descriptor)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FGV canonical academic workflow")
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan-plaud")
    plan.add_argument("--vault", type=Path, required=True)
    plan.add_argument("--source", type=Path, required=True)
    plan.add_argument("--analysis", type=Path, required=True)
    plan.add_argument("--class-date", required=True)
    plan.add_argument("--runtime", choices=("codex", "claude"), required=True)
    plan.add_argument("--output", type=Path)
    apply = commands.add_parser("apply-plaud")
    apply.add_argument("--plan", type=Path, required=True)
    apply.add_argument("--vault", type=Path, required=True)
    apply.add_argument("--source", type=Path, required=True)
    apply.add_argument("--analysis", type=Path, required=True)
    apply.add_argument("--processor", choices=("codex", "claude"), required=True)
    apply.add_argument("--as-of", required=True)
    state = commands.add_parser("build-state")
    state.add_argument("--vault", type=Path, required=True)
    state.add_argument("--as-of", required=True)
    state.add_argument("--check", action="store_true")
    adapters = commands.add_parser("stage-adapters")
    adapters.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "plan-plaud":
        payload = plan_for_runtime(
            runtime=args.runtime,
            vault_root=args.vault,
            source=args.source,
            analysis_path=args.analysis,
            class_date=args.class_date,
        )
        encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if args.output:
            _write_plan_output(
                args.output,
                encoded.encode("utf-8"),
                source=args.source,
                analysis_path=args.analysis,
            )
        else:
            print(encoded, end="")
        return 0
    if args.command == "apply-plaud":
        result = apply_plan(
            json.loads(args.plan.read_text(encoding="utf-8")),
            vault_root=args.vault,
            source=args.source,
            analysis_path=args.analysis,
            processor=args.processor,
            as_of=args.as_of,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if result["state"] == "complete" else 1
    if args.command == "build-state":
        return refresh_state(args.vault, as_of=args.as_of, check=args.check)
    result = stage_adapters(args.output)
    print(f"staged adapters: {result.codex}, {result.claude}")
    print("live installations modified: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
