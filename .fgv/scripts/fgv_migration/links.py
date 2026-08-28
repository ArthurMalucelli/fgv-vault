"""Deterministically audit Obsidian wikilinks from an immutable Git tree."""

from collections import defaultdict
from dataclasses import dataclass
import hashlib
import os
from pathlib import Path, PurePosixPath
import posixpath
import re
import subprocess
import unicodedata
from typing import Mapping
from urllib.parse import unquote

from .inventory import normalize_relative_path
from .rules import validate_manifest


AUDIT_METHOD = "manifest-source-git-wikilink-audit-v2"
WIKILINK_PATTERN = re.compile(r"(?<!!)\[\[([^\]\n]+)\]\]")


class LinkAuditError(ValueError):
    """The fixed-tree link audit cannot be completed safely."""


@dataclass(frozen=True)
class LinkAudit:
    total: int
    resolved: int
    unresolved: int
    ambiguous: int

    def __post_init__(self) -> None:
        if self.total != self.resolved + self.unresolved + self.ambiguous:
            raise LinkAuditError("link audit counts do not sum to total")

    def as_dict(self) -> dict[str, int]:
        return {
            "total": self.total,
            "resolved": self.resolved,
            "unresolved": self.unresolved,
            "ambiguous": self.ambiguous,
        }


def _key(value: str) -> str:
    return unicodedata.normalize("NFC", value).casefold()


def _without_markdown_suffix(path: str) -> str:
    return path[:-3] if path.casefold().endswith(".md") else path


def _clean_target(raw_target: str) -> str:
    target = raw_target.split("|", 1)[0]
    target = target.split("#", 1)[0]
    target = unquote(target)
    target = target.replace("\\", "/")
    target = _without_markdown_suffix(target)
    return target.strip("/")


def audit_note_contents(notes: Mapping[str, str | bytes]) -> LinkAudit:
    """Audit wikilinks in the provided manifest-scoped Markdown notes."""
    normalized_notes: dict[str, str] = {}
    for raw_path, raw_content in notes.items():
        path = normalize_relative_path(raw_path)
        if path != raw_path:
            raise LinkAuditError(f"note path must be NFC canonical: {raw_path!r}")
        if not path.casefold().endswith(".md"):
            continue
        content = (
            raw_content.decode("utf-8", errors="replace")
            if isinstance(raw_content, bytes)
            else raw_content
        )
        if type(content) is not str:
            raise LinkAuditError(f"note content must be text or bytes: {path!r}")
        normalized_notes[path] = content

    path_index: dict[str, set[str]] = defaultdict(set)
    basename_index: dict[str, set[str]] = defaultdict(set)
    for path in normalized_notes:
        note_path = _without_markdown_suffix(path)
        path_index[_key(note_path)].add(path)
        basename_index[_key(PurePosixPath(note_path).name)].add(path)

    total = 0
    resolved = 0
    unresolved = 0
    ambiguous = 0
    for source, content in normalized_notes.items():
        source_note_path = _without_markdown_suffix(source)
        source_parent = PurePosixPath(source_note_path).parent.as_posix()
        for match in WIKILINK_PATTERN.finditer(content):
            total += 1
            target = _clean_target(match.group(1))
            if not target:
                candidates = {source}
            else:
                root_target = posixpath.normpath(target)
                relative_target = posixpath.normpath(
                    posixpath.join(source_parent, target)
                )
                basename_target = PurePosixPath(target).name
                candidates = set(path_index.get(_key(root_target), ()))
                candidates.update(path_index.get(_key(relative_target), ()))
                candidates.update(
                    basename_index.get(_key(basename_target), ())
                )

            if len(candidates) == 1:
                resolved += 1
            elif candidates:
                ambiguous += 1
            else:
                unresolved += 1

    return LinkAudit(
        total=total,
        resolved=resolved,
        unresolved=unresolved,
        ambiguous=ambiguous,
    )


def _run_git(
    vault: Path, arguments: tuple[str, ...], *, input_bytes: bytes | None = None
) -> subprocess.CompletedProcess:
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
            input=input_bytes,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as error:
        raise LinkAuditError(f"cannot execute git: {error}") from error


def _checked_git(
    vault: Path, arguments: tuple[str, ...], *, input_bytes: bytes | None = None
) -> bytes:
    result = _run_git(vault, arguments, input_bytes=input_bytes)
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise LinkAuditError(f"git {' '.join(arguments)} failed: {detail}")
    return result.stdout


def _tree_blob_ids(
    vault: Path, base_commit: str, sources: set[str]
) -> dict[str, str]:
    if (
        not base_commit
        or base_commit.startswith("-")
        or any(character in base_commit for character in ("\x00", "\n"))
    ):
        raise LinkAuditError(f"unsafe base commit: {base_commit!r}")
    resolved_commit = _checked_git(
        vault,
        (
            "rev-parse",
            "--verify",
            "--end-of-options",
            f"{base_commit}^{{commit}}",
        ),
    ).decode("ascii").strip()
    tree_oid = _checked_git(
        vault,
        (
            "rev-parse",
            "--verify",
            "--end-of-options",
            f"{resolved_commit}^{{tree}}",
        ),
    ).decode("ascii").strip()
    listing = _checked_git(vault, ("ls-tree", "-rz", "--full-tree", tree_oid))

    blob_ids: dict[str, str] = {}
    for raw_record in listing.split(b"\x00"):
        if not raw_record:
            continue
        try:
            metadata, raw_path = raw_record.split(b"\t", 1)
            mode, object_type, object_id = metadata.split(b" ", 2)
            path = normalize_relative_path(raw_path.decode("utf-8", errors="strict"))
        except (UnicodeDecodeError, ValueError) as error:
            raise LinkAuditError("Git tree contains an invalid path record") from error
        if path not in sources:
            continue
        if mode == b"120000" or object_type != b"blob":
            raise LinkAuditError(f"manifest source is not a regular blob: {path!r}")
        blob_ids[path] = object_id.decode("ascii")

    missing = sorted(sources.difference(blob_ids), key=lambda value: value.encode())
    if missing:
        raise LinkAuditError(f"manifest sources missing from base commit: {missing!r}")
    return blob_ids


def _read_blobs(vault: Path, blob_ids: Mapping[str, str]) -> dict[str, bytes]:
    sources = sorted(blob_ids, key=lambda value: value.encode("utf-8"))
    query = b"".join(blob_ids[source].encode("ascii") + b"\n" for source in sources)
    output = _checked_git(vault, ("cat-file", "--batch"), input_bytes=query)

    cursor = 0
    contents: dict[str, bytes] = {}
    for source in sources:
        header_end = output.find(b"\n", cursor)
        if header_end < 0:
            raise LinkAuditError("truncated git cat-file header")
        try:
            object_id, object_type, raw_size = output[cursor:header_end].split(b" ", 2)
            size = int(raw_size)
        except ValueError as error:
            raise LinkAuditError("invalid git cat-file header") from error
        if object_id.decode("ascii") != blob_ids[source] or object_type != b"blob":
            raise LinkAuditError(f"unexpected git object for {source!r}")
        content_start = header_end + 1
        content_end = content_start + size
        if content_end >= len(output) or output[content_end : content_end + 1] != b"\n":
            raise LinkAuditError(f"truncated git blob for {source!r}")
        contents[source] = output[content_start:content_end]
        cursor = content_end + 1
    if cursor != len(output):
        raise LinkAuditError("unexpected trailing git cat-file output")
    return contents


def audit_manifest_links(
    vault: Path, base_commit: str, manifest: object
) -> LinkAudit:
    """Audit only manifest sources, read byte-exactly from a fixed Git commit."""
    validate_manifest(manifest)
    markdown_records = {
        str(record["source"]): record
        for record in manifest
        if str(record["source"]).casefold().endswith(".md")
    }
    blob_ids = _tree_blob_ids(Path(vault), base_commit, set(markdown_records))
    contents = _read_blobs(Path(vault), blob_ids)
    for source, content in contents.items():
        record = markdown_records[source]
        if (
            hashlib.sha256(content).hexdigest() != record["sha256"]
            or len(content) != record["size_bytes"]
        ):
            raise LinkAuditError(f"manifest integrity mismatch for {source!r}")
    return audit_note_contents(contents)
