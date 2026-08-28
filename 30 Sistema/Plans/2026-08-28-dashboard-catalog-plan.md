# FGV Dashboard and Catalog Implementation Plan

> **For agentic workers:** REQUIRED SUB-SKILL: Use superpowers:subagent-driven-development (recommended) or superpowers:executing-plans to implement this plan task-by-task. Steps use checkbox (`- [ ]`) syntax for tracking.

**Goal:** Build a deterministic, filesystem-first read model that turns the migrated FGV vault into `30 Sistema/Estado/catalog.jsonl` and `30 Sistema/Estado/dashboard-snapshot.md`, while preserving `00 Home/Home.md` as the human-owned Obsidian entrypoint.

**Architecture:** Canonical state remains in Markdown, JSON and academic files under `00 Home/`, `10 Matérias/`, `20 Conhecimento/` and `30 Sistema/Tutor/`. A Python standard-library generator scans those files, normalizes legacy and canonical metadata, emits a versioned JSONL catalog, then renders a static Markdown snapshot from that catalog. Generated files have one writer, are validated fully before per-file atomic replacement, and are never treated as sources of truth.

**Tech Stack:** Python 3.11+ standard library only, `unittest`, `pathlib`, `dataclasses`, `json`, `hashlib`, `tempfile`, `os.replace`, `datetime`, `zoneinfo`, Markdown/YAML-subset parsing, Obsidian wikilinks, Git.

---

## Preconditions and scope boundaries

- Execute this plan only after the structural migration has created `00 Home/`, `10 Matérias/`, `20 Conhecimento/`, `30 Sistema/Estado/` and `30 Sistema/Tutor/`.
- `00 Home/Tasks.md` must already be the canonical task file.
- The seven active subject folders must already exist below `10 Matérias/`.
- `30 Sistema/Tutor/concepts-history.json` may be absent or empty on a fresh vault, but malformed JSON is a fatal generation error.
- This plan does not move legacy folders, rewrite Git history, extract PDFs, modify Hermes on the VPS, or implement the `/fgv` ingestion flow.
- This plan does not add a community plugin. The snapshot must remain readable without Dataview, Tasks or Bases.
- The generator may read `.fgv/config/subjects.json`, but it must never scan `.fgv/` as academic content.

## Locked file map

### Files created by this plan

- `.fgv/VERSION`: shared contract major version, exactly `1`.
- `.fgv/config/subjects.json`: canonical subject IDs, display names, paths, task tags and legacy aliases.
- `.fgv/scripts/fgv_state/__init__.py`: generator version constant.
- `.fgv/scripts/fgv_state/config.py`: validated subject configuration and subject resolution.
- `.fgv/scripts/fgv_state/frontmatter.py`: constrained YAML-frontmatter parser and Markdown metadata normalization.
- `.fgv/scripts/fgv_state/tasks.py`: Tasks-plugin line parser with optimistic-write locators.
- `.fgv/scripts/fgv_state/catalog.py`: filesystem scan, file and learning-state records, fingerprints and JSONL serialization.
- `.fgv/scripts/fgv_state/dashboard.py`: static snapshot projection from catalog records.
- `.fgv/scripts/fgv_state/io.py`: validation and atomic write-if-changed behavior.
- `.fgv/scripts/generate_state.py`: CLI orchestration and `--check` mode.
- `.fgv/tests/test_config.py`: configuration validation and legacy subject resolution.
- `.fgv/tests/test_frontmatter.py`: frontmatter compatibility and path-derived metadata tests.
- `.fgv/tests/test_tasks.py`: task syntax, metadata and line revision tests.
- `.fgv/tests/test_catalog.py`: scan exclusions, record schema, fingerprints and learning-state tests.
- `.fgv/tests/test_dashboard.py`: deadline boundaries, class completeness, review and mastery rendering tests.
- `.fgv/tests/test_generate_state.py`: deterministic end-to-end, idempotency and fail-closed tests.
- `.fgv/tests/fixtures/mini-vault/`: input fixture tree whose exact files are listed in Task 4.
- `00 Home/Home.md`: human-owned shell that embeds the generated snapshot.
- `30 Sistema/Estado/README.md`: ownership and regeneration instructions.
- `30 Sistema/Estado/catalog.jsonl`: generated catalog v1.
- `30 Sistema/Estado/dashboard-snapshot.md`: generated Markdown snapshot.

### Canonical inputs read but never rewritten by the generator

- `00 Home/Home.md`
- `00 Home/Tasks.md`
- `10 Matérias/**`
- `20 Conhecimento/Conceitos/**`
- `30 Sistema/Tutor/concepts-history.json`

### Explicitly excluded inputs

- `.git/**`
- `.obsidian/**`
- `.fgv/**`, except `.fgv/config/subjects.json`, which enters the source fingerprint explicitly
- `.trash/**`
- `.gstack/**`
- `30 Sistema/Estado/catalog.jsonl`
- `30 Sistema/Estado/dashboard-snapshot.md`
- `30 Sistema/Estado/sync-status.json`
- `.DS_Store`, `._.DS_Store`, `*.tmp`, `*.cache`, `*.mp3.processing`
- root and nested hidden files whose names begin with `.`, except the subjects config fingerprinted explicitly
- every symbolic link

## Catalog v1 contract

`catalog.jsonl` is UTF-8 with LF endings, compact JSON, lexicographically sorted object keys and one trailing newline. The first line is the only `manifest` record. Remaining records are ordered by record type, then by Unicode-NFC relative path, source line or concept name using Python code-point order, never locale collation.

Record types are:

- `manifest`: schema, build identity, subjects, counts and warning count.
- `file`: one line per regular academic artifact, without body text or excerpt.
- `task`: one line per Tasks-plugin checkbox in `00 Home/Tasks.md`.
- `learning_state`: one line per entry in `30 Sistema/Tutor/concepts-history.json`.

Every record includes integer `schema_version: 1`. Consumers ignore unknown fields within v1 and reject a higher major version.

No record contains absolute paths, filesystem modification times, hostnames, Git commit IDs or wall-clock generation timestamps.

## Determinism and fingerprints

- The CLI requires `--as-of YYYY-MM-DD`. The scheduler derives that value in `America/Sao_Paulo`; tests always pass it explicitly.
- Every indexed path is vault-relative, POSIX-style and normalized with Unicode NFC.
- A collision after NFC normalization is fatal.
- `source_fingerprint` is SHA-256 over ordered repetitions of `relative_path UTF8`, NUL, raw file SHA-256 bytes, NUL. The canonical subjects config is appended to that stream even though `.fgv/` is otherwise excluded.
- `build_fingerprint` is SHA-256 over `schema_version`, generator version, `as_of` and `source_fingerprint`, separated by NUL.
- `catalog_sha256` is SHA-256 over the final serialized catalog bytes.
- The snapshot includes `catalog_sha256`; a consumer seeing a mismatch must retry or fall back to direct filesystem reads.
- The generator builds and validates both outputs in memory before replacing either existing output.
- Each changed output is written to a temporary file in its destination directory, flushed, `fsync`ed and installed with `os.replace`.
- Identical bytes do not rewrite the destination, preserving mtime and preventing empty Git commits.
- Expected validation and parsing failures leave both previous outputs byte-identical.

## Task 1: Establish the versioned subject contract

**Files:**

- Create: `.fgv/VERSION`
- Create: `.fgv/config/subjects.json`
- Create: `.fgv/scripts/fgv_state/__init__.py`
- Create: `.fgv/scripts/fgv_state/config.py`
- Create: `.fgv/tests/test_config.py`

- [ ] **Step 1: Write failing configuration tests**

Create `.fgv/tests/test_config.py` with these cases:

```python
import json
import tempfile
import unittest
from pathlib import Path

from fgv_state.config import ConfigError, load_settings, resolve_subject_ids


class ConfigTests(unittest.TestCase):
    def write_config(self, root: Path, payload: dict) -> Path:
        path = root / "subjects.json"
        path.write_text(json.dumps(payload, ensure_ascii=False), encoding="utf-8")
        return path

    def valid_payload(self) -> dict:
        return {
            "schema_version": 1,
            "semester": "2026.2",
            "timezone": "America/Sao_Paulo",
            "subjects": [
                {
                    "id": "contabilidade-financeira",
                    "name": "Contabilidade Financeira",
                    "path": "10 Matérias/ContabilidadeFinanceira",
                    "task_tag": "cont",
                    "aliases": ["ContabilidadeFinanceira", "cont"],
                },
                {
                    "id": "tecnologia-dados-negocios",
                    "name": "Tecnologia, Dados e Negócios",
                    "path": "10 Matérias/TecnologiaDadosNegocios",
                    "task_tag": "tdn",
                    "aliases": ["TecnologiaDadosNegocios", "TecnologiaDadosENegocios"],
                },
            ],
        }

    def test_loads_valid_config_and_resolves_legacy_metadata(self):
        with tempfile.TemporaryDirectory() as tmp:
            settings = load_settings(self.write_config(Path(tmp), self.valid_payload()))
        self.assertEqual(settings.semester, "2026.2")
        self.assertEqual(
            resolve_subject_ids(["ContabilidadeFinanceira"], "", settings),
            ("contabilidade-financeira",),
        )
        self.assertEqual(
            resolve_subject_ids([], "10 Matérias/TecnologiaDadosNegocios/Aulas/08.28/Resumo.md", settings),
            ("tecnologia-dados-negocios",),
        )

    def test_rejects_duplicate_ids_tags_paths_and_unsafe_paths(self):
        mutations = (
            lambda p: p["subjects"].append(dict(p["subjects"][0])),
            lambda p: p["subjects"][1].update(task_tag="cont"),
            lambda p: p["subjects"][1].update(path=p["subjects"][0]["path"]),
            lambda p: p["subjects"][1].update(name=p["subjects"][0]["name"]),
            lambda p: p["subjects"][1].update(path="../outside"),
        )
        for mutate in mutations:
            with self.subTest(mutate=mutate), tempfile.TemporaryDirectory() as tmp:
                payload = self.valid_payload()
                mutate(payload)
                with self.assertRaises(ConfigError):
                    load_settings(self.write_config(Path(tmp), payload))

    def test_rejects_wrong_schema_semester_and_timezone(self):
        invalid = (
            {"schema_version": 2},
            {"semester": "2026-Q2"},
            {"timezone": "Brazil/East-Invalid"},
        )
        for patch in invalid:
            with self.subTest(patch=patch), tempfile.TemporaryDirectory() as tmp:
                payload = self.valid_payload()
                payload.update(patch)
                with self.assertRaises(ConfigError):
                    load_settings(self.write_config(Path(tmp), payload))


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the tests and verify the import failure**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/tests/test_config.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'fgv_state'`.

- [ ] **Step 3: Create the version and canonical subject configuration**

Create `.fgv/VERSION`:

```text
1
```

Create `.fgv/config/subjects.json`:

```json
{
  "schema_version": 1,
  "semester": "2026.2",
  "timezone": "America/Sao_Paulo",
  "subjects": [
    {
      "id": "contabilidade-financeira",
      "name": "Contabilidade Financeira",
      "path": "10 Matérias/ContabilidadeFinanceira",
      "task_tag": "cont",
      "aliases": ["ContabilidadeFinanceira", "cont"]
    },
    {
      "id": "direito-empresarial",
      "name": "Direito Empresarial",
      "path": "10 Matérias/DireitoEmpresarial",
      "task_tag": "dir",
      "aliases": ["DireitoEmpresarial", "dir"]
    },
    {
      "id": "estatistica-2",
      "name": "Estatística II",
      "path": "10 Matérias/Estatistica2",
      "task_tag": "est2",
      "aliases": ["Estatistica2", "Estatística II", "est2"]
    },
    {
      "id": "estudos-organizacionais",
      "name": "Estudos Organizacionais",
      "path": "10 Matérias/EstudosOrganizacionais",
      "task_tag": "eo",
      "aliases": ["EstudosOrganizacionais", "eo"]
    },
    {
      "id": "matematica-aplicada",
      "name": "Matemática Aplicada I",
      "path": "10 Matérias/MatemáticaAplicada",
      "task_tag": "ma1",
      "aliases": ["MatemáticaAplicada", "MatematicaAplicada", "MatematicaAplicada1", "ma1"]
    },
    {
      "id": "psicologia",
      "name": "Psicologia",
      "path": "10 Matérias/Psicologia",
      "task_tag": "psi",
      "aliases": ["Psicologia", "psi"]
    },
    {
      "id": "tecnologia-dados-negocios",
      "name": "Tecnologia, Dados e Negócios",
      "path": "10 Matérias/TecnologiaDadosNegocios",
      "task_tag": "tdn",
      "aliases": ["TecnologiaDadosNegocios", "TecnologiaDadosENegocios", "tdn"]
    }
  ]
}
```

- [ ] **Step 4: Implement validated settings and subject resolution**

Create `.fgv/scripts/fgv_state/__init__.py`:

```python
GENERATOR_VERSION = "1.0.0"
SCHEMA_VERSION = 1
```

Create `.fgv/scripts/fgv_state/config.py` with immutable `Subject` and `Settings` dataclasses. Implement these exact public interfaces:

```python
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
    if path.is_absolute() or ".." in path.parts or not path.parts:
        raise ConfigError(f"unsafe subject path: {value!r}")
    return path.as_posix()


def load_settings(path: Path) -> Settings:
    try:
        raw = json.loads(path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise ConfigError(f"cannot load {path}: {exc}") from exc
    if raw.get("schema_version") != 1:
        raise ConfigError("subjects schema_version must be 1")
    semester = str(raw.get("semester", ""))
    if not SEMESTER_RE.fullmatch(semester):
        raise ConfigError(f"invalid semester: {semester!r}")
    timezone = str(raw.get("timezone", ""))
    try:
        ZoneInfo(timezone)
    except ZoneInfoNotFoundError as exc:
        raise ConfigError(f"invalid timezone: {timezone!r}") from exc
    subjects: list[Subject] = []
    for item in raw.get("subjects", []):
        subject_id = _nfc(str(item.get("id", "")))
        task_tag = _nfc(str(item.get("task_tag", ""))).removeprefix("#")
        if not ID_RE.fullmatch(subject_id):
            raise ConfigError(f"invalid subject id: {subject_id!r}")
        if not ID_RE.fullmatch(task_tag):
            raise ConfigError(f"invalid task tag: {task_tag!r}")
        aliases = tuple(sorted({_nfc(str(value)) for value in item.get("aliases", []) if str(value).strip()}))
        name = _nfc(str(item.get("name", "")))
        if not name:
            raise ConfigError("subject name must not be empty")
        subjects.append(
            Subject(
                id=subject_id,
                name=name,
                path=_safe_relative_path(str(item.get("path", ""))),
                task_tag=task_tag,
                aliases=aliases,
            )
        )
    if not subjects:
        raise ConfigError("subjects must not be empty")
    for label, values in (
        ("id", [s.id for s in subjects]),
        ("name", [s.name.casefold() for s in subjects]),
        ("path", [s.path for s in subjects]),
        ("task_tag", [s.task_tag for s in subjects]),
    ):
        if len(values) != len(set(values)):
            raise ConfigError(f"duplicate subject {label}")
    lookup_owner: dict[str, str] = {}
    for subject in subjects:
        keys = {subject.id, subject.name, subject.task_tag, *subject.aliases}
        for key in {value.casefold() for value in keys}:
            owner = lookup_owner.setdefault(key, subject.id)
            if owner != subject.id:
                raise ConfigError(f"ambiguous subject lookup key: {key!r}")
    return Settings(1, semester, timezone, tuple(subjects))


def resolve_subject_ids(values: list[str] | tuple[str, ...], relative_path: str, settings: Settings) -> tuple[str, ...]:
    requested = {_nfc(str(value)).casefold() for value in values if str(value).strip()}
    resolved: set[str] = set()
    for subject in settings.subjects:
        keys = {subject.id.casefold(), subject.name.casefold(), subject.task_tag.casefold()}
        keys.update(alias.casefold() for alias in subject.aliases)
        if requested & keys:
            resolved.add(subject.id)
        path = _nfc(relative_path).replace("\\", "/")
        if path == subject.path or path.startswith(subject.path + "/"):
            resolved.add(subject.id)
    return tuple(sorted(resolved))
```

- [ ] **Step 5: Run the tests and verify they pass**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/tests/test_config.py -v
```

Expected: three tests report `ok`; final line is `OK`.

- [ ] **Step 6: Commit the configuration contract**

```bash
git add .fgv/VERSION .fgv/config/subjects.json .fgv/scripts/fgv_state/__init__.py .fgv/scripts/fgv_state/config.py .fgv/tests/test_config.py
git commit -m "feat: define dashboard subject contract"
```

## Task 2: Normalize Markdown frontmatter without third-party YAML

**Files:**

- Create: `.fgv/scripts/fgv_state/frontmatter.py`
- Create: `.fgv/tests/test_frontmatter.py`

- [ ] **Step 1: Write failing tests for `materia`, `materias`, dates and legacy paths**

Create `.fgv/tests/test_frontmatter.py`:

```python
import unittest

from fgv_state.frontmatter import parse_markdown_metadata


class FrontmatterTests(unittest.TestCase):
    def test_normalizes_singular_and_plural_subject_fields(self):
        text = """---
materia: ContabilidadeFinanceira
materias: [ProdutosFinanceiros, ContabilidadeFinanceira]
data: 2026-08-27
tema: DRE, provisões e arrendamentos
tags: [resumo, prova]
status: completo
dominio: 1
proxima_revisao: 2026-08-29
---
# Revisão final PP1
"""
        metadata = parse_markdown_metadata(
            text,
            "10 Matérias/ContabilidadeFinanceira/Aulas/08.27/Resumo - DRE.md",
            "2026.2",
        )
        self.assertEqual(metadata.subjects_raw, ("ContabilidadeFinanceira", "ProdutosFinanceiros"))
        self.assertEqual(metadata.date, "2026-08-27")
        self.assertEqual(metadata.date_source, "frontmatter")
        self.assertEqual(metadata.note_type, "resumo")
        self.assertEqual(metadata.title, "Revisão final PP1")
        self.assertEqual(metadata.tags, ("prova", "resumo"))
        self.assertEqual(metadata.mastery, 1)
        self.assertEqual(metadata.review_due, "2026-08-29")

    def test_derives_date_and_type_from_active_class_path(self):
        metadata = parse_markdown_metadata(
            "# Behaviorismo radical\n",
            "10 Matérias/Psicologia/Aulas/08.25/Transcrito - Skinner.md",
            "2026.2",
        )
        self.assertEqual(metadata.date, "2026-08-25")
        self.assertEqual(metadata.date_source, "path")
        self.assertEqual(metadata.note_type, "transcrito")

    def test_invalid_frontmatter_is_partial_not_fatal(self):
        metadata = parse_markdown_metadata(
            "---\ntags: [resumo\ndata: ontem\n---\n# Nota\n",
            "10 Matérias/Psicologia/Nota.md",
            "2026.2",
        )
        self.assertEqual(metadata.title, "Nota")
        self.assertIsNone(metadata.date)
        self.assertTrue(metadata.warnings)

    def test_supports_block_lists_and_unicode(self):
        text = """---
tipo: conceito
materias:
  - MatemáticaAplicada
tags:
  - cálculo
  - revisão
---
# Assíntota
"""
        metadata = parse_markdown_metadata(text, "20 Conhecimento/Conceitos/Assíntota.md", "2026.2")
        self.assertEqual(metadata.subjects_raw, ("MatemáticaAplicada",))
        self.assertEqual(metadata.tags, ("cálculo", "revisão"))
        self.assertEqual(metadata.note_type, "conceito")


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused test and verify it fails**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/tests/test_frontmatter.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'fgv_state.frontmatter'`.

- [ ] **Step 3: Implement the constrained parser and normalized metadata model**

Create `.fgv/scripts/fgv_state/frontmatter.py`. The module must expose exactly this immutable result type and function:

```python
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


def parse_markdown_metadata(text: str, relative_path: str, semester: str) -> MarkdownMetadata:
    raw, body, warnings = _parse_frontmatter(text)
    subjects = sorted(set(_as_strings(raw.get("materia")) + _as_strings(raw.get("materias"))))
    date_value = raw.get("data") if raw.get("data") is not None else raw.get("date")
    parsed_date = _valid_date(date_value, "data", warnings)
    date_source = "frontmatter" if parsed_date else None
    if parsed_date is None:
        match = CLASS_DATE_RE.search(_nfc(relative_path).replace("\\", "/"))
        if match:
            candidate = f"{semester[:4]}-{match.group(1)}-{match.group(2)}"
            parsed_date = _valid_date(candidate, "path date", warnings)
            if parsed_date:
                date_source = "path"
    title_value = raw.get("title")
    heading = H1_RE.search(body)
    title = _nfc(str(title_value)) if title_value else _nfc(heading.group(1) if heading else PurePosixPath(relative_path).stem)
    note_type = _nfc(str(raw.get("tipo"))) if raw.get("tipo") else _infer_type(relative_path)
    mastery_value = raw.get("dominio")
    mastery = mastery_value if isinstance(mastery_value, int) and not isinstance(mastery_value, bool) else None
    if mastery is not None and mastery not in range(4):
        warnings.append(f"invalid dominio: {mastery}")
        mastery = None
    elif mastery_value is not None and mastery is None:
        warnings.append(f"invalid dominio: {mastery_value}")
    return MarkdownMetadata(
        title=title,
        note_type=note_type,
        subjects_raw=tuple(subjects),
        date=parsed_date,
        date_source=date_source,
        topic=_nfc(str(raw["tema"])) if raw.get("tema") else None,
        tags=tuple(sorted(set(_as_strings(raw.get("tags"))))),
        aliases=tuple(sorted(set(_as_strings(raw.get("aliases"))))),
        status=_nfc(str(raw["status"])) if raw.get("status") else None,
        mastery=mastery,
        review_due=_valid_date(raw.get("proxima_revisao"), "proxima_revisao", warnings),
        warnings=tuple(sorted(set(warnings))),
    )


def _nfc(value: str) -> str:
    return unicodedata.normalize("NFC", value.strip())


def _parse_frontmatter(text: str) -> tuple[dict[str, object], str, list[str]]:
    lines = text.splitlines()
    if not lines or lines[0].strip() != "---":
        return {}, text, []
    try:
        closing = next(index for index, line in enumerate(lines[1:], start=1) if line.strip() == "---")
    except StopIteration:
        return {}, text, ["frontmatter has no closing delimiter"]
    metadata: dict[str, object] = {}
    warnings: list[str] = []
    current_list_key: str | None = None
    for line_number, line in enumerate(lines[1:closing], start=2):
        stripped = line.strip()
        if not stripped or stripped.startswith("#"):
            continue
        if line[:1].isspace():
            if current_list_key and stripped.startswith("- "):
                current = metadata.get(current_list_key)
                if current is None:
                    current = []
                    metadata[current_list_key] = current
                if isinstance(current, list):
                    current.append(_nfc(str(_parse_value(stripped[2:], warnings, current_list_key))))
                    continue
            warnings.append(f"unsupported nested frontmatter at line {line_number}")
            continue
        current_list_key = None
        if ":" not in line:
            warnings.append(f"invalid frontmatter line {line_number}")
            continue
        key, raw_value = line.split(":", 1)
        key = _nfc(key)
        if not key:
            warnings.append(f"empty frontmatter key at line {line_number}")
            continue
        raw_value = raw_value.strip()
        if raw_value == "":
            metadata[key] = None
            current_list_key = key
        else:
            metadata[key] = _parse_value(raw_value, warnings, key)
    body = "\n".join(lines[closing + 1 :])
    if text.endswith("\n"):
        body += "\n"
    return metadata, body, warnings


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
        fields = next(csv.reader(io.StringIO(inner), skipinitialspace=True))
        return [_nfc(str(_parse_value(field, warnings, key))) for field in fields]
    if value[:1] in {"'", '"'}:
        try:
            parsed = ast.literal_eval(value)
        except (SyntaxError, ValueError):
            warnings.append(f"invalid quoted scalar for {key}")
            return value
        return parsed
    return _nfc(value)


def _as_strings(value: object) -> list[str]:
    if value is None:
        return []
    values = value if isinstance(value, list) else [value]
    return [_nfc(str(item)) for item in values if str(item).strip()]


def _valid_date(value: object, field: str, warnings: list[str]) -> str | None:
    if value is None or str(value).strip() == "":
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
    if name.startswith("resumo"):
        return "resumo"
    if name.startswith("transcrito"):
        return "transcrito"
    if name == "disciplina.md":
        return "disciplina"
    return "other"
```

Implement the body with these concrete rules:

- Parse only a top-level YAML subset: `key: scalar`, inline lists and indented block lists.
- Use `ast.literal_eval` only for quoted scalars. Use `csv.reader` for the contents of inline lists so spaces and quoted commas are stable.
- Treat `null`, `~` and an empty scalar as `None`; parse booleans and integers; keep ISO dates as strings.
- Collect parser problems into sorted warning strings instead of raising for a single Markdown file.
- Combine `materia` and `materias`, deduplicate with NFC normalization, then sort.
- Read `tipo`; otherwise infer `resumo`, `transcrito`, `conceito`, `disciplina`, `home`, `tasks`, `tutor` or `other` from the normalized path and filename prefix.
- Validate `data`, `date` and `proxima_revisao` with `date.fromisoformat`.
- If no valid frontmatter date exists and the active path contains `Aulas/MM.DD`, use the four-digit year from `semester`.
- Read `dominio` only when it is an integer from zero through three. Invalid values become `None` plus a warning.
- Prefer frontmatter `title`; then first H1; then file stem.
- Never extract inline hashtags in v1.

Do not implement general YAML anchors, objects, folded blocks or tags. Encountering them yields a warning and leaves unrelated recognized fields usable.

- [ ] **Step 4: Run the focused tests and verify they pass**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/tests/test_frontmatter.py -v
```

Expected: four tests report `ok`; final line is `OK`.

- [ ] **Step 5: Commit the metadata parser**

```bash
git add .fgv/scripts/fgv_state/frontmatter.py .fgv/tests/test_frontmatter.py
git commit -m "feat: normalize vault frontmatter"
```

## Task 3: Parse canonical Tasks-plugin lines safely

**Files:**

- Create: `.fgv/scripts/fgv_state/tasks.py`
- Create: `.fgv/tests/test_tasks.py`

- [ ] **Step 1: Write failing task parser tests**

Create `.fgv/tests/test_tasks.py`:

```python
import json
import unittest
from pathlib import Path

from fgv_state.config import load_settings
from fgv_state.tasks import parse_tasks


class TaskParserTests(unittest.TestCase):
    def settings(self, root: Path):
        config = {
            "schema_version": 1,
            "semester": "2026.2",
            "timezone": "America/Sao_Paulo",
            "subjects": [
                {
                    "id": "contabilidade-financeira",
                    "name": "Contabilidade Financeira",
                    "path": "10 Matérias/ContabilidadeFinanceira",
                    "task_tag": "cont",
                    "aliases": ["ContabilidadeFinanceira"],
                }
            ],
        }
        path = root / "subjects.json"
        path.write_text(json.dumps(config, ensure_ascii=False), encoding="utf-8")
        return load_settings(path)

    def test_parses_status_due_priority_tags_and_revision(self):
        text = """# Tasks
- [ ] Prova parcial 1 #cont 📅 2026-08-28 🔺
- [/] Refazer exercício #cont ⏫
- [x] Imprimir caso #cont 📅 2026-08-21 ✅ 2026-08-24
- [-] Evento cancelado #cont
- [ ] Instalar prateleira #casa
"""
        with tempfile.TemporaryDirectory() as tmp:
            records = parse_tasks(text, "00 Home/Tasks.md", self.settings(Path(tmp)))
        self.assertEqual([r["status"] for r in records], ["todo", "in_progress", "done", "cancelled", "todo"])
        self.assertEqual(records[0]["due"], "2026-08-28")
        self.assertEqual(records[0]["priority"], "highest")
        self.assertEqual(records[0]["subject_ids"], ["contabilidade-financeira"])
        self.assertEqual(records[4]["subject_ids"], [])
        raw = "- [ ] Prova parcial 1 #cont 📅 2026-08-28 🔺"
        self.assertEqual(records[0]["source_line"], 2)
        self.assertEqual(records[0]["source_line_sha256"], "sha256:" + hashlib.sha256(raw.encode()).hexdigest())

    def test_invalid_due_date_is_retained_as_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            records = parse_tasks(
                "- [ ] Entrega #cont 📅 2026-02-30\n",
                "00 Home/Tasks.md",
                self.settings(Path(tmp)),
            )
        self.assertIsNone(records[0]["due"])
        self.assertEqual(records[0]["warnings"], ["invalid due date: 2026-02-30"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the focused tests and verify they fail**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/tests/test_tasks.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'fgv_state.tasks'`.

- [ ] **Step 3: Implement task records with optimistic-write locators**

Create `.fgv/scripts/fgv_state/tasks.py` with these constants and public function:

```python
from __future__ import annotations

import hashlib
import re
from datetime import date

from .config import Settings


TASK_RE = re.compile(r"^\s*-\s+\[(?P<marker>[ xX/\-])\]\s+(?P<body>.+?)\s*$")
DUE_RE = re.compile(r"📅\s*(\d{4}-\d{2}-\d{2})")
DONE_RE = re.compile(r"✅\s*\d{4}-\d{2}-\d{2}")
TAG_RE = re.compile(r"(?<!\S)#([\w/-]+)", re.UNICODE)
STATUS = {" ": "todo", "/": "in_progress", "x": "done", "X": "done", "-": "cancelled"}
PRIORITIES = (("🔺", "highest"), ("⏫", "high"), ("🔼", "medium"), ("🔽", "low"), ("⏬", "lowest"))


def parse_tasks(text: str, source_path: str, settings: Settings) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    tag_to_subject = {subject.task_tag: subject.id for subject in settings.subjects}
    for line_number, raw_line in enumerate(text.splitlines(), start=1):
        match = TASK_RE.match(raw_line)
        if not match:
            continue
        body = match.group("body")
        warnings: list[str] = []
        due_match = DUE_RE.search(body)
        due = due_match.group(1) if due_match else None
        if due is not None:
            try:
                date.fromisoformat(due)
            except ValueError:
                warnings.append(f"invalid due date: {due}")
                due = None
        tags = sorted(set(TAG_RE.findall(body)))
        priority = "normal"
        for emoji, value in PRIORITIES:
            if emoji in body:
                priority = value
                break
        description = DUE_RE.sub("", body)
        description = DONE_RE.sub("", description)
        for emoji, _ in PRIORITIES:
            description = description.replace(emoji, "")
        description = TAG_RE.sub("", description)
        description = " ".join(description.split())
        records.append(
            {
                "description": description,
                "due": due,
                "priority": priority,
                "record_type": "task",
                "schema_version": 1,
                "source_line": line_number,
                "source_line_sha256": "sha256:" + hashlib.sha256(raw_line.encode("utf-8")).hexdigest(),
                "source_path": source_path,
                "status": STATUS.get(match.group("marker"), "unknown"),
                "subject_ids": sorted({tag_to_subject[tag] for tag in tags if tag in tag_to_subject}),
                "tags": tags,
                "warnings": sorted(warnings),
            }
        )
    return records
```

The line hash covers the exact UTF-8 line without its newline. Hermes must re-read the source line and verify this hash before applying a task mutation. `source_line` is a locator for the current catalog build, not a durable task ID.

- [ ] **Step 4: Run the task tests and verify they pass**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/tests/test_tasks.py -v
```

Expected: two tests report `ok`; final line is `OK`.

- [ ] **Step 5: Commit the task parser**

```bash
git add .fgv/scripts/fgv_state/tasks.py .fgv/tests/test_tasks.py
git commit -m "feat: parse academic task records"
```

## Task 4: Build deterministic file and learning-state records

**Files:**

- Create: `.fgv/scripts/fgv_state/catalog.py`
- Create: `.fgv/tests/test_catalog.py`
- Create: `.fgv/tests/fixtures/mini-vault/.fgv/config/subjects.json`
- Create: `.fgv/tests/fixtures/mini-vault/00 Home/Home.md`
- Create: `.fgv/tests/fixtures/mini-vault/00 Home/Tasks.md`
- Create: `.fgv/tests/fixtures/mini-vault/10 Matérias/ContabilidadeFinanceira/Aulas/08.27/Resumo - DRE.md`
- Create: `.fgv/tests/fixtures/mini-vault/10 Matérias/ContabilidadeFinanceira/Aulas/08.28/Materiais/Slides - DRE.pdf`
- Create: `.fgv/tests/fixtures/mini-vault/20 Conhecimento/Conceitos/Regime de Competência.md`
- Create: `.fgv/tests/fixtures/mini-vault/30 Sistema/Tutor/concepts-history.json`

- [ ] **Step 1: Create the representative mini-vault fixture**

Use this exact fixture configuration:

```json
{
  "schema_version": 1,
  "semester": "2026.2",
  "timezone": "America/Sao_Paulo",
  "subjects": [
    {
      "id": "contabilidade-financeira",
      "name": "Contabilidade Financeira",
      "path": "10 Matérias/ContabilidadeFinanceira",
      "task_tag": "cont",
      "aliases": ["ContabilidadeFinanceira", "cont"]
    }
  ]
}
```

Use this exact fixture Home:

```md
---
tipo: dashboard
contract_version: 1
---
# FGV fixture
```

Use this exact fixture task file:

```md
# Tasks

- [ ] Prova de Contabilidade #cont 📅 2026-08-28 🔺
- [ ] Instalar prateleira #casa
```

Use this exact fixture summary:

```md
---
materia: ContabilidadeFinanceira
data: 2026-08-27
tema: DRE
tags: [resumo, prova]
status: completo
dominio: 1
proxima_revisao: 2026-08-28
---
# DRE
```

Use a small literal byte fixture, not a real PDF, for `Slides - DRE.pdf`:

```text
fixture-pdf-bytes
```

Use this concept note:

```md
---
tipo: conceito
materias: [ContabilidadeFinanceira]
tags: [conceito]
---
# Regime de Competência
```

Use this tutor state:

```json
{
  "Regime de Competência": {
    "subject": "ContabilidadeFinanceira",
    "first_probed": "2026-08-27",
    "times_probed": 1,
    "times_certo": 0,
    "times_parcial": 1,
    "times_gap": 0,
    "last_probed": "2026-08-27",
    "last_status": "parcial"
  },
  "DRE": {
    "subject": "ContabilidadeFinanceira",
    "first_probed": "2026-08-27",
    "times_probed": 1,
    "last_probed": "2026-08-27",
    "last_status": "nao_testado"
  }
}
```

- [ ] **Step 2: Write failing catalog tests**

Create `.fgv/tests/test_catalog.py` with tests that call these public interfaces:

```python
import json
import unittest
from pathlib import Path

from fgv_state.catalog import _ensure_unique_normalized_paths, build_catalog, serialize_catalog
from fgv_state.config import load_settings


FIXTURE = Path(__file__).parent / "fixtures" / "mini-vault"


class CatalogTests(unittest.TestCase):
    def test_indexes_files_tasks_and_learning_without_generated_or_hidden_files(self):
        settings = load_settings(FIXTURE / ".fgv/config/subjects.json")
        build = build_catalog(FIXTURE, settings, "2026-08-28")
        paths = [record["path"] for record in build.records if record["record_type"] == "file"]
        self.assertIn("00 Home/Home.md", paths)
        self.assertIn("10 Matérias/ContabilidadeFinanceira/Aulas/08.28/Materiais/Slides - DRE.pdf", paths)
        self.assertNotIn(".fgv/config/subjects.json", paths)
        self.assertNotIn("30 Sistema/Estado/catalog.jsonl", paths)
        tasks = [record for record in build.records if record["record_type"] == "task"]
        learning = [record for record in build.records if record["record_type"] == "learning_state"]
        self.assertEqual(len(tasks), 2)
        self.assertEqual(len(learning), 2)

    def test_file_record_normalizes_legacy_subject_and_review_fields(self):
        settings = load_settings(FIXTURE / ".fgv/config/subjects.json")
        build = build_catalog(FIXTURE, settings, "2026-08-28")
        record = next(r for r in build.records if r.get("path", "").endswith("Resumo - DRE.md"))
        self.assertEqual(record["subject_ids"], ["contabilidade-financeira"])
        self.assertEqual(record["review_due"], "2026-08-28")
        self.assertEqual(record["mastery"], 1)
        self.assertEqual(record["note_type"], "resumo")

    def test_serialization_and_fingerprints_are_order_independent(self):
        settings = load_settings(FIXTURE / ".fgv/config/subjects.json")
        first = build_catalog(FIXTURE, settings, "2026-08-28")
        second = build_catalog(FIXTURE, settings, "2026-08-28", reverse_walk_for_test=True)
        self.assertEqual(first.source_fingerprint, second.source_fingerprint)
        self.assertEqual(first.build_fingerprint, second.build_fingerprint)
        self.assertEqual(serialize_catalog(first, settings), serialize_catalog(second, settings))
        self.assertTrue(serialize_catalog(first, settings).endswith(b"\n"))

    def test_each_jsonl_line_is_valid_and_manifest_is_first(self):
        settings = load_settings(FIXTURE / ".fgv/config/subjects.json")
        payload = serialize_catalog(build_catalog(FIXTURE, settings, "2026-08-28"), settings)
        records = [json.loads(line) for line in payload.decode("utf-8").splitlines()]
        self.assertEqual(records[0]["record_type"], "manifest")
        self.assertEqual(sum(r["record_type"] == "manifest" for r in records), 1)
        self.assertTrue(all(r["schema_version"] == 1 for r in records))
        self.assertNotIn(str(FIXTURE), payload.decode("utf-8"))

    def test_nfc_collision_is_fatal(self):
        with self.assertRaises(ValueError):
            _ensure_unique_normalized_paths(["Café.md", "Cafe\u0301.md"])


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 3: Run the catalog tests and verify they fail**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/tests/test_catalog.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'fgv_state.catalog'`.

- [ ] **Step 4: Implement catalog models, scanning and serialization**

Create `.fgv/scripts/fgv_state/catalog.py` with these public types and functions:

```python
from __future__ import annotations

import hashlib
import json
import os
import unicodedata
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from . import GENERATOR_VERSION, SCHEMA_VERSION
from .config import Settings, resolve_subject_ids
from .frontmatter import parse_markdown_metadata
from .tasks import parse_tasks


OUTPUT_PATHS = {
    "30 Sistema/Estado/catalog.jsonl",
    "30 Sistema/Estado/dashboard-snapshot.md",
    "30 Sistema/Estado/sync-status.json",
}
EXCLUDED_ROOTS = {".git", ".obsidian", ".fgv", ".trash", ".gstack"}
EXCLUDED_NAMES = {".DS_Store", "._.DS_Store"}
KIND_BY_SUFFIX = {
    ".md": "note",
    ".pdf": "document",
    ".doc": "document",
    ".docx": "document",
    ".xls": "spreadsheet",
    ".xlsx": "spreadsheet",
    ".ppt": "slides",
    ".pptx": "slides",
    ".ipynb": "notebook",
    ".csv": "dataset",
    ".json": "dataset",
    ".py": "code",
    ".r": "code",
    ".jpg": "image",
    ".jpeg": "image",
    ".png": "image",
    ".heic": "image",
}


@dataclass(frozen=True)
class CatalogBuild:
    as_of: str
    source_fingerprint: str
    build_fingerprint: str
    records: tuple[dict[str, object], ...]


def canonical_json(record: dict[str, object]) -> str:
    return json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(data: bytes) -> str:
    return "sha256:" + hashlib.sha256(data).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return "sha256:" + digest.hexdigest()


def _ensure_unique_normalized_paths(paths: list[str]) -> list[str]:
    normalized: list[str] = []
    seen: dict[str, str] = {}
    for original in paths:
        relative = unicodedata.normalize("NFC", original.replace("\\", "/"))
        if relative in seen and seen[relative] != original:
            raise ValueError(f"NFC path collision: {seen[relative]!r} and {original!r}")
        seen[relative] = original
        normalized.append(relative)
    return normalized


def iter_source_files(vault: Path, reverse_walk_for_test: bool = False) -> list[tuple[str, Path]]:
    vault = vault.resolve()
    raw_discovered: list[tuple[str, Path]] = []
    for current_raw, directory_names, file_names in os.walk(vault, followlinks=False):
        current = Path(current_raw)
        for directory_name in list(directory_names):
            candidate = current / directory_name
            if candidate.is_symlink():
                raise ValueError(f"symbolic link is not allowed: {candidate.relative_to(vault)}")
        directory_names[:] = sorted(name for name in directory_names if name not in EXCLUDED_ROOTS)
        names = sorted(file_names, reverse=reverse_walk_for_test)
        for name in names:
            path = current / name
            if path.is_symlink():
                raise ValueError(f"symbolic link is not allowed: {path.relative_to(vault)}")
            if not path.is_file() or name in EXCLUDED_NAMES or name.startswith("."):
                continue
            if name.endswith((".tmp", ".cache", ".mp3.processing")):
                continue
            original = path.relative_to(vault).as_posix()
            raw_discovered.append((original, path))
    normalized = _ensure_unique_normalized_paths([item[0] for item in raw_discovered])
    discovered = [
        (relative, item[1])
        for relative, item in zip(normalized, raw_discovered)
        if relative not in OUTPUT_PATHS
    ]
    discovered.sort(key=lambda item: item[0])
    return discovered


def _file_record(relative: str, path: Path, settings: Settings) -> dict[str, object]:
    payload = path.read_bytes()
    extension = path.suffix.lower().removeprefix(".")
    kind = KIND_BY_SUFFIX.get(path.suffix.lower(), "other")
    record: dict[str, object] = {
        "aliases": [],
        "date": None,
        "date_source": None,
        "extension": extension,
        "kind": kind,
        "mastery": None,
        "note_type": "other",
        "path": relative,
        "record_type": "file",
        "review_due": None,
        "schema_version": SCHEMA_VERSION,
        "sha256": sha256_bytes(payload),
        "size_bytes": len(payload),
        "status": None,
        "subject_ids": list(resolve_subject_ids([], relative, settings)),
        "subjects_raw": [],
        "tags": [],
        "title": unicodedata.normalize("NFC", path.stem),
        "topic": None,
        "warnings": [],
    }
    if kind != "note":
        return record
    decoding_warnings: list[str] = []
    try:
        text = payload.decode("utf-8")
    except UnicodeDecodeError:
        text = payload.decode("utf-8", errors="replace")
        decoding_warnings.append("invalid UTF-8 replaced")
    metadata = parse_markdown_metadata(text, relative, settings.semester)
    record.update(
        aliases=list(metadata.aliases),
        date=metadata.date,
        date_source=metadata.date_source,
        mastery=metadata.mastery,
        note_type=metadata.note_type,
        review_due=metadata.review_due,
        status=metadata.status,
        subject_ids=list(resolve_subject_ids(metadata.subjects_raw, relative, settings)),
        subjects_raw=list(metadata.subjects_raw),
        tags=list(metadata.tags),
        title=metadata.title,
        topic=metadata.topic,
        warnings=sorted(set(decoding_warnings + list(metadata.warnings))),
    )
    return record


def _learning_records(vault: Path, file_records: list[dict[str, object]]) -> list[dict[str, object]]:
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
    existing_paths = {str(record["path"]) for record in file_records}
    records: list[dict[str, object]] = []
    counter_names = (
        "times_probed",
        "times_certo",
        "times_parcial",
        "times_gap",
        "times_nao_sabe",
        "times_nao_testado",
    )
    for concept, value in raw.items():
        if not isinstance(value, dict):
            raise ValueError(f"learning state for {concept!r} must be an object")
        status = value.get("last_status")
        if status not in valid_statuses:
            raise ValueError(f"invalid learning status for {concept!r}: {status!r}")
        counters: dict[str, int] = {}
        for name in counter_names:
            counter = value.get(name, 0)
            if not isinstance(counter, int) or isinstance(counter, bool) or counter < 0:
                raise ValueError(f"invalid {name} for {concept!r}")
            counters[name] = counter
        candidate = unicodedata.normalize("NFC", f"20 Conhecimento/Conceitos/{concept}.md")
        records.append(
            {
                "concept": unicodedata.normalize("NFC", str(concept)),
                "concept_path": candidate if candidate in existing_paths else None,
                "first_probed": value.get("first_probed"),
                "last_probed": value.get("last_probed"),
                "last_status": status,
                "record_type": "learning_state",
                "schema_version": SCHEMA_VERSION,
                "subject": value.get("subject"),
                **counters,
            }
        )
    records.sort(key=lambda record: str(record["concept"]))
    return records


def _record_key(record: dict[str, object]) -> tuple[object, ...]:
    order = {"file": 0, "task": 1, "learning_state": 2}
    record_type = str(record["record_type"])
    if record_type == "file":
        return (order[record_type], str(record["path"]))
    if record_type == "task":
        return (order[record_type], str(record["source_path"]), int(record["source_line"]))
    return (order[record_type], str(record["concept"]))


def build_catalog(vault: Path, settings: Settings, as_of: str, reverse_walk_for_test: bool = False) -> CatalogBuild:
    date.fromisoformat(as_of)
    vault = vault.resolve()
    discovered = iter_source_files(vault, reverse_walk_for_test=reverse_walk_for_test)
    file_records = [_file_record(relative, path, settings) for relative, path in discovered]
    records: list[dict[str, object]] = list(file_records)
    tasks_path = vault / "00 Home/Tasks.md"
    if tasks_path.exists():
        records.extend(parse_tasks(tasks_path.read_text(encoding="utf-8"), "00 Home/Tasks.md", settings))
    records.extend(_learning_records(vault, file_records))
    records.sort(key=_record_key)

    source_digest = hashlib.sha256()
    file_by_path = {str(record["path"]): record for record in file_records}
    for relative, _ in discovered:
        digest = str(file_by_path[relative]["sha256"]).removeprefix("sha256:")
        source_digest.update(relative.encode("utf-8"))
        source_digest.update(b"\0")
        source_digest.update(bytes.fromhex(digest))
        source_digest.update(b"\0")
    config_path = vault / ".fgv/config/subjects.json"
    config_relative = ".fgv/config/subjects.json"
    source_digest.update(config_relative.encode("utf-8"))
    source_digest.update(b"\0")
    source_digest.update(bytes.fromhex(sha256_file(config_path).removeprefix("sha256:")))
    source_digest.update(b"\0")
    source_fingerprint = "sha256:" + source_digest.hexdigest()
    fingerprint_payload = "\0".join(
        (str(SCHEMA_VERSION), GENERATOR_VERSION, as_of, source_fingerprint)
    ).encode("utf-8")
    build_fingerprint = sha256_bytes(fingerprint_payload)
    return CatalogBuild(as_of, source_fingerprint, build_fingerprint, tuple(records))


def serialize_catalog(build: CatalogBuild, settings: Settings) -> bytes:
    counts = {
        "files": sum(record["record_type"] == "file" for record in build.records),
        "learning_states": sum(record["record_type"] == "learning_state" for record in build.records),
        "tasks": sum(record["record_type"] == "task" for record in build.records),
        "warnings": sum(len(record.get("warnings", [])) for record in build.records),
    }
    manifest: dict[str, object] = {
        "as_of": build.as_of,
        "build_fingerprint": build.build_fingerprint,
        "counts": counts,
        "generator_version": GENERATOR_VERSION,
        "record_type": "manifest",
        "schema_version": SCHEMA_VERSION,
        "source_fingerprint": build.source_fingerprint,
        "subjects": [
            {
                "id": subject.id,
                "name": subject.name,
                "path": subject.path,
                "task_tag": subject.task_tag,
            }
            for subject in sorted(settings.subjects, key=lambda item: item.id)
        ],
    }
    lines = [canonical_json(manifest)]
    lines.extend(canonical_json(record) for record in build.records)
    return ("\n".join(lines) + "\n").encode("utf-8")
```

`iter_source_files` uses `os.walk(vault, followlinks=False)`, prunes excluded roots before descending, rejects every symlink, normalizes paths with NFC and `/`, skips output and temporary paths, then sorts after the optional test reversal.

For each regular file, emit a fixed-shape `file` record:

```json
{
  "aliases": [],
  "date": null,
  "date_source": null,
  "extension": "md",
  "kind": "note",
  "mastery": null,
  "note_type": "other",
  "path": "00 Home/Home.md",
  "record_type": "file",
  "review_due": null,
  "schema_version": 1,
  "sha256": "sha256:<hex>",
  "size_bytes": 123,
  "status": null,
  "subject_ids": [],
  "subjects_raw": [],
  "tags": [],
  "title": "Home",
  "topic": null,
  "warnings": []
}
```

Markdown records use `parse_markdown_metadata` and `resolve_subject_ids`. Binary records use the static extension map, file stem as title and empty normalized metadata. Never include file content.

Read `00 Home/Tasks.md` after file records and append `parse_tasks` output if the file exists. Read `30 Sistema/Tutor/concepts-history.json` and append normalized learning records. Missing tutor state produces zero records; malformed JSON or a non-object root raises `ValueError`.

Learning records use this fixed shape and fill missing counters with zero:

```json
{
  "concept": "Regime de Competência",
  "concept_path": "20 Conhecimento/Conceitos/Regime de Competência.md",
  "first_probed": "2026-08-27",
  "last_probed": "2026-08-27",
  "last_status": "parcial",
  "record_type": "learning_state",
  "schema_version": 1,
  "subject": "ContabilidadeFinanceira",
  "times_certo": 0,
  "times_gap": 0,
  "times_nao_sabe": 0,
  "times_nao_testado": 0,
  "times_parcial": 1,
  "times_probed": 1
}
```

Resolve `concept_path` by exact NFC filename under `20 Conhecimento/Conceitos/`; use `None` when absent. Accept only `certo`, `parcial`, `gap`, `nao_sabe`, `nao_testado`; an unknown value is fatal because it changes dashboard semantics.

Compute the source fingerprint from all scanned files plus `.fgv/config/subjects.json`. Do not rely on traversal order. Compute the build fingerprint with:

```python
payload = "\0".join((str(SCHEMA_VERSION), GENERATOR_VERSION, as_of, source_fingerprint)).encode("utf-8")
build_fingerprint = sha256_bytes(payload)
```

`serialize_catalog` prepends a manifest containing `subjects` sorted by ID and counts for files, tasks, learning states and warnings. It then emits records in type order `file`, `task`, `learning_state`. Return encoded UTF-8 bytes with one final LF.

- [ ] **Step 5: Run the catalog tests and verify they pass**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/tests/test_catalog.py -v
```

Expected: five tests report `ok`; final line is `OK`.

- [ ] **Step 6: Commit the catalog core and fixture**

```bash
git add .fgv/scripts/fgv_state/catalog.py .fgv/tests/test_catalog.py .fgv/tests/fixtures/mini-vault
git commit -m "feat: build deterministic catalog v1"
```

## Task 5: Render the static dashboard projection

**Files:**

- Create: `.fgv/scripts/fgv_state/dashboard.py`
- Create: `.fgv/tests/test_dashboard.py`

- [ ] **Step 1: Write failing deadline and learning-section tests**

Create `.fgv/tests/test_dashboard.py`:

```python
import hashlib
import unittest
from pathlib import Path

from fgv_state.catalog import build_catalog, serialize_catalog
from fgv_state.config import load_settings
from fgv_state.dashboard import render_dashboard


FIXTURE = Path(__file__).parent / "fixtures" / "mini-vault"


class DashboardTests(unittest.TestCase):
    def render(self) -> str:
        settings = load_settings(FIXTURE / ".fgv/config/subjects.json")
        build = build_catalog(FIXTURE, settings, "2026-08-28")
        catalog = serialize_catalog(build, settings)
        catalog_sha = "sha256:" + hashlib.sha256(catalog).hexdigest()
        return render_dashboard(build.records, settings, "2026-08-28", build.build_fingerprint, catalog_sha)

    def test_renders_static_task_sections_without_checkboxes(self):
        output = self.render()
        self.assertIn("# Painel", output)
        self.assertIn("### Hoje", output)
        self.assertIn("Prova de Contabilidade", output)
        self.assertNotIn("Instalar prateleira", output)
        self.assertNotIn("- [ ]", output)
        self.assertIn("[[00 Home/Tasks|Tasks]]", output)

    def test_renders_processing_review_learning_and_subject_state(self):
        output = self.render()
        self.assertIn("## Processamento", output)
        self.assertIn("08.28", output)
        self.assertIn("sem resumo", output)
        self.assertIn("sem transcrito", output)
        self.assertIn("## Revisões vencidas", output)
        self.assertIn("Resumo - DRE", output)
        self.assertIn("Regime de Competência", output)
        self.assertIn("nao_testado", output)
        self.assertIn("| Contabilidade Financeira |", output)

    def test_frontmatter_has_no_wall_clock_or_git_identity(self):
        output = self.render()
        self.assertIn("as_of: 2026-08-28", output)
        self.assertIn("catalog_sha256: \"sha256:", output)
        self.assertNotIn("generated_at", output)
        self.assertNotIn("git_commit", output)


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the renderer tests and verify they fail**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/tests/test_dashboard.py -v
```

Expected: FAIL with `ModuleNotFoundError: No module named 'fgv_state.dashboard'`.

- [ ] **Step 3: Implement deterministic dashboard rendering**

Create `.fgv/scripts/fgv_state/dashboard.py` with this public interface:

```python
from __future__ import annotations

from collections import defaultdict
from datetime import date, timedelta
from pathlib import PurePosixPath
import re

from .config import Settings


PRIORITY_RANK = {"highest": 5, "high": 4, "medium": 3, "normal": 2, "low": 1, "lowest": 0}
GAP_RANK = {"gap": 0, "nao_sabe": 0, "parcial": 1, "nao_testado": 2, "certo": 3}
CLASS_FOLDER_RE = re.compile(r"^(\d{2})\.(\d{2})$")


def _escape(value: object) -> str:
    return (
        str(value)
        .replace("\\", "\\\\")
        .replace("\n", " ")
        .replace("\r", " ")
        .replace("|", "\\|")
        .replace("[", "\\[")
        .replace("]", "\\]")
        .replace("<", "&lt;")
        .replace(">", "&gt;")
    )


def _wikilink(path: str, label: object) -> str:
    target = path[:-3] if path.endswith(".md") else path
    return f"[[{target}|{_escape(label)}]]"


def _append_items(lines: list[str], heading: str, items: list[str]) -> None:
    lines.extend((heading, ""))
    lines.extend(items if items else ["Nenhuma."])
    lines.append("")


def _class_states(records: tuple[dict[str, object], ...], settings: Settings) -> list[dict[str, object]]:
    grouped: dict[tuple[str, str], dict[str, object]] = {}
    for record in records:
        if record.get("record_type") != "file":
            continue
        path = str(record["path"])
        for subject in settings.subjects:
            prefix = subject.path + "/Aulas/"
            if not path.startswith(prefix):
                continue
            remainder = path[len(prefix) :]
            folder = remainder.split("/", 1)[0]
            match = CLASS_FOLDER_RE.fullmatch(folder)
            if not match:
                continue
            candidate = f"{settings.semester[:4]}-{match.group(1)}-{match.group(2)}"
            try:
                class_date = date.fromisoformat(candidate).isoformat()
            except ValueError:
                continue
            state = grouped.setdefault(
                (subject.id, folder),
                {
                    "date": class_date,
                    "files": [],
                    "folder": folder,
                    "subject_id": subject.id,
                },
            )
            state["files"].append(record)
    return sorted(
        grouped.values(),
        key=lambda item: (
            -date.fromisoformat(str(item["date"])).toordinal(),
            str(item["subject_id"]),
            str(item["folder"]),
        ),
    )


def _class_link(state: dict[str, object], subject_name: str) -> str:
    files = list(state["files"])
    notes = [record for record in files if record.get("kind") == "note"]
    preferred = sorted(
        notes,
        key=lambda record: (
            0 if PurePosixPath(str(record["path"])).name.casefold().startswith("resumo") else 1,
            str(record["path"]),
        ),
    )
    label = f"{subject_name} {state['folder']}"
    return _wikilink(str(preferred[0]["path"]), label) if preferred else f"`{_escape(label)}`"


def render_dashboard(
    records: tuple[dict[str, object], ...],
    settings: Settings,
    as_of: str,
    build_fingerprint: str,
    catalog_sha256: str,
) -> str:
    today = date.fromisoformat(as_of)
    subject_by_id = settings.subject_by_id
    tasks = [
        record
        for record in records
        if record.get("record_type") == "task"
        and record.get("status") in {"todo", "in_progress"}
        and record.get("subject_ids")
    ]

    def task_sort(record: dict[str, object]) -> tuple[object, ...]:
        return (
            str(record.get("due") or "9999-12-31"),
            -PRIORITY_RANK.get(str(record.get("priority")), 0),
            str(record["subject_ids"][0]),
            str(record.get("description", "")).casefold(),
        )

    def task_line(record: dict[str, object]) -> str:
        names = ", ".join(subject_by_id[item].name for item in record["subject_ids"] if item in subject_by_id)
        return (
            f"- {_escape(record.get('due') or 'sem prazo')}, {_escape(record['description'])} "
            f"({_escape(names)}, [[00 Home/Tasks|Tasks]])"
        )

    overdue = sorted(
        [record for record in tasks if record.get("due") and date.fromisoformat(str(record["due"])) < today],
        key=task_sort,
    )
    due_today = sorted([record for record in tasks if record.get("due") == as_of], key=task_sort)
    horizon = today + timedelta(days=7)
    upcoming = sorted(
        [
            record
            for record in tasks
            if record.get("due") and today < date.fromisoformat(str(record["due"])) <= horizon
        ],
        key=task_sort,
    )

    classes = _class_states(records, settings)
    missing_transcript: list[str] = []
    material_without_summary: list[str] = []
    latest_class: dict[str, dict[str, object]] = {}
    for state in classes:
        subject = subject_by_id[str(state["subject_id"])]
        files = list(state["files"])
        markdown_names = [
            PurePosixPath(str(record["path"])).name.casefold()
            for record in files
            if record.get("kind") == "note"
        ]
        has_transcript = any(name.startswith("transcrito") for name in markdown_names)
        has_summary = any(name.startswith("resumo") for name in markdown_names)
        has_material = any(
            record.get("kind") != "note" or "/Materiais/" in str(record["path"])
            for record in files
        )
        link = _class_link(state, subject.name)
        if not has_transcript:
            missing_transcript.append(f"- {link}: sem transcrito")
        if has_material and not has_summary:
            material_without_summary.append(f"- {link}: com material e sem resumo")
        current = latest_class.get(subject.id)
        if current is None or str(state["date"]) > str(current["date"]):
            latest_class[subject.id] = state
    reviews = sorted(
        [
            record
            for record in records
            if record.get("record_type") == "file"
            and record.get("kind") == "note"
            and record.get("review_due")
            and date.fromisoformat(str(record["review_due"])) <= today
            and record.get("mastery") != 3
        ],
        key=lambda record: (str(record["review_due"]), str(record["path"])),
    )
    review_lines = [
        f"- {_escape(record['review_due'])}, {_wikilink(str(record['path']), record['title'])}"
        for record in reviews
    ]

    learning = [record for record in records if record.get("record_type") == "learning_state"]
    gaps = sorted(
        [record for record in learning if record.get("last_status") in {"gap", "nao_sabe", "parcial"}],
        key=lambda record: (
            GAP_RANK[str(record["last_status"])],
            str(record.get("last_probed") or "0000-00-00"),
            str(record["concept"]),
        ),
    )
    not_tested = sorted(
        [record for record in learning if record.get("last_status") == "nao_testado"],
        key=lambda record: (str(record.get("last_probed") or "0000-00-00"), str(record["concept"])),
    )[:10]

    def learning_line(record: dict[str, object]) -> str:
        concept = (
            _wikilink(str(record["concept_path"]), record["concept"])
            if record.get("concept_path")
            else _escape(record["concept"])
        )
        return f"- {concept}: {_escape(record['last_status'])}, última sondagem {_escape(record.get('last_probed') or 'sem data')}"

    lines = [
        "---",
        "tipo: dashboard_snapshot",
        "schema_version: 1",
        f"as_of: {as_of}",
        f'build_fingerprint: "{build_fingerprint}"',
        f'catalog_sha256: "{catalog_sha256}"',
        "---",
        "",
        "<!-- GENERATED FILE. Edite as fontes e regenere. -->",
        "# Painel",
        "",
        "## Agora",
        "",
    ]
    _append_items(lines, "### Atrasadas", [task_line(record) for record in overdue])
    _append_items(lines, "### Hoje", [task_line(record) for record in due_today])
    _append_items(lines, "### Próximos 7 dias", [task_line(record) for record in upcoming])
    lines.extend(("## Processamento", ""))
    _append_items(lines, "### Aulas sem transcrito", missing_transcript)
    _append_items(lines, "### Aulas com material e sem resumo", material_without_summary)
    _append_items(lines, "## Revisões vencidas", review_lines)
    lines.extend(("## Aprendizagem", ""))
    _append_items(lines, "### Gaps abertos", [learning_line(record) for record in gaps])
    _append_items(lines, "### Não testados", [learning_line(record) for record in not_tested])
    lines.extend(("## Matérias", "", "| Matéria | Pendentes | Atrasadas | Última aula | Gaps |", "|---|---:|---:|---|---:|"))
    for subject in sorted(settings.subjects, key=lambda item: item.name):
        pending_count = sum(subject.id in record["subject_ids"] for record in tasks)
        overdue_count = sum(subject.id in record["subject_ids"] for record in overdue)
        gap_count = sum(
            record.get("subject") in {subject.id, subject.name, *subject.aliases}
            and record.get("last_status") in {"gap", "nao_sabe", "parcial"}
            for record in learning
        )
        state = latest_class.get(subject.id)
        latest = _class_link(state, subject.name) if state else "Nenhuma"
        lines.append(f"| {_escape(subject.name)} | {pending_count} | {overdue_count} | {latest} | {gap_count} |")
    warning_count = sum(len(record.get("warnings", [])) for record in records)
    lines.extend(("", "## Integridade", ""))
    lines.append("Nenhum aviso." if warning_count == 0 else f"- {warning_count} aviso(s) de metadata no catálogo.")
    return "\n".join(lines).rstrip() + "\n"
```

The frontmatter must be exactly these fields and no wall-clock value:

```yaml
---
tipo: dashboard_snapshot
schema_version: 1
as_of: 2026-08-28
build_fingerprint: "sha256:<hex>"
catalog_sha256: "sha256:<hex>"
---
```

Render these sections in fixed order:

```md
<!-- GENERATED FILE. Edite as fontes e regenere. -->
# Painel

## Agora
### Atrasadas
### Hoje
### Próximos 7 dias

## Processamento
### Aulas sem transcrito
### Aulas com material e sem resumo

## Revisões vencidas

## Aprendizagem
### Gaps abertos
### Não testados

## Matérias

## Integridade
```

Implement the exact projection rules:

- Include only open tasks with at least one active `subject_id` in deadline sections.
- `Atrasadas`: `due < as_of`.
- `Hoje`: `due == as_of`.
- `Próximos 7 dias`: `as_of < due <= as_of + 7 days`.
- Sort tasks by due ascending, priority rank descending, first subject ID, then case-folded description.
- Render tasks as plain bullets with due date, description, subject display name and `[[00 Home/Tasks|Tasks]]`. Never render checkboxes.
- Group file records below each configured `<subject.path>/Aulas/MM.DD/` folder.
- A class is `sem transcrito` when it has at least one indexed file but no Markdown filename beginning with `Transcrito`.
- A class is `com material e sem resumo` when it has a non-Markdown file or `/Materiais/` file and no Markdown filename beginning with `Resumo`.
- Derive the class date from `MM.DD` and the configured semester year. Sort incomplete classes by date descending, then path.
- A review is due when a note has non-null `review_due <= as_of` and `mastery != 3`.
- `Gaps abertos` includes `gap`, `nao_sabe` and `parcial`, sorted by `GAP_RANK`, oldest `last_probed`, then concept.
- `Não testados` includes `nao_testado`, limited to ten records.
- Resolve a concept to `[[concept_path|concept]]`; render plain escaped text when `concept_path` is null.
- The subject table columns are `Matéria`, `Pendentes`, `Atrasadas`, `Última aula`, `Gaps`. Sort rows by configured display name.
- `Integridade` shows the sum of `warnings` arrays and writes `Nenhum aviso.` when zero.
- Every empty list section contains one line, `Nenhuma.`.
- Escape backslashes, pipes, newlines, brackets and HTML-sensitive task text before rendering.
- Return a Python string ending with exactly one LF.

- [ ] **Step 4: Run renderer tests and verify they pass**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/tests/test_dashboard.py -v
```

Expected: three tests report `ok`; final line is `OK`.

- [ ] **Step 5: Commit the static projection**

```bash
git add .fgv/scripts/fgv_state/dashboard.py .fgv/tests/test_dashboard.py
git commit -m "feat: render dashboard snapshot"
```

## Task 6: Add fail-closed atomic I/O and CLI orchestration

**Files:**

- Create: `.fgv/scripts/fgv_state/io.py`
- Create: `.fgv/scripts/generate_state.py`
- Create: `.fgv/tests/test_generate_state.py`

- [ ] **Step 1: Write failing end-to-end and failure-safety tests**

Create `.fgv/tests/test_generate_state.py`:

```python
import os
import shutil
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".fgv/scripts/generate_state.py"
FIXTURE = Path(__file__).parent / "fixtures/mini-vault"


class GenerateStateTests(unittest.TestCase):
    def copy_fixture(self, root: Path) -> Path:
        vault = root / "vault"
        shutil.copytree(FIXTURE, vault)
        return vault

    def run_cli(self, vault: Path, *extra: str) -> subprocess.CompletedProcess[str]:
        env = dict(os.environ)
        env["PYTHONPATH"] = str(ROOT / ".fgv/scripts")
        return subprocess.run(
            [sys.executable, str(SCRIPT), "--vault", str(vault), "--as-of", "2026-08-28", *extra],
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_generates_both_outputs_and_second_run_is_byte_and_mtime_idempotent(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = self.copy_fixture(Path(tmp))
            first = self.run_cli(vault)
            self.assertEqual(first.returncode, 0, first.stderr)
            catalog = vault / "30 Sistema/Estado/catalog.jsonl"
            snapshot = vault / "30 Sistema/Estado/dashboard-snapshot.md"
            first_bytes = (catalog.read_bytes(), snapshot.read_bytes())
            first_mtimes = (catalog.stat().st_mtime_ns, snapshot.stat().st_mtime_ns)
            time.sleep(0.01)
            second = self.run_cli(vault)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(first_bytes, (catalog.read_bytes(), snapshot.read_bytes()))
            self.assertEqual(first_mtimes, (catalog.stat().st_mtime_ns, snapshot.stat().st_mtime_ns))
            self.assertIn("catalog changed=no", second.stdout)
            self.assertIn("snapshot changed=no", second.stdout)

    def test_check_mode_reports_fresh_then_stale_without_writing(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = self.copy_fixture(Path(tmp))
            self.assertEqual(self.run_cli(vault).returncode, 0)
            fresh = self.run_cli(vault, "--check")
            self.assertEqual(fresh.returncode, 0)
            self.assertIn("state fresh", fresh.stdout)
            home = vault / "00 Home/Home.md"
            home.write_text(home.read_text(encoding="utf-8") + "\nchange\n", encoding="utf-8")
            before = (vault / "30 Sistema/Estado/catalog.jsonl").read_bytes()
            stale = self.run_cli(vault, "--check")
            self.assertEqual(stale.returncode, 1)
            self.assertIn("state stale", stale.stdout)
            self.assertEqual(before, (vault / "30 Sistema/Estado/catalog.jsonl").read_bytes())

    def test_malformed_canonical_state_leaves_previous_outputs_untouched(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = self.copy_fixture(Path(tmp))
            self.assertEqual(self.run_cli(vault).returncode, 0)
            catalog = vault / "30 Sistema/Estado/catalog.jsonl"
            snapshot = vault / "30 Sistema/Estado/dashboard-snapshot.md"
            before = (catalog.read_bytes(), snapshot.read_bytes())
            (vault / "30 Sistema/Tutor/concepts-history.json").write_text("{broken", encoding="utf-8")
            failed = self.run_cli(vault)
            self.assertEqual(failed.returncode, 2)
            self.assertIn("generation failed", failed.stderr)
            self.assertEqual(before, (catalog.read_bytes(), snapshot.read_bytes()))

    def test_home_is_never_modified(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = self.copy_fixture(Path(tmp))
            home = vault / "00 Home/Home.md"
            before = home.read_bytes()
            self.assertEqual(self.run_cli(vault).returncode, 0)
            self.assertEqual(before, home.read_bytes())


if __name__ == "__main__":
    unittest.main()
```

- [ ] **Step 2: Run the end-to-end tests and verify they fail**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/tests/test_generate_state.py -v
```

Expected: four tests fail because `.fgv/scripts/generate_state.py` does not exist.

- [ ] **Step 3: Implement atomic write-if-changed**

Create `.fgv/scripts/fgv_state/io.py`:

```python
from __future__ import annotations

import os
import tempfile
from pathlib import Path


def write_if_changed(path: Path, payload: bytes) -> bool:
    if path.exists() and path.read_bytes() == payload:
        return False
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.",
        suffix=".tmp",
        dir=path.parent,
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
        return True
    finally:
        if temporary.exists():
            temporary.unlink()
```

- [ ] **Step 4: Implement the generator CLI**

Create `.fgv/scripts/generate_state.py` with this behavior:

```python
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

from fgv_state.catalog import build_catalog, serialize_catalog
from fgv_state.config import load_settings
from fgv_state.dashboard import render_dashboard
from fgv_state.io import write_if_changed


CATALOG = Path("30 Sistema/Estado/catalog.jsonl")
SNAPSHOT = Path("30 Sistema/Estado/dashboard-snapshot.md")
CONFIG = Path(".fgv/config/subjects.json")


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate the FGV catalog and dashboard snapshot")
    parser.add_argument("--vault", required=True, type=Path)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def validate_as_of(value: str) -> str:
    date.fromisoformat(value)
    return value


def build_outputs(vault: Path, as_of: str) -> tuple[bytes, bytes]:
    settings = load_settings(vault / CONFIG)
    build = build_catalog(vault, settings, validate_as_of(as_of))
    catalog = serialize_catalog(build, settings)
    for line_number, line in enumerate(catalog.decode("utf-8").splitlines(), start=1):
        record = json.loads(line)
        if record.get("schema_version") != 1:
            raise ValueError(f"catalog line {line_number} has wrong schema")
    catalog_sha = "sha256:" + hashlib.sha256(catalog).hexdigest()
    snapshot_text = render_dashboard(
        build.records,
        settings,
        as_of,
        build.build_fingerprint,
        catalog_sha,
    )
    snapshot = snapshot_text.encode("utf-8")
    if not snapshot.endswith(b"\n"):
        raise ValueError("snapshot must end with LF")
    if f'catalog_sha256: "{catalog_sha}"'.encode("utf-8") not in snapshot:
        raise ValueError("snapshot/catalog fingerprint mismatch")
    return catalog, snapshot


def main() -> int:
    args = parse_args()
    vault = args.vault.resolve()
    try:
        catalog, snapshot = build_outputs(vault, args.as_of)
        catalog_path = vault / CATALOG
        snapshot_path = vault / SNAPSHOT
        if args.check:
            fresh = (
                catalog_path.exists()
                and snapshot_path.exists()
                and catalog_path.read_bytes() == catalog
                and snapshot_path.read_bytes() == snapshot
            )
            print("state fresh" if fresh else "state stale")
            return 0 if fresh else 1
        catalog_changed = write_if_changed(catalog_path, catalog)
        snapshot_changed = write_if_changed(snapshot_path, snapshot)
        print(f"catalog changed={'yes' if catalog_changed else 'no'}")
        print(f"snapshot changed={'yes' if snapshot_changed else 'no'}")
        return 0
    except Exception as exc:
        print(f"generation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
```

`build_outputs` must perform every parse, serialization and cross-file validation before the first call to `write_if_changed`. Do not catch per-file configuration or tutor-state errors inside the build.

- [ ] **Step 5: Run the end-to-end tests and verify they pass**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/tests/test_generate_state.py -v
```

Expected: four tests report `ok`; final line is `OK`.

- [ ] **Step 6: Run the complete test suite**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 -m unittest discover -s .fgv/tests -p 'test_*.py' -v
```

Expected: all configuration, frontmatter, task, catalog, dashboard and end-to-end tests pass; final line is `OK`.

- [ ] **Step 7: Commit atomic generation**

```bash
git add .fgv/scripts/fgv_state/io.py .fgv/scripts/generate_state.py .fgv/tests/test_generate_state.py
git commit -m "feat: generate state atomically"
```

## Task 7: Add cross-environment determinism and contract regression tests

**Files:**

- Modify: `.fgv/tests/test_generate_state.py`
- Modify: `.fgv/tests/test_catalog.py`

- [ ] **Step 1: Add failing locale, timezone and schema-regression tests**

Add to `GenerateStateTests`:

```python
    def test_explicit_as_of_is_timezone_and_locale_independent(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = self.copy_fixture(Path(tmp))
            outputs = []
            for timezone, locale in (("UTC", "C"), ("America/Sao_Paulo", "C")):
                env = dict(os.environ)
                env.update(PYTHONPATH=str(ROOT / ".fgv/scripts"), TZ=timezone, LC_ALL=locale)
                completed = subprocess.run(
                    [sys.executable, str(SCRIPT), "--vault", str(vault), "--as-of", "2026-08-28"],
                    text=True,
                    capture_output=True,
                    env=env,
                    check=False,
                )
                self.assertEqual(completed.returncode, 0, completed.stderr)
                outputs.append(
                    (
                        (vault / "30 Sistema/Estado/catalog.jsonl").read_bytes(),
                        (vault / "30 Sistema/Estado/dashboard-snapshot.md").read_bytes(),
                    )
                )
            self.assertEqual(outputs[0], outputs[1])

    def test_catalog_and_snapshot_reference_the_same_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = self.copy_fixture(Path(tmp))
            self.assertEqual(self.run_cli(vault).returncode, 0)
            catalog = (vault / "30 Sistema/Estado/catalog.jsonl").read_bytes()
            expected = "sha256:" + __import__("hashlib").sha256(catalog).hexdigest()
            snapshot = (vault / "30 Sistema/Estado/dashboard-snapshot.md").read_text(encoding="utf-8")
            self.assertIn(f'catalog_sha256: "{expected}"', snapshot)
```

Add to `CatalogTests`:

```python
    def test_catalog_has_only_relative_paths_and_fixed_record_types(self):
        settings = load_settings(FIXTURE / ".fgv/config/subjects.json")
        payload = serialize_catalog(build_catalog(FIXTURE, settings, "2026-08-28"), settings)
        records = [json.loads(line) for line in payload.decode("utf-8").splitlines()]
        self.assertEqual(
            {record["record_type"] for record in records},
            {"manifest", "file", "task", "learning_state"},
        )
        for record in records:
            path = record.get("path") or record.get("source_path") or record.get("concept_path")
            if path:
                self.assertFalse(Path(path).is_absolute())
                self.assertNotIn("..", Path(path).parts)
```

- [ ] **Step 2: Run the new tests before any fixes**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/tests/test_generate_state.py -v
PYTHONPATH=.fgv/scripts python3 .fgv/tests/test_catalog.py -v
```

Expected: the new tests expose any locale-dependent sort, timezone-dependent date or absolute-path leak. If the existing implementation already satisfies them, record that they pass without code changes and continue.

- [ ] **Step 3: Remove any environment dependence found by the tests**

Apply only the fix indicated by the failing assertion:

- Replace locale-based sorting with Python tuple sorting over NFC strings.
- Replace implicit `date.today()` or `datetime.now()` with the parsed `as_of` argument.
- Replace absolute path serialization with `path.relative_to(vault).as_posix()` followed by NFC normalization.
- Keep `ensure_ascii=False`, `sort_keys=True` and compact separators in every JSON line.

Do not introduce locale setup, process-wide timezone mutation or a generated timestamp.

- [ ] **Step 4: Run the complete suite twice**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 -m unittest discover -s .fgv/tests -p 'test_*.py' -v
PYTHONPATH=.fgv/scripts python3 -m unittest discover -s .fgv/tests -p 'test_*.py' -v
```

Expected: both runs end in `OK` with identical test counts.

- [ ] **Step 5: Commit determinism guards**

```bash
git add .fgv/tests/test_generate_state.py .fgv/tests/test_catalog.py .fgv/scripts/fgv_state
git commit -m "test: lock dashboard determinism"
```

## Task 8: Create the human-owned Home and state documentation

**Files:**

- Create: `00 Home/Home.md`
- Create: `30 Sistema/Estado/README.md`
- Create: `.fgv/tests/test_home_contract.py`

- [ ] **Step 1: Write a failing ownership and embed contract test**

Create `.fgv/tests/test_home_contract.py`:

```python
import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class HomeContractTests(unittest.TestCase):
    def test_home_is_human_owned_shell_with_snapshot_embed(self):
        home = (ROOT / "00 Home/Home.md").read_text(encoding="utf-8")
        self.assertIn("tipo: dashboard", home)
        self.assertIn("contract_version: 1", home)
        self.assertIn("[[00 Home/Tasks|Tasks]]", home)
        self.assertIn("![[30 Sistema/Estado/dashboard-snapshot#Painel]]", home)
        self.assertNotIn("GENERATED FILE", home)

    def test_state_readme_declares_single_writer_and_fallback(self):
        readme = (ROOT / "30 Sistema/Estado/README.md").read_text(encoding="utf-8")
        self.assertIn("único escritor", readme)
        self.assertIn("fonte canônica", readme)
        self.assertIn("filesystem", readme)


if __name__ == "__main__":
    unittest.main()
```

`Path(__file__).resolve().parents[2]` is the vault root for a test stored at `.fgv/tests/test_home_contract.py`; the test must use that exact root without conditional path logic.

- [ ] **Step 2: Run the contract test and verify it fails because Home is absent**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/tests/test_home_contract.py -v
```

Expected: FAIL with `FileNotFoundError` for `00 Home/Home.md` or `30 Sistema/Estado/README.md`.

- [ ] **Step 3: Create the human-owned Home shell**

Create `00 Home/Home.md` exactly as follows:

```md
---
id: home-dashboard
tipo: dashboard
semestre: 2026.2
contract_version: 1
tags: [home]
---

# FGV

[[00 Home/Tasks|Tasks]] · [[00 Home/Revisões|Revisões]] · [[30 Sistema/Tutor/gaps|Gaps]]

![[30 Sistema/Estado/dashboard-snapshot#Painel]]
```

This file is never regenerated. Arthur may add navigation, callouts, Bases, Dataview or Tasks queries later without changing the machine contract. The only required body element is the snapshot embed.

- [ ] **Step 4: Document state ownership and degraded operation**

Create `30 Sistema/Estado/README.md`:

```md
# Estado gerado

`catalog.jsonl` e `dashboard-snapshot.md` são read models. O gerador compartilhado é o único escritor destes dois arquivos.

As fontes canônicas são as notas, tarefas e estados de aprendizagem do filesystem. Arthur, `/fgv` e Hermes alteram as fontes que possuem e depois executam `.fgv/scripts/generate_state.py`.

Não edite arquivos gerados manualmente. Se houver conflito Git, preserve as fontes, remova a resolução manual do estado e regenere.

Hermes valida `schema_version` e `catalog_sha256`. Se o catálogo estiver ausente, incompatível ou inconsistente com o snapshot, Hermes volta à leitura direta do filesystem.
```

- [ ] **Step 5: Run the Home contract and full suite**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/tests/test_home_contract.py -v
PYTHONPATH=.fgv/scripts python3 -m unittest discover -s .fgv/tests -p 'test_*.py' -v
```

Expected: Home contract reports two `ok` tests; the complete suite ends in `OK`.

- [ ] **Step 6: Commit the human shell and ownership docs**

```bash
git add '00 Home/Home.md' '30 Sistema/Estado/README.md' .fgv/tests/test_home_contract.py
git commit -m "docs: add human dashboard entrypoint"
```

## Task 9: Generate and validate the real migrated vault state

**Files:**

- Create: `30 Sistema/Estado/catalog.jsonl`
- Create: `30 Sistema/Estado/dashboard-snapshot.md`

- [ ] **Step 1: Verify migration preconditions without writing**

Run:

```bash
test -f '00 Home/Tasks.md'
test -d '10 Matérias'
test -d '20 Conhecimento/Conceitos'
test -f '.fgv/config/subjects.json'
python3 -c 'import json; from pathlib import Path; c=json.loads(Path(".fgv/config/subjects.json").read_text()); missing=[s["path"] for s in c["subjects"] if not Path(s["path"]).is_dir()]; raise SystemExit("missing subject folders: "+", ".join(missing) if missing else 0)'
```

Expected: all commands exit zero and produce no missing-folder message. If they fail, stop and finish the structural migration plan first. Do not make the dashboard generator understand both old and new roots.

- [ ] **Step 2: Run the full tests before touching real generated outputs**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 -m unittest discover -s .fgv/tests -p 'test_*.py' -v
```

Expected: final line is `OK`.

- [ ] **Step 3: Generate state for the explicit cutover date**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/scripts/generate_state.py --vault . --as-of 2026-08-28
```

Expected on the first run:

```text
catalog changed=yes
snapshot changed=yes
```

- [ ] **Step 4: Validate every JSONL record and cross-file fingerprint**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 - <<'PY'
import hashlib
import json
from pathlib import Path

catalog_path = Path("30 Sistema/Estado/catalog.jsonl")
snapshot_path = Path("30 Sistema/Estado/dashboard-snapshot.md")
catalog = catalog_path.read_bytes()
records = [json.loads(line) for line in catalog.decode("utf-8").splitlines()]
assert records[0]["record_type"] == "manifest"
assert sum(record["record_type"] == "manifest" for record in records) == 1
assert all(record["schema_version"] == 1 for record in records)
assert all(not Path(path).is_absolute() for record in records for path in [record.get("path"), record.get("source_path"), record.get("concept_path")] if path)
digest = "sha256:" + hashlib.sha256(catalog).hexdigest()
snapshot = snapshot_path.read_text(encoding="utf-8")
assert f'catalog_sha256: "{digest}"' in snapshot
assert "- [ ]" not in snapshot
print(f"records={len(records)} catalog_sha256={digest}")
PY
```

Expected: one line beginning `records=` and no assertion traceback.

- [ ] **Step 5: Verify idempotency on the real vault**

Run:

```bash
before_catalog=$(shasum -a 256 '30 Sistema/Estado/catalog.jsonl')
before_snapshot=$(shasum -a 256 '30 Sistema/Estado/dashboard-snapshot.md')
PYTHONPATH=.fgv/scripts python3 .fgv/scripts/generate_state.py --vault . --as-of 2026-08-28
after_catalog=$(shasum -a 256 '30 Sistema/Estado/catalog.jsonl')
after_snapshot=$(shasum -a 256 '30 Sistema/Estado/dashboard-snapshot.md')
test "$before_catalog" = "$after_catalog"
test "$before_snapshot" = "$after_snapshot"
```

Expected generator output:

```text
catalog changed=no
snapshot changed=no
```

All four hash comparisons exit zero.

- [ ] **Step 6: Inspect generated scope before committing**

Run:

```bash
git status --short
git diff --stat
git diff -- '30 Sistema/Estado/dashboard-snapshot.md'
```

Expected: only the two generated state files are new in this task. The snapshot contains no checkbox, no absolute path, no generated wall-clock timestamp and no content copied from academic notes beyond titles and task descriptions.

- [ ] **Step 7: Commit generated state**

```bash
git add '30 Sistema/Estado/catalog.jsonl' '30 Sistema/Estado/dashboard-snapshot.md'
git commit -m "feat: materialize academic dashboard state"
```

## Task 10: Prove fail-closed behavior and complete the handoff

**Files:**

- Modify only if a verification fails: `.fgv/scripts/fgv_state/*.py`, `.fgv/scripts/generate_state.py`, corresponding `.fgv/tests/test_*.py`
- Verify: `00 Home/Home.md`
- Verify: `30 Sistema/Estado/catalog.jsonl`
- Verify: `30 Sistema/Estado/dashboard-snapshot.md`

- [ ] **Step 1: Capture canonical and generated hashes**

Run:

```bash
home_hash=$(shasum -a 256 '00 Home/Home.md')
tasks_hash=$(shasum -a 256 '00 Home/Tasks.md')
catalog_hash=$(shasum -a 256 '30 Sistema/Estado/catalog.jsonl')
snapshot_hash=$(shasum -a 256 '30 Sistema/Estado/dashboard-snapshot.md')
```

Expected: all commands exit zero.

- [ ] **Step 2: Run check mode against the committed state**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 .fgv/scripts/generate_state.py --vault . --as-of 2026-08-28 --check
```

Expected:

```text
state fresh
```

Exit code is zero.

- [ ] **Step 3: Run the full verification suite**

Run:

```bash
PYTHONPATH=.fgv/scripts python3 -m unittest discover -s .fgv/tests -p 'test_*.py' -v
```

Expected: every test passes; final line is `OK`.

- [ ] **Step 4: Confirm the generator did not mutate canonical files**

Run:

```bash
test "$home_hash" = "$(shasum -a 256 '00 Home/Home.md')"
test "$tasks_hash" = "$(shasum -a 256 '00 Home/Tasks.md')"
test "$catalog_hash" = "$(shasum -a 256 '30 Sistema/Estado/catalog.jsonl')"
test "$snapshot_hash" = "$(shasum -a 256 '30 Sistema/Estado/dashboard-snapshot.md')"
```

Expected: all four comparisons exit zero.

- [ ] **Step 5: Verify no plugin runtime leaked into generated output**

Run:

```bash
! rg -n '```(dataview|tasks)|- \[ \]|generated_at|git_commit|/Users/|/root/' '30 Sistema/Estado/dashboard-snapshot.md' '30 Sistema/Estado/catalog.jsonl'
```

Expected: no matches and exit zero after shell negation.

- [ ] **Step 6: Verify clean incremental history**

Run:

```bash
git log --oneline -10
git status --short
```

Expected: separate commits exist for configuration, frontmatter, tasks, catalog, dashboard, atomic generation, determinism tests, Home/docs and generated state. Working tree is clean.

- [ ] **Step 7: Add a final fix commit only if verification required code changes**

If and only if Steps 2 through 6 exposed a defect, write a focused failing regression test, apply the smallest fix, rerun the complete suite, then commit only those files:

```bash
git add .fgv/scripts .fgv/tests
git commit -m "fix: enforce dashboard state contract"
```

If verification passed without changes, do not create an empty commit.

## Obsidian and Hermes handoff rules

- No committed `.obsidian` change is required for this subsystem.
- Add `00 Home/Home.md` to Obsidian Bookmarks through the UI. Core Bookmarks is already enabled.
- Open and pin Home in the local workspace. `.obsidian/workspace.json` remains ignored and device-specific.
- Tasks, Dataview and Bases may enrich the human Home later, but generated state and Hermes cannot depend on them.
- Hermes reads the manifest first, rejects schema major versions above one and streams remaining lines.
- Before Hermes edits a task, it reopens `00 Home/Tasks.md`, verifies `source_line_sha256`, then applies a minimal line patch. A mismatch aborts the write and triggers a fresh catalog read.
- If catalog or snapshot is missing, corrupt or cross-hash inconsistent, Hermes searches canonical files directly with filesystem tools.
- The scheduled generator has one active writer. Local runs use `--check` unless the scheduler is paused.
- A Git conflict in either generated file is never hand-merged. Resolve canonical inputs first and regenerate both outputs.
