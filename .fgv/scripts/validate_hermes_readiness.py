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

from hermes_common import (
    COMMIT_RE,
    HermesError,
    SHA256_RE,
    canonical_json,
    load_manifest,
    read_relative_file,
    safe_relative,
    sha256_bytes,
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


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--report", required=True, type=Path)
    value.add_argument("--tested-commit", required=True)
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
    return sha256_bytes(payload)


def validate_report_shape(
    report: dict[str, object], expected_commit: str, manifest: dict[str, object], manifest_sha256: str
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
        for item in timings:
            if not isinstance(item, dict) or set(item) != {"id", "duration_ms"} or not isinstance(item["id"], str) or not item["id"] or type(item["duration_ms"]) is not int or item["duration_ms"] < 0:
                failures.append("query_timings")
                break
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


def validate_evidence(report: dict[str, object], tested_commit: str) -> list[str]:
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
    if cutover.get("status") != "ready" or cutover.get("vault_commit") != tested_commit:
        failures.append("evidence:cutover_validation")
    retrieval = payloads["retrieval_smoke"]
    if not (
        retrieval.get("status") == "pass"
        and retrieval.get("as_of_commit") == tested_commit
        and retrieval.get("sync_state") == "clean"
        and retrieval.get("stale") is False
        and retrieval.get("fixture_mode") is False
        and retrieval.get("state_check") == "pass"
    ):
        failures.append("evidence:retrieval_smoke")
    suite = payloads["test_suite"]
    if suite.get("status") != "pass" or suite.get("tested_commit") != tested_commit or suite.get("failures") != 0:
        failures.append("evidence:test_suite")
    for evidence_id in ("eclass_smoke", "whatsapp_smoke"):
        value = payloads[evidence_id]
        if value.get("status") != "pass" or value.get("tested_commit") != tested_commit:
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
        report_payload = stable_payload(args.report, "report")
        report_sha256 = sha256_bytes(report_payload)
        if report_sha256 != args.expected_report_sha256:
            failures.append("report_sha256")
        report = json_object(report_payload, "report")
        failures.extend(validate_report_shape(report, args.tested_commit, manifest, manifest_sha256))
        bundle_sha256 = validate_bundle(args.bundle, args.manifest, manifest_sha256)
        if report.get("prepare_bundle_sha256") != bundle_sha256:
            failures.append("prepare_bundle_sha256")
        if not failures:
            failures.extend(validate_production_and_backup(report, args.production_vault, args.hermes_home))
            failures.extend(validate_evidence(report, args.tested_commit))
    except (HermesError, KeyError, TypeError, OSError) as error:
        failures.append(f"invalid_input:{error}")
    failures = sorted(set(failures))
    output = {
        "bundle_sha256": bundle_sha256,
        "failures": failures,
        "report_sha256": report_sha256,
        "status": "ready" if not failures else "blocked",
    }
    print(json.dumps(output, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if not failures else 2


if __name__ == "__main__":
    sys.exit(main())
