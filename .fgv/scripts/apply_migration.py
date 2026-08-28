#!/usr/bin/env python3
"""Apply one byte-identical vault migration phase transactionally."""

import argparse
from dataclasses import dataclass
import hashlib
import json
import os
from pathlib import Path
import re
import stat
import subprocess
import sys
from typing import Sequence

from fgv_migration.inventory import InventoryError, normalize_relative_path
from fgv_migration.rules import RuleError, validate_manifest


DIRECTORY_OPEN_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
FILE_OPEN_FLAGS = os.O_RDONLY | os.O_NOFOLLOW
OID_PATTERN = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")


class MigrationApplyError(RuntimeError):
    """The migration cannot be applied without violating a safety gate."""


@dataclass(frozen=True)
class Move:
    source: str
    destination: str
    sha256: str
    size_bytes: int


@dataclass(frozen=True)
class Preflight:
    moves: tuple[Move, ...]
    no_op: bool


@dataclass
class JournalEntry:
    move: Move
    source_unlinked: bool = False


def parse_args(arguments: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Apply byte-identical moves from a validated migration manifest."
    )
    parser.add_argument("--vault", required=True)
    parser.add_argument("--manifest", required=True)
    parser.add_argument("--phase", required=True)
    parser.add_argument("--expected-head", required=True)
    parser.add_argument("--dry-run", action="store_true")
    return parser.parse_args(arguments)


def _run_git(vault: Path, arguments: tuple[str, ...]) -> subprocess.CompletedProcess:
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    environment["GIT_CONFIG_NOSYSTEM"] = "1"
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    environment["LC_ALL"] = "C"
    try:
        return subprocess.run(
            ("git", *arguments),
            cwd=vault,
            env=environment,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as error:
        raise MigrationApplyError(f"cannot execute git: {error}") from error


def _validate_head(vault: Path, expected_head: str) -> None:
    if OID_PATTERN.fullmatch(expected_head) is None:
        raise MigrationApplyError("expected-head must be a lowercase full object ID")
    result = _run_git(
        vault,
        ("rev-parse", "--verify", "--end-of-options", "HEAD^{commit}"),
    )
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise MigrationApplyError(f"cannot resolve Git HEAD: {detail}")
    try:
        actual_head = result.stdout.decode("ascii").strip()
    except UnicodeDecodeError as error:
        raise MigrationApplyError("Git HEAD is not an ASCII object ID") from error
    if OID_PATTERN.fullmatch(actual_head) is None:
        raise MigrationApplyError("Git returned an invalid full object ID for HEAD")
    if actual_head != expected_head:
        raise MigrationApplyError(
            f"HEAD does not match expected-head: {actual_head} != {expected_head}"
        )


def _relative_manifest_path(vault: Path, value: str) -> str:
    if not value or "\x00" in value or "\\" in value:
        raise MigrationApplyError(f"unsafe manifest path: {value!r}")
    raw = Path(value)
    if raw.is_absolute():
        lexical = Path(os.path.abspath(raw))
        try:
            relative = lexical.relative_to(vault)
        except ValueError as error:
            raise MigrationApplyError("manifest must be inside vault") from error
        candidate = relative.as_posix()
    else:
        candidate = raw.as_posix()
    try:
        normalized = normalize_relative_path(candidate)
    except InventoryError as error:
        raise MigrationApplyError(f"unsafe manifest path: {value!r}") from error
    if normalized != candidate:
        raise MigrationApplyError("manifest path must be canonical")
    return normalized


def _open_existing_directory(parent_fd: int, name: str, label: str) -> int:
    try:
        metadata = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError as error:
        raise MigrationApplyError(f"{label} is missing") from error
    if stat.S_ISLNK(metadata.st_mode):
        raise MigrationApplyError(f"{label} is a symlink")
    if not stat.S_ISDIR(metadata.st_mode):
        raise MigrationApplyError(f"{label} is not a directory")
    try:
        return os.open(name, DIRECTORY_OPEN_FLAGS, dir_fd=parent_fd)
    except OSError as error:
        raise MigrationApplyError(f"cannot securely open {label}: {error}") from error


def _open_parent(
    root_fd: int,
    relative: str,
    *,
    create: bool = False,
    created: list[tuple[str, ...]] | None = None,
) -> tuple[int, str]:
    parts = Path(relative).parts
    parent_fd = os.dup(root_fd)
    traversed: list[str] = []
    try:
        for name in parts[:-1]:
            traversed.append(name)
            try:
                metadata = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
            except FileNotFoundError:
                if not create:
                    raise MigrationApplyError(
                        f"ancestor is missing: {'/'.join(traversed)}"
                    )
                try:
                    os.mkdir(name, dir_fd=parent_fd)
                except OSError as error:
                    raise MigrationApplyError(
                        f"cannot create destination directory {'/'.join(traversed)}: {error}"
                    ) from error
                if created is not None:
                    created.append(tuple(traversed))
                metadata = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
            label = f"ancestor {'/'.join(traversed)}"
            if stat.S_ISLNK(metadata.st_mode):
                raise MigrationApplyError(f"{label} is a symlink")
            if not stat.S_ISDIR(metadata.st_mode):
                raise MigrationApplyError(f"{label} is not a directory")
            next_fd = _open_existing_directory(parent_fd, name, label)
            os.close(parent_fd)
            parent_fd = next_fd
        return parent_fd, parts[-1]
    except BaseException:
        os.close(parent_fd)
        raise


def _manifest_bytes(root_fd: int, relative_manifest: str) -> bytes:
    parent_fd, name = _open_parent(root_fd, relative_manifest)
    file_fd: int | None = None
    try:
        try:
            metadata = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError as error:
            raise MigrationApplyError("manifest is missing") from error
        if stat.S_ISLNK(metadata.st_mode):
            raise MigrationApplyError("manifest is a symlink")
        if not stat.S_ISREG(metadata.st_mode):
            raise MigrationApplyError("manifest is not a regular file")
        try:
            file_fd = os.open(name, FILE_OPEN_FLAGS, dir_fd=parent_fd)
        except OSError as error:
            raise MigrationApplyError(f"cannot securely open manifest: {error}") from error
        opened = os.fstat(file_fd)
        if not stat.S_ISREG(opened.st_mode):
            raise MigrationApplyError("manifest is not a regular file")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(file_fd, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > 64 * 1024 * 1024:
                raise MigrationApplyError("manifest exceeds 64 MiB safety limit")
            chunks.append(chunk)
        return b"".join(chunks)
    finally:
        if file_fd is not None:
            os.close(file_fd)
        os.close(parent_fd)


def _load_manifest(root_fd: int, relative_manifest: str, phase: str) -> tuple[Move, ...]:
    payload = _manifest_bytes(root_fd, relative_manifest)
    try:
        records = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise MigrationApplyError(f"manifest is not valid UTF-8 JSON: {error}") from error
    try:
        validate_manifest(records)
    except (InventoryError, RuleError) as error:
        raise MigrationApplyError(str(error)) from error
    if phase != "structural":
        raise MigrationApplyError("phase must be structural")
    moves = tuple(
        Move(
            source=record["source"],
            destination=record["destination"],
            sha256=record["sha256"],
            size_bytes=record["size_bytes"],
        )
        for record in records
    )
    manifest_paths = {move.source for move in moves} | {
        move.destination for move in moves
    }
    if relative_manifest in manifest_paths:
        raise MigrationApplyError("manifest cannot be a migration source or destination")
    source_paths = {move.source for move in moves}
    destination_paths = {move.destination for move in moves}
    overlap = source_paths & destination_paths
    if overlap:
        raise MigrationApplyError(
            f"source and destination sets overlap: {min(overlap)!r}"
        )
    return moves


def _hash_open_file(parent_fd: int, name: str, label: str) -> tuple[str, int, int]:
    try:
        metadata = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError as error:
        raise MigrationApplyError(f"{label} is missing") from error
    if stat.S_ISLNK(metadata.st_mode):
        raise MigrationApplyError(f"{label} is a symlink")
    if not stat.S_ISREG(metadata.st_mode):
        raise MigrationApplyError(f"{label} is not a regular file")
    file_fd: int | None = None
    try:
        file_fd = os.open(name, FILE_OPEN_FLAGS, dir_fd=parent_fd)
        opened = os.fstat(file_fd)
        if not stat.S_ISREG(opened.st_mode):
            raise MigrationApplyError(f"{label} is not a regular file")
        digest = hashlib.sha256()
        size = 0
        while True:
            chunk = os.read(file_fd, 1024 * 1024)
            if not chunk:
                break
            digest.update(chunk)
            size += len(chunk)
        after = os.fstat(file_fd)
        if (opened.st_dev, opened.st_ino, opened.st_size) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
        ):
            raise MigrationApplyError(f"{label} changed while being verified")
        return digest.hexdigest(), size, opened.st_dev
    except OSError as error:
        raise MigrationApplyError(f"cannot securely read {label}: {error}") from error
    finally:
        if file_fd is not None:
            os.close(file_fd)


def _verify_file(root_fd: int, relative: str, move: Move, role: str) -> int:
    parent_fd, name = _open_parent(root_fd, relative)
    try:
        digest, size, device = _hash_open_file(parent_fd, name, f"{role} {relative}")
    finally:
        os.close(parent_fd)
    if size != move.size_bytes:
        raise MigrationApplyError(
            f"{role} size mismatch for {relative}: {size} != {move.size_bytes}"
        )
    if digest != move.sha256:
        raise MigrationApplyError(f"{role} hash mismatch for {relative}")
    return device


def _inspect_destination(root_fd: int, move: Move) -> tuple[str, int]:
    parts = Path(move.destination).parts
    parent_fd = os.dup(root_fd)
    traversed: list[str] = []
    try:
        for name in parts[:-1]:
            traversed.append(name)
            try:
                metadata = os.stat(
                    name, dir_fd=parent_fd, follow_symlinks=False
                )
            except FileNotFoundError:
                return "missing", os.fstat(parent_fd).st_dev
            label = f"destination ancestor {'/'.join(traversed)}"
            if stat.S_ISLNK(metadata.st_mode):
                raise MigrationApplyError(f"{label} is a symlink")
            if not stat.S_ISDIR(metadata.st_mode):
                raise MigrationApplyError(f"{label} is not a directory")
            next_fd = _open_existing_directory(parent_fd, name, label)
            os.close(parent_fd)
            parent_fd = next_fd

        name = parts[-1]
        parent_device = os.fstat(parent_fd).st_dev
        try:
            metadata = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            return "missing", parent_device
        if stat.S_ISLNK(metadata.st_mode):
            raise MigrationApplyError(
                f"destination {move.destination} is a symlink"
            )
        if not stat.S_ISREG(metadata.st_mode):
            raise MigrationApplyError(
                f"destination {move.destination} is not a regular file"
            )
        return "present", parent_device
    finally:
        os.close(parent_fd)


def _source_state(root_fd: int, move: Move) -> tuple[str, int | None]:
    try:
        device = _verify_file(root_fd, move.source, move, "source")
    except MigrationApplyError as error:
        if " is missing" in str(error) or "ancestor is missing" in str(error):
            return "missing", None
        raise
    return "present", device


def _preflight(root_fd: int, moves: Sequence[Move]) -> Preflight:
    pending: list[Move] = []
    complete: list[Move] = []
    for move in moves:
        source_state, source_device = _source_state(root_fd, move)
        destination_state, destination_parent_device = _inspect_destination(
            root_fd, move
        )
        if source_state == "present" and destination_state == "missing":
            if source_device != destination_parent_device:
                raise MigrationApplyError(
                    f"source and destination are on different filesystems: {move.source}"
                )
            pending.append(move)
        elif source_state == "missing" and destination_state == "present":
            _verify_file(root_fd, move.destination, move, "destination")
            complete.append(move)
        elif source_state == "present" and destination_state == "present":
            raise MigrationApplyError(
                f"source and destination both exist: {move.source} -> {move.destination}"
            )
        else:
            raise MigrationApplyError(
                f"source and destination are both missing: {move.source} -> {move.destination}"
            )
    if pending and complete:
        raise MigrationApplyError(
            f"migration is partially applied: pending={len(pending)} complete={len(complete)}"
        )
    return Preflight(tuple(pending), no_op=bool(complete) or not moves)


def _ensure_destination_absent(parent_fd: int, name: str, relative: str) -> None:
    try:
        metadata = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        return
    if stat.S_ISLNK(metadata.st_mode):
        raise MigrationApplyError(f"destination {relative} is a symlink")
    raise MigrationApplyError(f"destination already exists: {relative}")


def _path_identity(root_fd: int, relative: str, label: str) -> tuple[int, int]:
    parent_fd, name = _open_parent(root_fd, relative)
    try:
        try:
            metadata = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError as error:
            raise MigrationApplyError(f"{label} is missing") from error
        if stat.S_ISLNK(metadata.st_mode):
            raise MigrationApplyError(f"{label} is a symlink")
        if not stat.S_ISREG(metadata.st_mode):
            raise MigrationApplyError(f"{label} is not a regular file")
        return metadata.st_dev, metadata.st_ino
    finally:
        os.close(parent_fd)


def _move_one(
    root_fd: int,
    move: Move,
    created: list[tuple[str, ...]],
    journal: list[JournalEntry],
) -> None:
    source_parent_fd, source_name = _open_parent(root_fd, move.source)
    destination_parent_fd: int | None = None
    try:
        digest, size, _ = _hash_open_file(
            source_parent_fd, source_name, f"source {move.source}"
        )
        if size != move.size_bytes:
            raise MigrationApplyError(f"source size mismatch for {move.source}")
        if digest != move.sha256:
            raise MigrationApplyError(f"source hash mismatch for {move.source}")
        destination_parent_fd, destination_name = _open_parent(
            root_fd, move.destination, create=True, created=created
        )
        if os.fstat(source_parent_fd).st_dev != os.fstat(destination_parent_fd).st_dev:
            raise MigrationApplyError(
                f"source and destination are on different filesystems: {move.source}"
            )
        _ensure_destination_absent(
            destination_parent_fd, destination_name, move.destination
        )
        try:
            os.link(
                source_name,
                destination_name,
                src_dir_fd=source_parent_fd,
                dst_dir_fd=destination_parent_fd,
                follow_symlinks=False,
            )
        except FileExistsError as error:
            raise MigrationApplyError(
                f"destination appeared after preflight: {move.destination}"
            ) from error
        entry = JournalEntry(move)
        journal.append(entry)
        try:
            source_metadata = os.stat(
                source_name, dir_fd=source_parent_fd, follow_symlinks=False
            )
            destination_metadata = os.stat(
                destination_name,
                dir_fd=destination_parent_fd,
                follow_symlinks=False,
            )
            linked_identity = (
                destination_metadata.st_dev,
                destination_metadata.st_ino,
            )
            if (source_metadata.st_dev, source_metadata.st_ino) != linked_identity:
                raise MigrationApplyError(
                    f"linked destination inode mismatch: {move.destination}"
                )
            linked_digest, linked_size, _ = _hash_open_file(
                destination_parent_fd,
                destination_name,
                f"destination {move.destination}",
            )
            if linked_size != move.size_bytes or linked_digest != move.sha256:
                raise MigrationApplyError(
                    f"linked destination hash mismatch: {move.destination}"
                )
            if _path_identity(
                root_fd, move.source, f"source {move.source}"
            ) != linked_identity or _path_identity(
                root_fd,
                move.destination,
                f"destination {move.destination}",
            ) != linked_identity:
                raise MigrationApplyError(
                    f"source or destination changed after preflight: {move.source}"
                )
        except BaseException as verification_error:
            try:
                os.unlink(destination_name, dir_fd=destination_parent_fd)
                journal.pop()
            except BaseException as cleanup_error:
                raise MigrationApplyError(
                    "CRITICAL linked destination cleanup failed after "
                    f"{verification_error}: {cleanup_error}"
                ) from verification_error
            if isinstance(verification_error, MigrationApplyError):
                if " is missing" in str(verification_error):
                    raise MigrationApplyError(
                        f"source or destination changed after preflight: {move.source}"
                    ) from verification_error
                raise
            raise MigrationApplyError(str(verification_error)) from verification_error
        os.unlink(source_name, dir_fd=source_parent_fd)
        entry.source_unlinked = True
    finally:
        if destination_parent_fd is not None:
            os.close(destination_parent_fd)
        os.close(source_parent_fd)


def _rollback_entry(root_fd: int, entry: JournalEntry) -> None:
    move = entry.move
    destination_parent_fd, destination_name = _open_parent(
        root_fd, move.destination
    )
    source_parent_fd: int | None = None
    try:
        source_parent_fd, source_name = _open_parent(root_fd, move.source)
        destination_digest, destination_size, _ = _hash_open_file(
            destination_parent_fd,
            destination_name,
            f"rollback destination {move.destination}",
        )
        if (
            destination_size != move.size_bytes
            or destination_digest != move.sha256
        ):
            raise MigrationApplyError(
                f"rollback destination hash mismatch: {move.destination}"
            )
        if entry.source_unlinked:
            _ensure_destination_absent(source_parent_fd, source_name, move.source)
            os.link(
                destination_name,
                source_name,
                src_dir_fd=destination_parent_fd,
                dst_dir_fd=source_parent_fd,
                follow_symlinks=False,
            )
            _verify_file(root_fd, move.source, move, "rolled back source")
        else:
            source_digest, source_size, _ = _hash_open_file(
                source_parent_fd, source_name, f"rollback source {move.source}"
            )
            if source_size != move.size_bytes or source_digest != move.sha256:
                raise MigrationApplyError(
                    f"rollback source hash mismatch: {move.source}"
                )
            source_metadata = os.stat(
                source_name, dir_fd=source_parent_fd, follow_symlinks=False
            )
            destination_metadata = os.stat(
                destination_name,
                dir_fd=destination_parent_fd,
                follow_symlinks=False,
            )
            if (source_metadata.st_dev, source_metadata.st_ino) != (
                destination_metadata.st_dev,
                destination_metadata.st_ino,
            ):
                raise MigrationApplyError(
                    f"rollback paths do not share an inode: {move.destination}"
                )
        os.unlink(destination_name, dir_fd=destination_parent_fd)
    finally:
        if source_parent_fd is not None:
            os.close(source_parent_fd)
        os.close(destination_parent_fd)


def _remove_created_directory(root_fd: int, parts: tuple[str, ...]) -> None:
    relative = "/".join(parts)
    parent_relative = "/".join(parts[:-1])
    if parent_relative:
        parent_fd, _ = _open_parent(root_fd, f"{parent_relative}/placeholder")
    else:
        parent_fd = os.dup(root_fd)
    try:
        os.rmdir(parts[-1], dir_fd=parent_fd)
    except FileNotFoundError:
        pass
    except OSError as error:
        raise MigrationApplyError(
            f"cannot remove created directory {relative}: {error}"
        ) from error
    finally:
        os.close(parent_fd)


def _rollback(
    root_fd: int,
    journal: Sequence[JournalEntry],
    created: Sequence[tuple[str, ...]],
) -> list[str]:
    failures: list[str] = []
    for entry in reversed(journal):
        move = entry.move
        try:
            _rollback_entry(root_fd, entry)
        except BaseException as error:
            failures.append(f"{move.destination} -> {move.source}: {error}")
    for parts in reversed(created):
        try:
            _remove_created_directory(root_fd, parts)
        except BaseException as error:
            failures.append(str(error))
    return failures


def _apply(root_fd: int, moves: Sequence[Move]) -> int:
    journal: list[JournalEntry] = []
    created: list[tuple[str, ...]] = []
    try:
        for move in moves:
            _move_one(root_fd, move, created, journal)
            _verify_file(root_fd, move.destination, move, "destination")
        return len(journal)
    except BaseException as original_error:
        failures = _rollback(root_fd, journal, created)
        if failures:
            detail = "; ".join(failures)
            raise MigrationApplyError(
                f"CRITICAL rollback failed after {original_error}: {detail}"
            ) from original_error
        if isinstance(original_error, MigrationApplyError):
            raise
        raise MigrationApplyError(str(original_error)) from original_error


def main(arguments: list[str] | None = None) -> int:
    root_fd: int | None = None
    try:
        args = parse_args(arguments)
        lexical_vault = Path(os.path.abspath(args.vault))
        try:
            vault_metadata = os.lstat(lexical_vault)
        except OSError as error:
            raise MigrationApplyError(f"cannot inspect vault: {error}") from error
        if stat.S_ISLNK(vault_metadata.st_mode):
            raise MigrationApplyError("vault is a symlink")
        if not stat.S_ISDIR(vault_metadata.st_mode):
            raise MigrationApplyError("vault is not a directory")
        vault = lexical_vault.resolve(strict=True)
        relative_manifest = _relative_manifest_path(vault, args.manifest)
        _validate_head(vault, args.expected_head)
        root_fd = os.open(vault, DIRECTORY_OPEN_FLAGS)
        moves = _load_manifest(root_fd, relative_manifest, args.phase)
        preflight = _preflight(root_fd, moves)
        if args.dry_run:
            print(f"planned_moves={len(preflight.moves)}")
            print("preflight=ok")
            print("files_written=0")
            return 0
        if preflight.no_op:
            print("planned_moves=0")
            print("preflight=ok")
            print("files_moved=0")
            print("no_op=true")
            return 0
        files_moved = _apply(root_fd, preflight.moves)
        print(f"planned_moves={len(preflight.moves)}")
        print("preflight=ok")
        print(f"files_moved={files_moved}")
        return 0
    except (MigrationApplyError, InventoryError, RuleError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    finally:
        if root_fd is not None:
            os.close(root_fd)


if __name__ == "__main__":
    raise SystemExit(main())
