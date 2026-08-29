#!/usr/bin/env python3
from pathlib import Path
import sys


SOURCE = Path(__file__).resolve().parents[1] / "src"
sys.path.insert(0, SOURCE.as_posix())

from fgv_workflow.cli import main


if __name__ == "__main__":
    raise SystemExit(main())
