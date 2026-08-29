#!/usr/bin/env python3
import argparse
import json
from pathlib import Path
import sys


SOURCE = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, SOURCE.as_posix())

from fgv_workflow.installer import apply_install, build_install_plan


def main() -> int:
    parser = argparse.ArgumentParser(
        description="Plan or apply adapter cutover with verified backups"
    )
    parser.add_argument("--manifest", type=Path, required=True)
    parser.add_argument("--codex-destination", type=Path, required=True)
    parser.add_argument("--claude-destination", type=Path, required=True)
    parser.add_argument("--backup-root", type=Path, required=True)
    parser.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    plan = build_install_plan(
        args.manifest,
        {"codex": args.codex_destination, "claude": args.claude_destination},
        backup_root=args.backup_root,
    )
    payload = {
        "mode": "apply" if args.apply else "dry-run",
        "operations": [
            {
                "runtime": item.runtime,
                "source": item.source.as_posix(),
                "destination": item.destination.as_posix(),
                "backup": item.backup.as_posix(),
                "destination_existed": item.destination_existed,
            }
            for item in plan.operations
        ],
    }
    print(json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True))
    if args.apply:
        apply_install(plan)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
