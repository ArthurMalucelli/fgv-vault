#!/usr/bin/env python3
"""Read-only compatibility audit for a Hermes home."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

from hermes_common import HermesError, atomic_json_write, audit_components, load_manifest


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--hermes-home", required=True, type=Path)
    value.add_argument("--vault", required=True, type=Path)
    value.add_argument("--manifest", required=True, type=Path)
    value.add_argument("--json-out", required=True, type=Path)
    return value


def main() -> int:
    args = parser().parse_args()
    try:
        manifest, manifest_sha256 = load_manifest(args.manifest)
        if not args.hermes_home.is_absolute() or not args.vault.is_absolute():
            raise HermesError("hermes-home and vault must be absolute paths")
        report = audit_components(args.hermes_home, manifest)
        report["manifest_sha256"] = manifest_sha256
        atomic_json_write(args.json_out, report)
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0 if report["status"] == "pass" else 2
    except HermesError as error:
        report = {
            "schema_version": 1,
            "status": "blocked",
            "components": [],
            "findings": [
                {
                    "detail": str(error),
                    "file": "<package>",
                    "line": 0,
                    "rule": "invalid_input",
                    "severity": "error",
                }
            ],
        }
        atomic_json_write(args.json_out, report)
        print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 2


if __name__ == "__main__":
    sys.exit(main())
