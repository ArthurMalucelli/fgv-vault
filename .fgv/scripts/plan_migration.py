#!/usr/bin/env python3
"""Generate a deterministic migration manifest without moving vault files."""

import argparse
import json
import os
from pathlib import Path
import secrets
import stat
import sys

from fgv_migration.inventory import InventoryError, inventory_from_git
from fgv_migration.rules import RuleError, build_manifest


def parse_args(arguments: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plan the FGV vault migration from an immutable Git tree."
    )
    parser.add_argument("--vault", required=True, help="path to the Git-backed vault")
    parser.add_argument(
        "--base-ref", required=True, help="Git tree used as the migration source"
    )
    parser.add_argument(
        "--output", required=True, help="destination path for the JSON manifest"
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="validate and report without writing the manifest",
    )
    return parser.parse_args(arguments)


DIRECTORY_OPEN_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
TEMPORARY_OPEN_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW


def _lexical_output_path(
    vault: Path, lexical_vault: Path, value: str
) -> tuple[Path, Path]:
    raw_output = Path(value)
    if "\x00" in value or "\\" in value or ".." in raw_output.parts:
        raise InventoryError(f"unsafe output path: {value!r}")

    if raw_output.is_absolute():
        lexical_output = Path(os.path.abspath(raw_output))
        try:
            relative_output = lexical_output.relative_to(lexical_vault)
        except ValueError as error:
            raise InventoryError(f"output must be inside vault: {value!r}") from error
    else:
        relative_output = raw_output
    if not relative_output.parts:
        raise InventoryError("output must name a file inside vault")
    return vault / relative_output, relative_output


def _validate_check_only_output(vault: Path, relative_output: Path) -> None:
    output = vault / relative_output

    current = vault
    existing_ancestor = vault
    for part in relative_output.parts[:-1]:
        current = current / part
        try:
            metadata = os.lstat(current)
        except FileNotFoundError:
            break
        if stat.S_ISLNK(metadata.st_mode):
            raise InventoryError(f"output ancestor is a symlink: {current}")
        if not stat.S_ISDIR(metadata.st_mode):
            raise InventoryError(
                f"output parent is not a directory: {output.parent}"
            )
        existing_ancestor = current

    resolved_ancestor = existing_ancestor.resolve(strict=True)
    try:
        resolved_ancestor.relative_to(vault)
    except ValueError as error:
        raise InventoryError(
            f"resolved output must be inside vault: {output}"
        ) from error

    if output.parent.exists():
        try:
            leaf_metadata = os.lstat(output)
        except FileNotFoundError:
            pass
        else:
            if stat.S_ISLNK(leaf_metadata.st_mode):
                raise InventoryError(f"output leaf is a symlink: {output}")
            if not stat.S_ISREG(leaf_metadata.st_mode):
                raise InventoryError(f"output is not a regular file: {output}")


def _open_output_parent(
    vault_fd: int, relative_output: Path, output: Path
) -> tuple[int, str]:
    parent_fd = os.dup(vault_fd)
    try:
        for part in relative_output.parts[:-1]:
            try:
                metadata = os.stat(part, dir_fd=parent_fd, follow_symlinks=False)
            except FileNotFoundError as error:
                raise InventoryError(
                    f"output parent is not a directory: {output.parent}"
                ) from error
            if stat.S_ISLNK(metadata.st_mode):
                raise InventoryError(f"output ancestor is a symlink: {part}")
            if not stat.S_ISDIR(metadata.st_mode):
                raise InventoryError(
                    f"output parent is not a directory: {output.parent}"
                )

            try:
                next_fd = os.open(part, DIRECTORY_OPEN_FLAGS, dir_fd=parent_fd)
            except OSError as error:
                raise InventoryError(
                    f"cannot securely open output ancestor: {part}: {error}"
                ) from error
            os.close(parent_fd)
            parent_fd = next_fd

        output_name = relative_output.name
        try:
            leaf_metadata = os.stat(
                output_name, dir_fd=parent_fd, follow_symlinks=False
            )
        except FileNotFoundError:
            pass
        else:
            if stat.S_ISLNK(leaf_metadata.st_mode):
                raise InventoryError(f"output leaf is a symlink: {output}")
            if not stat.S_ISREG(leaf_metadata.st_mode):
                raise InventoryError(f"output is not a regular file: {output}")
        return parent_fd, output_name
    except BaseException:
        os.close(parent_fd)
        raise


def _create_temporary_file(parent_fd: int, output_name: str) -> tuple[int, str]:
    for _ in range(100):
        temporary_name = f".{output_name}.{secrets.token_hex(8)}.tmp"
        try:
            file_descriptor = os.open(
                temporary_name,
                TEMPORARY_OPEN_FLAGS,
                0o600,
                dir_fd=parent_fd,
            )
        except FileExistsError:
            continue
        return file_descriptor, temporary_name
    raise InventoryError("cannot allocate a unique temporary manifest file")


def _atomic_write_output(parent_fd: int, output_name: str, payload: bytes) -> None:
    file_descriptor: int | None = None
    temporary_name: str | None = None
    try:
        file_descriptor, temporary_name = _create_temporary_file(
            parent_fd, output_name
        )
        stream = os.fdopen(file_descriptor, "wb")
        file_descriptor = None
        with stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(
            temporary_name,
            output_name,
            src_dir_fd=parent_fd,
            dst_dir_fd=parent_fd,
        )
        temporary_name = None
    finally:
        if file_descriptor is not None:
            os.close(file_descriptor)
        if temporary_name is not None:
            try:
                os.unlink(temporary_name, dir_fd=parent_fd)
            except FileNotFoundError:
                pass


def main(arguments: list[str] | None = None) -> int:
    args = parse_args(arguments)
    vault_fd: int | None = None
    parent_fd: int | None = None

    try:
        lexical_vault = Path(os.path.abspath(args.vault))
        vault = lexical_vault.resolve(strict=True)
        if not vault.is_dir():
            raise InventoryError(f"vault is not a directory: {vault}")
        output, relative_output = _lexical_output_path(
            vault, lexical_vault, args.output
        )
        if args.check_only:
            _validate_check_only_output(vault, relative_output)
        else:
            vault_fd = os.open(vault, DIRECTORY_OPEN_FLAGS)
            parent_fd, output_name = _open_output_parent(
                vault_fd, relative_output, output
            )
        output_paths = (output.relative_to(vault).as_posix(),)
        inventory = inventory_from_git(
            vault, args.base_ref, output_paths=output_paths
        )
        manifest = build_manifest(inventory)
        payload = (
            json.dumps(manifest, ensure_ascii=False, indent=2, separators=(",", ": "))
            + "\n"
        ).encode("utf-8")

        files_written = 0
        if not args.check_only:
            assert parent_fd is not None
            _atomic_write_output(parent_fd, output_name, payload)
            files_written = 1
    except (InventoryError, RuleError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    finally:
        if parent_fd is not None:
            os.close(parent_fd)
        if vault_fd is not None:
            os.close(vault_fd)

    print(f"legacy_files={len(manifest)}")
    print(f"unique_destinations={len(manifest)}")
    print("collisions=0")
    print("unclassified=0")
    print(f"files_written={files_written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
