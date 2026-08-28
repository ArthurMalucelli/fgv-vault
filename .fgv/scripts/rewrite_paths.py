#!/usr/bin/env python3
"""Rewrite the audited Plan B vault paths and Obsidian configuration."""

from __future__ import annotations

import argparse
import base64
from dataclasses import dataclass
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

from fgv_migration.inventory import InventoryError, normalize_relative_path
from fgv_migration.links import LinkAudit, audit_note_contents
from fgv_migration.rules import RuleError, validate_manifest
import rename_lesson_notes as lesson_renames


EXPECTED_MARKDOWN_OCCURRENCES = 59
EXPECTED_CONFIG_OCCURRENCES = 5
DIRECTORY_OPEN_FLAGS = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
FILE_OPEN_FLAGS = os.O_RDONLY | os.O_NOFOLLOW
TEMPORARY_OPEN_FLAGS = os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW
JOURNAL_NAME = "path-rewrite-journal.json"
JOURNAL_RELATIVE = f".fgv/{JOURNAL_NAME}"
JOURNAL_FIELDS = (
    "schema_version",
    "manifest_sha256",
    "completed_writes",
    "operations",
)
JOURNAL_OPERATION_FIELDS = (
    "path",
    "original_sha256",
    "output_sha256",
    "mode",
    "original_base64",
    "output_base64",
)
PRODUCTION_RECOVERY_COMMIT = "d766807e02e0e6b1f09122f4d3e8b7b75bf987be"

MARKDOWN_ALLOWLIST = (
    "00 Home/Home.md",
    "10 Matérias/Estatistica2/Aulas/08.17/AulaTestesHipoteseExcelR.md",
    "20 Conhecimento/Conceitos/Caso Marcus Dent.md",
    "20 Conhecimento/Conceitos/Caso Target Canada.md",
    "20 Conhecimento/Conceitos/Caso Zezinho Pipoqueiro.md",
    "30 Sistema/Automacoes/2026-05-25-weekly-summary-plan.md",
    "30 Sistema/Specs/2026-08-19-caso-marcus-dent-design.md",
    "30 Sistema/Specs/2026-08-19-caso-marcus-dent-plan.md",
    "30 Sistema/Tutor/README.md",
)

CONFIG_ALLOWLIST = (
    ".obsidian/app.json",
    ".obsidian/templates.json",
    ".obsidian/graph.json",
    ".obsidian/core-plugins.json",
    ".obsidian/daily-notes.json",
)

OLD_HOME_STRUCTURE = """```
~/FGV/
├── <Matéria>/            (matérias do semestre corrente)
│   └── Aulas/
│       └── MM.DD/
│           ├── Transcrito.md
│           └── Resumo.md
├── S1/                   (arquivo do semestre 2026.1, mesma estrutura)
└── Vault/
    ├── Index.md          (este arquivo)
    ├── Tasks.md          (lista de prazos consolidada, único arquivo de tasks)
    ├── Conceitos/        (notas atômicas: SELIC, Greenwashing, etc.)
    ├── Templates/        (templates de aula, resumo, conceito)
    ├── Attachments/      (imagens e arquivos colados)
    └── Daily/            (daily notes, se ativar)
```"""

NEW_HOME_STRUCTURE = """```
~/FGV/
├── 00 Home/
│   ├── Home.md
│   ├── Tasks.md
│   └── Daily/
├── 10 Matérias/
│   └── <Matéria>/
│       └── Aulas/MM.DD/
├── 20 Conhecimento/
│   └── Conceitos/
├── 30 Sistema/
│   ├── Automacoes/
│   ├── Estado/
│   ├── Specs/
│   ├── Templates/
│   ├── Tutor/
│   └── Anexos/
└── 90 Arquivo/
    └── 2026.1/
```"""


class RewriteError(ValueError):
    """The audited rewrite cannot be planned or committed safely."""


@dataclass(frozen=True)
class ManifestAuth:
    relative_path: str
    sha256: str
    record_count: int

    def __post_init__(self) -> None:
        try:
            normalized = normalize_relative_path(self.relative_path)
        except InventoryError as error:
            raise RewriteError("manifest auth path is invalid") from error
        if normalized != self.relative_path:
            raise RewriteError("manifest auth path must be canonical")
        if re.fullmatch(r"[0-9a-f]{64}", self.sha256) is None:
            raise RewriteError("manifest auth sha256 is invalid")
        if type(self.record_count) is not int or self.record_count <= 0:
            raise RewriteError("manifest auth record_count must be positive")


DEFAULT_MANIFEST_AUTH = ManifestAuth(
    relative_path="30 Sistema/Estado/migration-manifest.json",
    sha256="3910988998703f6a9cc01dcd4b40173241c602204ce4a4c6bc83a1a67fd29c96",
    record_count=1059,
)

LESSON_RENAME_MANIFEST_RELATIVE = (
    "30 Sistema/Estado/lesson-rename-manifest.json"
)
LESSON_RENAME_MANIFEST_SHA256 = (
    "8344e64f445e835a97cfbd51a07b943d9255d12d861c2b8e5d787d452a5dab45"
)
LESSON_RENAME_AUTHORITY_COMMIT = (
    "dc7a1cde627e2211fa7457367c160759e6ac7993"
)
LESSON_RENAME_AUTHORITY_TREE = (
    "1a8b7dd3abf7febbcb9d0b39d44d721e40ebe043"
)
LESSON_STRUCTURAL_SOURCE = re.compile(
    r"^10 Matérias/[^/]+/Aulas/\d{2}\.\d{2}/(?:Resumo|Transcrito)\.md$"
)


@dataclass(frozen=True)
class LessonRenameOverlayEntry:
    destination: str
    payload: bytes


@dataclass(frozen=True)
class RecoveryOperation:
    path: str
    original: bytes
    output: bytes
    mode: int

    def __post_init__(self) -> None:
        _validated_relative(self.path, "recovery operation path")
        if type(self.original) is not bytes or type(self.output) is not bytes:
            raise RewriteError("recovery operation bytes must be exact bytes")
        if type(self.mode) is not int or self.mode < 0 or self.mode > 0o7777:
            raise RewriteError("recovery operation mode is invalid")


@dataclass(frozen=True)
class RecoveryPlan:
    manifest_auth: ManifestAuth
    operations: tuple[RecoveryOperation, ...]

    def __post_init__(self) -> None:
        if type(self.manifest_auth) is not ManifestAuth:
            raise RewriteError("recovery plan manifest authority is invalid")
        if type(self.operations) is not tuple or not self.operations:
            raise RewriteError("recovery plan operations must be a non-empty tuple")
        paths = [operation.path for operation in self.operations]
        if paths != sorted(paths, key=lambda value: value.encode("utf-8")):
            raise RewriteError("recovery plan operations are not canonically ordered")
        if len(paths) != len(set(paths)):
            raise RewriteError("recovery plan operations contain duplicate paths")


@dataclass(frozen=True)
class LinkContract:
    expected_total: int | None
    max_unresolved: int
    max_ambiguous: int

    def __post_init__(self) -> None:
        values = (self.max_unresolved, self.max_ambiguous)
        if any(type(value) is not int or value < 0 for value in values):
            raise RewriteError("link limits must be non-negative integers")
        if self.expected_total is not None and (
            type(self.expected_total) is not int or self.expected_total < 0
        ):
            raise RewriteError("expected link total must be non-negative")


DEFAULT_LINK_CONTRACT = LinkContract(
    expected_total=5402,
    max_unresolved=408,
    max_ambiguous=3,
)


@dataclass(frozen=True)
class LiteralRewrite:
    source: str
    destination: str
    expected_count: int
    manifest_backed: bool = True

    def __post_init__(self) -> None:
        if not self.source or not self.destination or self.source == self.destination:
            raise RewriteError("literal rewrite must have distinct non-empty values")
        if type(self.expected_count) is not int or self.expected_count <= 0:
            raise RewriteError("literal rewrite expected_count must be positive")
        for label, value in (("source", self.source), ("destination", self.destination)):
            if unicodedata.normalize("NFC", value) != value:
                raise RewriteError(f"literal rewrite {label} must be NFC")


@dataclass(frozen=True)
class RewriteReport:
    status: str
    occurrences: int
    files_changed: int
    links: LinkAudit | None = None


@dataclass
class OpenOperation:
    relative: str
    parent_fd: int
    parent_device: int
    parent_inode: int
    name: str
    original: bytes
    output: bytes
    mode: int

    def close(self) -> None:
        if self.parent_fd >= 0:
            os.close(self.parent_fd)
            self.parent_fd = -1


MARKDOWN_SPECS: Mapping[str, tuple[LiteralRewrite, ...]] = {
    "00 Home/Home.md": (
        LiteralRewrite(OLD_HOME_STRUCTURE, NEW_HOME_STRUCTURE, 1, False),
        LiteralRewrite("Vault/Conceitos", "20 Conhecimento/Conceitos", 1),
    ),
    "10 Matérias/Estatistica2/Aulas/08.17/AulaTestesHipoteseExcelR.md": (
        LiteralRewrite(
            "cd ~/FGV/Estatistica2/Aulas",
            "cd ~/FGV/10\\ Matérias/Estatistica2/Aulas",
            1,
            False,
        ),
        LiteralRewrite(
            "~/FGV/Estatistica2/Aulas",
            "~/FGV/10 Matérias/Estatistica2/Aulas",
            1,
        ),
    ),
    "20 Conhecimento/Conceitos/Caso Marcus Dent.md": (
        LiteralRewrite(
            "ContabilidadeFinanceira/Aulas",
            "10 Matérias/ContabilidadeFinanceira/Aulas",
            1,
        ),
    ),
    "20 Conhecimento/Conceitos/Caso Target Canada.md": (
        LiteralRewrite(
            "TecnologiaDadosNegocios/Aulas",
            "10 Matérias/TecnologiaDadosNegocios/Aulas",
            1,
        ),
    ),
    "20 Conhecimento/Conceitos/Caso Zezinho Pipoqueiro.md": (
        LiteralRewrite(
            "ContabilidadeFinanceira/Aulas",
            "10 Matérias/ContabilidadeFinanceira/Aulas",
            1,
        ),
    ),
    "30 Sistema/Automacoes/2026-05-25-weekly-summary-plan.md": (
        LiteralRewrite(
            "ls -la ~/FGV/Vault/automation/",
            "ls -la ~/FGV/30\\ Sistema/Automacoes/",
            1,
            False,
        ),
        LiteralRewrite(
            "~/FGV/Vault/automation/",
            "~/FGV/30 Sistema/Automacoes/",
            10,
        ),
    ),
    "30 Sistema/Specs/2026-08-19-caso-marcus-dent-design.md": (
        LiteralRewrite(
            "ContabilidadeFinanceira/Aulas",
            "10 Matérias/ContabilidadeFinanceira/Aulas",
            2,
        ),
        LiteralRewrite("Vault/Templates", "30 Sistema/Templates", 1),
    ),
    "30 Sistema/Specs/2026-08-19-caso-marcus-dent-plan.md": (
        LiteralRewrite(
            "AULA=$VAULT/ContabilidadeFinanceira/Aulas/08.19",
            'AULA="$VAULT/10 Matérias/ContabilidadeFinanceira/Aulas/08.19"',
            1,
            False,
        ),
        LiteralRewrite(
            "~/FGV/Vault/Specs/", "~/FGV/30 Sistema/Specs/", 1
        ),
        LiteralRewrite("Vault/Conceitos", "20 Conhecimento/Conceitos", 26),
        LiteralRewrite("Vault/Templates", "30 Sistema/Templates", 1),
        LiteralRewrite("Vault/Specs", "30 Sistema/Specs", 1),
        LiteralRewrite(
            "ContabilidadeFinanceira/Aulas",
            "10 Matérias/ContabilidadeFinanceira/Aulas",
            7,
        ),
    ),
    "30 Sistema/Tutor/README.md": (
        LiteralRewrite("Vault/Tutor", "30 Sistema/Tutor", 1),
    ),
}

URL_PATTERN = re.compile(
    r"(?<![A-Za-z0-9+.-])[A-Za-z][A-Za-z0-9+.-]*:[^\s<>\])}]+",
    re.IGNORECASE,
)
OLD_ACTIVE_PATTERN = re.compile(
    r"~/FGV/Vault/"
    r"|Vault/(?:Conceitos|Templates|Specs|Tutor|automation)"
    r"|~/FGV/Estatistica2/Aulas"
    r"|(?<!10 Matérias/)ContabilidadeFinanceira/Aulas"
    r"|(?<!10 Matérias/)TecnologiaDadosNegocios/Aulas"
    r"|^└── Vault/$",
    re.MULTILINE,
)


def _ordered_rules(rules: Sequence[LiteralRewrite], *, inverse: bool = False):
    attribute = "destination" if inverse else "source"
    return tuple(
        sorted(
            rules,
            key=lambda rule: (
                -len(getattr(rule, attribute)),
                getattr(rule, attribute).encode("utf-8"),
            ),
        )
    )


def _is_word_character(character: str) -> bool:
    return character == "_" or character.isalnum()


def _eligible_spans(
    text: str, literal: str, *, exclude_within: str | None = None
) -> list[tuple[int, int]]:
    url_spans = [(match.start(), match.end()) for match in URL_PATTERN.finditer(text)]
    excluded_spans: list[tuple[int, int]] = []
    if exclude_within and exclude_within != literal:
        excluded_spans = _eligible_spans(text, exclude_within)
    spans: list[tuple[int, int]] = []
    cursor = 0
    while True:
        start = text.find(literal, cursor)
        if start < 0:
            break
        end = start + len(literal)
        cursor = end
        if any(url_start <= start < url_end for url_start, url_end in url_spans):
            continue
        if any(
            excluded_start <= start and end <= excluded_end
            for excluded_start, excluded_end in excluded_spans
        ):
            continue
        if literal[0].isalnum() and start and _is_word_character(text[start - 1]):
            continue
        if literal[-1].isalnum() and end < len(text) and _is_word_character(text[end]):
            continue
        spans.append((start, end))
    return spans


def _replace_literal(
    text: str,
    source: str,
    destination: str,
    *,
    exclude_within: str | None = None,
) -> tuple[str, int]:
    spans = _eligible_spans(text, source, exclude_within=exclude_within)
    if not spans:
        return text, 0
    pieces: list[str] = []
    cursor = 0
    for start, end in spans:
        pieces.append(text[cursor:start])
        pieces.append(destination)
        cursor = end
    pieces.append(text[cursor:])
    return "".join(pieces), len(spans)


def _simulate_rewrites(
    text: str, rules: Sequence[LiteralRewrite], *, inverse: bool = False
) -> str:
    result = text
    for rule in _ordered_rules(rules, inverse=inverse):
        source = rule.destination if inverse else rule.source
        destination = rule.source if inverse else rule.destination
        result, count = _replace_literal(
            result,
            source,
            destination,
            exclude_within=destination,
        )
        if count != rule.expected_count:
            direction = "fresh" if inverse else "stale"
            raise RewriteError(
                f"{direction} literal count diverged for {source!r}: "
                f"expected {rule.expected_count}, found {count}"
            )
    return result


def rewrite_markdown_text(
    text: str, rules: Sequence[LiteralRewrite]
) -> tuple[str, int]:
    """Apply one exact, URL-safe set of longest-first Markdown rewrites."""
    if type(text) is not str:
        raise RewriteError("Markdown content must be text")
    output = _simulate_rewrites(text, rules)
    return output, sum(rule.expected_count for rule in rules)


def _classify_markdown_state(
    text: str, rules: Sequence[LiteralRewrite], relative: str
) -> tuple[str, str]:
    stale_output: str | None = None
    fresh_source: str | None = None
    try:
        stale_output = _simulate_rewrites(text, rules)
        if _simulate_rewrites(stale_output, rules, inverse=True) != text:
            stale_output = None
    except RewriteError:
        pass
    try:
        fresh_source = _simulate_rewrites(text, rules, inverse=True)
        if _simulate_rewrites(fresh_source, rules) != text:
            fresh_source = None
    except RewriteError:
        pass
    if stale_output is not None and fresh_source is None:
        return "stale", stale_output
    if fresh_source is not None and stale_output is None:
        return "fresh", text
    raise RewriteError(f"Markdown file is partial or unexpected: {relative!r}")


def _safe_relative_path(vault: Path, relative: str) -> Path:
    try:
        normalized = normalize_relative_path(relative)
    except (InventoryError, TypeError) as error:
        raise RewriteError(f"allowlisted path must be relative NFC: {relative!r}") from error
    if type(relative) is not str or normalized != relative:
        raise RewriteError(f"allowlisted path must be relative NFC: {relative!r}")
    pure = PurePosixPath(relative)
    if pure.is_absolute() or ".." in pure.parts:
        raise RewriteError(f"unsafe allowlisted path: {relative!r}")
    path = vault.joinpath(*pure.parts)
    cursor = vault
    for part in pure.parts:
        cursor = cursor / part
        if cursor.is_symlink():
            raise RewriteError(f"symlink is not allowed in rewrite path: {relative!r}")
    if not path.is_file():
        raise RewriteError(f"allowlisted file is missing: {relative!r}")
    return path


def _validated_relative(relative: str, label: str) -> str:
    try:
        normalized = normalize_relative_path(relative)
    except (InventoryError, TypeError) as error:
        raise RewriteError(f"{label} must be a canonical relative path") from error
    if normalized != relative:
        raise RewriteError(f"{label} must be a canonical relative path")
    return relative


def _open_existing_directory(parent_fd: int, name: str, label: str) -> int:
    try:
        metadata = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
    except FileNotFoundError as error:
        raise RewriteError(f"{label} is missing") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise RewriteError(f"{label} is not a regular directory")
    try:
        return os.open(name, DIRECTORY_OPEN_FLAGS, dir_fd=parent_fd)
    except OSError as error:
        raise RewriteError(f"cannot securely open {label}: {error}") from error


def _open_parent(root_fd: int, relative: str) -> tuple[int, str]:
    relative = _validated_relative(relative, "path")
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


def _read_file_at(parent_fd: int, name: str, label: str) -> tuple[bytes, int]:
    file_fd: int | None = None
    try:
        metadata = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
            raise RewriteError(f"{label} is not a regular non-symlink file")
        file_fd = os.open(name, FILE_OPEN_FLAGS, dir_fd=parent_fd)
        opened = os.fstat(file_fd)
        if not stat.S_ISREG(opened.st_mode):
            raise RewriteError(f"{label} is not a regular file")
        chunks: list[bytes] = []
        total = 0
        while True:
            chunk = os.read(file_fd, 1024 * 1024)
            if not chunk:
                break
            total += len(chunk)
            if total > 64 * 1024 * 1024:
                raise RewriteError(f"{label} exceeds 64 MiB")
            chunks.append(chunk)
        after = os.fstat(file_fd)
        if (opened.st_dev, opened.st_ino, opened.st_size) != (
            after.st_dev,
            after.st_ino,
            after.st_size,
        ):
            raise RewriteError(f"{label} changed while being read")
        return b"".join(chunks), stat.S_IMODE(opened.st_mode)
    except OSError as error:
        raise RewriteError(f"cannot securely read {label}: {error}") from error
    finally:
        if file_fd is not None:
            os.close(file_fd)


def _secure_read(root_fd: int, relative: str) -> bytes:
    return _secure_read_with_mode(root_fd, relative)[0]


def _secure_read_with_mode(root_fd: int, relative: str) -> tuple[bytes, int]:
    parent_fd, name = _open_parent(root_fd, relative)
    try:
        return _read_file_at(parent_fd, name, relative)
    finally:
        os.close(parent_fd)


def _secure_optional_read_with_mode(
    root_fd: int, relative: str
) -> tuple[bytes, int] | None:
    parent_fd, name = _open_parent(root_fd, relative)
    try:
        try:
            os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        except FileNotFoundError:
            return None
        return _read_file_at(parent_fd, name, relative)
    finally:
        os.close(parent_fd)


def _secure_is_file(root_fd: int, relative: str) -> bool:
    try:
        parent_fd, name = _open_parent(root_fd, relative)
    except RewriteError:
        return False
    try:
        metadata = os.stat(name, dir_fd=parent_fd, follow_symlinks=False)
        return stat.S_ISREG(metadata.st_mode) and not stat.S_ISLNK(metadata.st_mode)
    except FileNotFoundError:
        return False
    finally:
        os.close(parent_fd)


def _load_manifest(
    root_fd: int,
    manifest_path: Path,
    auth: ManifestAuth,
) -> list[dict[str, object]]:
    raw_path = manifest_path.as_posix()
    if manifest_path.is_absolute() or raw_path != auth.relative_path:
        raise RewriteError(
            f"manifest path must be exactly {auth.relative_path!r}"
        )
    payload = _secure_read(root_fd, auth.relative_path)
    digest = hashlib.sha256(payload).hexdigest()
    if digest != auth.sha256:
        raise RewriteError(
            f"manifest sha256 mismatch: {digest} != {auth.sha256}"
        )
    try:
        manifest = json.loads(payload)
        validate_manifest(manifest)
    except (
        OSError,
        UnicodeDecodeError,
        json.JSONDecodeError,
        InventoryError,
        RuleError,
        ValueError,
    ) as error:
        raise RewriteError(f"invalid migration manifest: {error}") from error
    if len(manifest) != auth.record_count:
        raise RewriteError(
            f"manifest record count mismatch: {len(manifest)} != {auth.record_count}"
        )
    return manifest


def _manifest_literal_prefix(value: str) -> str:
    prefix = "~/FGV/"
    return value[len(prefix) :] if value.startswith(prefix) else value


def _verify_manifest_backing(
    manifest: Sequence[Mapping[str, object]],
    specs: Mapping[str, Sequence[LiteralRewrite]],
) -> None:
    checked: set[tuple[str, str]] = set()
    for rules in specs.values():
        for rule in rules:
            if not rule.manifest_backed:
                continue
            source_root = _manifest_literal_prefix(rule.source).rstrip("/")
            destination_root = _manifest_literal_prefix(rule.destination).rstrip("/")
            pair = (source_root, destination_root)
            if pair in checked:
                continue
            checked.add(pair)
            matches = [
                record
                for record in manifest
                if str(record["source"]) == source_root
                or str(record["source"]).startswith(source_root + "/")
            ]
            if not matches:
                raise RewriteError(f"literal source prefix absent from manifest: {source_root!r}")
            supported = []
            for record in matches:
                source = str(record["source"])
                expected = destination_root + source[len(source_root) :]
                if record["destination"] == expected:
                    supported.append(source)
            if not supported:
                raise RewriteError(
                    f"manifest does not support rewrite {source_root!r} -> "
                    f"{destination_root!r}"
                )


def _read_utf8(path: Path, relative: str) -> tuple[bytes, str]:
    try:
        payload = path.read_bytes()
        text = payload.decode("utf-8")
    except (OSError, UnicodeDecodeError) as error:
        raise RewriteError(f"cannot read UTF-8 file {relative!r}: {error}") from error
    return payload, text


def _load_json(path: Path, relative: str) -> tuple[bytes, dict[str, object]]:
    payload, text = _read_utf8(path, relative)
    try:
        value = json.loads(text)
    except json.JSONDecodeError as error:
        raise RewriteError(f"invalid JSON in {relative!r}: {error}") from error
    if type(value) is not dict:
        raise RewriteError(f"JSON root must be an object: {relative!r}")
    return payload, value


def _json_bytes(value: object) -> bytes:
    return (json.dumps(value, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _replace_config_value(
    relative: str,
    value: object,
    old: object,
    final: object,
) -> str:
    if type(value) is type(old) and value == old:
        return "stale"
    if type(value) is type(final) and value == final:
        return "fresh"
    raise RewriteError(f"config value is partial or unexpected in {relative!r}")


def _plan_config(
    daily_template_exists: bool, relative: str, value: dict[str, object]
) -> tuple[str, bytes, int]:
    output = json.loads(json.dumps(value, ensure_ascii=False))
    if relative == ".obsidian/app.json":
        if output.get("alwaysUpdateLinks") is not True:
            raise RewriteError("app.json must keep alwaysUpdateLinks true")
        state = _replace_config_value(
            relative,
            output.get("attachmentFolderPath"),
            "Vault/Attachments",
            "30 Sistema/Anexos",
        )
        output["attachmentFolderPath"] = "30 Sistema/Anexos"
        return state, _json_bytes(output), 1

    if relative == ".obsidian/templates.json":
        state = _replace_config_value(
            relative, output.get("folder"), "Vault/Templates", "30 Sistema/Templates"
        )
        output["folder"] = "30 Sistema/Templates"
        return state, _json_bytes(output), 1

    if relative == ".obsidian/graph.json":
        groups = output.get("colorGroups")
        if type(groups) is not list:
            raise RewriteError("graph.json colorGroups must be an array")
        old = "path:Vault/Conceitos"
        final = "path:20 Conhecimento/Conceitos"
        old_groups = [group for group in groups if type(group) is dict and group.get("query") == old]
        final_groups = [group for group in groups if type(group) is dict and group.get("query") == final]
        if len(old_groups) == 1 and not final_groups:
            state = "stale"
            old_groups[0]["query"] = final
        elif not old_groups and len(final_groups) == 1:
            state = "fresh"
        else:
            raise RewriteError("graph.json concept group is partial or unexpected")
        return state, _json_bytes(output), 1

    if relative == ".obsidian/core-plugins.json":
        state = _replace_config_value(
            relative, output.get("daily-notes"), True, False
        )
        output["daily-notes"] = False
        return state, _json_bytes(output), 0

    if relative == ".obsidian/daily-notes.json":
        if output.get("autorun") is not False:
            raise RewriteError("daily-notes.json autorun must remain false")
        final_template = (
            "30 Sistema/Templates/Daily.md"
            if daily_template_exists
            else ""
        )
        current = (output.get("folder"), output.get("template"))
        old = ("Vault/Daily", "Vault/Templates/Daily.md")
        final = ("00 Home/Daily", final_template)
        state = _replace_config_value(relative, current, old, final)
        output["folder"] = final[0]
        output["template"] = final[1]
        return state, _json_bytes(output), 2

    raise RewriteError(f"config file is not allowlisted: {relative!r}")


def _trusted_git(vault: Path, arguments: Sequence[str]) -> bytes:
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    environment["GIT_CONFIG_NOSYSTEM"] = "1"
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    environment["LC_ALL"] = "C"
    try:
        result = subprocess.run(
            ("git", *arguments),
            cwd=vault,
            env=environment,
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )
    except OSError as error:
        raise RewriteError(f"cannot execute Git recovery authority: {error}") from error
    if result.returncode != 0:
        detail = result.stderr.decode("utf-8", errors="replace").strip()
        raise RewriteError(
            f"Git recovery authority failed ({' '.join(arguments)}): {detail}"
        )
    return result.stdout


def _production_recovery_plan(
    vault: Path,
    manifest_auth: ManifestAuth,
    specs: Mapping[str, Sequence[LiteralRewrite]],
) -> RecoveryPlan:
    resolved = _trusted_git(
        vault,
        (
            "rev-parse",
            "--verify",
            "--end-of-options",
            f"{PRODUCTION_RECOVERY_COMMIT}^{{commit}}",
        ),
    ).decode("ascii").strip()
    if resolved != PRODUCTION_RECOVERY_COMMIT:
        raise RewriteError("pinned recovery authority commit did not resolve exactly")

    expected_paths = set(specs) | set(CONFIG_ALLOWLIST)
    daily_template = "30 Sistema/Templates/Daily.md"
    listing = _trusted_git(
        vault,
        ("ls-tree", "-rz", "--full-tree", PRODUCTION_RECOVERY_COMMIT),
    )
    tree: dict[str, tuple[str, str]] = {}
    daily_template_exists = False
    for record in listing.split(b"\0"):
        if not record:
            continue
        try:
            metadata, raw_path = record.split(b"\t", 1)
            raw_mode, object_type, raw_oid = metadata.split(b" ", 2)
            relative = raw_path.decode("utf-8", errors="strict")
            mode = raw_mode.decode("ascii")
            oid = raw_oid.decode("ascii")
        except (UnicodeDecodeError, ValueError) as error:
            raise RewriteError("Git recovery authority tree is invalid") from error
        if relative == daily_template:
            daily_template_exists = True
        if relative not in expected_paths:
            continue
        if object_type != b"blob" or mode not in {"100644", "100755"}:
            raise RewriteError(
                f"Git recovery authority path is not a regular blob: {relative!r}"
            )
        tree[relative] = (oid, mode)
    if set(tree) != expected_paths:
        missing = sorted(expected_paths.difference(tree), key=lambda value: value.encode())
        raise RewriteError(f"Git recovery authority is missing paths: {missing!r}")

    trusted: list[RecoveryOperation] = []
    for relative in sorted(expected_paths, key=lambda value: value.encode("utf-8")):
        oid, git_mode = tree[relative]
        original = _trusted_git(vault, ("cat-file", "blob", oid))
        if relative in specs:
            try:
                text = original.decode("utf-8")
            except UnicodeDecodeError as error:
                raise RewriteError(
                    f"Git recovery authority is not UTF-8: {relative!r}"
                ) from error
            state, rewritten = _classify_markdown_state(
                text,
                specs[relative],
                relative,
            )
            output = rewritten.encode("utf-8")
        else:
            try:
                value = json.loads(original.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise RewriteError(
                    f"Git recovery authority config is invalid: {relative!r}"
                ) from error
            state, output, _ = _plan_config(
                daily_template_exists,
                relative,
                value,
            )
        if state != "stale" or output == original:
            raise RewriteError(
                f"Git recovery authority is not the stale canonical source: {relative!r}"
            )
        trusted.append(
            RecoveryOperation(
                path=relative,
                original=original,
                output=output,
                mode=0o755 if git_mode == "100755" else 0o644,
            )
        )
    return RecoveryPlan(manifest_auth=manifest_auth, operations=tuple(trusted))


def _open_operation(root_fd: int, relative: str) -> OpenOperation:
    parent_fd, name = _open_parent(root_fd, relative)
    try:
        payload, mode = _read_file_at(parent_fd, name, relative)
        parent = os.fstat(parent_fd)
        return OpenOperation(
            relative=relative,
            parent_fd=parent_fd,
            parent_device=parent.st_dev,
            parent_inode=parent.st_ino,
            name=name,
            original=payload,
            output=payload,
            mode=mode,
        )
    except BaseException:
        os.close(parent_fd)
        raise


def _validate_parent_anchor(root_fd: int, operation: OpenOperation) -> None:
    current_fd, _ = _open_parent(root_fd, operation.relative)
    try:
        current = os.fstat(current_fd)
        if (current.st_dev, current.st_ino) != (
            operation.parent_device,
            operation.parent_inode,
        ):
            raise RewriteError(
                f"parent changed after preflight: {operation.relative!r}"
            )
    finally:
        os.close(current_fd)


def _temporary_write(parent_fd: int, name: str, payload: bytes, mode: int) -> str:
    temporary_name = ""
    descriptor: int | None = None
    try:
        for _ in range(100):
            candidate = f".{name}.rewrite.{secrets.token_hex(8)}.tmp"
            try:
                descriptor = os.open(
                    candidate,
                    TEMPORARY_OPEN_FLAGS,
                    mode,
                    dir_fd=parent_fd,
                )
            except FileExistsError:
                continue
            temporary_name = candidate
            break
        if descriptor is None:
            raise RewriteError("cannot allocate atomic rewrite temporary file")
        stream = os.fdopen(descriptor, "wb")
        descriptor = None
        with stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        result = temporary_name
        temporary_name = ""
        return result
    finally:
        if descriptor is not None:
            os.close(descriptor)
        if temporary_name:
            try:
                os.unlink(temporary_name, dir_fd=parent_fd)
            except FileNotFoundError:
                pass


def _atomic_write_at(operation: OpenOperation, payload: bytes) -> None:
    temporary = _temporary_write(
        operation.parent_fd,
        operation.name,
        payload,
        operation.mode,
    )
    try:
        os.replace(
            temporary,
            operation.name,
            src_dir_fd=operation.parent_fd,
            dst_dir_fd=operation.parent_fd,
        )
        temporary = ""
        os.fsync(operation.parent_fd)
    finally:
        if temporary:
            try:
                os.unlink(temporary, dir_fd=operation.parent_fd)
            except FileNotFoundError:
                pass


def _open_journal_directory(root_fd: int) -> int:
    directory_fd = _open_existing_directory(root_fd, ".fgv", ".fgv")
    try:
        fcntl.flock(directory_fd, fcntl.LOCK_EX | fcntl.LOCK_NB)
    except OSError as error:
        os.close(directory_fd)
        raise RewriteError(f"another path rewriter holds the .fgv lock: {error}") from error
    return directory_fd


def _validate_recovery_plan(
    plan: RecoveryPlan,
    manifest_auth: ManifestAuth,
    expected_paths: Sequence[str],
) -> None:
    if type(plan) is not RecoveryPlan or plan.manifest_auth != manifest_auth:
        raise RewriteError("recovery plan manifest authority mismatch")
    canonical_paths = sorted(expected_paths, key=lambda value: value.encode("utf-8"))
    if [operation.path for operation in plan.operations] != canonical_paths:
        raise RewriteError("recovery plan scope mismatch")


def _authenticate_open_plan(
    operations: Sequence[OpenOperation],
    plan: RecoveryPlan,
) -> None:
    trusted = plan.operations
    if len(operations) != len(trusted):
        raise RewriteError("planned rewrite operation count is not authenticated")
    for operation, authority in zip(operations, trusted):
        if (
            operation.relative != authority.path
            or operation.original != authority.original
            or operation.output != authority.output
            or operation.mode != authority.mode
        ):
            raise RewriteError(
                f"planned rewrite operation is not authenticated: {operation.relative!r}"
            )


def _authenticate_journal_plan(
    record: Mapping[str, object],
    plan: RecoveryPlan,
) -> None:
    if record["manifest_sha256"] != plan.manifest_auth.sha256:
        raise RewriteError("CRITICAL recovery journal manifest authority mismatch")
    raw_operations = list(record["operations"])
    if len(raw_operations) != len(plan.operations):
        raise RewriteError("CRITICAL recovery journal operation count mismatch")
    for raw, authority in zip(raw_operations, plan.operations):
        original = base64.b64decode(str(raw["original_base64"]), validate=True)
        output = base64.b64decode(str(raw["output_base64"]), validate=True)
        if (
            raw["path"] != authority.path
            or original != authority.original
            or output != authority.output
            or raw["original_sha256"]
            != hashlib.sha256(authority.original).hexdigest()
            or raw["output_sha256"] != hashlib.sha256(authority.output).hexdigest()
            or raw["mode"] != authority.mode
        ):
            raise RewriteError(
                f"CRITICAL recovery journal plan is not authenticated: "
                f"{raw['path']!r}"
            )


def _operation_record(operation: OpenOperation) -> dict[str, object]:
    return dict(
        zip(
            JOURNAL_OPERATION_FIELDS,
            (
                operation.relative,
                hashlib.sha256(operation.original).hexdigest(),
                hashlib.sha256(operation.output).hexdigest(),
                operation.mode,
                base64.b64encode(operation.original).decode("ascii"),
                base64.b64encode(operation.output).decode("ascii"),
            ),
        )
    )


def _journal_payload(
    manifest_sha256: str,
    operations: Sequence[OpenOperation],
    completed_writes: int,
) -> bytes:
    record = dict(
        zip(
            JOURNAL_FIELDS,
            (
                1,
                manifest_sha256,
                completed_writes,
                [_operation_record(operation) for operation in operations],
            ),
        )
    )
    return (json.dumps(record, ensure_ascii=False, indent=2) + "\n").encode("utf-8")


def _install_journal(
    journal_fd: int,
    manifest_sha256: str,
    operations: Sequence[OpenOperation],
) -> None:
    try:
        os.stat(JOURNAL_NAME, dir_fd=journal_fd, follow_symlinks=False)
    except FileNotFoundError:
        pass
    else:
        raise RewriteError("CRITICAL path rewrite journal already exists")
    temporary = _temporary_write(
        journal_fd,
        JOURNAL_NAME,
        _journal_payload(manifest_sha256, operations, 0),
        0o600,
    )
    try:
        os.link(
            temporary,
            JOURNAL_NAME,
            src_dir_fd=journal_fd,
            dst_dir_fd=journal_fd,
            follow_symlinks=False,
        )
        os.unlink(temporary, dir_fd=journal_fd)
        temporary = ""
        os.fsync(journal_fd)
    except FileExistsError as error:
        raise RewriteError("CRITICAL path rewrite journal appeared concurrently") from error
    finally:
        if temporary:
            try:
                os.unlink(temporary, dir_fd=journal_fd)
            except FileNotFoundError:
                pass


def _checkpoint_journal(
    journal_fd: int,
    manifest_sha256: str,
    operations: Sequence[OpenOperation],
    completed_writes: int,
) -> None:
    _replace_journal_payload(
        journal_fd,
        _journal_payload(manifest_sha256, operations, completed_writes),
    )


def _replace_journal_payload(journal_fd: int, payload: bytes) -> None:
    metadata = os.stat(JOURNAL_NAME, dir_fd=journal_fd, follow_symlinks=False)
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise RewriteError("CRITICAL path rewrite journal changed")
    temporary = _temporary_write(
        journal_fd,
        JOURNAL_NAME,
        payload,
        0o600,
    )
    try:
        os.replace(
            temporary,
            JOURNAL_NAME,
            src_dir_fd=journal_fd,
            dst_dir_fd=journal_fd,
        )
        temporary = ""
        os.fsync(journal_fd)
    finally:
        if temporary:
            try:
                os.unlink(temporary, dir_fd=journal_fd)
            except FileNotFoundError:
                pass


def _checkpoint_recovery_journal(
    journal_fd: int,
    record: Mapping[str, object],
    completed_writes: int,
) -> None:
    updated = dict(record)
    updated["completed_writes"] = completed_writes
    payload = (json.dumps(updated, ensure_ascii=False, indent=2) + "\n").encode(
        "utf-8"
    )
    _replace_journal_payload(journal_fd, payload)


def _delete_journal(journal_fd: int) -> None:
    metadata = os.stat(JOURNAL_NAME, dir_fd=journal_fd, follow_symlinks=False)
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISREG(metadata.st_mode):
        raise RewriteError("CRITICAL path rewrite journal changed before deletion")
    os.unlink(JOURNAL_NAME, dir_fd=journal_fd)
    os.fsync(journal_fd)


def _read_journal(journal_fd: int) -> dict[str, object] | None:
    try:
        payload, _ = _read_file_at(journal_fd, JOURNAL_NAME, "path rewrite journal")
    except RewriteError as error:
        if "cannot securely read" in str(error) and "No such file" in str(error):
            return None
        try:
            os.stat(JOURNAL_NAME, dir_fd=journal_fd, follow_symlinks=False)
        except FileNotFoundError:
            os.fsync(journal_fd)
            return None
        raise
    try:
        record = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise RewriteError(f"CRITICAL invalid path rewrite journal: {error}") from error
    if type(record) is not dict or tuple(record) != JOURNAL_FIELDS:
        raise RewriteError("CRITICAL invalid path rewrite journal schema")
    if type(record["schema_version"]) is not int or record["schema_version"] != 1:
        raise RewriteError("CRITICAL invalid path rewrite journal version")
    if type(record["manifest_sha256"]) is not str:
        raise RewriteError("CRITICAL invalid path rewrite journal manifest hash")
    completed = record["completed_writes"]
    raw_operations = record["operations"]
    if (
        type(completed) is not int
        or completed < 0
        or type(raw_operations) is not list
        or completed > len(raw_operations)
    ):
        raise RewriteError("CRITICAL invalid path rewrite journal counts")
    for raw in raw_operations:
        if type(raw) is not dict or tuple(raw) != JOURNAL_OPERATION_FIELDS:
            raise RewriteError("CRITICAL invalid path rewrite journal operation")
        if (
            type(raw["path"]) is not str
            or type(raw["original_sha256"]) is not str
            or type(raw["output_sha256"]) is not str
            or type(raw["mode"]) is not int
            or type(raw["original_base64"]) is not str
            or type(raw["output_base64"]) is not str
        ):
            raise RewriteError("CRITICAL invalid path rewrite journal operation types")
        if (
            re.fullmatch(r"[0-9a-f]{64}", raw["original_sha256"]) is None
            or re.fullmatch(r"[0-9a-f]{64}", raw["output_sha256"]) is None
            or raw["mode"] < 0
            or raw["mode"] > 0o7777
        ):
            raise RewriteError("CRITICAL invalid path rewrite journal operation values")
        _validated_relative(raw["path"], "journal path")
        try:
            original = base64.b64decode(raw["original_base64"], validate=True)
            output = base64.b64decode(raw["output_base64"], validate=True)
        except (ValueError, TypeError) as error:
            raise RewriteError("CRITICAL invalid journal operation bytes") from error
        if hashlib.sha256(original).hexdigest() != raw["original_sha256"]:
            raise RewriteError("CRITICAL journal original hash mismatch")
        if hashlib.sha256(output).hexdigest() != raw["output_sha256"]:
            raise RewriteError("CRITICAL journal output hash mismatch")
    return record


def _journal_operation_open(root_fd: int, raw: Mapping[str, object]) -> OpenOperation:
    operation = _open_operation(root_fd, str(raw["path"]))
    operation.original = base64.b64decode(str(raw["original_base64"]), validate=True)
    operation.output = base64.b64decode(str(raw["output_base64"]), validate=True)
    operation.mode = int(raw["mode"])
    return operation


def _recover_journal(
    root_fd: int,
    journal_fd: int,
    record: Mapping[str, object],
    plan: RecoveryPlan,
) -> None:
    _authenticate_journal_plan(record, plan)
    raw_operations = list(record["operations"])
    paths = [str(raw["path"]) for raw in raw_operations]
    expected_paths = [operation.path for operation in plan.operations]
    if len(paths) != len(set(paths)) or paths != expected_paths:
        raise RewriteError("CRITICAL recovery journal scope mismatch")
    operations: list[OpenOperation] = []
    states: list[str] = []
    try:
        for raw in raw_operations:
            operation = _journal_operation_open(root_fd, raw)
            operations.append(operation)
            current_hash = hashlib.sha256(
                _read_file_at(operation.parent_fd, operation.name, operation.relative)[0]
            ).hexdigest()
            if current_hash == raw["output_sha256"]:
                states.append("output")
            elif current_hash == raw["original_sha256"]:
                states.append("original")
            else:
                raise RewriteError(
                    f"CRITICAL recovery file has unknown bytes: {operation.relative!r}"
                )
        first_original = next(
            (index for index, state in enumerate(states) if state == "original"),
            len(states),
        )
        if any(state == "output" for state in states[first_original:]):
            raise RewriteError("CRITICAL recovery state is not a completed prefix")
        observed_completed = first_original
        recorded_completed = int(record["completed_writes"])
        if abs(observed_completed - recorded_completed) > 1:
            raise RewriteError(
                "CRITICAL recovery checkpoint diverges from file state"
            )
        if observed_completed != recorded_completed:
            _checkpoint_recovery_journal(
                journal_fd,
                record,
                observed_completed,
            )
        for index in range(observed_completed - 1, -1, -1):
            operation = operations[index]
            state = states[index]
            if state == "output":
                _validate_parent_anchor(root_fd, operation)
                _atomic_write_at(operation, operation.original)
                _validate_parent_anchor(root_fd, operation)
                _checkpoint_recovery_journal(journal_fd, record, index)
        _delete_journal(journal_fd)
    finally:
        for operation in operations:
            operation.close()


def _rollback_open_operations(
    journal_fd: int,
    operations: Sequence[OpenOperation],
    manifest_sha256: str,
) -> list[str]:
    failures: list[str] = []
    for index in range(len(operations) - 1, -1, -1):
        operation = operations[index]
        try:
            current = _read_file_at(
                operation.parent_fd, operation.name, operation.relative
            )[0]
            if current == operation.output:
                _atomic_write_at(operation, operation.original)
                _checkpoint_journal(
                    journal_fd,
                    manifest_sha256,
                    operations,
                    index,
                )
            elif current != operation.original:
                raise RewriteError("unknown bytes during rollback")
        except Exception as error:
            failures.append(f"{operation.relative}: {error}")
            break
    if not failures:
        try:
            _delete_journal(journal_fd)
        except Exception as error:
            failures.append(f"journal: {error}")
    return failures


def _apply_batch(
    root_fd: int,
    journal_fd: int,
    operations: Sequence[OpenOperation],
    manifest_sha256: str,
) -> None:
    _install_journal(journal_fd, manifest_sha256, operations)
    try:
        for index, operation in enumerate(operations):
            _validate_parent_anchor(root_fd, operation)
            current = _read_file_at(
                operation.parent_fd, operation.name, operation.relative
            )[0]
            if current != operation.original:
                raise RewriteError(
                    f"file changed after preflight: {operation.relative!r}"
                )
            _atomic_write_at(operation, operation.output)
            _validate_parent_anchor(root_fd, operation)
            _checkpoint_journal(
                journal_fd,
                manifest_sha256,
                operations,
                index + 1,
            )
    except Exception as error:
        failures = _rollback_open_operations(
            journal_fd,
            operations,
            manifest_sha256,
        )
        if failures:
            raise RewriteError(
                f"CRITICAL batch failed ({error}); rollback failed: "
                + "; ".join(failures)
            ) from error
        raise RewriteError(f"batch write failed and was rolled back: {error}") from error
    _delete_journal(journal_fd)


def _validate_lesson_rename_manifest(
    payload: bytes,
) -> Mapping[str, object]:
    try:
        manifest = lesson_renames.validate_manifest_bytes(
            payload, LESSON_RENAME_AUTHORITY_COMMIT
        )
    except (TypeError, ValueError) as error:
        raise RewriteError(f"invalid lesson rename manifest: {error}") from error
    if manifest["authority_tree"] != LESSON_RENAME_AUTHORITY_TREE:
        raise RewriteError("lesson rename authority tree mismatch")
    records = manifest["records"]
    if manifest["record_count"] != 42 or len(records) != 42:
        raise RewriteError("lesson rename overlay must contain exactly 42 records")

    sources: set[str] = set()
    destinations: set[str] = set()
    folded_destinations: set[str] = set()
    nfd_folded_destinations: set[str] = set()
    for record in records:
        source = record["source"]
        destination = record["destination"]
        if (
            type(source) is not str
            or type(destination) is not str
            or LESSON_STRUCTURAL_SOURCE.fullmatch(source) is None
        ):
            raise RewriteError("lesson rename source is not a structural generic note")
        try:
            normalized_source = normalize_relative_path(source)
            normalized_destination = normalize_relative_path(destination)
        except (InventoryError, TypeError) as error:
            raise RewriteError("lesson rename overlay path is invalid") from error
        if normalized_source != source or normalized_destination != destination:
            raise RewriteError("lesson rename overlay paths must be canonical NFC")
        source_path = PurePosixPath(source)
        destination_path = PurePosixPath(destination)
        if source_path.parent != destination_path.parent:
            raise RewriteError("lesson rename destination left its class folder")
        expected_prefix = (
            "Resumo - " if source_path.name == "Resumo.md" else "Transcrito - "
        )
        if (
            not destination_path.name.startswith(expected_prefix)
            or not destination_path.name.endswith(".md")
        ):
            raise RewriteError("lesson rename destination kind is inconsistent")
        if source in sources or destination in destinations:
            raise RewriteError("lesson rename overlay contains duplicate paths")
        folded = destination.casefold()
        nfd_folded = unicodedata.normalize("NFD", destination).casefold()
        if folded in folded_destinations or nfd_folded in nfd_folded_destinations:
            raise RewriteError("lesson rename overlay contains portable collisions")
        sources.add(source)
        destinations.add(destination)
        folded_destinations.add(folded)
        nfd_folded_destinations.add(nfd_folded)
    return manifest


def _load_lesson_rename_overlay(
    root_fd: int,
) -> dict[str, LessonRenameOverlayEntry]:
    snapshot = _secure_optional_read_with_mode(
        root_fd, LESSON_RENAME_MANIFEST_RELATIVE
    )
    if snapshot is None:
        return {}
    payload, mode = snapshot
    if mode != 0o644:
        raise RewriteError("lesson rename manifest mode mismatch")
    digest = hashlib.sha256(payload).hexdigest()
    if digest != LESSON_RENAME_MANIFEST_SHA256:
        raise RewriteError(
            f"lesson rename manifest sha256 mismatch: {digest} != "
            f"{LESSON_RENAME_MANIFEST_SHA256}"
        )
    manifest = _validate_lesson_rename_manifest(payload)
    overlay: dict[str, LessonRenameOverlayEntry] = {}
    for record in manifest["records"]:
        source = str(record["source"])
        destination = str(record["destination"])
        if _secure_optional_read_with_mode(root_fd, source) is not None:
            raise RewriteError(f"lesson rename source still exists: {source!r}")
        final_payload, final_mode = _secure_read_with_mode(root_fd, destination)
        if len(final_payload) != record["final_size_bytes"]:
            raise RewriteError(f"lesson rename final size mismatch: {destination!r}")
        if hashlib.sha256(final_payload).hexdigest() != record["final_sha256"]:
            raise RewriteError(f"lesson rename final hash mismatch: {destination!r}")
        expected_mode = int(str(record["final_mode"])[-3:], 8)
        if final_mode != expected_mode:
            raise RewriteError(f"lesson rename final mode mismatch: {destination!r}")
        overlay[source] = LessonRenameOverlayEntry(destination, final_payload)
    if len(overlay) != 42:
        raise RewriteError("lesson rename overlay scope mismatch")
    return overlay


def _overlay_payload(
    root_fd: int,
    relative: str,
    overlay: Mapping[str, LessonRenameOverlayEntry],
) -> tuple[str, bytes]:
    entry = overlay.get(relative)
    if entry is not None:
        return entry.destination, entry.payload
    try:
        return relative, _secure_read(root_fd, relative)
    except RewriteError as error:
        if LESSON_STRUCTURAL_SOURCE.fullmatch(relative) is not None and not overlay:
            raise RewriteError(
                "lesson rename manifest is required because structural lesson paths "
                "are missing"
            ) from error
        raise


def audit_projected_links(
    root_fd: int,
    manifest: Sequence[Mapping[str, object]],
    projected: Mapping[str, bytes],
) -> LinkAudit:
    notes: dict[str, bytes] = {}
    lesson_overlay = _load_lesson_rename_overlay(root_fd)
    for record in manifest:
        destination = str(record["destination"])
        if not destination.casefold().endswith(".md"):
            continue
        try:
            if destination in projected:
                catalog_path, payload = destination, projected[destination]
            else:
                catalog_path, payload = _overlay_payload(
                    root_fd, destination, lesson_overlay
                )
            notes[catalog_path] = payload
        except RewriteError as error:
            raise RewriteError(
                f"projected link audit target is unavailable: {destination!r}: {error}"
            ) from error
    try:
        return audit_note_contents(notes)
    except ValueError as error:
        raise RewriteError(f"projected link audit failed: {error}") from error


def _enforce_link_contract(audit: LinkAudit, contract: LinkContract) -> None:
    if contract.expected_total is not None and audit.total != contract.expected_total:
        raise RewriteError(
            f"link total regressed: {audit.total} != {contract.expected_total}"
        )
    if audit.unresolved > contract.max_unresolved:
        raise RewriteError(
            f"unresolved links regressed: {audit.unresolved} > {contract.max_unresolved}"
        )
    if audit.ambiguous > contract.max_ambiguous:
        raise RewriteError(
            f"ambiguous links regressed: {audit.ambiguous} > {contract.max_ambiguous}"
        )


def is_active_catalog_path(relative: str) -> bool:
    try:
        normalized = normalize_relative_path(relative)
    except (InventoryError, TypeError):
        return False
    return normalized == relative and all(
        not component.startswith(".") for component in PurePosixPath(relative).parts
    )


def _active_old_literal_count(
    root_fd: int,
    manifest: Sequence[Mapping[str, object]],
    projected: Mapping[str, bytes],
) -> int:
    count = 0
    lesson_overlay = _load_lesson_rename_overlay(root_fd)
    for record in manifest:
        destination = str(record["destination"])
        if not destination.casefold().endswith(".md"):
            continue
        if destination in projected:
            catalog_path, payload = destination, projected[destination]
        else:
            catalog_path, payload = _overlay_payload(
                root_fd, destination, lesson_overlay
            )
        if not is_active_catalog_path(catalog_path):
            continue
        text = payload.decode("utf-8", errors="replace")
        count += len(OLD_ACTIVE_PATTERN.findall(text))
    return count


def _open_vault(vault: Path) -> tuple[Path, int]:
    lexical = Path(os.path.abspath(vault))
    try:
        metadata = os.lstat(lexical)
    except OSError as error:
        raise RewriteError(f"cannot inspect vault: {error}") from error
    if stat.S_ISLNK(metadata.st_mode) or not stat.S_ISDIR(metadata.st_mode):
        raise RewriteError("vault must be a regular non-symlink directory")
    try:
        return lexical, os.open(lexical, DIRECTORY_OPEN_FLAGS)
    except OSError as error:
        raise RewriteError(f"cannot securely open vault: {error}") from error


def audit_filesystem_links(
    vault: Path, manifest: Sequence[Mapping[str, object]]
) -> LinkAudit:
    _, root_fd = _open_vault(Path(vault))
    try:
        return audit_projected_links(root_fd, manifest, {})
    finally:
        os.close(root_fd)


def audit_active_old_literals(
    vault: Path,
    manifest_path: Path,
    *,
    manifest_auth: ManifestAuth,
) -> int:
    _, root_fd = _open_vault(Path(vault))
    try:
        manifest = _load_manifest(root_fd, Path(manifest_path), manifest_auth)
        return _active_old_literal_count(root_fd, manifest, {})
    finally:
        os.close(root_fd)


_DEFAULT_LINK_SENTINEL = object()


def rewrite_vault(
    vault: Path,
    manifest_path: Path,
    *,
    check: bool = False,
    markdown_specs: Mapping[str, Sequence[LiteralRewrite]] | None = None,
    expected_markdown_occurrences: int | None = None,
    manifest_auth: ManifestAuth | None = None,
    recovery_plan: RecoveryPlan | None = None,
    link_contract: LinkContract | None | object = _DEFAULT_LINK_SENTINEL,
) -> RewriteReport:
    production = markdown_specs is None
    if manifest_auth is None:
        if not production:
            raise RewriteError("custom rewrite fixtures require explicit manifest auth")
        manifest_auth = DEFAULT_MANIFEST_AUTH
    if link_contract is _DEFAULT_LINK_SENTINEL:
        link_contract = DEFAULT_LINK_CONTRACT if production else None
    if production and link_contract is None:
        raise RewriteError("production link audit cannot be disabled")
    if production and recovery_plan is not None:
        raise RewriteError("production recovery authority cannot be caller-supplied")
    if not production and recovery_plan is None:
        raise RewriteError("custom rewrite fixtures require an explicit recovery plan")

    lexical_vault, root_fd = _open_vault(Path(vault))
    journal_fd: int | None = None
    operations: list[OpenOperation] = []
    try:
        specs = MARKDOWN_SPECS if markdown_specs is None else markdown_specs
        expected_markdown = (
            EXPECTED_MARKDOWN_OCCURRENCES
            if expected_markdown_occurrences is None
            else expected_markdown_occurrences
        )
        actual_expected = sum(
            rule.expected_count for rules in specs.values() for rule in rules
        )
        if actual_expected != expected_markdown:
            raise RewriteError(
                f"Markdown occurrence contract diverged: expected {expected_markdown}, "
                f"specifies {actual_expected}"
            )

        manifest = _load_manifest(root_fd, Path(manifest_path), manifest_auth)
        _verify_manifest_backing(manifest, specs)
        journal_fd = _open_journal_directory(root_fd)
        existing_journal = _read_journal(journal_fd)
        expected_paths = sorted(
            set(specs) | set(CONFIG_ALLOWLIST),
            key=lambda value: value.encode("utf-8"),
        )

        def trusted_recovery_plan() -> RecoveryPlan:
            nonlocal recovery_plan
            if recovery_plan is None:
                recovery_plan = _production_recovery_plan(
                    lexical_vault,
                    manifest_auth,
                    specs,
                )
            _validate_recovery_plan(
                recovery_plan,
                manifest_auth,
                expected_paths,
            )
            return recovery_plan

        if existing_journal is not None:
            if check:
                raise RewriteError(
                    "CRITICAL recovery journal requires a non-check invocation"
                )
            _recover_journal(
                root_fd,
                journal_fd,
                existing_journal,
                trusted_recovery_plan(),
            )

        by_relative: dict[str, OpenOperation] = {}
        states: list[str] = []
        for relative in sorted(specs, key=lambda value: value.encode("utf-8")):
            operation = _open_operation(root_fd, relative)
            operations.append(operation)
            by_relative[relative] = operation
            try:
                text = operation.original.decode("utf-8")
            except UnicodeDecodeError as error:
                raise RewriteError(f"cannot read UTF-8 file {relative!r}") from error
            state, output = _classify_markdown_state(text, specs[relative], relative)
            operation.output = output.encode("utf-8")
            states.append(state)

        daily_template_exists = _secure_is_file(
            root_fd, "30 Sistema/Templates/Daily.md"
        )
        config_occurrences = 0
        for relative in CONFIG_ALLOWLIST:
            operation = _open_operation(root_fd, relative)
            operations.append(operation)
            by_relative[relative] = operation
            try:
                value = json.loads(operation.original.decode("utf-8"))
            except (UnicodeDecodeError, json.JSONDecodeError) as error:
                raise RewriteError(f"invalid JSON in {relative!r}: {error}") from error
            if type(value) is not dict:
                raise RewriteError(f"JSON root must be an object: {relative!r}")
            state, output, occurrences = _plan_config(
                daily_template_exists, relative, value
            )
            operation.output = output
            states.append(state)
            config_occurrences += occurrences
        if config_occurrences != EXPECTED_CONFIG_OCCURRENCES:
            raise RewriteError("config occurrence contract diverged")

        if all(state == "stale" for state in states):
            planned_status = "stale"
        elif all(state == "fresh" for state in states):
            planned_status = "fresh"
        else:
            raise RewriteError("rewrite scope is partially stale and partially fresh")
        changed_operations = [
            operation for operation in operations if operation.output != operation.original
        ]
        expected_changed = len(specs) + len(CONFIG_ALLOWLIST)
        if planned_status == "stale" and len(changed_operations) != expected_changed:
            raise RewriteError("stale rewrite did not change every allowlisted file")
        if planned_status == "fresh" and changed_operations:
            raise RewriteError("fresh rewrite would change bytes")

        projected = {
            relative: operation.output for relative, operation in by_relative.items()
        }
        links: LinkAudit | None = None
        if isinstance(link_contract, LinkContract):
            links = audit_projected_links(root_fd, manifest, projected)
            _enforce_link_contract(links, link_contract)
        if production:
            old_literals = _active_old_literal_count(root_fd, manifest, projected)
            if old_literals:
                raise RewriteError(
                    f"active catalog still has {old_literals} old path literals"
                )

        if planned_status == "stale" and not check:
            ordered_changed = sorted(
                changed_operations,
                key=lambda operation: operation.relative.encode("utf-8"),
            )
            _authenticate_open_plan(
                ordered_changed,
                trusted_recovery_plan(),
            )
            _apply_batch(
                root_fd,
                journal_fd,
                ordered_changed,
                manifest_auth.sha256,
            )
            status = "updated"
        else:
            if planned_status == "stale":
                ordered_changed = sorted(
                    changed_operations,
                    key=lambda operation: operation.relative.encode("utf-8"),
                )
                _authenticate_open_plan(
                    ordered_changed,
                    trusted_recovery_plan(),
                )
            status = planned_status
        return RewriteReport(
            status=status,
            occurrences=expected_markdown + EXPECTED_CONFIG_OCCURRENCES,
            files_changed=len(changed_operations),
            links=links,
        )
    except (InventoryError, RuleError) as error:
        raise RewriteError(str(error)) from error
    finally:
        for operation in operations:
            operation.close()
        if journal_fd is not None:
            os.close(journal_fd)
        os.close(root_fd)


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="Rewrite the closed set of audited Plan B vault paths."
    )
    parser.add_argument("--vault", required=True, type=Path)
    parser.add_argument("--manifest", required=True, type=Path)
    parser.add_argument(
        "--check",
        action="store_true",
        help="report stale/fresh state without writing",
    )
    return parser


def main(arguments: Sequence[str] | None = None) -> int:
    args = _parser().parse_args(arguments)
    try:
        report = rewrite_vault(
            args.vault,
            args.manifest,
            check=args.check,
        )
    except (OSError, RewriteError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"status={report.status}")
    print(f"occurrences={report.occurrences}")
    print(f"files_changed={report.files_changed}")
    if report.links is not None:
        print(f"links_total={report.links.total}")
        print(f"links_resolved={report.links.resolved}")
        print(f"links_unresolved={report.links.unresolved}")
        print(f"links_ambiguous={report.links.ambiguous}")
    if args.check and report.status == "stale":
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
