from __future__ import annotations

import json
import re
import unicodedata
from dataclasses import dataclass
from pathlib import Path, PurePosixPath
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


ID_RE = re.compile(r"^[a-z][a-z0-9-]*$")
SEMESTER_RE = re.compile(r"^\d{4}\.[12]$")


class ConfigError(ValueError):
    pass


@dataclass(frozen=True)
class Subject:
    id: str
    name: str
    folder: str
    path: str
    task_tag: str
    aliases: tuple[str, ...]


@dataclass(frozen=True)
class Settings:
    schema_version: int
    semester: str
    timezone: str
    subjects: tuple[Subject, ...]

    @property
    def subject_by_id(self) -> dict[str, Subject]:
        return {subject.id: subject for subject in self.subjects}

    @property
    def subject_by_task_tag(self) -> dict[str, Subject]:
        return {subject.task_tag: subject for subject in self.subjects}


def _nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value.strip())


def _safe_relative_path(value: str) -> str:
    normalized = _nfc(value).replace("\\", "/")
    path = PurePosixPath(normalized)
    if not normalized or path.is_absolute() or ".." in path.parts:
        raise ConfigError(f"unsafe subject path: {value!r}")
    return path.as_posix()


def _required_string(item: dict[str, object], *keys: str) -> str:
    for key in keys:
        value = item.get(key)
        if isinstance(value, str) and value.strip():
            return _nfc(value)
    raise ConfigError(f"missing non-empty field: {'/'.join(keys)}")


def load_settings(path: Path) -> Settings:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"cannot load {path}: {exc}") from exc
    if not isinstance(raw, dict) or raw.get("schema_version") != 1:
        raise ConfigError("subjects schema_version must be 1")
    semester = raw.get("semester")
    timezone = raw.get("timezone")
    if not isinstance(semester, str) or not SEMESTER_RE.fullmatch(semester):
        raise ConfigError(f"invalid semester: {semester!r}")
    if not isinstance(timezone, str):
        raise ConfigError(f"invalid timezone: {timezone!r}")
    try:
        ZoneInfo(timezone)
    except ZoneInfoNotFoundError as exc:
        raise ConfigError(f"invalid timezone: {timezone!r}") from exc
    raw_subjects = raw.get("subjects")
    if not isinstance(raw_subjects, list) or not raw_subjects:
        raise ConfigError("subjects must be a non-empty list")
    subjects: list[Subject] = []
    for item in raw_subjects:
        if not isinstance(item, dict):
            raise ConfigError("each subject must be an object")
        subject_id = _required_string(item, "id")
        if not ID_RE.fullmatch(subject_id):
            raise ConfigError(f"invalid subject id: {subject_id!r}")
        name = _required_string(item, "display_name", "name")
        path_value = _safe_relative_path(_required_string(item, "path"))
        folder = _nfc(str(item.get("folder") or PurePosixPath(path_value).name))
        task_tag = _required_string(item, "task_tag").removeprefix("#")
        if not ID_RE.fullmatch(task_tag):
            raise ConfigError(f"invalid task tag: {task_tag!r}")
        alias_values: list[str] = []
        for field in ("aliases", "legacy_frontmatter_values"):
            values = item.get(field, [])
            if not isinstance(values, list) or any(not isinstance(value, str) for value in values):
                raise ConfigError(f"{field} must be a list of strings")
            alias_values.extend(values)
        alias_values.extend((folder, name, subject_id, task_tag))
        aliases = tuple(sorted({_nfc(value) for value in alias_values if value.strip()}))
        subjects.append(Subject(subject_id, name, folder, path_value, task_tag, aliases))
    for label, values in (
        ("id", [subject.id for subject in subjects]),
        ("name", [subject.name.casefold() for subject in subjects]),
        ("path", [subject.path for subject in subjects]),
        ("task_tag", [subject.task_tag for subject in subjects]),
    ):
        if len(values) != len(set(values)):
            raise ConfigError(f"duplicate subject {label}")
    lookup_owner: dict[str, str] = {}
    for subject in subjects:
        for key in {alias.casefold() for alias in subject.aliases}:
            owner = lookup_owner.setdefault(key, subject.id)
            if owner != subject.id:
                raise ConfigError(f"ambiguous subject lookup key: {key!r}")
    return Settings(1, semester, timezone, tuple(subjects))


def resolve_subject_ids(
    values: list[str] | tuple[str, ...], relative_path: str, settings: Settings
) -> tuple[str, ...]:
    requested = {_nfc(str(value)).casefold().removeprefix("#") for value in values if str(value).strip()}
    path = _nfc(relative_path).replace("\\", "/")
    resolved: set[str] = set()
    for subject in settings.subjects:
        if requested.intersection(alias.casefold().removeprefix("#") for alias in subject.aliases):
            resolved.add(subject.id)
        if path == subject.path or path.startswith(subject.path + "/"):
            resolved.add(subject.id)
    return tuple(sorted(resolved))
