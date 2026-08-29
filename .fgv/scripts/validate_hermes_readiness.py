#!/usr/bin/env python3
"""Authorize Hermes cutover only for an exact READY report and package."""

from __future__ import annotations

import argparse
from datetime import datetime
import json
from pathlib import Path
import sys

from hermes_common import COMMIT_RE, HermesError, SHA256_RE, load_manifest, read_relative_file


REPORT_KEYS = {
    "schema_version",
    "timestamp_utc",
    "host_role",
    "recommendation",
    "production_commit",
    "tested_commit",
    "package_manifest_sha256",
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
}
BACKUP_KEYS = {"path", "sha256"}
UNTRACKED_KEYS = {"inventory_sha256", "backup_sha256", "preserved", "classified"}
FINDING_KEYS = {"required_remaining", "warnings"}
SMOKE_IDS = {"academic_retrieval", "eclass", "whatsapp"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--report", required=True, type=Path)
    value.add_argument("--tested-commit", required=True)
    value.add_argument("--manifest", required=True, type=Path)
    return value


def load_report(path: Path) -> dict[str, object]:
    payload, issue = read_relative_file(path.parent, path.name)
    if issue or payload is None:
        raise HermesError(f"report must be a stable regular non-symlink file: {issue}")
    try:
        value = json.loads(payload.decode("utf-8"))
    except (OSError, UnicodeDecodeError, json.JSONDecodeError) as error:
        raise HermesError(f"report is not valid UTF-8 JSON: {error}") from error
    if not isinstance(value, dict) or set(value) != REPORT_KEYS:
        raise HermesError("readiness report root schema is closed and invalid")
    return value


def validate(report: dict[str, object], expected_commit: str, manifest: dict[str, object], manifest_sha256: str) -> list[str]:
    failures: list[str] = []
    if type(report["schema_version"]) is not int or report["schema_version"] != 1:
        failures.append("schema_version")
    timestamp = report["timestamp_utc"]
    if not isinstance(timestamp, str) or not timestamp.endswith("Z"):
        failures.append("timestamp_utc")
    else:
        try:
            datetime.fromisoformat(timestamp.removesuffix("Z") + "+00:00")
        except ValueError:
            failures.append("timestamp_utc")
    if report["host_role"] != "hermes-vps":
        failures.append("host_role")
    if report["recommendation"] != "READY":
        failures.append("recommendation")
    if not COMMIT_RE.fullmatch(str(report["production_commit"])):
        failures.append("production_commit")
    if report["tested_commit"] != expected_commit:
        failures.append("tested_commit")
    if report["package_manifest_sha256"] != manifest_sha256:
        failures.append("package_manifest_sha256")

    backup = report["backup"]
    if not isinstance(backup, dict) or set(backup) != BACKUP_KEYS:
        failures.append("backup")
    elif not isinstance(backup["path"], str) or not backup["path"].startswith("/") or not SHA256_RE.fullmatch(str(backup["sha256"])):
        failures.append("backup")

    untracked = report["untracked"]
    if not isinstance(untracked, dict) or set(untracked) != UNTRACKED_KEYS:
        failures.append("untracked")
    elif (
        untracked["preserved"] is not True
        or untracked["classified"] is not True
        or not SHA256_RE.fullmatch(str(untracked["inventory_sha256"]))
        or not SHA256_RE.fullmatch(str(untracked["backup_sha256"]))
    ):
        failures.append("untracked")

    findings = report["findings"]
    if not isinstance(findings, dict) or set(findings) != FINDING_KEYS:
        failures.append("findings")
    elif type(findings["required_remaining"]) is not int or findings["required_remaining"] != 0:
        failures.append("required_findings")
    elif type(findings["warnings"]) is not int or findings["warnings"] < 0:
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
            if (
                not isinstance(item, dict)
                or set(item) != {"id", "duration_ms"}
                or not isinstance(item["id"], str)
                or not item["id"]
                or type(item["duration_ms"]) is not int
                or item["duration_ms"] < 0
            ):
                failures.append("query_timings")
                break
    if type(report["context_tokens"]) is not int or report["context_tokens"] < 0:
        failures.append("context_tokens")
    summary = report["diff_summary"]
    if not isinstance(summary, list) or any(not isinstance(item, str) or not item for item in summary):
        failures.append("diff_summary")
    return sorted(set(failures))


def main() -> int:
    args = parser().parse_args()
    try:
        if COMMIT_RE.fullmatch(args.tested_commit) is None:
            raise HermesError("tested-commit must be a lowercase 40-character Git SHA")
        manifest, manifest_sha256 = load_manifest(args.manifest)
        report = load_report(args.report)
        failures = validate(report, args.tested_commit, manifest, manifest_sha256)
    except (HermesError, KeyError, TypeError) as error:
        failures = [f"invalid_input:{error}"]
    output = {"failures": failures, "status": "ready" if not failures else "blocked"}
    print(json.dumps(output, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if not failures else 2


if __name__ == "__main__":
    sys.exit(main())
