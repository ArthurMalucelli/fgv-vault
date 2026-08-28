"""Read deterministic inventories from a vault or a Git tree."""

from dataclasses import dataclass
import hashlib
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import unicodedata
from typing import Iterable


IGNORED_ROOTS = frozenset(
    {
        ".git",
        ".obsidian",
        ".fgv",
        "00 Home",
        "10 Matérias",
        "20 Conhecimento",
        "30 Sistema",
        "90 Arquivo",
    }
)
IGNORED_FILES = frozenset({".gitignore"})


class InventoryError(ValueError):
    """The source inventory cannot be represented safely."""


@dataclass(frozen=True)
class InventoryEntry:
    path: str
    sha256: str
    size_bytes: int


def normalize_relative_path(value: str) -> str:
    if "\x00" in value or "\\" in value:
        raise InventoryError(f"unsafe relative path: {value!r}")
    normalized = unicodedata.normalize("NFC", value)
    path = PurePosixPath(normalized)
    if not normalized or path.is_absolute() or ".." in path.parts:
        raise InventoryError(f"unsafe relative path: {value!r}")
    return path.as_posix()


def _ignored(path: str, output_paths: frozenset[str]) -> bool:
    parsed = PurePosixPath(path)
    return (
        parsed.name in IGNORED_FILES
        or parsed.parts[0] in IGNORED_ROOTS
        or path in output_paths
    )


def _normalized_outputs(output_paths: Iterable[str]) -> frozenset[str]:
    return frozenset(normalize_relative_path(path) for path in output_paths)


def _entry(path: str, data: bytes) -> InventoryEntry:
    return InventoryEntry(
        path=path,
        sha256=hashlib.sha256(data).hexdigest(),
        size_bytes=len(data),
    )


def _sort_and_validate(entries: list[InventoryEntry]) -> tuple[InventoryEntry, ...]:
    by_path: dict[str, str] = {}
    for item in entries:
        normalized = unicodedata.normalize("NFC", item.path)
        previous = by_path.get(normalized)
        if previous is not None:
            raise InventoryError(
                f"source path collision after NFC: {previous!r} and {item.path!r}"
            )
        by_path[normalized] = item.path
    return tuple(sorted(entries, key=lambda item: item.path.encode("utf-8")))


def inventory_from_filesystem(
    vault: Path, *, output_paths: Iterable[str] = ()
) -> tuple[InventoryEntry, ...]:
    root = Path(vault)
    if not root.is_dir():
        raise InventoryError(f"vault is not a directory: {root}")
    outputs = _normalized_outputs(output_paths)
    entries: list[InventoryEntry] = []

    for directory, directory_names, file_names in os.walk(root, followlinks=False):
        current = Path(directory)
        relative_directory = current.relative_to(root)
        retained_directories: list[str] = []
        for name in directory_names:
            candidate = current / name
            relative = normalize_relative_path((relative_directory / name).as_posix())
            if _ignored(relative, outputs):
                continue
            if candidate.is_symlink():
                raise InventoryError(f"symlink is not allowed: {relative}")
            retained_directories.append(name)
        directory_names[:] = retained_directories

        for name in file_names:
            candidate = current / name
            relative = normalize_relative_path((relative_directory / name).as_posix())
            if _ignored(relative, outputs):
                continue
            if candidate.is_symlink():
                raise InventoryError(f"symlink is not allowed: {relative}")
            try:
                data = candidate.read_bytes()
            except OSError as error:
                raise InventoryError(f"cannot read {relative}: {error}") from error
            entries.append(_entry(relative, data))

    return _sort_and_validate(entries)


def _run_git(vault: Path, arguments: tuple[str, ...]) -> subprocess.CompletedProcess:
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
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
        raise InventoryError(f"cannot execute git: {error}") from error


def inventory_from_git(
    vault: Path, base_ref: str, *, output_paths: Iterable[str] = ()
) -> tuple[InventoryEntry, ...]:
    root = Path(vault)
    if not root.is_dir():
        raise InventoryError(f"vault is not a directory: {root}")
    if not base_ref or base_ref.startswith("-") or "\x00" in base_ref or "\n" in base_ref:
        raise InventoryError(f"unsafe base-ref: {base_ref!r}")

    resolved_tree = _run_git(
        root,
        (
            "rev-parse",
            "--verify",
            "--end-of-options",
            f"{base_ref}^{{tree}}",
        ),
    )
    if resolved_tree.returncode != 0:
        detail = resolved_tree.stderr.decode("utf-8", errors="replace").strip()
        raise InventoryError(f"cannot read base-ref {base_ref!r}: {detail}")
    try:
        tree_oid = resolved_tree.stdout.decode("ascii").strip()
    except UnicodeDecodeError as error:
        raise InventoryError(f"invalid tree OID for base-ref {base_ref!r}") from error
    if re.fullmatch(r"(?:[0-9a-f]{40}|[0-9a-f]{64})", tree_oid) is None:
        raise InventoryError(f"invalid tree OID for base-ref {base_ref!r}")

    outputs = _normalized_outputs(output_paths)
    listing = _run_git(root, ("ls-tree", "-rz", "--full-tree", tree_oid))
    if listing.returncode != 0:
        detail = listing.stderr.decode("utf-8", errors="replace").strip()
        raise InventoryError(f"cannot read base-ref {base_ref!r}: {detail}")

    entries: list[InventoryEntry] = []
    for raw_record in listing.stdout.split(b"\x00"):
        if not raw_record:
            continue
        try:
            metadata, raw_path = raw_record.split(b"\t", 1)
            mode, object_type, object_id = metadata.split(b" ", 2)
            source = normalize_relative_path(raw_path.decode("utf-8", errors="strict"))
        except (UnicodeDecodeError, ValueError) as error:
            raise InventoryError("Git tree contains an invalid path record") from error

        if _ignored(source, outputs):
            continue
        if mode == b"120000":
            raise InventoryError(f"symlink is not allowed: {source}")
        if object_type != b"blob":
            raise InventoryError(
                f"unsupported Git tree entry for {source}: {object_type.decode('ascii', errors='replace')}"
            )

        blob = _run_git(root, ("cat-file", "blob", object_id.decode("ascii")))
        if blob.returncode != 0:
            detail = blob.stderr.decode("utf-8", errors="replace").strip()
            raise InventoryError(f"cannot read blob for {source}: {detail}")
        entries.append(_entry(source, blob.stdout))

    return _sort_and_validate(entries)
