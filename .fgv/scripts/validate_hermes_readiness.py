#!/usr/bin/env python3
"""Authorize CUTOVER only from recent, hashed, production-bound PREPARAR evidence."""

from __future__ import annotations

import argparse
from datetime import datetime, timezone
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

from hermes_catalog_query import query_catalog
from hermes_common import (
    COMMIT_RE,
    HermesError,
    SHA256_RE,
    canonical_json,
    load_manifest,
    normalize_remote_url,
    read_relative_file,
    safe_relative,
    sha256_bytes,
    require_current_operational_as_of,
)


MAX_REPORT_AGE_SECONDS = 1800
MAX_FUTURE_SKEW_SECONDS = 120
REPORT_KEYS = {
    "schema_version",
    "timestamp_utc",
    "host_role",
    "recommendation",
    "production_commit",
    "tested_commit",
    "operational_as_of",
    "expected_upstream",
    "expected_remote_url",
    "package_manifest_sha256",
    "prepare_bundle_sha256",
    "backup",
    "untracked",
    "findings",
    "component_results",
    "smoke_tests",
    "retrieval_fixture_mode",
    "retrieval_sync_state",
    "query_timings",
    "context_tokens",
    "diff_summary",
    "evidence",
}
BACKUP_KEYS = {"path", "manifest_path", "manifest_sha256"}
UNTRACKED_KEYS = {"inventory_sha256", "files", "preserved", "classified"}
UNTRACKED_FILE_KEYS = {"source_path", "backup_path", "sha256"}
FINDING_KEYS = {"required_remaining", "warnings"}
SMOKE_IDS = {"academic_retrieval", "eclass", "whatsapp"}
EVIDENCE_IDS = {
    "audit_after",
    "cutover_validation",
    "retrieval_smoke",
    "test_suite",
    "eclass_smoke",
    "whatsapp_smoke",
}
EVIDENCE_RECORD_KEYS = {"path", "sha256"}
BUNDLE_KEYS = {"schema_version", "phase", "package_manifest_sha256", "files"}
BUNDLE_FILE_KEYS = {"path", "sha256"}
BACKUP_MANIFEST_KEYS = {"schema_version", "production_commit", "inventory_sha256", "files"}
LIVE_QUERY_PATHS = {
    "ultima-aula-matematica": "10 Matérias/MatemáticaAplicada/Aulas/08.20/Resumo - Introdução a derivadas.md",
    "transcrito-matematica": "10 Matérias/MatemáticaAplicada/Aulas/08.20/Transcrito - Introdução a derivadas.md",
    "proxima-avaliacao": "00 Home/Tasks.md",
    "material-eclass": "10 Matérias/Estatistica2/Aulas/08.18/Material/Exercicios_Aula05.docx",
    "conceito-gap": "20 Conhecimento/Conceitos/Dividend Yield.md",
    "compat-resumo": "10 Matérias/MatemáticaAplicada/Aulas/08.20/Resumo - Introdução a derivadas.md",
}
RETRIEVAL_EVIDENCE_KEYS = {
    "as_of_commit",
    "fixture_mode",
    "operational_as_of",
    "origin_url",
    "queries",
    "stale",
    "state_check",
    "sync_state",
    "status",
    "upstream",
}
RETRIEVAL_QUERY_KEYS = {
    "bytes_opened",
    "candidate_count",
    "catalog_query_bytes",
    "catalog_query_lines",
    "duration_ms",
    "id",
    "matched",
    "opened_files",
    "selected_path",
    "steps",
}
RETRIEVAL_STEPS = [
    "catalog_query",
    "dashboard_snapshot",
    "checkout_status",
    "select_exact_path",
    "verify_sha256",
    "open_exact_file",
]
MAX_CATALOG_QUERY_BYTES = 16_384
MAX_CATALOG_QUERY_LINES = 1
MAX_CATALOG_CANDIDATES = 5
CUTOVER_EVIDENCE_KEYS = {
    "failures",
    "manifest_sha256",
    "operational_as_of",
    "origin_url",
    "schema_version",
    "status",
    "upstream",
    "vault_commit",
}
CHANNEL_SMOKE_KEYS = {
    "candidate_count",
    "catalog_query_artifact",
    "catalog_query_bytes",
    "catalog_query_lines",
    "catalog_query_sha256",
    "filesystem_scan",
    "full_catalog_in_context",
    "matched",
    "opened_files",
    "operational_as_of",
    "origin_url",
    "query_id",
    "selected_path",
    "status",
    "steps",
    "tested_commit",
    "upstream",
}
CHANNEL_QUERY_SPECS = {
    "eclass_smoke": ("material-eclass", "eclass_material", "estatistica-2"),
    "whatsapp_smoke": ("ultima-aula-matematica", "latest_class", "matematica-aplicada"),
}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--report", required=True, type=Path)
    value.add_argument("--tested-commit", required=True)
    value.add_argument("--as-of", required=True)
    value.add_argument("--manifest", required=True, type=Path)
    value.add_argument("--production-vault", required=True, type=Path)
    value.add_argument("--hermes-home", required=True, type=Path)
    value.add_argument("--bundle", required=True, type=Path)
    value.add_argument("--expected-report-sha256", required=True)
    return value


def stable_payload(path: Path, label: str) -> bytes:
    if not path.is_absolute():
        raise HermesError(f"{label} path must be absolute")
    payload, issue = read_relative_file(path.parent, path.name)
    if issue or payload is None:
        raise HermesError(f"{label} must be a stable regular non-symlink file: {issue}")
    return payload


def json_object(payload: bytes, label: str) -> dict[str, object]:
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise HermesError(f"{label} is not valid UTF-8 JSON: {error}") from error
    if not isinstance(value, dict):
        raise HermesError(f"{label} must be a JSON object")
    return value


def git(vault: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(vault), *arguments], text=True, capture_output=True, check=False
    )


def validate_timestamp(value: object, failures: list[str]) -> None:
    if not isinstance(value, str) or not value.endswith("Z"):
        failures.append("timestamp_utc")
        return
    try:
        parsed = datetime.fromisoformat(value.removesuffix("Z") + "+00:00")
    except ValueError:
        failures.append("timestamp_utc")
        return
    age = (datetime.now(timezone.utc) - parsed).total_seconds()
    if age > MAX_REPORT_AGE_SECONDS or age < -MAX_FUTURE_SKEW_SECONDS:
        failures.append("timestamp_not_recent")


def validate_bundle(
    bundle_path: Path,
    manifest_path: Path,
    manifest_sha256: str,
) -> str:
    package_root = manifest_path.parent.parent.parent.absolute()
    expected_bundle = package_root / "30 Sistema/Hermes/PREPARAR-BUNDLE.json"
    if bundle_path.absolute() != expected_bundle:
        raise HermesError("bundle must be the canonical PREPARAR-BUNDLE.json")
    payload = stable_payload(bundle_path, "bundle")
    bundle = json_object(payload, "bundle")
    if set(bundle) != BUNDLE_KEYS or bundle.get("schema_version") != 1 or bundle.get("phase") != "PREPARAR":
        raise HermesError("PREPARAR bundle schema is closed and invalid")
    if bundle.get("package_manifest_sha256") != manifest_sha256:
        raise HermesError("bundle does not pin the selected package manifest")
    files = bundle.get("files")
    if not isinstance(files, list) or not files:
        raise HermesError("bundle files are missing")
    paths: list[str] = []
    for record in files:
        if not isinstance(record, dict) or set(record) != BUNDLE_FILE_KEYS:
            raise HermesError("bundle file schema is closed and invalid")
        relative = safe_relative(record["path"], "bundle file path")
        expected_hash = str(record["sha256"])
        if SHA256_RE.fullmatch(expected_hash) is None:
            raise HermesError("bundle file checksum is invalid")
        file_payload, issue = read_relative_file(package_root, relative)
        if issue or file_payload is None or sha256_bytes(file_payload) != expected_hash:
            raise HermesError(f"bundle pin failed for {relative}")
        paths.append(relative)
    if paths != sorted(paths) or len(paths) != len(set(paths)):
        raise HermesError("bundle paths must be sorted and unique")
    if not {
        "30 Sistema/Hermes/hermes-manifest.json",
        "30 Sistema/Hermes/retrieval-queries.json",
    } <= set(paths):
        raise HermesError("bundle must pin the manifest and canonical live query set")
    return sha256_bytes(payload)


def load_live_query_paths(manifest_path: Path) -> dict[str, str]:
    package_root = manifest_path.parent.parent.parent.absolute()
    payload, issue = read_relative_file(package_root, "30 Sistema/Hermes/retrieval-queries.json")
    if issue or payload is None:
        raise HermesError(f"canonical live query set cannot be trusted: {issue}")
    try:
        queries = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise HermesError(f"canonical live query set is invalid JSON: {error}") from error
    if not isinstance(queries, list) or len(queries) != len(LIVE_QUERY_PATHS):
        raise HermesError("canonical live query set must contain exactly six queries")
    loaded: dict[str, str] = {}
    for query in queries:
        allowed_schemas = (
            {"id", "question", "query_type", "expected_path"},
            {"id", "question", "query_type", "subject_id", "expected_path"},
        )
        if not isinstance(query, dict) or set(query) not in allowed_schemas:
            raise HermesError("canonical live query schema is closed and invalid")
        query_id = query.get("id")
        expected_path = query.get("expected_path")
        if not isinstance(query_id, str) or not isinstance(expected_path, str) or query_id in loaded:
            raise HermesError("canonical live query ID or path is invalid")
        safe_relative(expected_path, f"canonical live query {query_id} expected_path")
        loaded[query_id] = expected_path
    if loaded != LIVE_QUERY_PATHS or list(loaded) != list(LIVE_QUERY_PATHS):
        raise HermesError("canonical live query IDs or expected paths diverged")
    return loaded


def validate_report_shape(
    report: dict[str, object],
    expected_commit: str,
    manifest: dict[str, object],
    manifest_sha256: str,
    live_query_paths: dict[str, str],
    operational_as_of: str,
) -> list[str]:
    failures: list[str] = []
    if set(report) != REPORT_KEYS:
        return ["report_schema"]
    if type(report["schema_version"]) is not int or report["schema_version"] != 1:
        failures.append("schema_version")
    validate_timestamp(report["timestamp_utc"], failures)
    if report["host_role"] != "hermes-vps":
        failures.append("host_role")
    if report["recommendation"] != "READY":
        failures.append("recommendation")
    if COMMIT_RE.fullmatch(str(report["production_commit"])) is None:
        failures.append("production_commit")
    if report["tested_commit"] != expected_commit:
        failures.append("tested_commit")
    if report["operational_as_of"] != operational_as_of:
        failures.append("operational_as_of")
    if report["expected_upstream"] != manifest["expected_upstream"]:
        failures.append("expected_upstream")
    try:
        report_remote = normalize_remote_url(report["expected_remote_url"])
    except HermesError:
        report_remote = ""
    if report_remote != manifest["expected_remote_url"]:
        failures.append("expected_remote_url")
    if report["package_manifest_sha256"] != manifest_sha256:
        failures.append("package_manifest_sha256")
    if SHA256_RE.fullmatch(str(report["prepare_bundle_sha256"])) is None:
        failures.append("prepare_bundle_sha256")
    findings = report["findings"]
    if not isinstance(findings, dict) or set(findings) != FINDING_KEYS:
        failures.append("findings")
    elif findings.get("required_remaining") != 0 or type(findings.get("warnings")) is not int or int(findings["warnings"]) < 0:
        failures.append("findings")
    expected_components = {item["id"] for item in manifest["components"] if item["classification"] == "required"}
    components = report["component_results"]
    if not isinstance(components, dict) or set(components) != expected_components or any(value != "pass" for value in components.values()):
        failures.append("component_results")
    smoke = report["smoke_tests"]
    if not isinstance(smoke, dict) or set(smoke) != SMOKE_IDS or any(value != "pass" for value in smoke.values()):
        failures.append("smoke_tests")
    if report["retrieval_fixture_mode"] is not False:
        failures.append("retrieval_fixture_mode")
    if report["retrieval_sync_state"] != "clean":
        failures.append("retrieval_sync_state")
    timings = report["query_timings"]
    if not isinstance(timings, list) or not timings:
        failures.append("query_timings")
    else:
        timing_ids: list[str] = []
        for item in timings:
            if not isinstance(item, dict) or set(item) != {"id", "duration_ms"} or not isinstance(item["id"], str) or not item["id"] or type(item["duration_ms"]) is not int or item["duration_ms"] < 0:
                failures.append("query_timings")
                break
            timing_ids.append(item["id"])
        if timing_ids != list(live_query_paths):
            failures.append("query_timings")
    if type(report["context_tokens"]) is not int or report["context_tokens"] < 0:
        failures.append("context_tokens")
    summary = report["diff_summary"]
    if not isinstance(summary, list) or any(not isinstance(item, str) or not item for item in summary):
        failures.append("diff_summary")
    return failures


def hermes_inventory(home: Path) -> tuple[list[str], list[str]]:
    if not home.is_absolute() or not home.is_dir() or home.is_symlink():
        return [], ["hermes_home"]
    paths: list[str] = []
    failures: list[str] = []
    for directory, names, filenames in os.walk(home, followlinks=False):
        directory_path = Path(directory)
        for name in names:
            candidate = directory_path / name
            try:
                if stat.S_ISLNK(candidate.lstat().st_mode):
                    failures.append("hermes_home_symlink")
            except OSError:
                failures.append("hermes_home_unreadable")
        for name in filenames:
            candidate = directory_path / name
            relative = candidate.relative_to(home).as_posix()
            try:
                mode = candidate.lstat().st_mode
            except OSError:
                failures.append("hermes_home_unreadable")
                continue
            if stat.S_ISLNK(mode) or not stat.S_ISREG(mode):
                failures.append("hermes_home_unsafe_file")
            else:
                paths.append(relative)
    return sorted(paths), failures


def validate_production_and_backup(report: dict[str, object], vault: Path, hermes_home: Path) -> list[str]:
    failures: list[str] = []
    if not vault.is_absolute() or not vault.is_dir() or vault.is_symlink():
        return ["production_vault"]
    root = git(vault, "rev-parse", "--show-toplevel")
    head = git(vault, "rev-parse", "HEAD")
    tracked = git(vault, "status", "--porcelain=v1", "--untracked-files=no")
    untracked_result = git(vault, "ls-files", "--others", "--exclude-standard", "-z")
    if root.returncode != 0 or Path(root.stdout.strip()).resolve() != vault.resolve():
        return ["production_git_root"]
    if head.returncode != 0 or head.stdout.strip() != report["production_commit"]:
        failures.append("production_head")
    if tracked.returncode != 0 or tracked.stdout:
        failures.append("production_tracked_dirty")
    if untracked_result.returncode != 0:
        failures.append("production_untracked_unavailable")
        actual_untracked: list[str] = []
    else:
        actual_untracked = sorted(item for item in untracked_result.stdout.split("\0") if item)

    untracked = report["untracked"]
    if not isinstance(untracked, dict) or set(untracked) != UNTRACKED_KEYS or untracked.get("preserved") is not True or untracked.get("classified") is not True:
        return failures + ["untracked"]
    files = untracked.get("files")
    if not isinstance(files, list):
        return failures + ["untracked_files"]
    normalized: list[dict[str, str]] = []
    for record in files:
        if not isinstance(record, dict) or set(record) != UNTRACKED_FILE_KEYS:
            failures.append("untracked_files")
            continue
        try:
            source = safe_relative(record["source_path"], "untracked source_path")
            backup_path = safe_relative(record["backup_path"], "untracked backup_path")
        except HermesError:
            failures.append("untracked_files")
            continue
        checksum = str(record["sha256"])
        if SHA256_RE.fullmatch(checksum) is None:
            failures.append("untracked_files")
            continue
        normalized.append({"backup_path": backup_path, "sha256": checksum, "source_path": source})
    if normalized != sorted(normalized, key=lambda item: item["source_path"]):
        failures.append("untracked_files_order")
    if [item["source_path"] for item in normalized] != actual_untracked:
        failures.append("untracked_inventory_mismatch")
    if normalized or actual_untracked:
        failures.append("untracked_expected_empty")
    expected_inventory = sha256_bytes(canonical_json(normalized).encode("utf-8"))
    if untracked.get("inventory_sha256") != expected_inventory:
        failures.append("untracked_inventory_sha256")

    backup = report["backup"]
    if not isinstance(backup, dict) or set(backup) != BACKUP_KEYS:
        return failures + ["backup"]
    backup_root = Path(str(backup.get("path", "")))
    if not backup_root.is_absolute() or not backup_root.is_dir() or backup_root.is_symlink():
        return failures + ["backup"]
    try:
        manifest_relative = safe_relative(backup.get("manifest_path"), "backup manifest_path")
    except HermesError:
        return failures + ["backup"]
    manifest_payload, issue = read_relative_file(backup_root, manifest_relative)
    if issue or manifest_payload is None or sha256_bytes(manifest_payload) != backup.get("manifest_sha256"):
        return failures + ["backup_manifest"]
    backup_manifest = json_object(manifest_payload, "backup manifest")
    if set(backup_manifest) != BACKUP_MANIFEST_KEYS or backup_manifest.get("schema_version") != 1 or backup_manifest.get("production_commit") != report["production_commit"]:
        return failures + ["backup_manifest_schema"]
    backup_files = backup_manifest.get("files")
    if not isinstance(backup_files, list) or not backup_files:
        return failures + ["backup_manifest_files"]
    normalized_backup: list[dict[str, str]] = []
    for record in backup_files:
        if not isinstance(record, dict) or set(record) != UNTRACKED_FILE_KEYS:
            failures.append("backup_manifest_files")
            continue
        try:
            source = safe_relative(record["source_path"], "backup source_path")
            backup_path = safe_relative(record["backup_path"], "backup backup_path")
        except HermesError:
            failures.append("backup_manifest_files")
            continue
        checksum = str(record["sha256"])
        if SHA256_RE.fullmatch(checksum) is None:
            failures.append("backup_manifest_files")
            continue
        normalized_backup.append({"backup_path": backup_path, "sha256": checksum, "source_path": source})
    normalized_backup.sort(key=lambda item: item["source_path"])
    if backup_files != normalized_backup:
        failures.append("backup_manifest_files_order")
    source_paths, home_failures = hermes_inventory(hermes_home)
    failures.extend(home_failures)
    if [item["source_path"] for item in normalized_backup] != source_paths:
        failures.append("backup_inventory_mismatch")
    if backup_manifest.get("inventory_sha256") != sha256_bytes(canonical_json(normalized_backup).encode("utf-8")):
        failures.append("backup_inventory_sha256")
    for record in normalized_backup:
        source_payload, source_issue = read_relative_file(hermes_home, record["source_path"])
        backup_payload, backup_issue = read_relative_file(backup_root, record["backup_path"])
        if source_issue or backup_issue or source_payload is None or backup_payload is None:
            failures.append("backup_file_missing")
        elif source_payload != backup_payload or sha256_bytes(source_payload) != record["sha256"]:
            failures.append("backup_file_hash")
    return failures


def validate_evidence(
    report: dict[str, object],
    tested_commit: str,
    live_query_paths: dict[str, str],
    operational_as_of: str,
    manifest: dict[str, object],
    package_root: Path,
) -> list[str]:
    evidence = report["evidence"]
    if not isinstance(evidence, dict) or set(evidence) != EVIDENCE_IDS:
        return ["evidence"]
    payloads: dict[str, dict[str, object]] = {}
    failures: list[str] = []
    for evidence_id in sorted(EVIDENCE_IDS):
        record = evidence[evidence_id]
        if not isinstance(record, dict) or set(record) != EVIDENCE_RECORD_KEYS:
            failures.append(f"evidence:{evidence_id}")
            continue
        path = Path(str(record.get("path", "")))
        checksum = str(record.get("sha256", ""))
        if SHA256_RE.fullmatch(checksum) is None:
            failures.append(f"evidence:{evidence_id}")
            continue
        try:
            payload = stable_payload(path, f"evidence {evidence_id}")
            if sha256_bytes(payload) != checksum:
                raise HermesError("checksum mismatch")
            payloads[evidence_id] = json_object(payload, f"evidence {evidence_id}")
        except HermesError:
            failures.append(f"evidence:{evidence_id}")
    if failures:
        return failures
    audit = payloads["audit_after"]
    if audit.get("status") != "pass" or audit.get("findings") != []:
        failures.append("evidence:audit_after")
    cutover = payloads["cutover_validation"]
    if set(cutover) != CUTOVER_EVIDENCE_KEYS or not (
        cutover.get("schema_version") == 1
        and cutover.get("status") == "ready"
        and cutover.get("failures") == []
        and cutover.get("vault_commit") == tested_commit
        and cutover.get("operational_as_of") == operational_as_of
        and cutover.get("upstream") == manifest["expected_upstream"]
        and cutover.get("origin_url") == manifest["expected_remote_url"]
        and cutover.get("manifest_sha256") == report["package_manifest_sha256"]
    ):
        failures.append("evidence:cutover_validation")
    retrieval = payloads["retrieval_smoke"]
    if set(retrieval) != RETRIEVAL_EVIDENCE_KEYS or not (
        retrieval.get("status") == "pass"
        and retrieval.get("as_of_commit") == tested_commit
        and retrieval.get("sync_state") == "clean"
        and retrieval.get("stale") is False
        and retrieval.get("fixture_mode") is False
        and retrieval.get("state_check") == "pass"
        and retrieval.get("operational_as_of") == operational_as_of
        and retrieval.get("upstream") == manifest["expected_upstream"]
        and retrieval.get("origin_url") == manifest["expected_remote_url"]
    ):
        failures.append("evidence:retrieval_smoke")
    else:
        queries = retrieval.get("queries")
        query_durations: dict[str, int] = {}
        if not isinstance(queries, list) or len(queries) != len(live_query_paths):
            failures.append("evidence:retrieval_smoke")
        else:
            for expected_id, query in zip(live_query_paths, queries, strict=True):
                expected_path = live_query_paths[expected_id]
                if not isinstance(query, dict) or set(query) != RETRIEVAL_QUERY_KEYS:
                    failures.append("evidence:retrieval_smoke")
                    break
                if not (
                    query.get("id") == expected_id
                    and query.get("selected_path") == expected_path
                    and query.get("opened_files") == [expected_path]
                    and query.get("matched") is True
                    and query.get("steps") == RETRIEVAL_STEPS
                    and type(query.get("duration_ms")) is int
                    and int(query["duration_ms"]) >= 0
                    and type(query.get("bytes_opened")) is int
                    and int(query["bytes_opened"]) > 0
                    and type(query.get("catalog_query_bytes")) is int
                    and 0 < int(query["catalog_query_bytes"]) <= MAX_CATALOG_QUERY_BYTES
                    and type(query.get("catalog_query_lines")) is int
                    and int(query["catalog_query_lines"]) == MAX_CATALOG_QUERY_LINES
                    and type(query.get("candidate_count")) is int
                    and 0 < int(query["candidate_count"]) <= MAX_CATALOG_CANDIDATES
                ):
                    failures.append("evidence:retrieval_smoke")
                    break
                query_durations[expected_id] = int(query["duration_ms"])
            report_timings = report.get("query_timings")
            expected_timings = [
                {"duration_ms": query_durations.get(query_id), "id": query_id}
                for query_id in live_query_paths
            ]
            if report_timings != expected_timings:
                failures.append("evidence:retrieval_smoke_timings")
    suite = payloads["test_suite"]
    if suite.get("status") != "pass" or suite.get("tested_commit") != tested_commit or suite.get("failures") != 0:
        failures.append("evidence:test_suite")
    for evidence_id in ("eclass_smoke", "whatsapp_smoke"):
        value = payloads[evidence_id]
        expected_query_id, query_type, subject_id = CHANNEL_QUERY_SPECS[evidence_id]
        expected_path = live_query_paths[expected_query_id]
        artifact_valid = False
        actual_query_bytes = 0
        actual_query_lines = 0
        actual_candidate_count = 0
        try:
            artifact_path = Path(str(value.get("catalog_query_artifact", "")))
            artifact_payload = stable_payload(
                artifact_path, f"evidence {evidence_id} catalog query artifact"
            )
            expected_query, expected_payload = query_catalog(
                package_root, query_type, subject_id, MAX_CATALOG_CANDIDATES
            )
            artifact_query = json_object(
                artifact_payload, f"evidence {evidence_id} catalog query artifact"
            )
            candidates = artifact_query.get("candidates")
            selected_path = (
                candidates[0].get("path")
                if isinstance(candidates, list)
                and candidates
                and isinstance(candidates[0], dict)
                else None
            )
            manifest_record = artifact_query.get("manifest")
            actual_query_bytes = len(artifact_payload)
            actual_query_lines = len(artifact_payload.splitlines())
            actual_candidate_count = len(candidates) if isinstance(candidates, list) else 0
            artifact_valid = (
                artifact_payload == expected_payload
                and artifact_query == expected_query
                and SHA256_RE.fullmatch(str(value.get("catalog_query_sha256"))) is not None
                and sha256_bytes(artifact_payload) == value.get("catalog_query_sha256")
                and isinstance(manifest_record, dict)
                and manifest_record.get("as_of") == operational_as_of
                and selected_path == expected_path
                and 0 < actual_query_bytes <= MAX_CATALOG_QUERY_BYTES
                and actual_query_lines == MAX_CATALOG_QUERY_LINES
                and 0 < actual_candidate_count <= MAX_CATALOG_CANDIDATES
            )
        except (HermesError, OSError, KeyError, TypeError, AttributeError):
            artifact_valid = False
        if set(value) != CHANNEL_SMOKE_KEYS or not (
            value.get("status") == "pass"
            and value.get("tested_commit") == tested_commit
            and value.get("operational_as_of") == operational_as_of
            and value.get("upstream") == manifest["expected_upstream"]
            and value.get("origin_url") == manifest["expected_remote_url"]
            and value.get("query_id") == expected_query_id
            and value.get("selected_path") == expected_path
            and value.get("opened_files") == [expected_path]
            and value.get("matched") is True
            and value.get("steps") == RETRIEVAL_STEPS
            and artifact_valid
            and type(value.get("catalog_query_bytes")) is int
            and int(value["catalog_query_bytes"]) == actual_query_bytes
            and type(value.get("catalog_query_lines")) is int
            and int(value["catalog_query_lines"]) == actual_query_lines
            and type(value.get("candidate_count")) is int
            and int(value["candidate_count"]) == actual_candidate_count
            and value.get("full_catalog_in_context") is False
            and value.get("filesystem_scan") is False
        ):
            failures.append(f"evidence:{evidence_id}")
    return failures


def main() -> int:
    args = parser().parse_args()
    failures: list[str] = []
    report_sha256: str | None = None
    bundle_sha256: str | None = None
    try:
        if COMMIT_RE.fullmatch(args.tested_commit) is None:
            raise HermesError("tested-commit must be a lowercase full Git SHA")
        if SHA256_RE.fullmatch(args.expected_report_sha256) is None:
            raise HermesError("expected-report-sha256 must be lowercase SHA-256")
        manifest, manifest_sha256 = load_manifest(args.manifest)
        operational_as_of = require_current_operational_as_of(
            args.as_of, manifest["operational_timezone"]
        )
        live_query_paths = load_live_query_paths(args.manifest)
        report_payload = stable_payload(args.report, "report")
        report_sha256 = sha256_bytes(report_payload)
        if report_sha256 != args.expected_report_sha256:
            failures.append("report_sha256")
        report = json_object(report_payload, "report")
        failures.extend(
            validate_report_shape(
                report,
                args.tested_commit,
                manifest,
                manifest_sha256,
                live_query_paths,
                operational_as_of,
            )
        )
        bundle_sha256 = validate_bundle(args.bundle, args.manifest, manifest_sha256)
        if report.get("prepare_bundle_sha256") != bundle_sha256:
            failures.append("prepare_bundle_sha256")
        if not failures:
            failures.extend(validate_production_and_backup(report, args.production_vault, args.hermes_home))
            failures.extend(
                validate_evidence(
                    report,
                    args.tested_commit,
                    live_query_paths,
                    operational_as_of,
                    manifest,
                    args.manifest.parent.parent.parent.absolute(),
                )
            )
    except (HermesError, KeyError, TypeError, OSError) as error:
        failures.append(f"invalid_input:{error}")
    failures = sorted(set(failures))
    output = {
        "bundle_sha256": bundle_sha256,
        "failures": failures,
        "operational_as_of": args.as_of,
        "report_sha256": report_sha256,
        "status": "ready" if not failures else "blocked",
    }
    print(json.dumps(output, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if not failures else 2


if __name__ == "__main__":
    sys.exit(main())
