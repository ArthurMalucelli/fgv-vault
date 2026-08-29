from __future__ import annotations

import hashlib
import json
import os
import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from pathlib import Path, PurePosixPath

from . import GENERATOR_VERSION, SCHEMA_VERSION
from .config import Settings, resolve_subject_ids
from .frontmatter import parse_markdown_metadata
from .tasks import parse_tasks


ACADEMIC_ROOTS = (
    "00 Home",
    "10 Matérias",
    "20 Conhecimento",
    "30 Sistema/Tutor",
    "90 Arquivo",
)
EXCLUDED_NAMES = {".DS_Store", "._.DS_Store"}
EXCLUDED_SUFFIXES = (".tmp", ".cache", ".mp3.processing")
KIND_BY_SUFFIX = {
    ".md": "note", ".pdf": "document", ".doc": "document", ".docx": "document",
    ".xls": "spreadsheet", ".xlsx": "spreadsheet", ".ppt": "slides", ".pptx": "slides",
    ".ipynb": "notebook", ".csv": "dataset", ".json": "dataset", ".py": "code",
    ".r": "code", ".jpg": "image", ".jpeg": "image", ".png": "image", ".heic": "image",
    ".mp3": "audio", ".m4a": "audio", ".wav": "audio", ".mp4": "video",
}
ARCHIVE_RE = re.compile(r"^90 Arquivo/(\d{4}\.[12])/([^/]+)(?:/|$)")


@dataclass(frozen=True)
class ArchiveSubject:
    id: str
    name: str
    semester: str
    path: str


@dataclass(frozen=True)
class CatalogBuild:
    as_of: str
    source_fingerprint: str
    build_fingerprint: str
    records: tuple[dict[str, object], ...]
    archive_subjects: tuple[ArchiveSubject, ...]


def canonical_json(record: dict[str, object]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(payload: bytes) -> str:
    return "sha256:" + hashlib.sha256(payload).hexdigest()


def _nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value)


def _slug(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value)
    ascii_value = decomposed.encode("ascii", "ignore").decode("ascii")
    words = re.findall(r"[A-Z]+(?=[A-Z][a-z]|\d|$)|[A-Z]?[a-z]+|\d+", ascii_value)
    return "-".join(word.casefold() for word in words) or "materia"


def _ensure_unique_normalized_paths(paths: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: dict[str, str] = {}
    for original in paths:
        relative = _nfc(original.replace("\\", "/"))
        if relative in seen and seen[relative] != original:
            raise ValueError(f"NFC path collision: {seen[relative]!r} and {original!r}")
        seen[relative] = original
        normalized.append(relative)
    return normalized


def _walk_root(vault: Path, root_relative: str, reverse: bool) -> list[tuple[str, Path]]:
    root = vault / root_relative
    if root.is_symlink():
        raise ValueError(f"symbolic link is not allowed: {root_relative}")
    if not root.exists():
        return []
    found: list[tuple[str, Path]] = []
    for current_raw, directory_names, file_names in os.walk(root, followlinks=False):
        current = Path(current_raw)
        kept: list[str] = []
        for name in directory_names:
            candidate = current / name
            if name.startswith("."):
                continue
            if candidate.is_symlink():
                raise ValueError(f"symbolic link is not allowed: {candidate.relative_to(vault)}")
            kept.append(name)
        directory_names[:] = sorted(kept, reverse=reverse)
        for name in sorted(file_names, reverse=reverse):
            path = current / name
            if name.startswith(".") or name in EXCLUDED_NAMES or name.endswith(EXCLUDED_SUFFIXES):
                continue
            if path.is_symlink():
                raise ValueError(f"symbolic link is not allowed: {path.relative_to(vault)}")
            if path.is_file():
                found.append((path.relative_to(vault).as_posix(), path))
    return found


def iter_source_files(vault: Path, reverse_walk_for_test: bool = False) -> list[tuple[str, Path]]:
    vault = vault.resolve()
    raw: list[tuple[str, Path]] = []
    for root in ACADEMIC_ROOTS:
        raw.extend(_walk_root(vault, root, reverse_walk_for_test))
    normalized = _ensure_unique_normalized_paths([relative for relative, _ in raw])
    result = [(relative, raw[index][1]) for index, relative in enumerate(normalized)]
    result.sort(key=lambda item: item[0])
    return result


def _archive_subjects(discovered: list[tuple[str, Path]]) -> tuple[ArchiveSubject, ...]:
    values: dict[tuple[str, str], ArchiveSubject] = {}
    for relative, _ in discovered:
        match = ARCHIVE_RE.match(relative)
        if not match:
            continue
        semester, folder = match.groups()
        subject_id = f"archive:{semester}:{_slug(folder)}"
        values[(semester, folder)] = ArchiveSubject(
            id=subject_id,
            name=folder,
            semester=semester,
            path=f"90 Arquivo/{semester}/{folder}",
        )
    return tuple(sorted(values.values(), key=lambda item: (item.semester, item.path)))


def _scope_and_semester(relative: str, settings: Settings) -> tuple[str, str | None]:
    match = ARCHIVE_RE.match(relative)
    if match:
        return "archive", match.group(1)
    if relative.startswith("10 Matérias/"):
        return "active", settings.semester
    return "shared", None


def _archive_ids(relative: str, archive_subjects: tuple[ArchiveSubject, ...]) -> tuple[str, ...]:
    return tuple(subject.id for subject in archive_subjects if relative == subject.path or relative.startswith(subject.path + "/"))


def _file_record(
    relative: str,
    path: Path,
    settings: Settings,
    archive_subjects: tuple[ArchiveSubject, ...],
) -> dict[str, object]:
    payload = path.read_bytes()
    kind = KIND_BY_SUFFIX.get(path.suffix.casefold(), "other")
    scope, semester = _scope_and_semester(relative, settings)
    subject_ids = tuple(sorted(set(resolve_subject_ids([], relative, settings) + _archive_ids(relative, archive_subjects))))
    record: dict[str, object] = {
        "aliases": [], "date": None, "date_source": None,
        "extension": path.suffix.casefold().removeprefix("."), "kind": kind,
        "mastery": None, "note_type": "other", "path": relative,
        "record_type": "file", "review_due": None, "schema_version": SCHEMA_VERSION,
        "scope": scope, "semester": semester, "sha256": sha256_bytes(payload), "size_bytes": len(payload),
        "status": None, "subject_ids": list(subject_ids), "subjects_raw": [], "tags": [],
        "title": _nfc(path.stem), "topic": None, "warnings": [],
    }
    if kind != "note":
        return record
    warnings: list[str] = []
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError:
        text = payload.decode("utf-8", errors="replace")
        warnings.append("invalid UTF-8 replaced")
    metadata = parse_markdown_metadata(text, relative, semester or settings.semester)
    active_ids = resolve_subject_ids(metadata.subjects_raw, relative, settings)
    ids = tuple(sorted(set(active_ids + _archive_ids(relative, archive_subjects))))
    record.update({
        "aliases": list(metadata.aliases), "date": metadata.date, "date_source": metadata.date_source,
        "mastery": metadata.mastery, "note_type": metadata.note_type, "review_due": metadata.review_due,
        "status": metadata.status, "subject_ids": list(ids), "subjects_raw": list(metadata.subjects_raw),
        "tags": list(metadata.tags), "title": metadata.title, "topic": metadata.topic,
        "warnings": sorted(set(warnings + list(metadata.warnings))),
    })
    return record


def _valid_optional_date(value: object, label: str, concept: str) -> str | None:
    if value is None:
        return None
    if not isinstance(value, str):
        raise ValueError(f"invalid {label} for {concept!r}")
    try:
        return date.fromisoformat(value).isoformat()
    except ValueError as exc:
        raise ValueError(f"invalid {label} for {concept!r}: {value!r}") from exc


def _learning_records(
    vault: Path,
    file_records: list[dict[str, object]],
    settings: Settings,
    archive_subjects: tuple[ArchiveSubject, ...],
) -> list[dict[str, object]]:
    state_path = vault / "30 Sistema/Tutor/concepts-history.json"
    if not state_path.exists():
        return []
    try:
        raw = json.loads(state_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ValueError(f"invalid tutor state: {exc}") from exc
    if not isinstance(raw, dict):
        raise ValueError("tutor state root must be an object")
    valid_statuses = {"certo", "parcial", "gap", "nao_sabe", "nao_testado"}
    paths = {str(record["path"]) for record in file_records}
    archive_lookup: dict[str, ArchiveSubject] = {}
    for subject in archive_subjects:
        archive_lookup[PurePosixPath(subject.path).name.casefold()] = subject
        archive_lookup[_slug(PurePosixPath(subject.path).name)] = subject
    counters = ("times_probed", "times_certo", "times_parcial", "times_gap", "times_nao_sabe", "times_nao_testado")
    records: list[dict[str, object]] = []
    for concept_raw, value in raw.items():
        concept = _nfc(str(concept_raw))
        if not isinstance(value, dict):
            raise ValueError(f"learning state for {concept!r} must be an object")
        status = value.get("last_status")
        if status not in valid_statuses:
            raise ValueError(f"invalid learning status for {concept!r}: {status!r}")
        counter_values: dict[str, int] = {}
        for name in counters:
            counter = value.get(name, 0)
            if not isinstance(counter, int) or isinstance(counter, bool) or counter < 0:
                raise ValueError(f"invalid {name} for {concept!r}")
            counter_values[name] = counter
        subject_raw = _nfc(str(value.get("subject", "")))
        active_ids = resolve_subject_ids([subject_raw], "", settings)
        archive = archive_lookup.get(subject_raw.casefold()) or archive_lookup.get(_slug(subject_raw))
        subject_ids = active_ids or ((archive.id,) if archive else ())
        scope = "active" if active_ids else ("archive" if archive else "unscoped")
        candidate = f"20 Conhecimento/Conceitos/{concept}.md"
        records.append({
            "concept": concept, "concept_path": candidate if candidate in paths else None,
            "first_probed": _valid_optional_date(value.get("first_probed"), "first_probed", concept),
            "last_probed": _valid_optional_date(value.get("last_probed"), "last_probed", concept),
            "last_status": status, "record_type": "learning_state", "schema_version": SCHEMA_VERSION,
            "scope": scope, "subject": subject_raw or None, "subject_ids": list(subject_ids), **counter_values,
        })
    return sorted(records, key=lambda record: str(record["concept"]))


def _record_key(record: dict[str, object]) -> tuple[object, ...]:
    order = {"file": 0, "task": 1, "learning_state": 2}
    kind = str(record["record_type"])
    if kind == "file":
        return order[kind], str(record["path"])
    if kind == "task":
        return order[kind], str(record["source_path"]), int(record["source_line"])
    return order[kind], str(record["concept"])


def build_catalog(vault: Path, settings: Settings, as_of: str, reverse_walk_for_test: bool = False) -> CatalogBuild:
    date.fromisoformat(as_of)
    vault = vault.resolve()
    discovered = iter_source_files(vault, reverse_walk_for_test)
    archive_subjects = _archive_subjects(discovered)
    file_records = [_file_record(relative, path, settings, archive_subjects) for relative, path in discovered]
    records: list[dict[str, object]] = list(file_records)
    task_path = vault / "00 Home/Tasks.md"
    if task_path.exists():
        records.extend(parse_tasks(task_path.read_text(encoding="utf-8"), "00 Home/Tasks.md", settings))
    records.extend(_learning_records(vault, file_records, settings, archive_subjects))
    records.sort(key=_record_key)
    source = hashlib.sha256()
    for relative, path in discovered:
        source.update(relative.encode("utf-8")); source.update(b"\0")
        source.update(hashlib.sha256(path.read_bytes()).digest()); source.update(b"\0")
    config_path = vault / ".fgv/config/subjects.json"
    source.update(b".fgv/config/subjects.json\0")
    source.update(hashlib.sha256(config_path.read_bytes()).digest()); source.update(b"\0")
    source_fingerprint = "sha256:" + source.hexdigest()
    build_fingerprint = sha256_bytes("\0".join((str(SCHEMA_VERSION), GENERATOR_VERSION, as_of, source_fingerprint)).encode("utf-8"))
    return CatalogBuild(as_of, source_fingerprint, build_fingerprint, tuple(records), archive_subjects)


def serialize_catalog(build: CatalogBuild, settings: Settings) -> bytes:
    counts = {
        "files": sum(record["record_type"] == "file" for record in build.records),
        "tasks": sum(record["record_type"] == "task" for record in build.records),
        "learning_states": sum(record["record_type"] == "learning_state" for record in build.records),
        "warnings": sum(len(record.get("warnings", [])) for record in build.records),
    }
    subjects = [{"id": subject.id, "name": subject.name, "path": subject.path, "scope": "active", "semester": settings.semester, "task_tag": subject.task_tag}
                for subject in sorted(settings.subjects, key=lambda item: item.id)]
    subjects.extend({"id": subject.id, "name": subject.name, "path": subject.path, "scope": "archive", "semester": subject.semester, "task_tag": None}
                    for subject in build.archive_subjects)
    manifest = {
        "as_of": build.as_of, "build_fingerprint": build.build_fingerprint, "counts": counts,
        "generator_version": GENERATOR_VERSION, "record_type": "manifest", "schema_version": SCHEMA_VERSION,
        "source_fingerprint": build.source_fingerprint,
        "subjects": sorted(subjects, key=lambda item: (str(item["scope"]), str(item["id"]))),
    }
    lines = [canonical_json(manifest), *(canonical_json(record) for record in build.records)]
    return ("\n".join(lines) + "\n").encode("utf-8")
