#!/usr/bin/env python3
import argparse
from pathlib import Path
import sys


SOURCE = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, SOURCE.as_posix())

from fgv_workflow.adapters import stage_adapters


def main() -> int:
    parser = argparse.ArgumentParser(description="Stage FGV runtime adapters")
    parser.add_argument("--output", type=Path, required=True)
    args = parser.parse_args()
    result = stage_adapters(args.output)
    print(f"staged adapters: {result.codex}, {result.claude}")
    print("live installations modified: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
