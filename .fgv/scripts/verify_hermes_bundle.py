#!/usr/bin/env python3
"""Verify every file pinned by a Hermes phase bundle."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from hermes_common import HermesError, SHA256_RE, read_relative_file, safe_relative, sha256_bytes


ROOT_KEYS = {"schema_version", "phase", "package_manifest_sha256", "files"}
FILE_KEYS = {"path", "sha256"}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--root", required=True, type=Path)
    value.add_argument("--bundle", required=True)
    return value


def main() -> int:
    args = parser().parse_args()
    failures: list[dict[str, str]] = []
    phase: str | None = None
    try:
        if not args.root.is_absolute():
            raise HermesError("root must be absolute")
        bundle_relative = safe_relative(args.bundle, "bundle path")
        bundle_payload, issue = read_relative_file(args.root, bundle_relative)
        if issue or bundle_payload is None:
            raise HermesError(f"bundle cannot be trusted: {issue}")
        try:
            bundle = json.loads(bundle_payload.decode("utf-8"))
        except (UnicodeDecodeError, json.JSONDecodeError) as error:
            raise HermesError(f"bundle is not valid UTF-8 JSON: {error}") from error
        if not isinstance(bundle, dict) or set(bundle) != ROOT_KEYS:
            raise HermesError("bundle root schema is closed and invalid")
        if type(bundle["schema_version"]) is not int or bundle["schema_version"] != 1:
            raise HermesError("bundle schema_version must be 1")
        phase = bundle["phase"]
        if phase not in {"PREPARAR", "CUTOVER"}:
            raise HermesError("bundle phase is invalid")
        expected_manifest = bundle["package_manifest_sha256"]
        if not isinstance(expected_manifest, str) or SHA256_RE.fullmatch(expected_manifest) is None:
            raise HermesError("package manifest checksum is invalid")
        records = bundle["files"]
        if not isinstance(records, list) or not records:
            raise HermesError("bundle files must be a non-empty list")
        paths: list[str] = []
        manifest_seen = False
        for record in records:
            if not isinstance(record, dict) or set(record) != FILE_KEYS:
                raise HermesError("bundle file schema is closed and invalid")
            relative = safe_relative(record["path"], "bundle file path")
            expected = record["sha256"]
            if not isinstance(expected, str) or SHA256_RE.fullmatch(expected) is None:
                raise HermesError("bundle file checksum is invalid")
            paths.append(relative)
            payload, issue = read_relative_file(args.root, relative)
            if issue or payload is None:
                failures.append({"path": relative, "reason": issue or "missing"})
                continue
            actual = sha256_bytes(payload)
            if actual != expected:
                failures.append({"path": relative, "reason": "checksum_mismatch"})
            if relative == "30 Sistema/Hermes/hermes-manifest.json":
                manifest_seen = True
                if actual != expected_manifest:
                    failures.append({"path": relative, "reason": "package_manifest_pin_mismatch"})
        if paths != sorted(paths) or len(paths) != len(set(paths)):
            raise HermesError("bundle paths must be unique and sorted")
        if not manifest_seen:
            raise HermesError("bundle must pin hermes-manifest.json")
    except (HermesError, OSError, KeyError, TypeError) as error:
        failures.append({"path": "<bundle>", "reason": str(error)})
    failures.sort(key=lambda item: (item["path"], item["reason"]))
    report = {"failures": failures, "phase": phase, "status": "pass" if not failures else "blocked"}
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if not failures else 2


if __name__ == "__main__":
    sys.exit(main())
