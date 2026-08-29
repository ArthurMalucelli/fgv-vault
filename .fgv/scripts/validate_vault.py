#!/usr/bin/env python3
"""Certify the integrated FGV Plan B vault without changing it."""

from __future__ import annotations

import argparse
from dataclasses import asdict, dataclass
from datetime import date
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys
from typing import Sequence

sys.dont_write_bytecode = True

import import_live_delta
import rename_lesson_notes
import rewrite_paths
from fgv_migration.rules import validate_manifest


SCHEMA = "fgv.vault-validation.v1"
VISIBLE_ROOTS = (
    "00 Home",
    "10 Matérias",
    "20 Conhecimento",
    "30 Sistema",
    "90 Arquivo",
)
ADAPTER_MANIFEST = Path("30 Sistema/Estado/adapter-staging/manifest.json")
HERMES_MANIFEST = Path("30 Sistema/Hermes/hermes-manifest.json")


class ValidationError(RuntimeError):
    pass


@dataclass(frozen=True)
class Check:
    name: str
    status: str
    detail: str


def _require(condition: bool, message: str) -> None:
    if not condition:
        raise ValidationError(message)


def _sha256(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def _read_json(path: Path) -> object:
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise ValidationError(f"invalid JSON {path}: {error}") from error


def _git(root: Path, *arguments: str) -> str:
    environment = {
        key: value for key, value in os.environ.items() if not key.startswith("GIT_")
    }
    environment["GIT_NO_REPLACE_OBJECTS"] = "1"
    result = subprocess.run(
        ["git", *arguments],
        cwd=root,
        env=environment,
        check=False,
        capture_output=True,
        text=True,
    )
    if result.returncode != 0:
        raise ValidationError(f"Git command failed: {' '.join(arguments)}")
    return result.stdout.strip()


def _validate_root(root: Path) -> tuple[str, str]:
    resolved = root.resolve(strict=True)
    _require(root.absolute() == resolved, "vault root must not traverse a symlink")
    _require(resolved.is_dir(), "vault root must be a directory")
    _require(_git(resolved, "rev-parse", "--show-toplevel") == resolved.as_posix(), "vault must be the Git root")
    visible = tuple(sorted(path.name for path in resolved.iterdir() if not path.name.startswith(".")))
    _require(visible == VISIBLE_ROOTS, f"visible roots diverged: {visible!r}")
    return _git(resolved, "rev-parse", "HEAD"), _git(resolved, "rev-parse", "HEAD^{tree}")


def _reject_symlinks(root: Path) -> int:
    checked = 0
    for current_raw, directory_names, file_names in os.walk(root, followlinks=False):
        current = Path(current_raw)
        relative = current.relative_to(root)
        if relative.parts and relative.parts[0] == ".git":
            directory_names[:] = []
            continue
        directory_names[:] = [name for name in directory_names if name != ".git"]
        for name in (*directory_names, *file_names):
            candidate = current / name
            _require(not candidate.is_symlink(), f"symlink is not allowed: {candidate.relative_to(root)}")
            checked += 1
    return checked


def _validate_content_chain(root: Path) -> dict[str, int]:
    structural_raw = _read_json(root / "30 Sistema/Estado/migration-manifest.json")
    _require(isinstance(structural_raw, list), "structural manifest root must be a list")
    try:
        validate_manifest(structural_raw)
    except Exception as error:
        raise ValidationError(f"structural manifest rejected: {error}") from error
    structural = structural_raw
    _require(len(structural) == 1059, "structural manifest must contain 1059 records")

    lesson_raw = _read_json(root / "30 Sistema/Estado/lesson-rename-manifest.json")
    _require(isinstance(lesson_raw, dict), "lesson manifest root must be an object")
    lesson_records = lesson_raw.get("records")
    _require(isinstance(lesson_records, list) and len(lesson_records) == 42, "lesson manifest must contain 42 records")
    lesson_by_source = {str(record["source"]): record for record in lesson_records}
    _require(len(lesson_by_source) == 42, "lesson sources must be unique")

    rewrite_paths_set = set(rewrite_paths.MARKDOWN_SPECS)
    _require(not rewrite_paths_set.intersection(lesson_by_source), "content classes overlap")
    byte_identical = 0
    path_rewritten = 0
    lesson_metadata = 0
    lesson_body = 0
    seen_final: set[str] = set()
    for record in structural:
        destination = str(record["destination"])
        if destination in lesson_by_source:
            lesson = lesson_by_source[destination]
            final_relative = str(lesson["destination"])
            final = root / PurePosixPath(final_relative)
            _require(not (root / PurePosixPath(destination)).exists(), f"generic lesson source remains: {destination}")
            _require(final.is_file() and not final.is_symlink(), f"renamed lesson missing: {final_relative}")
            payload = final.read_bytes()
            _require(_sha256(payload) == lesson["final_sha256"], f"renamed lesson hash diverged: {final_relative}")
            if lesson["content_class"] == "metadata-only":
                lesson_metadata += 1
            elif lesson["content_class"] == "authorized-body-transform":
                lesson_body += 1
            else:
                raise ValidationError(f"unknown lesson content class: {lesson['content_class']!r}")
        else:
            final_relative = destination
            final = root / PurePosixPath(final_relative)
            _require(final.is_file() and not final.is_symlink(), f"structural destination missing: {final_relative}")
            if destination in rewrite_paths_set:
                path_rewritten += 1
            else:
                payload = final.read_bytes()
                _require(_sha256(payload) == record["sha256"], f"byte-identical file diverged: {destination}")
                _require(len(payload) == record["size_bytes"], f"byte-identical size diverged: {destination}")
                byte_identical += 1
        _require(final_relative not in seen_final, f"duplicate final path: {final_relative}")
        seen_final.add(final_relative)

    _require(
        (byte_identical, path_rewritten, lesson_metadata, lesson_body) == (1008, 9, 40, 2),
        "migration content-class counts diverged",
    )
    rewrite_report = rewrite_paths.rewrite_vault(
        root,
        Path("30 Sistema/Estado/migration-manifest.json"),
        check=True,
    )
    _require(rewrite_report.status == "fresh", "path rewrite state is not fresh")
    rename_report = rename_lesson_notes.execute_rename(
        root,
        rename_lesson_notes.DEFAULT_EXPECTED_HEAD,
        apply=False,
        expected_active=42,
        expected_archive=47,
    )
    _require(rename_report.status == "no_op", "lesson rename state is not no-op")
    _require(import_live_delta.apply(root, check=True) == "no_op", "live delta is not authenticated no-op")

    live_records = [dict(item) for item in import_live_delta.RECORDS]
    combined = [*structural, *({"destination": item["destination"]} for item in live_records)]
    _, root_fd = rewrite_paths._open_vault(root)
    try:
        links = rewrite_paths.audit_projected_links(root_fd, combined, {})
    finally:
        os.close(root_fd)
    _require(
        (links.total, links.resolved, links.unresolved, links.ambiguous) == (5442, 5035, 407, 0),
        "migration-scoped link contract diverged",
    )
    return {
        "structural_records": len(structural),
        "byte_identical": byte_identical,
        "path_rewritten": path_rewritten,
        "lesson_metadata_only": lesson_metadata,
        "authorized_body_transforms": path_rewritten + lesson_body,
        "live_delta_records": len(live_records),
        "links_total": links.total,
        "links_resolved": links.resolved,
        "links_unresolved": links.unresolved,
        "links_ambiguous": links.ambiguous,
    }


def _validate_navigation(root: Path) -> dict[str, int]:
    registry = _read_json(root / ".fgv/config/subjects.json")
    _require(isinstance(registry, dict) and isinstance(registry.get("subjects"), list), "subject registry is invalid")
    subjects = registry["subjects"]
    _require(len(subjects) == 7, "exactly seven active subjects are required")
    for subject in subjects:
        shell = root / str(subject["path"]) / "Disciplina.md"
        _require(shell.is_file() and not shell.is_symlink(), f"subject shell missing: {subject['id']}")
    for required in (
        "00 Home/Home.md",
        "00 Home/Revisões.md",
        "00 Home/Inbox/README.md",
        "00 Home/Tasks.md",
        "30 Sistema/Estado/catalog.jsonl",
        "30 Sistema/Estado/dashboard-snapshot.md",
    ):
        _require((root / PurePosixPath(required)).is_file(), f"navigation/state file missing: {required}")
    generic = [
        path
        for path in (root / "10 Matérias").glob("*/Aulas/*/*.md")
        if path.name in {"Resumo.md", "Transcrito.md"}
    ]
    _require(not generic, f"active generic lesson names remain: {generic!r}")
    return {"active_subjects": len(subjects), "active_generic_notes": len(generic)}


def _validate_state(root: Path, as_of: str) -> dict[str, int]:
    command = [
        sys.executable,
        (root / ".fgv/scripts/generate_state.py").as_posix(),
        "--vault",
        root.as_posix(),
        "--as-of",
        as_of,
        "--check",
    ]
    environment = dict(os.environ)
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(command, cwd=root, env=environment, check=False, capture_output=True, text=True)
    _require(result.returncode == 0 and result.stdout.strip() == "state fresh", "generated state is stale")
    with (root / "30 Sistema/Estado/catalog.jsonl").open(encoding="utf-8") as handle:
        first_line = handle.readline()
    manifest = json.loads(first_line)
    counts = manifest.get("counts")
    _require(isinstance(counts, dict), "catalog counts are missing")
    _require(counts.get("files") == 1036, "catalog academic file count diverged")
    _require(counts.get("tasks") == 9, "catalog task count diverged")
    _require(counts.get("learning_states") == 5, "catalog learning-state count diverged")
    _require(counts.get("warnings") == 0, "catalog contains warnings")
    return {str(key): int(value) for key, value in counts.items()}


def _validate_packages(root: Path) -> dict[str, object]:
    adapter = _read_json(root / ADAPTER_MANIFEST)
    _require(isinstance(adapter, dict), "adapter manifest is invalid")
    _require(adapter.get("install_performed") is False, "live adapter install must remain false")
    parity = adapter.get("parity")
    _require(isinstance(parity, dict) and parity.get("normative_contract_identical") is True, "adapter parity failed")
    for runtime in ("codex", "claude"):
        record = adapter.get("adapters", {}).get(runtime)
        _require(isinstance(record, dict), f"adapter record missing: {runtime}")
        path = root / ADAPTER_MANIFEST.parent / str(record["path"])
        _require(path.is_file() and _sha256(path.read_bytes()) == record["sha256"], f"adapter hash diverged: {runtime}")
    hermes = _read_json(root / HERMES_MANIFEST)
    _require(isinstance(hermes, dict), "Hermes manifest is invalid")
    return {
        "adapter_contract_version": adapter.get("contract_version"),
        "adapter_parity": True,
        "hermes_schema_version": hermes.get("schema_version"),
    }


def validate(root: Path, as_of: str, *, require_packages: bool = True) -> dict[str, object]:
    _require(re.fullmatch(r"\d{4}-\d{2}-\d{2}", as_of) is not None, "as_of must be YYYY-MM-DD")
    _require(date.fromisoformat(as_of).isoformat() == as_of, "as_of must be canonical")
    root = root.resolve(strict=True)
    head, tree = _validate_root(root)
    checks: list[Check] = []
    symlinks = _reject_symlinks(root)
    checks.append(Check("filesystem", "pass", f"checked_entries={symlinks}"))
    content = _validate_content_chain(root)
    checks.append(Check("content_chain", "pass", json.dumps(content, sort_keys=True)))
    navigation = _validate_navigation(root)
    checks.append(Check("navigation", "pass", json.dumps(navigation, sort_keys=True)))
    state_counts = _validate_state(root, as_of)
    checks.append(Check("generated_state", "pass", json.dumps(state_counts, sort_keys=True)))
    packages: dict[str, object] = {}
    if require_packages:
        packages = _validate_packages(root)
        checks.append(Check("runtime_packages", "pass", json.dumps(packages, sort_keys=True)))
    payload: dict[str, object] = {
        "schema": SCHEMA,
        "schema_version": 1,
        "authority_commit": head,
        "authority_tree": tree,
        "as_of": as_of,
        "status": "pass",
        "checks": [asdict(check) for check in checks],
        "counts": {**content, **navigation, **state_counts},
        "packages": packages,
        "known_limitations": [
            "Migration applicators are integrity tools for a quiescent trusted-user vault, not an OS security boundary.",
            "Hermes and VPS production remain unchanged until the separately authorized cutover.",
        ],
    }
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")
    payload["aggregate_sha256"] = _sha256(canonical)
    return payload


def main(arguments: Sequence[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--output", type=Path)
    args = parser.parse_args(arguments)
    try:
        report = validate(args.vault, args.as_of)
    except (OSError, ValueError, ValidationError) as error:
        print(json.dumps({"status": "blocked", "reason": str(error)}, ensure_ascii=False, sort_keys=True))
        return 2
    encoded = json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    if args.output is not None:
        output = args.output
        if not output.is_absolute():
            output = args.vault / output
        output.parent.mkdir(parents=True, exist_ok=True)
        output.write_text(encoded, encoding="utf-8")
    else:
        print(encoded, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
