#!/usr/bin/env python3
"""Apply one byte-identical vault migration phase transactionally."""

import argparse
import ctypes
from dataclasses import dataclass
import errno
import fcntl
import hashlib
import json
import os
from pathlib import Path
import re
import secrets
import stat
import subprocess
import sys
from typing import Sequence

from fgv_migration.inventory import InventoryError, normalize_relative_path
from fgv_migration.rules import RuleError, validate_manifest


DIRECTORY_OPEN_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
FILE_OPEN_FLAGS = os.O_RDONLY | os.O_NOFOLLOW
OID_PATTERN = re.compile(r"(?:[0-9a-f]{40}|[0-9a-f]{64})")
SHA256_PATTERN = re.compile(r"[0-9a-f]{64}")
JOURNAL_NAME = "migration-apply-journal.json"
JOURNAL_PATH = f".fgv/{JOURNAL_NAME}"
JOURNAL_FIELDS = (
    "schema_version",
    "expected_head",
    "manifest_path",
    "manifest_sha256",
    "move_set_sha256",
    "phase",
    "move_count",
    "completed_moves",
    "created_directories",
)
TEMPORARY_OPEN_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
ATOMIC_RENAME_FLAGS = {
    "darwin": ("renameatx_np", 0x00000004),
    "linux": ("renameat2", 0x00000001),
}


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


@dataclass(frozen=True)
class ManifestBundle:
    moves: tuple[Move, ...]
    sha256: str


@dataclass
class RecoveryJournal:
    expected_head: str
    manifest_path: str
    manifest_sha256: str
    move_set_sha256: str
    phase: str
    move_count: int
    completed_moves: int
    created_directories: tuple[str, ...]


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


def _expected_manifest_bytes(
    vault: Path, expected_head: str, relative_manifest: str
) -> bytes:
    listing = _run_git(
        vault,
        (
            "ls-tree",
            "-z",
            "--full-tree",
            expected_head,
            "--",
            relative_manifest,
        ),
    )
    if listing.returncode != 0:
        detail = listing.stderr.decode("utf-8", errors="replace").strip()
        raise MigrationApplyError(f"cannot read manifest from expected-head: {detail}")
    records = [record for record in listing.stdout.split(b"\x00") if record]
    if len(records) != 1:
        raise MigrationApplyError(
            "manifest must be exactly one regular blob in expected-head"
        )
    try:
        metadata, raw_path = records[0].split(b"\t", 1)
        mode, object_type, raw_oid = metadata.split(b" ", 2)
        listed_path = raw_path.decode("utf-8", errors="strict")
        object_id = raw_oid.decode("ascii", errors="strict")
    except (UnicodeDecodeError, ValueError) as error:
        raise MigrationApplyError(
            "manifest has an invalid expected-head tree record"
        ) from error
    if (
        listed_path != relative_manifest
        or mode not in {b"100644", b"100755"}
        or object_type != b"blob"
        or OID_PATTERN.fullmatch(object_id) is None
    ):
        raise MigrationApplyError("manifest is not a regular blob in expected-head")
    blob = _run_git(vault, ("cat-file", "blob", object_id))
    if blob.returncode != 0:
        detail = blob.stderr.decode("utf-8", errors="replace").strip()
        raise MigrationApplyError(f"cannot read expected manifest blob: {detail}")
    return blob.stdout


def _load_manifest(
    vault: Path,
    root_fd: int,
    relative_manifest: str,
    phase: str,
    expected_head: str,
) -> ManifestBundle:
    payload = _manifest_bytes(root_fd, relative_manifest)
    if payload != _expected_manifest_bytes(vault, expected_head, relative_manifest):
        raise MigrationApplyError("manifest does not match expected-head blob")
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
    return ManifestBundle(moves, hashlib.sha256(payload).hexdigest())


def _move_set_sha256(moves: Sequence[Move]) -> str:
    records = [
        {
            "source": move.source,
            "destination": move.destination,
            "sha256": move.sha256,
            "size_bytes": move.size_bytes,
        }
        for move in moves
    ]
    payload = json.dumps(
        records,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def _journal_record(journal: RecoveryJournal) -> dict[str, object]:
    return dict(
        zip(
            JOURNAL_FIELDS,
            (
                1,
                journal.expected_head,
                journal.manifest_path,
                journal.manifest_sha256,
                journal.move_set_sha256,
                journal.phase,
                journal.move_count,
                journal.completed_moves,
                list(journal.created_directories),
            ),
        )
    )


def _journal_payload(journal: RecoveryJournal) -> bytes:
    return (
        json.dumps(
            _journal_record(journal),
            ensure_ascii=False,
            indent=2,
            separators=(",", ": "),
        )
        + "\n"
    ).encode("utf-8")


def _open_journal_directory(root_fd: int) -> int:
    directory_fd = _open_existing_directory(root_fd, ".fgv", ".fgv")
    try:
        fcntl.flock(directory_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as error:
        os.close(directory_fd)
        raise MigrationApplyError(
            f"another migration applicator holds the .fgv lock: {error}"
        ) from error
    return directory_fd


def _read_limited_file(file_fd: int, label: str, limit: int) -> bytes:
    chunks: list[bytes] = []
    total = 0
    while True:
        chunk = os.read(file_fd, min(1024 * 1024, limit + 1 - total))
        if not chunk:
            return b"".join(chunks)
        total += len(chunk)
        if total > limit:
            raise MigrationApplyError(f"{label} exceeds its safety limit")
        chunks.append(chunk)


def _read_journal(journal_directory_fd: int) -> RecoveryJournal | None:
    try:
        metadata = os.stat(
            JOURNAL_NAME,
            dir_fd=journal_directory_fd,
            follow_symlinks=False,
        )
    except FileNotFoundError:
        return None
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise MigrationApplyError(
            "CRITICAL recovery journal is not a regular non-symlink file"
        )
    file_fd: int | None = None
    try:
        file_fd = os.open(
            JOURNAL_NAME,
            FILE_OPEN_FLAGS,
            dir_fd=journal_directory_fd,
        )
        opened = os.fstat(file_fd)
        if not stat.S_ISREG(opened.st_mode):
            raise MigrationApplyError(
                "CRITICAL recovery journal is not a regular file"
            )
        payload = _read_limited_file(file_fd, "recovery journal", 16 * 1024 * 1024)
    except OSError as error:
        raise MigrationApplyError(
            f"CRITICAL recovery journal cannot be read: {error}"
        ) from error
    finally:
        if file_fd is not None:
            os.close(file_fd)
    try:
        record = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise MigrationApplyError(
            f"CRITICAL recovery journal is invalid JSON: {error}"
        ) from error
    if type(record) is not dict or tuple(record) != JOURNAL_FIELDS:
        raise MigrationApplyError("CRITICAL recovery journal has invalid schema")
    if type(record["schema_version"]) is not int or record["schema_version"] != 1:
        raise MigrationApplyError(
            "CRITICAL recovery journal has invalid schema_version"
        )
    string_fields = (
        "expected_head",
        "manifest_path",
        "manifest_sha256",
        "move_set_sha256",
        "phase",
    )
    if any(type(record[field]) is not str for field in string_fields):
        raise MigrationApplyError("CRITICAL recovery journal has invalid field types")
    try:
        normalized_manifest_path = normalize_relative_path(record["manifest_path"])
    except InventoryError as error:
        raise MigrationApplyError(
            "CRITICAL recovery journal has invalid manifest_path"
        ) from error
    if (
        OID_PATTERN.fullmatch(record["expected_head"]) is None
        or normalized_manifest_path != record["manifest_path"]
        or SHA256_PATTERN.fullmatch(record["manifest_sha256"]) is None
        or SHA256_PATTERN.fullmatch(record["move_set_sha256"]) is None
        or record["phase"] != "structural"
    ):
        raise MigrationApplyError("CRITICAL recovery journal has invalid identity")
    move_count = record["move_count"]
    completed_moves = record["completed_moves"]
    if (
        type(move_count) is not int
        or move_count < 0
        or type(completed_moves) is not int
        or completed_moves < 0
        or completed_moves > move_count
    ):
        raise MigrationApplyError("CRITICAL recovery journal has invalid counts")
    raw_directories = record["created_directories"]
    if type(raw_directories) is not list or any(
        type(path) is not str for path in raw_directories
    ):
        raise MigrationApplyError(
            "CRITICAL recovery journal has invalid created_directories"
        )
    directories: list[str] = []
    for path in raw_directories:
        try:
            normalized = normalize_relative_path(path)
        except InventoryError as error:
            raise MigrationApplyError(
                "CRITICAL recovery journal has unsafe created_directories"
            ) from error
        if normalized != path or path in directories:
            raise MigrationApplyError(
                "CRITICAL recovery journal has invalid created_directories"
            )
        directories.append(path)
    return RecoveryJournal(
        expected_head=record["expected_head"],
        manifest_path=record["manifest_path"],
        manifest_sha256=record["manifest_sha256"],
        move_set_sha256=record["move_set_sha256"],
        phase=record["phase"],
        move_count=move_count,
        completed_moves=completed_moves,
        created_directories=tuple(directories),
    )


def _write_journal(journal_directory_fd: int, journal: RecoveryJournal) -> None:
    payload = _journal_payload(journal)
    temporary_name: str | None = None
    temporary_fd: int | None = None
    try:
        for _ in range(100):
            candidate = f".{JOURNAL_NAME}.{secrets.token_hex(8)}.tmp"
            try:
                temporary_fd = os.open(
                    candidate,
                    TEMPORARY_OPEN_FLAGS,
                    0o600,
                    dir_fd=journal_directory_fd,
                )
            except FileExistsError:
                continue
            temporary_name = candidate
            break
        if temporary_fd is None or temporary_name is None:
            raise MigrationApplyError("cannot allocate recovery journal temporary file")
        stream = os.fdopen(temporary_fd, "wb")
        temporary_fd = None
        with stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(
            temporary_name,
            JOURNAL_NAME,
            src_dir_fd=journal_directory_fd,
            dst_dir_fd=journal_directory_fd,
        )
        temporary_name = None
        os.fsync(journal_directory_fd)
    finally:
        if temporary_fd is not None:
            os.close(temporary_fd)
        if temporary_name is not None:
            try:
                os.unlink(temporary_name, dir_fd=journal_directory_fd)
            except FileNotFoundError:
                pass


def _delete_journal(journal_directory_fd: int) -> None:
    try:
        metadata = os.stat(
            JOURNAL_NAME,
            dir_fd=journal_directory_fd,
            follow_symlinks=False,
        )
    except FileNotFoundError:
        return
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise MigrationApplyError(
            "CRITICAL recovery journal changed before deletion"
        )
    os.unlink(JOURNAL_NAME, dir_fd=journal_directory_fd)
    os.fsync(journal_directory_fd)


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


def _destination_directory_paths(moves: Sequence[Move]) -> tuple[str, ...]:
    paths: list[str] = []
    seen: set[str] = set()
    for move in moves:
        parts = Path(move.destination).parts[:-1]
        for end in range(1, len(parts) + 1):
            relative = "/".join(parts[:end])
            if relative not in seen:
                seen.add(relative)
                paths.append(relative)
    return tuple(paths)


def _planned_destination_directories(
    root_fd: int, moves: Sequence[Move]
) -> tuple[str, ...]:
    planned: list[str] = []
    missing: set[str] = set()
    for relative in _destination_directory_paths(moves):
        parent = relative.rpartition("/")[0]
        if parent and parent in missing:
            missing.add(relative)
            planned.append(relative)
            continue
        try:
            directory_fd, _ = _open_parent(root_fd, f"{relative}/placeholder")
        except MigrationApplyError as error:
            if "ancestor is missing" not in str(error):
                raise
            missing.add(relative)
            planned.append(relative)
        else:
            os.close(directory_fd)
    return tuple(planned)


def _create_planned_directories(
    root_fd: int, directories: Sequence[str]
) -> None:
    for relative in directories:
        parent_fd, name = _open_parent(root_fd, relative)
        try:
            try:
                os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
            except FileNotFoundError:
                pass
            else:
                raise MigrationApplyError(
                    f"destination directory appeared after preflight: {relative}"
                )
            os.mkdir(name, dir_fd=parent_fd)
        finally:
            os.close(parent_fd)


def _move_state(root_fd: int, move: Move) -> str:
    source_state, _ = _source_state(root_fd, move)
    destination_state, _ = _inspect_destination(root_fd, move)
    if source_state == "present" and destination_state == "missing":
        return "pending"
    if source_state == "missing" and destination_state == "present":
        _verify_file(root_fd, move.destination, move, "destination")
        return "complete"
    if source_state == "present" and destination_state == "present":
        raise MigrationApplyError(
            f"source and destination both exist: {move.source} -> {move.destination}"
        )
    raise MigrationApplyError(
        f"source and destination are both missing: {move.source} -> {move.destination}"
    )


def _validate_journal_compatibility(
    journal: RecoveryJournal,
    *,
    expected_head: str,
    relative_manifest: str,
    bundle: ManifestBundle,
    phase: str,
) -> None:
    identity = (
        journal.expected_head,
        journal.manifest_path,
        journal.manifest_sha256,
        journal.move_set_sha256,
        journal.phase,
        journal.move_count,
    )
    expected_identity = (
        expected_head,
        relative_manifest,
        bundle.sha256,
        _move_set_sha256(bundle.moves),
        phase,
        len(bundle.moves),
    )
    if identity != expected_identity:
        raise MigrationApplyError(
            "CRITICAL recovery journal is incompatible with this invocation"
        )
    allowed_directories = set(_destination_directory_paths(bundle.moves))
    positions = {
        path: index for index, path in enumerate(journal.created_directories)
    }
    for path in journal.created_directories:
        if path not in allowed_directories:
            raise MigrationApplyError(
                "CRITICAL recovery journal contains an unrelated directory"
            )
        parent = path.rpartition("/")[0]
        if parent in positions and positions[parent] > positions[path]:
            raise MigrationApplyError(
                "CRITICAL recovery journal directory order is invalid"
            )


def _remove_journal_directories(
    root_fd: int, directories: Sequence[str]
) -> None:
    for relative in reversed(directories):
        _remove_created_directory(root_fd, tuple(relative.split("/")))


def _recover_journal(
    root_fd: int,
    journal_directory_fd: int,
    journal: RecoveryJournal,
    *,
    expected_head: str,
    relative_manifest: str,
    bundle: ManifestBundle,
    phase: str,
) -> None:
    _validate_journal_compatibility(
        journal,
        expected_head=expected_head,
        relative_manifest=relative_manifest,
        bundle=bundle,
        phase=phase,
    )
    try:
        states = tuple(_move_state(root_fd, move) for move in bundle.moves)
    except MigrationApplyError as error:
        raise MigrationApplyError(
            f"CRITICAL recovery journal path state is invalid: {error}"
        ) from error
    completed = 0
    while completed < len(states) and states[completed] == "complete":
        completed += 1
    if any(state != "pending" for state in states[completed:]):
        raise MigrationApplyError(
            "CRITICAL recovery journal does not describe a complete-prefix state"
        )
    if abs(completed - journal.completed_moves) > 1:
        raise MigrationApplyError(
            "CRITICAL recovery journal checkpoint diverges from path state"
        )
    if completed == len(bundle.moves):
        _delete_journal(journal_directory_fd)
        return
    if journal.completed_moves != completed:
        journal.completed_moves = completed
        _write_journal(journal_directory_fd, journal)
    if completed:
        for index in range(completed - 1, -1, -1):
            try:
                _rollback_entry(root_fd, JournalEntry(bundle.moves[index], True))
            except BaseException as error:
                raise MigrationApplyError(
                    f"CRITICAL recovery rollback failed at move {index}: {error}"
                ) from error
            journal.completed_moves = index
            _write_journal(journal_directory_fd, journal)
    try:
        _remove_journal_directories(root_fd, journal.created_directories)
        _delete_journal(journal_directory_fd)
    except BaseException as error:
        raise MigrationApplyError(
            f"CRITICAL recovery cleanup failed: {error}"
        ) from error


def _ensure_destination_absent(parent_fd: int, name: str, relative: str) -> None:
    try:
        metadata = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError:
        return
    if stat.S_ISLNK(metadata.st_mode):
        raise MigrationApplyError(f"destination {relative} is a symlink")
    raise MigrationApplyError(f"destination already exists: {relative}")


def _rename_noreplace(
    source_name: str,
    destination_name: str,
    *,
    src_dir_fd: int,
    dst_dir_fd: int,
) -> None:
    platform = "linux" if sys.platform.startswith("linux") else sys.platform
    primitive = ATOMIC_RENAME_FLAGS.get(platform)
    if primitive is None:
        raise MigrationApplyError(
            f"atomic no-replace rename is unsupported on {sys.platform}"
        )
    symbol, flag = primitive
    library = ctypes.CDLL(None, use_errno=True)
    try:
        function = getattr(library, symbol)
    except AttributeError as error:
        raise MigrationApplyError(
            f"atomic no-replace rename primitive {symbol} is unavailable"
        ) from error
    function.argtypes = (
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_int,
        ctypes.c_char_p,
        ctypes.c_uint,
    )
    function.restype = ctypes.c_int
    result = function(
        src_dir_fd,
        os.fsencode(source_name),
        dst_dir_fd,
        os.fsencode(destination_name),
        flag,
    )
    if result == 0:
        return
    error_number = ctypes.get_errno()
    if error_number == errno.EEXIST:
        raise FileExistsError(
            error_number, os.strerror(error_number), destination_name
        )
    raise OSError(error_number, os.strerror(error_number), destination_name)


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
            root_fd, move.destination
        )
        if os.fstat(source_parent_fd).st_dev != os.fstat(destination_parent_fd).st_dev:
            raise MigrationApplyError(
                f"source and destination are on different filesystems: {move.source}"
            )
        _ensure_destination_absent(
            destination_parent_fd, destination_name, move.destination
        )
        try:
            _rename_noreplace(
                source_name,
                destination_name,
                src_dir_fd=source_parent_fd,
                dst_dir_fd=destination_parent_fd,
            )
        except FileExistsError as error:
            raise MigrationApplyError(
                f"destination appeared after preflight: {move.destination}"
            ) from error
        entry = JournalEntry(move, source_unlinked=True)
        journal.append(entry)
        try:
            destination_metadata = os.stat(
                destination_name,
                dir_fd=destination_parent_fd,
                follow_symlinks=False,
            )
            moved_identity = (
                destination_metadata.st_dev,
                destination_metadata.st_ino,
            )
            moved_digest, moved_size, _ = _hash_open_file(
                destination_parent_fd,
                destination_name,
                f"destination {move.destination}",
            )
            if moved_size != move.size_bytes or moved_digest != move.sha256:
                raise MigrationApplyError(
                    f"source hash mismatch after atomic move: {move.source}"
                )
            if _path_identity(
                root_fd,
                move.destination,
                f"destination {move.destination}",
            ) != moved_identity:
                raise MigrationApplyError(
                    f"source or destination changed after preflight: {move.source}"
                )
            try:
                os.stat(
                    source_name,
                    dir_fd=source_parent_fd,
                    follow_symlinks=False,
                )
            except FileNotFoundError:
                pass
            else:
                raise MigrationApplyError(
                    f"source or destination changed after preflight: {move.source}"
                )
        except BaseException as verification_error:
            try:
                _rename_noreplace(
                    destination_name,
                    source_name,
                    src_dir_fd=destination_parent_fd,
                    dst_dir_fd=source_parent_fd,
                )
                journal.pop()
            except BaseException as cleanup_error:
                raise MigrationApplyError(
                    "CRITICAL atomic move cleanup failed after "
                    f"{verification_error}: {cleanup_error}"
                ) from verification_error
            if isinstance(verification_error, MigrationApplyError):
                if " is missing" in str(verification_error):
                    raise MigrationApplyError(
                        f"source or destination changed after preflight: {move.source}"
                    ) from verification_error
                raise
            raise MigrationApplyError(str(verification_error)) from verification_error
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
        _ensure_destination_absent(source_parent_fd, source_name, move.source)
        _rename_noreplace(
            destination_name,
            source_name,
            src_dir_fd=destination_parent_fd,
            dst_dir_fd=source_parent_fd,
        )
        _verify_file(root_fd, move.source, move, "rolled back source")
    finally:
        if source_parent_fd is not None:
            os.close(source_parent_fd)
        os.close(destination_parent_fd)


def _remove_created_directory(root_fd: int, parts: tuple[str, ...]) -> None:
    relative = "/".join(parts)
    parent_relative = "/".join(parts[:-1])
    if parent_relative:
        try:
            parent_fd, _ = _open_parent(
                root_fd, f"{parent_relative}/placeholder"
            )
        except MigrationApplyError as error:
            if "ancestor is missing" in str(error):
                return
            raise
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
    journal: list[JournalEntry],
    recovery_journal: RecoveryJournal,
    journal_directory_fd: int,
) -> list[str]:
    failures: list[str] = []
    while journal:
        entry = journal[-1]
        move = entry.move
        try:
            _rollback_entry(root_fd, entry)
        except BaseException as error:
            failures.append(f"{move.destination} -> {move.source}: {error}")
            return failures
        journal.pop()
        recovery_journal.completed_moves = len(journal)
        try:
            _write_journal(journal_directory_fd, recovery_journal)
        except BaseException as error:
            failures.append(f"cannot checkpoint rollback: {error}")
            return failures
    try:
        _remove_journal_directories(
            root_fd, recovery_journal.created_directories
        )
        _delete_journal(journal_directory_fd)
    except BaseException as error:
        failures.append(str(error))
    return failures


def _apply(
    root_fd: int,
    moves: Sequence[Move],
    recovery_journal: RecoveryJournal,
    journal_directory_fd: int,
) -> int:
    journal: list[JournalEntry] = []
    try:
        for move in moves:
            _move_one(root_fd, move, journal)
            _verify_file(root_fd, move.destination, move, "destination")
            recovery_journal.completed_moves = len(journal)
            _write_journal(journal_directory_fd, recovery_journal)
        return len(journal)
    except BaseException as original_error:
        failures = _rollback(
            root_fd,
            journal,
            recovery_journal,
            journal_directory_fd,
        )
        if failures:
            detail = "; ".join(failures)
            raise MigrationApplyError(
                f"CRITICAL rollback failed after {original_error}: {detail}"
            ) from original_error
        if isinstance(original_error, MigrationApplyError):
            raise
        raise MigrationApplyError(str(original_error)) from original_error


def _start_application(
    root_fd: int,
    journal_directory_fd: int,
    moves: Sequence[Move],
    recovery_journal: RecoveryJournal,
) -> int:
    _write_journal(journal_directory_fd, recovery_journal)
    try:
        _create_planned_directories(
            root_fd, recovery_journal.created_directories
        )
    except BaseException as original_error:
        failures = _rollback(
            root_fd,
            [],
            recovery_journal,
            journal_directory_fd,
        )
        if failures:
            raise MigrationApplyError(
                "CRITICAL rollback failed after directory creation error "
                f"{original_error}: {'; '.join(failures)}"
            ) from original_error
        if isinstance(original_error, MigrationApplyError):
            raise
        raise MigrationApplyError(str(original_error)) from original_error
    files_moved = _apply(
        root_fd,
        moves,
        recovery_journal,
        journal_directory_fd,
    )
    _delete_journal(journal_directory_fd)
    return files_moved


def main(arguments: list[str] | None = None) -> int:
    root_fd: int | None = None
    journal_directory_fd: int | None = None
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
        bundle = _load_manifest(
            vault,
            root_fd,
            relative_manifest,
            args.phase,
            args.expected_head,
        )
        journal_directory_fd = _open_journal_directory(root_fd)
        existing_journal = _read_journal(journal_directory_fd)
        if existing_journal is not None:
            if args.dry_run:
                raise MigrationApplyError(
                    "CRITICAL recovery journal requires a non-dry-run recovery"
                )
            _recover_journal(
                root_fd,
                journal_directory_fd,
                existing_journal,
                expected_head=args.expected_head,
                relative_manifest=relative_manifest,
                bundle=bundle,
                phase=args.phase,
            )
        preflight = _preflight(root_fd, bundle.moves)
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
        planned_directories = _planned_destination_directories(
            root_fd, preflight.moves
        )
        recovery_journal = RecoveryJournal(
            expected_head=args.expected_head,
            manifest_path=relative_manifest,
            manifest_sha256=bundle.sha256,
            move_set_sha256=_move_set_sha256(bundle.moves),
            phase=args.phase,
            move_count=len(bundle.moves),
            completed_moves=0,
            created_directories=planned_directories,
        )
        files_moved = _start_application(
            root_fd,
            journal_directory_fd,
            preflight.moves,
            recovery_journal,
        )
        print(f"planned_moves={len(preflight.moves)}")
        print("preflight=ok")
        print(f"files_moved={files_moved}")
        return 0
    except (MigrationApplyError, InventoryError, RuleError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    finally:
        if journal_directory_fd is not None:
            os.close(journal_directory_fd)
        if root_fd is not None:
            os.close(root_fd)


if __name__ == "__main__":
    raise SystemExit(main())
