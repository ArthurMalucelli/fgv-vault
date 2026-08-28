#!/usr/bin/env python3
"""Plan and transactionally apply the audited active lesson-note renames."""

from __future__ import annotations

import argparse
import ast
from dataclasses import dataclass
from datetime import date
import fcntl
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import secrets
import stat
import subprocess
import sys
import unicodedata
from typing import Mapping, Sequence


DEFAULT_EXPECTED_HEAD = "dc7a1cde627e2211fa7457367c160759e6ac7993"
DEFAULT_EXPECTED_TREE = "1a8b7dd3abf7febbcb9d0b39d44d721e40ebe043"
MANIFEST_RELATIVE = "30 Sistema/Estado/lesson-rename-manifest.json"
JOURNAL_NAME = "lesson-rename-journal.json"
JOURNAL_RELATIVE = f".fgv/{JOURNAL_NAME}"
SCHEMA = "fgv.lesson-renames.v1"
TRANSFORM_ID = "matematica-aplicada-08.06-short-links-v1"
NONE_TRANSFORM_ID = "none"
CORRECTED_TOPIC = (
    "Exercício prático (Loja da Sofia) - equação patrimonial, "
    "BP, DRE e DFC pelo método direto"
)
CORRECTED_TOPIC_PREFIX = "10 Matérias/ContabilidadeFinanceira/Aulas/08.10/"
MATH_SUMMARY = "10 Matérias/MatemáticaAplicada/Aulas/08.06/Resumo.md"
MATH_TRANSCRIPT = "10 Matérias/MatemáticaAplicada/Aulas/08.06/Transcrito.md"
TOOLING_DIRTY_ALLOWLIST = {
    ".fgv/scripts/rename_lesson_notes.py",
    ".fgv/tests/test_lesson_renames.py",
}

MANIFEST_FIELDS = (
    "schema",
    "schema_version",
    "authority_commit",
    "authority_tree",
    "record_count",
    "aggregate_sha256",
    "records",
)
MANIFEST_RECORD_FIELDS = (
    "source",
    "destination",
    "subject_id",
    "class_date",
    "kind",
    "topic",
    "original_sha256",
    "original_size_bytes",
    "original_mode",
    "final_sha256",
    "final_size_bytes",
    "final_mode",
    "original_body_sha256",
    "final_body_sha256",
    "content_class",
    "transform_id",
    "transform_occurrences",
)
JOURNAL_FIELDS = (
    "schema_version",
    "expected_head",
    "manifest_sha256",
    "completed_steps",
    "operations",
)
JOURNAL_OPERATION_FIELDS = (
    "source",
    "destination",
    "original_sha256",
    "final_sha256",
    "mode",
)

GENERIC_NAMES = {"Resumo.md": "resumo", "Transcrito.md": "transcrito"}
FORBIDDEN_COMPONENT = re.compile(r"[<>:\"/\\|?*\x00-\x1f\x7f]+")
CLASS_PATH = re.compile(
    r"^10 Matérias/([^/]+)/Aulas/(\d{2})\.(\d{2})/(Resumo|Transcrito)\.md$"
)
HEX_OID = re.compile(r"[0-9a-f]{40}|[0-9a-f]{64}")
HEX_SHA256 = re.compile(r"[0-9a-f]{64}")
DIRECTORY_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
FILE_FLAGS = os.O_RDONLY | os.O_NOFOLLOW
TEMP_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW


class RenameError(ValueError):
    """The rename plan or filesystem state violates the closed contract."""


@dataclass(frozen=True)
class ParsedFrontmatter:
    values: Mapping[str, str]
    preserved_lines: tuple[str, ...]
    body: bytes


@dataclass(frozen=True)
class NormalizedNote:
    topic: str
    class_date: str
    legacy_subject: str
    original_body: bytes
    final_body: bytes
    final_bytes: bytes
    content_class: str
    transform_id: str
    transform_occurrences: int


@dataclass(frozen=True)
class GitEntry:
    path: str
    mode: str
    oid: str
    payload: bytes


@dataclass(frozen=True)
class RenameOperation:
    source: str
    destination: str
    subject_id: str
    class_date: str
    kind: str
    topic: str
    original: bytes
    final: bytes
    mode: str
    original_body: bytes
    final_body: bytes
    content_class: str
    transform_id: str
    transform_occurrences: int

    @property
    def permission_mode(self) -> int:
        return int(self.mode[-3:], 8)

    def record(self) -> dict[str, object]:
        values: tuple[object, ...] = (
            self.source,
            self.destination,
            self.subject_id,
            self.class_date,
            self.kind,
            self.topic,
            _sha256(self.original),
            len(self.original),
            self.mode,
            _sha256(self.final),
            len(self.final),
            self.mode,
            _sha256(self.original_body),
            _sha256(self.final_body),
            self.content_class,
            self.transform_id,
            self.transform_occurrences,
        )
        return dict(zip(MANIFEST_RECORD_FIELDS, values))


@dataclass(frozen=True)
class RenamePlan:
    expected_head: str
    authority_tree: str
    operations: tuple[RenameOperation, ...]
    archive_entries: tuple[GitEntry, ...]
    manifest: Mapping[str, object]
    manifest_bytes: bytes


@dataclass(frozen=True)
class RenameReport:
    status: str
    active_generic_notes: int
    rename_operations: int
    missing_tema: int
    collisions: int
    archive_operations: int
    plan: RenamePlan


@dataclass
class OpenRename:
    operation: RenameOperation
    parent_fd: int
    parent_device: int
    parent_inode: int
    source_name: str
    destination_name: str

    def close(self) -> None:
        if self.parent_fd >= 0:
            os.close(self.parent_fd)
            self.parent_fd = -1


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def _canonical_relative(value: str) -> str:
    if type(value) is not str or not value or "\x00" in value or "\\" in value:
        raise RenameError(f"invalid relative path: {value!r}")
    normalized = _nfc(value)
    pure = PurePosixPath(normalized)
    if normalized != value or pure.is_absolute() or not pure.parts or ".." in pure.parts:
        raise RenameError(f"path is not canonical NFC relative POSIX: {value!r}")
    if pure.as_posix() != value:
        raise RenameError(f"path is not canonical: {value!r}")
    return value


def assert_distinct_paths(source: str, destination: str) -> None:
    _canonical_relative(source)
    _canonical_relative(destination)
    if source == destination:
        raise RenameError(f"source and destination are identical: {source!r}")


def normalize_topic(topic: str) -> str:
    if type(topic) is not str:
        raise RenameError("tema must be text")
    value = _nfc(topic)
    separator = "\x00"
    value = FORBIDDEN_COMPONENT.sub(separator, value)
    value = re.sub(r"\s+", " ", value)
    value = re.sub(rf"(?: *{separator} *)+", separator, value)
    value = value.strip(f" .{separator}")
    if not value:
        raise RenameError("tema is empty after portable normalization")
    return re.sub(r" +", " ", value.replace(separator, " - "))


def destination_name(kind: str, topic: str) -> str:
    prefixes = {"resumo": "Resumo", "transcrito": "Transcrito"}
    if kind not in prefixes:
        raise RenameError(f"invalid note kind: {kind!r}")
    normalized = normalize_topic(topic)
    component = f"{prefixes[kind]} - {normalized}.md"
    if len(component.encode("utf-8")) > 255:
        raise RenameError("destination basename exceeds 255 UTF-8 bytes")
    if component.endswith((" ", ". ")):
        raise RenameError("destination basename has a non-portable suffix")
    return component


def _parse_scalar(value: str, field: str) -> str:
    stripped = value.strip()
    if not stripped:
        return ""
    if stripped[:1] in {"'", '"'}:
        try:
            parsed = ast.literal_eval(stripped)
        except (SyntaxError, ValueError) as error:
            raise RenameError(f"invalid quoted {field}") from error
        if type(parsed) is not str:
            raise RenameError(f"{field} must be text")
        return _nfc(parsed)
    return _nfc(stripped)


def _split_frontmatter(payload: bytes, source: str) -> ParsedFrontmatter:
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError as error:
        raise RenameError(f"note is not valid UTF-8: {source!r}") from error
    lines = text.splitlines(keepends=True)
    if not lines or lines[0].rstrip("\r\n") != "---":
        raise RenameError(f"frontmatter is missing: {source!r}")
    closing = None
    for index, line in enumerate(lines[1:], start=1):
        if line.rstrip("\r\n") == "---":
            closing = index
            break
    if closing is None:
        raise RenameError(f"frontmatter has no closing delimiter: {source!r}")
    values: dict[str, str] = {}
    preserved: list[str] = []
    canonical_keys = {
        "materia",
        "materias",
        "semestre",
        "data",
        "tipo",
        "tema",
        "status",
        "contract_version",
    }
    active_preserved = False
    for raw_line in lines[1:closing]:
        line = raw_line.rstrip("\r\n")
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            preserved.append(line)
            active_preserved = True
            continue
        if line[:1].isspace():
            if not active_preserved:
                raise RenameError(f"unsupported nested canonical frontmatter: {source!r}")
            preserved.append(line)
            continue
        if ":" not in line:
            raise RenameError(f"invalid frontmatter line in {source!r}: {line!r}")
        raw_key, raw_value = line.split(":", 1)
        key = _nfc(raw_key.strip())
        if not key or key in values:
            raise RenameError(f"duplicate or empty frontmatter key {key!r} in {source!r}")
        values[key] = _parse_scalar(raw_value, key)
        active_preserved = key not in canonical_keys
        if active_preserved:
            preserved.append(line)
    body = "".join(lines[closing + 1 :]).encode("utf-8")
    return ParsedFrontmatter(values, tuple(preserved), body)


def _yaml_plain(value: str) -> str:
    if (
        not value
        or value != value.strip()
        or any(character in value for character in ("\n", "\r", "#"))
        or ": " in value
        or value[:1] in "-?:,[]{}&*!|>'\"%@`"
    ):
        return json.dumps(value, ensure_ascii=False)
    return value


def _transform_body(source: str, body: bytes, topic: str) -> tuple[bytes, str, str, int]:
    if source == MATH_SUMMARY:
        old = b"[[Transcrito]]"
        count = body.count(old)
        if count == 0:
            return body, "metadata-only", NONE_TRANSFORM_ID, 0
        if count != 1:
            raise RenameError(f"authorized short-link count diverged in {source!r}")
        replacement = f"[[{destination_name('transcrito', topic)[:-3]}]]".encode("utf-8")
        return body.replace(old, replacement), "authorized-body-transform", TRANSFORM_ID, count
    if source == MATH_TRANSCRIPT:
        old = b"[[Resumo]]"
        count = body.count(old)
        if count == 0:
            return body, "metadata-only", NONE_TRANSFORM_ID, 0
        if count != 2:
            raise RenameError(f"authorized short-link count diverged in {source!r}")
        replacement = f"[[{destination_name('resumo', topic)[:-3]}]]".encode("utf-8")
        return body.replace(old, replacement), "authorized-body-transform", TRANSFORM_ID, count
    return body, "metadata-only", NONE_TRANSFORM_ID, 0


def normalize_note(
    payload: bytes,
    *,
    source: str,
    subject_id: str,
    kind: str,
    topic_override: str | None,
) -> NormalizedNote:
    _canonical_relative(source)
    parsed = _split_frontmatter(payload, source)
    legacy_subject = parsed.values.get("materia", "")
    if not legacy_subject:
        raise RenameError(f"legacy materia is missing: {source!r}")
    raw_topic = parsed.values.get("tema", "")
    if not raw_topic:
        raise RenameError(f"tema is missing: {source!r}")
    topic = CORRECTED_TOPIC if topic_override is not None else raw_topic
    if _nfc(topic) != topic:
        raise RenameError(f"tema is not NFC: {source!r}")
    normalize_topic(topic)
    class_date = parsed.values.get("data", "")
    try:
        parsed_date = date.fromisoformat(class_date)
    except ValueError as error:
        raise RenameError(f"invalid ISO data in {source!r}: {class_date!r}") from error
    match = CLASS_PATH.fullmatch(source)
    if match is None:
        raise RenameError(f"active generic note has invalid path: {source!r}")
    if (parsed_date.year, parsed_date.month, parsed_date.day) != (
        2026,
        int(match.group(2)),
        int(match.group(3)),
    ):
        raise RenameError(f"data does not match class folder: {source!r}")
    if kind != GENERIC_NAMES[PurePosixPath(source).name]:
        raise RenameError(f"kind does not match source filename: {source!r}")
    final_body, content_class, transform_id, occurrences = _transform_body(
        source, parsed.body, topic
    )
    lines = [
        "---",
        f"materias: [{subject_id}]",
        "semestre: 2026.2",
        f"data: {class_date}",
        f"tipo: {kind}",
        f"tema: {_yaml_plain(topic)}",
        "status: completo",
        "contract_version: 1",
    ]
    lines.extend(parsed.preserved_lines)
    while len(lines) > 1 and not lines[-1].strip():
        lines.pop()
    lines.extend(("---", ""))
    final = "\n".join(lines).encode("utf-8") + final_body
    return NormalizedNote(
        topic=topic,
        class_date=class_date,
        legacy_subject=legacy_subject,
        original_body=parsed.body,
        final_body=final_body,
        final_bytes=final,
        content_class=content_class,
        transform_id=transform_id,
        transform_occurrences=occurrences,
    )


def _git_environment() -> dict[str, str]:
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    environment["GIT_CONFIG_NOSYSTEM"] = "1"
    environment["GIT_CONFIG_SYSTEM"] = os.devnull
    environment["GIT_CONFIG_GLOBAL"] = os.devnull
    environment["LC_ALL"] = "C"
    return environment


def _git_bytes(
    vault: Path,
    arguments: Sequence[str],
    *,
    input_bytes: bytes | None = None,
    check: bool = True,
) -> subprocess.CompletedProcess[bytes]:
    try:
        result = subprocess.run(
            ("git", *arguments),
            cwd=vault,
            env=_git_environment(),
            input=input_bytes,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            check=False,
        )
    except OSError as error:
        raise RenameError(f"cannot execute git: {error}") from error
    if check and result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RenameError(f"git {' '.join(arguments)} failed: {detail}")
    return result


def _git_text(vault: Path, arguments: Sequence[str], *, check: bool = True) -> str:
    result = _git_bytes(vault, arguments, check=check)
    try:
        return result.stdout.decode("utf-8").strip()
    except UnicodeDecodeError as error:
        raise RenameError("git returned invalid UTF-8") from error


def _load_git_tree(vault: Path, expected_head: str) -> tuple[str, dict[str, GitEntry]]:
    if HEX_OID.fullmatch(expected_head) is None:
        raise RenameError("expected head is not a full object id")
    resolved = _git_text(
        vault,
        ("rev-parse", "--verify", "--end-of-options", f"{expected_head}^{{commit}}"),
    )
    if resolved != expected_head:
        raise RenameError("expected head does not resolve byte-exactly")
    tree = _git_text(
        vault,
        ("rev-parse", "--verify", "--end-of-options", f"{expected_head}^{{tree}}"),
    )
    listing = _git_bytes(
        vault, ("ls-tree", "-rz", "--full-tree", tree)
    ).stdout
    metadata: list[tuple[str, str, str]] = []
    for raw_record in listing.split(b"\0"):
        if not raw_record:
            continue
        try:
            raw_meta, raw_path = raw_record.split(b"\t", 1)
            raw_mode, raw_type, raw_oid = raw_meta.split(b" ", 2)
            path = raw_path.decode("utf-8")
            mode = raw_mode.decode("ascii")
            object_type = raw_type.decode("ascii")
            oid = raw_oid.decode("ascii")
        except (UnicodeDecodeError, ValueError) as error:
            raise RenameError("invalid Git tree record") from error
        _canonical_relative(path)
        if object_type != "blob":
            continue
        if mode == "120000":
            raise RenameError(f"Git symlink is forbidden: {path!r}")
        if mode not in {"100644", "100755"}:
            raise RenameError(f"unsupported Git mode for {path!r}: {mode}")
        metadata.append((path, mode, oid))
    payload_paths = {
        path
        for path, _, _ in metadata
        if path == ".fgv/config/subjects.json"
        or (
            path.startswith("10 Matérias/")
            and PurePosixPath(path).name in GENERIC_NAMES
        )
        or (
            path.startswith("90 Arquivo/2026.1/")
            and PurePosixPath(path).name in GENERIC_NAMES
        )
    }
    requested = [item for item in metadata if item[0] in payload_paths]
    query = b"".join(oid.encode("ascii") + b"\n" for _, _, oid in requested)
    batch = _git_bytes(vault, ("cat-file", "--batch"), input_bytes=query).stdout
    cursor = 0
    entries: dict[str, GitEntry] = {}
    payload_by_path: dict[str, bytes] = {}
    for path, mode, expected_oid in requested:
        header_end = batch.find(b"\n", cursor)
        if header_end < 0:
            raise RenameError("truncated git cat-file header")
        try:
            oid_raw, kind_raw, size_raw = batch[cursor:header_end].split(b" ", 2)
            size = int(size_raw)
        except ValueError as error:
            raise RenameError("invalid git cat-file header") from error
        if oid_raw.decode("ascii") != expected_oid or kind_raw != b"blob":
            raise RenameError(f"unexpected Git object for {path!r}")
        start = header_end + 1
        end = start + size
        if end >= len(batch) or batch[end : end + 1] != b"\n":
            raise RenameError("truncated git cat-file payload")
        payload_by_path[path] = batch[start:end]
        cursor = end + 1
    if cursor != len(batch):
        raise RenameError("unexpected trailing git cat-file bytes")
    for path, mode, oid in metadata:
        entries[path] = GitEntry(path, mode, oid, payload_by_path.get(path, b""))
    return tree, entries


def _load_subjects(payload: bytes) -> tuple[dict[str, Mapping[str, object]], str]:
    try:
        raw = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RenameError("invalid canonical subjects config") from error
    if type(raw) is not dict or raw.get("schema_version") != 1:
        raise RenameError("subjects config schema is invalid")
    if raw.get("semester") != "2026.2":
        raise RenameError("subjects config semester is not 2026.2")
    subjects = raw.get("subjects")
    if type(subjects) is not list:
        raise RenameError("subjects config subjects must be an array")
    by_path: dict[str, Mapping[str, object]] = {}
    for subject in subjects:
        if type(subject) is not dict:
            raise RenameError("subject record must be an object")
        subject_id = subject.get("id")
        path = subject.get("path")
        if type(subject_id) is not str or type(path) is not str:
            raise RenameError("subject id/path must be text")
        _canonical_relative(path)
        if path in by_path:
            raise RenameError(f"duplicate subject path: {path!r}")
        by_path[path] = subject
    return by_path, str(raw["semester"])


def _subject_accepts_legacy(subject: Mapping[str, object], legacy: str) -> bool:
    values: set[str] = set()
    for key in ("id", "display_name", "folder"):
        value = subject.get(key)
        if type(value) is str:
            values.add(_nfc(value).casefold())
    for key in ("aliases", "legacy_frontmatter_values"):
        value = subject.get(key, [])
        if type(value) is list:
            values.update(
                _nfc(item).casefold() for item in value if type(item) is str
            )
    return _nfc(legacy).casefold() in values


def _collision_keys(path: str) -> tuple[str, str, str]:
    return (
        path,
        path.casefold(),
        unicodedata.normalize("NFD", path).casefold(),
    )


def _manifest_record_json(record: Mapping[str, object]) -> bytes:
    return json.dumps(
        record,
        ensure_ascii=False,
        separators=(",", ":"),
    ).encode("utf-8")


def _aggregate_manifest(
    authority_commit: str,
    authority_tree: str,
    records: Sequence[Mapping[str, object]],
) -> str:
    digest = hashlib.sha256()
    for component in (
        SCHEMA.encode("utf-8"),
        authority_commit.encode("ascii"),
        authority_tree.encode("ascii"),
        str(len(records)).encode("ascii"),
    ):
        digest.update(component)
        digest.update(b"\0")
    for record in records:
        digest.update(_manifest_record_json(record))
        digest.update(b"\0")
    return digest.hexdigest()


def _serialize_manifest(value: Mapping[str, object]) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def validate_manifest_bytes(payload: bytes, expected_head: str) -> Mapping[str, object]:
    try:
        value = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RenameError("invalid lesson rename manifest JSON") from error
    if type(value) is not dict or tuple(value) != MANIFEST_FIELDS:
        raise RenameError("lesson rename manifest root schema is not closed")
    if value["schema"] != SCHEMA or value["schema_version"] != 1:
        raise RenameError("lesson rename manifest schema/version is invalid")
    if value["authority_commit"] != expected_head:
        raise RenameError("lesson rename authority commit mismatch")
    authority_tree = value["authority_tree"]
    if type(authority_tree) is not str or HEX_OID.fullmatch(authority_tree) is None:
        raise RenameError("lesson rename authority tree is invalid")
    records = value["records"]
    if type(records) is not list or value["record_count"] != len(records):
        raise RenameError("lesson rename record count mismatch")
    if type(value["record_count"]) is not int or not records:
        raise RenameError("lesson rename records must be non-empty")
    previous = ""
    for record in records:
        if type(record) is not dict or tuple(record) != MANIFEST_RECORD_FIELDS:
            raise RenameError("lesson rename record schema is not closed")
        source = record["source"]
        destination = record["destination"]
        if type(source) is not str or type(destination) is not str:
            raise RenameError("manifest paths must be text")
        _canonical_relative(source)
        _canonical_relative(destination)
        assert_distinct_paths(source, destination)
        if previous and source <= previous:
            raise RenameError("manifest records are not strictly source-sorted")
        previous = source
        if record["kind"] not in {"resumo", "transcrito"}:
            raise RenameError("manifest kind is invalid")
        try:
            date.fromisoformat(str(record["class_date"]))
        except ValueError as error:
            raise RenameError("manifest class_date is invalid") from error
        for key in (
            "original_sha256",
            "final_sha256",
            "original_body_sha256",
            "final_body_sha256",
        ):
            if type(record[key]) is not str or HEX_SHA256.fullmatch(record[key]) is None:
                raise RenameError(f"manifest {key} is invalid")
        for key in ("original_size_bytes", "final_size_bytes", "transform_occurrences"):
            if type(record[key]) is not int or record[key] < 0:
                raise RenameError(f"manifest {key} is invalid")
        if record["original_mode"] not in {"100644", "100755"}:
            raise RenameError("manifest original mode is invalid")
        if record["final_mode"] != record["original_mode"]:
            raise RenameError("manifest mode changed")
        content_class = record["content_class"]
        if content_class == "metadata-only":
            if (
                record["transform_id"] != NONE_TRANSFORM_ID
                or record["transform_occurrences"] != 0
                or record["original_body_sha256"] != record["final_body_sha256"]
            ):
                raise RenameError("metadata-only manifest record is inconsistent")
        elif content_class == "authorized-body-transform":
            if (
                record["transform_id"] != TRANSFORM_ID
                or record["transform_occurrences"] <= 0
            ):
                raise RenameError("body-transform manifest record is inconsistent")
        else:
            raise RenameError("manifest content class is invalid")
    expected_aggregate = _aggregate_manifest(
        expected_head,
        str(authority_tree),
        records,
    )
    if value["aggregate_sha256"] != expected_aggregate:
        raise RenameError("lesson rename aggregate hash mismatch")
    if _serialize_manifest(value) != payload:
        raise RenameError("lesson rename manifest serialization is not canonical")
    return value


def build_plan(
    vault: Path,
    expected_head: str,
    *,
    expected_active: int,
    expected_archive: int,
) -> RenamePlan:
    vault = Path(vault).resolve(strict=True)
    tree, entries = _load_git_tree(vault, expected_head)
    config_entry = entries.get(".fgv/config/subjects.json")
    if config_entry is None:
        raise RenameError("canonical subjects config is absent from authority tree")
    subjects_by_path, semester = _load_subjects(config_entry.payload)
    if semester != "2026.2":
        raise RenameError("unexpected active semester")
    source_paths = sorted(
        (
            path
            for path in entries
            if path.startswith("10 Matérias/")
            and PurePosixPath(path).name in GENERIC_NAMES
        ),
        key=lambda item: item.encode("utf-8"),
    )
    archive_paths = sorted(
        (
            path
            for path in entries
            if path.startswith("90 Arquivo/2026.1/")
            and PurePosixPath(path).name in GENERIC_NAMES
        ),
        key=lambda item: item.encode("utf-8"),
    )
    if len(source_paths) != expected_active:
        raise RenameError(
            f"active generic count mismatch: {len(source_paths)} != {expected_active}"
        )
    if len(archive_paths) != expected_archive:
        raise RenameError(
            f"archive generic count mismatch: {len(archive_paths)} != {expected_archive}"
        )
    operations: list[RenameOperation] = []
    for source in source_paths:
        entry = entries[source]
        match = CLASS_PATH.fullmatch(source)
        if match is None:
            raise RenameError(f"generic note is outside canonical class path: {source!r}")
        subject_path = f"10 Matérias/{match.group(1)}"
        subject = subjects_by_path.get(subject_path)
        if subject is None:
            raise RenameError(f"active subject is not registered: {subject_path!r}")
        subject_id = str(subject["id"])
        kind = GENERIC_NAMES[PurePosixPath(source).name]
        override = CORRECTED_TOPIC if source.startswith(CORRECTED_TOPIC_PREFIX) else None
        normalized = normalize_note(
            entry.payload,
            source=source,
            subject_id=subject_id,
            kind=kind,
            topic_override=override,
        )
        if not _subject_accepts_legacy(subject, normalized.legacy_subject):
            raise RenameError(f"legacy materia does not match subject path: {source!r}")
        destination = (
            PurePosixPath(source).parent / destination_name(kind, normalized.topic)
        ).as_posix()
        _canonical_relative(destination)
        assert_distinct_paths(source, destination)
        operations.append(
            RenameOperation(
                source=source,
                destination=destination,
                subject_id=subject_id,
                class_date=normalized.class_date,
                kind=kind,
                topic=normalized.topic,
                original=entry.payload,
                final=normalized.final_bytes,
                mode=entry.mode,
                original_body=normalized.original_body,
                final_body=normalized.final_body,
                content_class=normalized.content_class,
                transform_id=normalized.transform_id,
                transform_occurrences=normalized.transform_occurrences,
            )
        )
    by_class: dict[str, list[RenameOperation]] = {}
    for operation in operations:
        by_class.setdefault(PurePosixPath(operation.source).parent.as_posix(), []).append(
            operation
        )
    for class_path, pair in by_class.items():
        if len(pair) != 2 or {item.kind for item in pair} != {"resumo", "transcrito"}:
            raise RenameError(f"class does not contain one generic pair: {class_path!r}")
        if len({item.topic for item in pair}) != 1:
            raise RenameError(f"Resumo/Transcrito tema diverges: {class_path!r}")
    source_set = set(source_paths)
    occupied = [path for path in entries if path not in source_set]
    exact: dict[str, str] = {}
    folded: dict[str, str] = {}
    nfd_folded: dict[str, str] = {}

    def register_destination(path: str, owner: str) -> None:
        keys = _collision_keys(path)
        for index, (mapping, key) in enumerate(
            ((exact, keys[0]), (folded, keys[1]), (nfd_folded, keys[2]))
        ):
            previous = mapping.get(key)
            if previous is not None and previous != owner:
                labels = ("exact", "casefold", "NFD-casefold")
                raise RenameError(
                    f"{labels[index]} destination collision: {previous!r} and {owner!r}"
                )
            mapping[key] = owner

    for path in occupied:
        keys = _collision_keys(path)
        exact.setdefault(keys[0], path)
        folded.setdefault(keys[1], path)
        nfd_folded.setdefault(keys[2], path)
    for operation in operations:
        register_destination(operation.destination, operation.source)
    records = [operation.record() for operation in operations]
    aggregate = _aggregate_manifest(expected_head, tree, records)
    manifest: dict[str, object] = dict(
        zip(
            MANIFEST_FIELDS,
            (
                SCHEMA,
                1,
                expected_head,
                tree,
                len(records),
                aggregate,
                records,
            ),
        )
    )
    manifest_bytes = _serialize_manifest(manifest)
    validate_manifest_bytes(manifest_bytes, expected_head)
    if expected_active == 42:
        if tree != DEFAULT_EXPECTED_TREE:
            raise RenameError(f"production authority tree mismatch: {tree}")
        classes = [operation.content_class for operation in operations]
        if classes.count("metadata-only") != 40 or classes.count(
            "authorized-body-transform"
        ) != 2:
            raise RenameError("production content-class counts diverged")
        if sum(operation.transform_occurrences for operation in operations) != 3:
            raise RenameError("production transform occurrence count diverged")
    return RenamePlan(
        expected_head=expected_head,
        authority_tree=tree,
        operations=tuple(operations),
        archive_entries=tuple(entries[path] for path in archive_paths),
        manifest=manifest,
        manifest_bytes=manifest_bytes,
    )


def _open_existing_directory(parent_fd: int, name: str, label: str) -> int:
    descriptor: int | None = None
    try:
        metadata = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
            raise RenameError(f"{label} is not a regular non-symlink directory")
        descriptor = os.open(name, DIRECTORY_FLAGS, dir_fd=parent_fd)
        opened = os.fstat(descriptor)
        if (opened.st_dev, opened.st_ino) != (metadata.st_dev, metadata.st_ino):
            raise RenameError(f"{label} changed while being opened")
        result = descriptor
        descriptor = None
        return result
    except OSError as error:
        raise RenameError(f"cannot securely open {label}: {error}") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _open_parent(root_fd: int, relative: str) -> tuple[int, str]:
    relative = _canonical_relative(relative)
    parts = PurePosixPath(relative).parts
    parent_fd = os.dup(root_fd)
    traversed: list[str] = []
    try:
        for name in parts[:-1]:
            traversed.append(name)
            next_fd = _open_existing_directory(
                parent_fd, name, f"ancestor {'/'.join(traversed)}"
            )
            os.close(parent_fd)
            parent_fd = next_fd
        return parent_fd, parts[-1]
    except BaseException:
        os.close(parent_fd)
        raise


def _read_optional_at(
    parent_fd: int,
    name: str,
    label: str,
    *,
    limit: int = 64 * 1024 * 1024,
) -> tuple[bytes, int] | None:
    descriptor: int | None = None
    try:
        try:
            metadata = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            return None
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
            raise RenameError(f"{label} is not a regular non-symlink file")
        descriptor = os.open(name, FILE_FLAGS, dir_fd=parent_fd)
        opened = os.fstat(descriptor)
        if (
            not stat.S_ISREG(opened.st_mode)
            or (opened.st_dev, opened.st_ino) != (metadata.st_dev, metadata.st_ino)
        ):
            raise RenameError(f"{label} changed while being opened")
        chunks: list[bytes] = []
        size = 0
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            size += len(chunk)
            if size > limit:
                raise RenameError(f"{label} exceeds the secure read limit")
            chunks.append(chunk)
        after = os.fstat(descriptor)
        if (
            (after.st_dev, after.st_ino, after.st_size)
            != (opened.st_dev, opened.st_ino, opened.st_size)
        ):
            raise RenameError(f"{label} changed while being read")
        return b"".join(chunks), stat.S_IMODE(opened.st_mode)
    except OSError as error:
        raise RenameError(f"cannot securely read {label}: {error}") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _read_optional(root_fd: int, relative: str) -> tuple[bytes, int] | None:
    parent_fd, name = _open_parent(root_fd, relative)
    try:
        return _read_optional_at(parent_fd, name, relative)
    finally:
        os.close(parent_fd)


def _expected_mode(git_mode: str) -> int:
    if git_mode == "100644":
        return 0o644
    if git_mode == "100755":
        return 0o755
    raise RenameError(f"unsupported Git mode: {git_mode!r}")


def _require_snapshot(
    snapshot: tuple[bytes, int] | None,
    payload: bytes,
    mode: int,
    label: str,
) -> None:
    if snapshot is None:
        raise RenameError(f"{label} is missing")
    if snapshot != (payload, mode):
        raise RenameError(f"{label} bytes or mode diverged")


def _write_temporary(parent_fd: int, name: str, payload: bytes, mode: int) -> str:
    temporary = ""
    descriptor: int | None = None
    try:
        for _ in range(100):
            candidate = f".lesson-rename-{secrets.token_hex(12)}.tmp"
            try:
                descriptor = os.open(candidate, TEMP_FLAGS, mode, dir_fd=parent_fd)
            except FileExistsError:
                continue
            temporary = candidate
            break
        if descriptor is None:
            raise RenameError(f"cannot allocate a temporary file for {name!r}")
        os.fchmod(descriptor, mode)
        view = memoryview(payload)
        while view:
            written = os.write(descriptor, view)
            if written <= 0:
                raise RenameError(f"short write while publishing {name!r}")
            view = view[written:]
        os.fsync(descriptor)
        os.close(descriptor)
        descriptor = None
        result = temporary
        temporary = ""
        return result
    except OSError as error:
        raise RenameError(f"cannot prepare {name!r}: {error}") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if temporary:
            try:
                os.unlink(temporary, dir_fd=parent_fd)
            except FileNotFoundError:
                pass


def _publish_no_replace(
    parent_fd: int,
    name: str,
    payload: bytes,
    mode: int,
    label: str,
) -> None:
    temporary = _write_temporary(parent_fd, name, payload, mode)
    try:
        try:
            os.link(
                temporary,
                name,
                src_dir_fd=parent_fd,
                dst_dir_fd=parent_fd,
                follow_symlinks=False,
            )
        except FileExistsError as error:
            raise RenameError(f"{label} appeared concurrently; no overwrite") from error
        os.unlink(temporary, dir_fd=parent_fd)
        temporary = ""
        os.fsync(parent_fd)
    except OSError as error:
        raise RenameError(f"cannot publish {label}: {error}") from error
    finally:
        if temporary:
            try:
                os.unlink(temporary, dir_fd=parent_fd)
                os.fsync(parent_fd)
            except FileNotFoundError:
                pass


def _replace_owned_file(
    parent_fd: int,
    name: str,
    payload: bytes,
    mode: int,
    label: str,
) -> None:
    current = _read_optional_at(parent_fd, name, label)
    if current is None:
        raise RenameError(f"{label} disappeared")
    temporary = _write_temporary(parent_fd, name, payload, mode)
    try:
        os.replace(
            temporary,
            name,
            src_dir_fd=parent_fd,
            dst_dir_fd=parent_fd,
        )
        temporary = ""
        os.fsync(parent_fd)
    except OSError as error:
        raise RenameError(f"cannot checkpoint {label}: {error}") from error
    finally:
        if temporary:
            try:
                os.unlink(temporary, dir_fd=parent_fd)
            except FileNotFoundError:
                pass


def _open_vault(vault: Path) -> tuple[Path, int]:
    lexical = Path(os.path.abspath(vault))
    try:
        metadata = os.lstat(lexical)
    except OSError as error:
        raise RenameError(f"cannot inspect vault: {error}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise RenameError("vault must be a regular non-symlink directory")
    descriptor: int | None = None
    try:
        descriptor = os.open(lexical, DIRECTORY_FLAGS)
        opened = os.fstat(descriptor)
        if (opened.st_dev, opened.st_ino) != (metadata.st_dev, metadata.st_ino):
            raise RenameError("vault changed while being opened")
        result = descriptor
        descriptor = None
        return lexical, result
    except OSError as error:
        raise RenameError(f"cannot securely open vault: {error}") from error
    finally:
        if descriptor is not None:
            os.close(descriptor)


def _open_journal_directory(root_fd: int) -> int:
    descriptor = _open_existing_directory(root_fd, ".fgv", ".fgv")
    try:
        fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as error:
        os.close(descriptor)
        raise RenameError(f"another lesson renamer holds the .fgv lock: {error}") from error
    return descriptor


def _journal_operation(operation: RenameOperation) -> dict[str, object]:
    values: tuple[object, ...] = (
        operation.source,
        operation.destination,
        _sha256(operation.original),
        _sha256(operation.final),
        operation.mode,
    )
    return dict(zip(JOURNAL_OPERATION_FIELDS, values))


def _journal_record(plan: RenamePlan, completed_steps: int) -> dict[str, object]:
    if type(completed_steps) is not int or not 0 <= completed_steps <= len(
        plan.operations
    ) + 1:
        raise RenameError("journal completed_steps is invalid")
    values: tuple[object, ...] = (
        1,
        plan.expected_head,
        _sha256(plan.manifest_bytes),
        completed_steps,
        [_journal_operation(operation) for operation in plan.operations],
    )
    return dict(zip(JOURNAL_FIELDS, values))


def _journal_payload(plan: RenamePlan, completed_steps: int) -> bytes:
    return (
        json.dumps(
            _journal_record(plan, completed_steps), ensure_ascii=False, indent=2
        )
        + "\n"
    ).encode("utf-8")


def _read_journal(journal_fd: int, plan: RenamePlan) -> Mapping[str, object] | None:
    snapshot = _read_optional_at(
        journal_fd, JOURNAL_NAME, "lesson rename recovery journal", limit=8 * 1024 * 1024
    )
    if snapshot is None:
        return None
    payload, mode = snapshot
    if mode != 0o600:
        raise RenameError("CRITICAL lesson rename journal mode changed")
    try:
        record = json.loads(payload)
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RenameError("CRITICAL invalid lesson rename journal JSON") from error
    if type(record) is not dict or tuple(record) != JOURNAL_FIELDS:
        raise RenameError("CRITICAL lesson rename journal schema is not closed")
    completed = record.get("completed_steps")
    if type(completed) is not int:
        raise RenameError("CRITICAL lesson rename journal checkpoint is invalid")
    expected = _journal_record(plan, completed)
    if record != expected or payload != _journal_payload(plan, completed):
        raise RenameError("CRITICAL lesson rename journal is not authenticated")
    return record


def _install_journal(journal_fd: int, plan: RenamePlan) -> None:
    if _read_optional_at(journal_fd, JOURNAL_NAME, "lesson rename journal") is not None:
        raise RenameError("CRITICAL lesson rename journal already exists")
    _publish_no_replace(
        journal_fd,
        JOURNAL_NAME,
        _journal_payload(plan, 0),
        0o600,
        "lesson rename journal",
    )


def _checkpoint_journal(
    journal_fd: int, plan: RenamePlan, completed_steps: int
) -> None:
    if _read_journal(journal_fd, plan) is None:
        raise RenameError("CRITICAL lesson rename journal disappeared")
    _replace_owned_file(
        journal_fd,
        JOURNAL_NAME,
        _journal_payload(plan, completed_steps),
        0o600,
        "lesson rename journal",
    )


def _delete_journal(journal_fd: int, plan: RenamePlan) -> None:
    if _read_journal(journal_fd, plan) is None:
        raise RenameError("CRITICAL lesson rename journal disappeared or changed")
    os.unlink(JOURNAL_NAME, dir_fd=journal_fd)
    os.fsync(journal_fd)


def _classify_operation(root_fd: int, operation: RenameOperation) -> str:
    source = _read_optional(root_fd, operation.source)
    destination = _read_optional(root_fd, operation.destination)
    original = (operation.original, _expected_mode(operation.mode))
    final = (operation.final, _expected_mode(operation.mode))
    if source == original and destination is None:
        return "stale"
    if source is None and destination == final:
        return "fresh"
    raise RenameError(
        f"rename scope is partial or tampered: {operation.source!r} -> "
        f"{operation.destination!r}"
    )


def _verify_archive(root_fd: int, plan: RenamePlan) -> None:
    for entry in plan.archive_entries:
        _require_snapshot(
            _read_optional(root_fd, entry.path),
            entry.payload,
            _expected_mode(entry.mode),
            f"archive note {entry.path!r}",
        )


def _classify_vault(root_fd: int, plan: RenamePlan) -> str:
    _verify_archive(root_fd, plan)
    states = [_classify_operation(root_fd, operation) for operation in plan.operations]
    if all(state == "stale" for state in states):
        if _read_optional(root_fd, MANIFEST_RELATIVE) is not None:
            raise RenameError("stale scope already has a lesson rename manifest")
        return "stale"
    if all(state == "fresh" for state in states):
        manifest = _read_optional(root_fd, MANIFEST_RELATIVE)
        _require_snapshot(
            manifest,
            plan.manifest_bytes,
            0o644,
            "lesson rename manifest",
        )
        validate_manifest_bytes(plan.manifest_bytes, plan.expected_head)
        return "fresh"
    raise RenameError("rename scope is partially stale and partially fresh")


def _git_status(vault: Path) -> list[tuple[str, str]]:
    payload = _git_bytes(
        vault, ("status", "--porcelain=v1", "-z", "--untracked-files=all")
    ).stdout
    pieces = payload.split(b"\0")
    result: list[tuple[str, str]] = []
    index = 0
    while index < len(pieces):
        raw = pieces[index]
        index += 1
        if not raw:
            continue
        if len(raw) < 4 or raw[2:3] != b" ":
            raise RenameError("Git status returned an invalid porcelain record")
        try:
            status_code = raw[:2].decode("ascii")
            relative = raw[3:].decode("utf-8")
        except UnicodeDecodeError as error:
            raise RenameError("Git status path is not UTF-8") from error
        _canonical_relative(relative)
        if "R" in status_code or "C" in status_code:
            if index >= len(pieces):
                raise RenameError("Git status rename record is truncated")
            index += 1
            raise RenameError("staged rename/copy state is forbidden")
        result.append((status_code, relative))
    return result


def _require_apply_authority(vault: Path, expected_head: str) -> None:
    current = _git_text(vault, ("rev-parse", "--verify", "HEAD"))
    if current != expected_head:
        raise RenameError(f"HEAD diverged from expected authority: {current}")
    for marker in ("MERGE_HEAD", "CHERRY_PICK_HEAD", "REVERT_HEAD"):
        result = _git_bytes(
            vault, ("rev-parse", "--verify", "-q", marker), check=False
        )
        if result.returncode == 0:
            raise RenameError(f"unfinished Git state is forbidden: {marker}")


def _require_dirty_contract(vault: Path, plan: RenamePlan, phase: str) -> None:
    source_paths = {operation.source for operation in plan.operations}
    destination_paths = {operation.destination for operation in plan.operations}
    for status_code, relative in _git_status(vault):
        if status_code not in {"??", " M", " D"}:
            raise RenameError(f"staged or unsupported dirty state: {status_code} {relative}")
        if relative in TOOLING_DIRTY_ALLOWLIST:
            if status_code not in {"??", " M"}:
                raise RenameError(f"tooling dirty state is not allowed: {relative}")
            continue
        if phase == "stale":
            raise RenameError(f"unrelated dirty path blocks apply: {relative}")
        if relative in source_paths and status_code == " D":
            continue
        if relative in destination_paths and status_code == "??":
            continue
        if relative == MANIFEST_RELATIVE and status_code == "??":
            continue
        if phase == "recovery" and relative == JOURNAL_RELATIVE and status_code == "??":
            continue
        raise RenameError(f"unrelated dirty path blocks apply: {relative}")


def _open_stale_operations(root_fd: int, plan: RenamePlan) -> list[OpenRename]:
    opened: list[OpenRename] = []
    try:
        for operation in plan.operations:
            source_parent = PurePosixPath(operation.source).parent
            destination_parent = PurePosixPath(operation.destination).parent
            if source_parent != destination_parent:
                raise RenameError("lesson rename must remain within one class folder")
            parent_fd, source_name = _open_parent(root_fd, operation.source)
            try:
                destination_name = PurePosixPath(operation.destination).name
                _require_snapshot(
                    _read_optional_at(parent_fd, source_name, operation.source),
                    operation.original,
                    _expected_mode(operation.mode),
                    operation.source,
                )
                if (
                    _read_optional_at(parent_fd, destination_name, operation.destination)
                    is not None
                ):
                    raise RenameError(
                        f"destination already exists: {operation.destination!r}"
                    )
                metadata = os.fstat(parent_fd)
                opened.append(
                    OpenRename(
                        operation,
                        parent_fd,
                        metadata.st_dev,
                        metadata.st_ino,
                        source_name,
                        destination_name,
                    )
                )
                parent_fd = -1
            finally:
                if parent_fd >= 0:
                    os.close(parent_fd)
        return opened
    except BaseException:
        for item in opened:
            item.close()
        raise


def _validate_parent_anchor(root_fd: int, opened: OpenRename) -> None:
    current_fd, _ = _open_parent(root_fd, opened.operation.source)
    try:
        current = os.fstat(current_fd)
        if (current.st_dev, current.st_ino) != (
            opened.parent_device,
            opened.parent_inode,
        ):
            raise RenameError(
                f"parent changed after preflight: {opened.operation.source!r}"
            )
    finally:
        os.close(current_fd)


def _before_operation_publish(operation: RenameOperation) -> None:
    del operation


def _after_destination_publish(operation: RenameOperation) -> None:
    del operation


def _after_source_delete(operation: RenameOperation) -> None:
    del operation


def _after_manifest_publish(plan: RenamePlan) -> None:
    del plan


def _before_journal_delete(plan: RenamePlan) -> None:
    del plan


def _recovery_operation_state(root_fd: int, operation: RenameOperation) -> str:
    source = _read_optional(root_fd, operation.source)
    destination = _read_optional(root_fd, operation.destination)
    original = (operation.original, _expected_mode(operation.mode))
    final = (operation.final, _expected_mode(operation.mode))
    if source == original:
        if destination is None:
            return "pending"
        if destination == final:
            return "published"
        return "blocked"
    if source is None and destination == final:
        return "complete"
    raise RenameError(
        f"CRITICAL recovery path has unknown bytes or mode: {operation.source!r}"
    )


def _unlink_exact(
    parent_fd: int,
    name: str,
    expected: bytes,
    mode: int,
    label: str,
) -> None:
    _require_snapshot(_read_optional_at(parent_fd, name, label), expected, mode, label)
    os.unlink(name, dir_fd=parent_fd)
    os.fsync(parent_fd)


def _rollback_operation(root_fd: int, operation: RenameOperation) -> None:
    state = _recovery_operation_state(root_fd, operation)
    if state in {"pending", "blocked"}:
        return
    parent_fd, source_name = _open_parent(root_fd, operation.source)
    try:
        destination_name = PurePosixPath(operation.destination).name
        mode = _expected_mode(operation.mode)
        if state == "complete":
            _publish_no_replace(
                parent_fd,
                source_name,
                operation.original,
                mode,
                f"rollback source {operation.source}",
            )
        _unlink_exact(
            parent_fd,
            destination_name,
            operation.final,
            mode,
            f"rollback destination {operation.destination}",
        )
    finally:
        os.close(parent_fd)


def _recover_journal(
    root_fd: int,
    journal_fd: int,
    record: Mapping[str, object],
    plan: RenamePlan,
    *,
    allow_blocked: bool = False,
) -> None:
    _verify_archive(root_fd, plan)
    completed_recorded = int(record["completed_steps"])
    states = [_recovery_operation_state(root_fd, operation) for operation in plan.operations]
    completed = 0
    while completed < len(states) and states[completed] == "complete":
        completed += 1
    tail = states[completed:]
    if tail:
        if tail[0] == "blocked" and not allow_blocked:
            raise RenameError("CRITICAL recovery destination has unknown bytes or mode")
        if tail[0] in {"published", "blocked"}:
            tail = tail[1:]
        if any(state != "pending" for state in tail):
            raise RenameError("CRITICAL recovery state is not a completed prefix")
    manifest = _read_optional(root_fd, MANIFEST_RELATIVE)
    manifest_present = manifest == (plan.manifest_bytes, 0o644)
    if manifest is not None and not manifest_present:
        raise RenameError("CRITICAL recovery manifest has unknown bytes or mode")
    if manifest_present and completed != len(plan.operations):
        raise RenameError("CRITICAL manifest exists before all renames are complete")
    observed_steps = completed + (1 if manifest_present else 0)
    if abs(observed_steps - completed_recorded) > 1:
        raise RenameError("CRITICAL journal checkpoint diverges from filesystem state")

    if manifest_present:
        parent_fd, name = _open_parent(root_fd, MANIFEST_RELATIVE)
        try:
            _unlink_exact(
                parent_fd,
                name,
                plan.manifest_bytes,
                0o644,
                "lesson rename manifest",
            )
        finally:
            os.close(parent_fd)
        _checkpoint_journal(journal_fd, plan, len(plan.operations))
    if completed < len(plan.operations) and states[completed] == "published":
        _rollback_operation(root_fd, plan.operations[completed])
        _checkpoint_journal(journal_fd, plan, completed)
    for index in range(completed - 1, -1, -1):
        _rollback_operation(root_fd, plan.operations[index])
        _checkpoint_journal(journal_fd, plan, index)
    _delete_journal(journal_fd, plan)


def _publish_manifest(root_fd: int, plan: RenamePlan) -> None:
    parent_fd, name = _open_parent(root_fd, MANIFEST_RELATIVE)
    try:
        if _read_optional_at(parent_fd, name, MANIFEST_RELATIVE) is not None:
            raise RenameError("lesson rename manifest already exists")
        _publish_no_replace(
            parent_fd,
            name,
            plan.manifest_bytes,
            0o644,
            "lesson rename manifest",
        )
    finally:
        os.close(parent_fd)


def _apply_plan(
    root_fd: int,
    journal_fd: int,
    plan: RenamePlan,
    opened: Sequence[OpenRename],
) -> None:
    _install_journal(journal_fd, plan)
    wrote = False
    try:
        for index, item in enumerate(opened):
            operation = item.operation
            _before_operation_publish(operation)
            _validate_parent_anchor(root_fd, item)
            _require_snapshot(
                _read_optional_at(item.parent_fd, item.source_name, operation.source),
                operation.original,
                _expected_mode(operation.mode),
                operation.source,
            )
            if (
                _read_optional_at(
                    item.parent_fd, item.destination_name, operation.destination
                )
                is not None
            ):
                raise RenameError(
                    f"destination appeared after preflight: {operation.destination!r}"
                )
            _publish_no_replace(
                item.parent_fd,
                item.destination_name,
                operation.final,
                _expected_mode(operation.mode),
                operation.destination,
            )
            wrote = True
            _after_destination_publish(operation)
            _validate_parent_anchor(root_fd, item)
            _require_snapshot(
                _read_optional_at(
                    item.parent_fd, item.destination_name, operation.destination
                ),
                operation.final,
                _expected_mode(operation.mode),
                operation.destination,
            )
            _unlink_exact(
                item.parent_fd,
                item.source_name,
                operation.original,
                _expected_mode(operation.mode),
                operation.source,
            )
            _after_source_delete(operation)
            _validate_parent_anchor(root_fd, item)
            _checkpoint_journal(journal_fd, plan, index + 1)
        _publish_manifest(root_fd, plan)
        wrote = True
        _after_manifest_publish(plan)
        _checkpoint_journal(journal_fd, plan, len(plan.operations) + 1)
        _before_journal_delete(plan)
        if _classify_vault(root_fd, plan) != "fresh":
            raise RenameError("transaction did not reach the authenticated fresh state")
        if _read_journal(journal_fd, plan) is None:
            raise RenameError("CRITICAL lesson rename journal disappeared")
        _delete_journal(journal_fd, plan)
    except Exception as error:
        try:
            current = _read_journal(journal_fd, plan)
            if current is None:
                raise RenameError("CRITICAL journal disappeared during rollback")
            _recover_journal(
                root_fd,
                journal_fd,
                current,
                plan,
                allow_blocked=not wrote,
            )
        except Exception as rollback_error:
            raise RenameError(
                f"CRITICAL transaction failed ({error}); rollback failed: {rollback_error}"
            ) from error
        raise RenameError(f"transaction failed and was rolled back: {error}") from error


def _report(status: str, plan: RenamePlan) -> RenameReport:
    return RenameReport(
        status=status,
        active_generic_notes=len(plan.operations),
        rename_operations=len(plan.operations),
        missing_tema=0,
        collisions=0,
        archive_operations=0,
        plan=plan,
    )


def execute_rename(
    vault: Path,
    expected_head: str,
    *,
    apply: bool,
    expected_active: int,
    expected_archive: int,
) -> RenameReport:
    lexical_vault, root_fd = _open_vault(Path(vault))
    journal_fd: int | None = None
    opened: list[OpenRename] = []
    try:
        if expected_active == 42 and (
            expected_archive != 47 or expected_head != DEFAULT_EXPECTED_HEAD
        ):
            raise RenameError("production lesson rename authority is not exact")
        plan = build_plan(
            lexical_vault,
            expected_head,
            expected_active=expected_active,
            expected_archive=expected_archive,
        )
        journal_fd = _open_journal_directory(root_fd)
        existing_journal = _read_journal(journal_fd, plan)
        if existing_journal is not None:
            if not apply:
                raise RenameError("recovery journal requires an apply invocation")
            _require_apply_authority(lexical_vault, expected_head)
            _require_dirty_contract(lexical_vault, plan, "recovery")
            _recover_journal(root_fd, journal_fd, existing_journal, plan)

        state = _classify_vault(root_fd, plan)
        if not apply:
            return _report("planned" if state == "stale" else "no_op", plan)

        _require_apply_authority(lexical_vault, expected_head)
        _require_dirty_contract(lexical_vault, plan, state)
        if state == "fresh":
            return _report("no_op", plan)

        opened = _open_stale_operations(root_fd, plan)
        _apply_plan(root_fd, journal_fd, plan, opened)
        if _classify_vault(root_fd, plan) != "fresh":
            raise RenameError("post-transaction state is not fresh")
        return _report("applied", plan)
    finally:
        for item in opened:
            item.close()
        if journal_fd is not None:
            os.close(journal_fd)
        os.close(root_fd)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Plan or apply the closed active lesson-note rename transaction."
    )
    parser.add_argument("--vault", required=True, type=Path)
    mode = parser.add_mutually_exclusive_group()
    mode.add_argument("--apply", action="store_true")
    mode.add_argument("--check", action="store_true")
    parser.add_argument("--expected-head")
    return parser


def main(arguments: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(arguments)
    if args.apply and args.expected_head != DEFAULT_EXPECTED_HEAD:
        print(
            f"error: --apply requires --expected-head {DEFAULT_EXPECTED_HEAD}",
            file=sys.stderr,
        )
        return 2
    expected_head = args.expected_head or DEFAULT_EXPECTED_HEAD
    try:
        report = execute_rename(
            args.vault,
            expected_head,
            apply=args.apply,
            expected_active=42,
            expected_archive=47,
        )
    except (OSError, RenameError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1
    print(f"status={report.status}")
    print(f"active_generic_notes={report.active_generic_notes}")
    print(f"rename_operations={report.rename_operations}")
    print(f"missing_tema={report.missing_tema}")
    print(f"collisions={report.collisions}")
    print(f"archive_operations={report.archive_operations}")
    print(f"manifest_sha256={_sha256(report.plan.manifest_bytes)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
