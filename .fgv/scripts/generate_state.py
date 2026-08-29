#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from datetime import date
from pathlib import Path

from fgv_state.catalog import build_catalog, serialize_catalog
from fgv_state.config import load_settings
from fgv_state.dashboard import render_dashboard
from fgv_state.io import write_pair_if_changed


CATALOG = Path("30 Sistema/Estado/catalog.jsonl")
SNAPSHOT = Path("30 Sistema/Estado/dashboard-snapshot.md")
CONFIG = Path(".fgv/config/subjects.json")


def build_outputs(vault: Path, as_of: str) -> tuple[bytes, bytes]:
    date.fromisoformat(as_of)
    settings = load_settings(vault / CONFIG)
    build = build_catalog(vault, settings, as_of)
    catalog = serialize_catalog(build, settings)
    decoded = [json.loads(line) for line in catalog.decode("utf-8").splitlines()]
    if not decoded or decoded[0].get("record_type") != "manifest":
        raise ValueError("catalog manifest missing")
    if sum(record.get("record_type") == "manifest" for record in decoded) != 1:
        raise ValueError("catalog must contain exactly one manifest")
    if any(record.get("schema_version") != 1 for record in decoded):
        raise ValueError("catalog schema mismatch")
    catalog_sha = "sha256:" + hashlib.sha256(catalog).hexdigest()
    snapshot = render_dashboard(build.records, settings, as_of, build.build_fingerprint, catalog_sha).encode("utf-8")
    if not snapshot.endswith(b"\n") or f'catalog_sha256: "{catalog_sha}"'.encode() not in snapshot:
        raise ValueError("snapshot/catalog validation failed")
    return catalog, snapshot


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Generate deterministic FGV catalog and dashboard")
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--as-of", required=True)
    parser.add_argument("--check", action="store_true")
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    vault = args.vault.resolve()
    try:
        catalog, snapshot = build_outputs(vault, args.as_of)
        paths = vault / CATALOG, vault / SNAPSHOT
        if args.check:
            fresh = all(path.exists() and path.read_bytes() == payload for path, payload in zip(paths, (catalog, snapshot)))
            print("state fresh" if fresh else "state stale")
            return 0 if fresh else 1
        catalog_changed, snapshot_changed = write_pair_if_changed((paths[0], catalog), (paths[1], snapshot))
        print(f"catalog changed={'yes' if catalog_changed else 'no'}")
        print(f"snapshot changed={'yes' if snapshot_changed else 'no'}")
        return 0
    except Exception as exc:
        print(f"generation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
