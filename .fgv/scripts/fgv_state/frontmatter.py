from __future__ import annotations

import ast
import csv
import io
import re
import unicodedata
from dataclasses import dataclass
from datetime import date
from pathlib import PurePosixPath


CLASS_DATE_RE = re.compile(r"(?:^|/)Aulas/(\d{2})\.(\d{2})(?:/|$)")
H1_RE = re.compile(r"^#\s+(.+?)\s*$", re.MULTILINE)


@dataclass(frozen=True)
class MarkdownMetadata:
    title: str
    note_type: str
    subjects_raw: tuple[str, ...]
    date: str | None
    date_source: str | None
    topic: str | None
    tags: tuple[str, ...]
    aliases: tuple[str, ...]
    status: str | None
    mastery: int | None
    review_due: str | None
    warnings: tuple[str, ...]


def _nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value.strip())


def _parse_value(raw: str, warnings: list[str], key: str) -> object:
    value = raw.strip()
    if value in {"", "null", "~"}:
        return None
    if value.casefold() in {"true", "false"}:
        return value.casefold() == "true"
    if re.fullmatch(r"-?\d+", value):
        return int(value)
    if value.startswith("["):
        if not value.endswith("]"):
            warnings.append(f"invalid inline list for {key}")
            return value
        inner = value[1:-1].strip()
        if not inner:
            return []
        try:
            fields = next(csv.reader(io.StringIO(inner), skipinitialspace=True))
        except csv.Error:
            warnings.append(f"invalid inline list for {key}")
            return value
        return [_nfc(str(_parse_value(field, warnings, key))) for field in fields]
    if value[:1] in {"'", '"'}:
        try:
            return ast.literal_eval(value)
        except (SyntaxError, ValueError):
            warnings.append(f"invalid quoted scalar for {key}")
    return _nfc(value)


def _parse_frontmatter(text: str) -> tuple[dict[str, object], str, list[str]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text, []
    try:
        closing = next(index for index, line in enumerate(lines[1:], 1) if line.strip() == "---")
    except StopIteration:
        return {}, text, ["frontmatter has no closing delimiter"]
    metadata: dict[str, object] = {}
    warnings: list[str] = []
    list_key: str | None = None
    for line_number, line in enumerate(lines[1:closing], 2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line[:1].isspace():
            if list_key and stripped.startswith("- "):
                existing = metadata.setdefault(list_key, [])
                if isinstance(existing, list):
                    existing.append(_nfc(str(_parse_value(stripped[2:], warnings, list_key))))
                    continue
            warnings.append(f"unsupported nested frontmatter at line {line_number}")
            continue
        list_key = None
        if ":" not in line:
            warnings.append(f"invalid frontmatter line {line_number}")
            continue
        key, value = line.split(":", 1)
        key = _nfc(key)
        if not key:
            warnings.append(f"empty frontmatter key at line {line_number}")
            continue
        if not value.strip():
            metadata[key] = []
            list_key = key
        else:
            metadata[key] = _parse_value(value, warnings, key)
    body = "\n".join(lines[closing + 1:]) + ("\n" if text.endswith("\n") else "")
    return metadata, body, warnings


def _as_strings(value: object) -> list[str]:
    if value is None:
        return []
    values = value if isinstance(value, list) else [value]
    return [_nfc(str(item)) for item in values if str(item).strip()]


def _valid_date(value: object, field: str, warnings: list[str]) -> str | None:
    if value is None or not str(value).strip():
        return None
    candidate = str(value).strip()
    try:
        return date.fromisoformat(candidate).isoformat()
    except ValueError:
        warnings.append(f"invalid {field}: {candidate}")
        return None


def _infer_type(relative_path: str) -> str:
    path = _nfc(relative_path).replace("\\", "/")
    name = PurePosixPath(path).name.casefold()
    if path == "00 Home/Home.md":
        return "home"
    if path == "00 Home/Tasks.md":
        return "tasks"
    if path.startswith("20 Conhecimento/Conceitos/"):
        return "conceito"
    if path.startswith("30 Sistema/Tutor/"):
        return "tutor"
    if name.startswith("resumo") or "_resumo" in name:
        return "resumo"
    if name.startswith("transcrito"):
        return "transcrito"
    if name == "disciplina.md":
        return "disciplina"
    return "other"


def parse_markdown_metadata(text: str, relative_path: str, semester: str) -> MarkdownMetadata:
    raw, body, warnings = _parse_frontmatter(text)
    subjects = tuple(sorted(set(_as_strings(raw.get("materia")) + _as_strings(raw.get("materias")))))
    date_value = raw.get("data") if raw.get("data") is not None else raw.get("date")
    parsed_date = _valid_date(date_value, "data", warnings)
    date_source = "frontmatter" if parsed_date else None
    if parsed_date is None:
        match = CLASS_DATE_RE.search(_nfc(relative_path).replace("\\", "/"))
        if match:
            parsed_date = _valid_date(f"{semester[:4]}-{match.group(1)}-{match.group(2)}", "path date", warnings)
            date_source = "path" if parsed_date else None
    heading = H1_RE.search(body)
    title = _nfc(str(raw.get("title") or (heading.group(1) if heading else PurePosixPath(relative_path).stem)))
    mastery_raw = raw.get("dominio")
    mastery = mastery_raw if isinstance(mastery_raw, int) and not isinstance(mastery_raw, bool) else None
    if mastery is not None and mastery not in range(4):
        warnings.append(f"invalid dominio: {mastery}")
        mastery = None
    elif mastery_raw is not None and mastery is None:
        warnings.append(f"invalid dominio: {mastery_raw}")
    return MarkdownMetadata(
        title=title,
        note_type=_nfc(str(raw.get("tipo"))) if raw.get("tipo") else _infer_type(relative_path),
        subjects_raw=subjects,
        date=parsed_date,
        date_source=date_source,
        topic=_nfc(str(raw.get("tema"))) if raw.get("tema") else None,
        tags=tuple(sorted(set(_as_strings(raw.get("tags"))))),
        aliases=tuple(sorted(set(_as_strings(raw.get("aliases"))))),
        status=_nfc(str(raw.get("status"))) if raw.get("status") else None,
        mastery=mastery,
        review_due=_valid_date(raw.get("proxima_revisao"), "proxima_revisao", warnings),
        warnings=tuple(sorted(set(warnings))),
    )
