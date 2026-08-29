#!/usr/bin/env python3
"""Fail closed unless staged Hermes and the exact Plan B checkout are trustworthy."""

from __future__ import annotations

import argparse
from datetime import date
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

from hermes_common import (
    COMMIT_RE,
    HermesError,
    SHA256_RE,
    audit_components,
    load_manifest,
    read_relative_file,
    safe_relative,
    sha256_bytes,
)


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--hermes-home", required=True, type=Path)
    value.add_argument("--vault", required=True, type=Path)
    value.add_argument("--manifest", required=True, type=Path)
    value.add_argument("--expected-commit", required=True)
    return value


def finding(rule: str, detail: str, file: str = "<vault>") -> dict[str, object]:
    return {"detail": detail, "file": file, "line": 0, "rule": rule, "severity": "error"}


def git(vault: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(vault), *arguments],
        text=True,
        capture_output=True,
        check=False,
    )


def checked_checkout(vault: Path, expected_commit: str) -> tuple[str, str]:
    if not vault.is_absolute():
        raise HermesError("vault must be absolute")
    try:
        mode = vault.lstat().st_mode
    except OSError as error:
        raise HermesError(f"vault is unavailable: {error}") from error
    if stat.S_ISLNK(mode) or not stat.S_ISDIR(mode):
        raise HermesError("vault must be a non-symlink directory")
    root = git(vault, "rev-parse", "--show-toplevel")
    if root.returncode != 0 or Path(root.stdout.strip()).resolve() != vault.resolve():
        raise HermesError("vault must be the Git repository root")
    head = git(vault, "rev-parse", "HEAD")
    actual = head.stdout.strip()
    if head.returncode != 0 or COMMIT_RE.fullmatch(actual) is None:
        raise HermesError("vault HEAD is invalid")
    if actual != expected_commit:
        raise HermesError("vault HEAD does not match expected commit")
    status_result = git(vault, "status", "--porcelain=v1", "--untracked-files=all")
    if status_result.returncode != 0:
        raise HermesError("vault status is unavailable")
    if status_result.stdout:
        raise HermesError("vault working tree is not clean")
    return actual, status_result.stdout


def required_file(vault: Path, relative: str) -> bytes:
    payload, issue = read_relative_file(vault, relative)
    if issue or payload is None:
        raise HermesError(f"cannot trust {relative}: {issue}")
    return payload


def validate_state_files(vault: Path) -> str:
    catalog = required_file(vault, "30 Sistema/Estado/catalog.jsonl")
    snapshot = required_file(vault, "30 Sistema/Estado/dashboard-snapshot.md").decode("utf-8")
    catalog_match = re.search(
        r'^catalog_sha256:\s*["\']?sha256:([0-9a-f]{64})["\']?\s*$', snapshot, re.MULTILINE
    )
    if catalog_match is None or catalog_match.group(1) != sha256_bytes(catalog):
        raise HermesError("dashboard snapshot does not authenticate catalog.jsonl")
    manifest_count = 0
    as_of = ""
    file_paths: set[str] = set()
    for number, line in enumerate(catalog.decode("utf-8").splitlines(), 1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise HermesError(f"catalog line {number} is invalid JSON") from error
        if not isinstance(record, dict) or record.get("schema_version") != 1:
            raise HermesError(f"catalog line {number} has an unsupported schema")
        record_type = record.get("record_type")
        if record_type == "manifest":
            manifest_count += 1
            if number != 1:
                raise HermesError("catalog manifest must be the first record")
            as_of = str(record.get("as_of", ""))
            try:
                date.fromisoformat(as_of)
            except ValueError as error:
                raise HermesError("catalog as_of is invalid") from error
            continue
        for key in ("path", "source_path", "concept_path"):
            if key in record:
                catalog_path = safe_relative(record[key], f"catalog line {number} {key}")
                if not catalog_path.startswith(("00 Home/", "10 Matérias/", "20 Conhecimento/", "30 Sistema/", "90 Arquivo/")):
                    raise HermesError(f"catalog line {number} uses a noncanonical root")
        if record_type == "file":
            relative = str(record.get("path", ""))
            if relative in file_paths:
                raise HermesError(f"catalog file path is duplicated: {relative}")
            file_paths.add(relative)
            if "/Materiais/" in relative or "/Slides/Material/" in relative:
                raise HermesError(f"catalog contains legacy material path: {relative}")
            expected_hash = str(record.get("sha256", "")).removeprefix("sha256:")
            if SHA256_RE.fullmatch(expected_hash) is None:
                raise HermesError(f"catalog file hash is invalid: {relative}")
            if sha256_bytes(required_file(vault, relative)) != expected_hash:
                raise HermesError(f"catalog file hash mismatch: {relative}")
    if manifest_count != 1 or not file_paths:
        raise HermesError("catalog needs one manifest and at least one file")
    return as_of


def run_gate(vault: Path, relative: str, arguments: list[str], reason: str) -> None:
    gate = vault / relative
    if not gate.is_file() or gate.is_symlink():
        raise HermesError(f"required gate is missing or unsafe: {relative}")
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    result = subprocess.run(
        [sys.executable, str(gate), *arguments],
        text=True,
        capture_output=True,
        check=False,
        env=environment,
    )
    if result.returncode != 0:
        raise HermesError(reason)


def validate_vault(vault: Path, expected_commit: str) -> str:
    actual, status_before = checked_checkout(vault, expected_commit)
    as_of = validate_state_files(vault)
    run_gate(
        vault,
        ".fgv/scripts/generate_state.py",
        ["--vault", str(vault), "--as-of", as_of, "--check"],
        "generate_state.py --check failed",
    )
    run_gate(
        vault,
        ".fgv/scripts/validate_vault.py",
        ["--vault", str(vault), "--as-of", as_of],
        "validate_vault.py failed",
    )
    head_after = git(vault, "rev-parse", "HEAD")
    status_after = git(vault, "status", "--porcelain=v1", "--untracked-files=all")
    if head_after.returncode != 0 or head_after.stdout.strip() != actual:
        raise HermesError("a validation gate changed vault HEAD")
    if status_after.returncode != 0 or status_after.stdout != status_before:
        raise HermesError("a validation gate changed the vault working tree")
    return actual


def main() -> int:
    args = parser().parse_args()
    failures: list[dict[str, object]] = []
    manifest_sha256: str | None = None
    vault_commit: str | None = None
    try:
        if COMMIT_RE.fullmatch(args.expected_commit) is None:
            raise HermesError("expected-commit must be a lowercase full Git SHA")
        manifest, manifest_sha256 = load_manifest(args.manifest)
        if not args.hermes_home.is_absolute():
            raise HermesError("hermes-home must be absolute")
        audit = audit_components(args.hermes_home, manifest)
        failures.extend(audit["findings"])
        for component in manifest["components"]:
            payload, issue = read_relative_file(args.hermes_home, component["path"])
            if issue or payload is None:
                continue
            text = payload.decode("utf-8")
            for marker in component["required_markers"]:
                if marker not in text:
                    failures.append(finding("missing_marker", f"required marker is missing: {marker}", component["path"]))
            if {"catalog.jsonl", "dashboard-snapshot.md"} <= set(component["required_markers"]):
                if text.find("catalog.jsonl") > text.find("dashboard-snapshot.md"):
                    failures.append(finding("retrieval_order", "catalog must precede dashboard snapshot", component["path"]))
        if not failures:
            vault_commit = validate_vault(args.vault, args.expected_commit)
    except (HermesError, OSError, UnicodeDecodeError, json.JSONDecodeError, TypeError) as error:
        failures.append(finding("invalid_input", str(error)))
    failures.sort(key=lambda item: (str(item["file"]), int(item["line"]), str(item["rule"])))
    report = {
        "failures": failures,
        "manifest_sha256": manifest_sha256,
        "schema_version": 1,
        "status": "blocked" if failures else "ready",
        "vault_commit": vault_commit,
    }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if not failures else 2


if __name__ == "__main__":
    sys.exit(main())
