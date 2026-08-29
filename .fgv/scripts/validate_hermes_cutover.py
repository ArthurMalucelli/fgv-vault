#!/usr/bin/env python3
"""Fail-closed validation of a staged Hermes configuration."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from hermes_common import HermesError, audit_components, load_manifest, read_relative_file


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--hermes-home", required=True, type=Path)
    value.add_argument("--vault", required=True, type=Path)
    value.add_argument("--manifest", required=True, type=Path)
    return value


def main() -> int:
    args = parser().parse_args()
    failures: list[dict[str, object]] = []
    try:
        manifest, manifest_sha256 = load_manifest(args.manifest)
        if not args.hermes_home.is_absolute() or not args.vault.is_absolute():
            raise HermesError("hermes-home and vault must be absolute paths")
        audit = audit_components(args.hermes_home, manifest)
        failures.extend(audit["findings"])
        for component in manifest["components"]:
            payload, issue = read_relative_file(args.hermes_home, component["path"])
            if issue or payload is None:
                continue
            text = payload.decode("utf-8")
            for marker in component["required_markers"]:
                if marker not in text:
                    failures.append(
                        {
                            "file": component["path"],
                            "line": 0,
                            "rule": "missing_marker",
                            "severity": "error",
                            "detail": f"required marker is missing: {marker}",
                        }
                    )
            if "catalog.jsonl" in component["required_markers"] and "dashboard-snapshot.md" in component["required_markers"]:
                if text.find("catalog.jsonl") > text.find("dashboard-snapshot.md"):
                    failures.append(
                        {
                            "file": component["path"],
                            "line": 0,
                            "rule": "retrieval_order",
                            "severity": "error",
                            "detail": "catalog must be consulted before dashboard snapshot",
                        }
                    )
        failures.sort(key=lambda item: (str(item["file"]), int(item["line"]), str(item["rule"])))
        report = {
            "schema_version": 1,
            "status": "blocked" if failures else "ready",
            "manifest_sha256": manifest_sha256,
            "failures": failures,
        }
    except (HermesError, OSError, UnicodeDecodeError) as error:
        report = {
            "schema_version": 1,
            "status": "blocked",
            "manifest_sha256": None,
            "failures": [{"file": "<package>", "line": 0, "rule": "invalid_input", "severity": "error", "detail": str(error)}],
        }
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if report["status"] == "ready" else 2


if __name__ == "__main__":
    sys.exit(main())
