#!/usr/bin/env python3
"""Rewrite the audited Plan B vault paths and Obsidian configuration."""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import sys
import tempfile
import unicodedata
from typing import Mapping, Sequence

from fgv_migration.inventory import normalize_relative_path
from fgv_migration.links import LinkAudit, audit_note_contents
from fgv_migration.rules import RuleError, validate_manifest


EXPECTED_MARKDOWN_OCCURRENCES = 59
EXPECTED_CONFIG_OCCURRENCES = 5

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

URL_PATTERN = re.compile(r"(?:https?|mailto):[^\s<>\])}]+", re.IGNORECASE)


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
    if type(relative) is not str or normalize_relative_path(relative) != relative:
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


def _load_manifest(vault: Path, manifest_path: Path) -> list[dict[str, object]]:
    path = manifest_path if manifest_path.is_absolute() else vault / manifest_path
    try:
        path.resolve(strict=True).relative_to(vault.resolve(strict=True))
    except (FileNotFoundError, ValueError) as error:
        raise RewriteError("manifest must be an existing file inside the vault") from error
    if path.is_symlink() or not path.is_file():
        raise RewriteError("manifest must be a regular non-symlink file")
    try:
        manifest = json.loads(path.read_bytes())
        validate_manifest(manifest)
    except (OSError, UnicodeDecodeError, json.JSONDecodeError, RuleError) as error:
        raise RewriteError(f"invalid migration manifest: {error}") from error
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
    vault: Path, relative: str, value: dict[str, object]
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
            if (vault / "30 Sistema/Templates/Daily.md").is_file()
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


def _atomic_write(path: Path, payload: bytes) -> None:
    mode = stat.S_IMODE(path.stat(follow_symlinks=False).st_mode)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.rewrite.", dir=path.parent
    )
    temporary_path = Path(temporary_name)
    try:
        os.fchmod(descriptor, mode)
        with os.fdopen(descriptor, "wb", closefd=True) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary_path, path)
    except BaseException:
        try:
            os.close(descriptor)
        except OSError:
            pass
        try:
            temporary_path.unlink()
        except FileNotFoundError:
            pass
        raise


def _apply_batch(outputs: Mapping[Path, bytes], originals: Mapping[Path, bytes]) -> None:
    changed = [path for path in sorted(outputs, key=lambda item: str(item).encode()) if outputs[path] != originals[path]]
    applied: list[Path] = []
    try:
        for path in changed:
            if path.read_bytes() != originals[path]:
                raise RewriteError(f"file changed after preflight: {path}")
            _atomic_write(path, outputs[path])
            applied.append(path)
    except BaseException as error:
        rollback_errors: list[str] = []
        for path in reversed(applied):
            try:
                _atomic_write(path, originals[path])
            except BaseException as rollback_error:
                rollback_errors.append(f"{path}: {rollback_error}")
        if rollback_errors:
            raise RewriteError(
                f"batch write failed ({error}); rollback also failed: "
                + "; ".join(rollback_errors)
            ) from error
        raise RewriteError(f"batch write failed and was rolled back: {error}") from error


def audit_filesystem_links(
    vault: Path, manifest: Sequence[Mapping[str, object]]
) -> LinkAudit:
    """Audit manifest-scoped Markdown destinations from the current filesystem."""
    notes: dict[str, bytes] = {}
    for record in manifest:
        destination = str(record["destination"])
        if not destination.casefold().endswith(".md"):
            continue
        path = _safe_relative_path(vault, destination)
        notes[destination] = path.read_bytes()
    return audit_note_contents(notes)


def rewrite_vault(
    vault: Path,
    manifest_path: Path,
    *,
    check: bool = False,
    markdown_specs: Mapping[str, Sequence[LiteralRewrite]] | None = None,
    expected_markdown_occurrences: int | None = None,
    audit_links: bool = True,
) -> RewriteReport:
    vault = Path(vault).resolve(strict=True)
    if not vault.is_dir():
        raise RewriteError("vault must be a directory")
    specs = MARKDOWN_SPECS if markdown_specs is None else markdown_specs
    expected_markdown = (
        EXPECTED_MARKDOWN_OCCURRENCES
        if expected_markdown_occurrences is None
        else expected_markdown_occurrences
    )
    if tuple(sorted(specs)) != tuple(sorted(set(specs))):
        raise RewriteError("Markdown allowlist contains duplicates")
    actual_expected = sum(
        rule.expected_count for rules in specs.values() for rule in rules
    )
    if actual_expected != expected_markdown:
        raise RewriteError(
            f"Markdown occurrence contract diverged: expected {expected_markdown}, "
            f"specifies {actual_expected}"
        )

    manifest = _load_manifest(vault, Path(manifest_path))
    _verify_manifest_backing(manifest, specs)

    originals: dict[Path, bytes] = {}
    outputs: dict[Path, bytes] = {}
    states: list[str] = []
    for relative in sorted(specs, key=lambda value: value.encode("utf-8")):
        path = _safe_relative_path(vault, relative)
        payload, text = _read_utf8(path, relative)
        state, output = _classify_markdown_state(text, specs[relative], relative)
        originals[path] = payload
        outputs[path] = output.encode("utf-8")
        states.append(state)

    config_occurrences = 0
    for relative in CONFIG_ALLOWLIST:
        path = _safe_relative_path(vault, relative)
        payload, value = _load_json(path, relative)
        state, output, occurrences = _plan_config(vault, relative, value)
        originals[path] = payload
        outputs[path] = output
        states.append(state)
        config_occurrences += occurrences
    if config_occurrences != EXPECTED_CONFIG_OCCURRENCES:
        raise RewriteError(
            f"config occurrence contract diverged: expected "
            f"{EXPECTED_CONFIG_OCCURRENCES}, found {config_occurrences}"
        )

    if all(state == "stale" for state in states):
        planned_status = "stale"
    elif all(state == "fresh" for state in states):
        planned_status = "fresh"
    else:
        raise RewriteError("rewrite scope is partially stale and partially fresh")

    changed = sum(outputs[path] != originals[path] for path in outputs)
    if planned_status == "stale" and changed != len(specs) + len(CONFIG_ALLOWLIST):
        raise RewriteError("stale rewrite did not plan one change per allowlisted file")
    if planned_status == "fresh" and changed:
        raise RewriteError("fresh rewrite would change bytes")

    links: LinkAudit | None = None
    if planned_status == "stale" and not check:
        _apply_batch(outputs, originals)
        status = "updated"
        if audit_links:
            links = audit_filesystem_links(vault, manifest)
    else:
        status = planned_status
        if audit_links:
            links = audit_filesystem_links(vault, manifest)

    return RewriteReport(
        status=status,
        occurrences=expected_markdown + EXPECTED_CONFIG_OCCURRENCES,
        files_changed=changed,
        links=links,
    )


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
