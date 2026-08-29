#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import re
import stat
import sys
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from fgv_state.catalog import ACADEMIC_ROOTS, build_catalog, serialize_catalog
from fgv_state.config import Settings, load_settings
from fgv_state.dashboard import render_dashboard
from fgv_state.io import generation_lock, write_pair_if_changed


CATALOG = Path("30 Sistema/Estado/catalog.jsonl")
SNAPSHOT = Path("30 Sistema/Estado/dashboard-snapshot.md")
CONFIG = Path(".fgv/config/subjects.json")
AS_OF_RE = re.compile(r"^[0-9]{4}-[0-9]{2}-[0-9]{2}$")


@dataclass(frozen=True)
class GenerationResult:
    check: bool
    fresh: bool | None
    catalog_changed: bool
    snapshot_changed: bool


def validate_as_of(value: str) -> str:
    if not AS_OF_RE.fullmatch(value):
        raise ValueError(f"as_of must be canonical YYYY-MM-DD: {value!r}")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as exc:
        raise ValueError(f"as_of must be canonical YYYY-MM-DD: {value!r}") from exc
    if parsed.isoformat() != value:
        raise ValueError(f"as_of must be canonical YYYY-MM-DD: {value!r}")
    return value


def _require_directory(path: Path, label: str) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        raise ValueError(f"required regular directory missing: {label}") from exc
    if not stat.S_ISDIR(mode):
        raise ValueError(f"required regular directory missing: {label}")


def _require_file(path: Path, label: str) -> None:
    try:
        mode = path.lstat().st_mode
    except OSError as exc:
        raise ValueError(f"required regular file missing: {label}") from exc
    if not stat.S_ISREG(mode):
        raise ValueError(f"required regular file missing: {label}")


def validate_preconditions(vault: Path, settings: Settings) -> None:
    _require_file(vault / "00 Home/Tasks.md", "00 Home/Tasks.md")
    for relative in ACADEMIC_ROOTS:
        _require_directory(vault / relative, relative)
    for subject in settings.subjects:
        _require_directory(vault / subject.path, subject.path)
    _require_directory(vault / "30 Sistema/Estado", "30 Sistema/Estado")
    _require_file(vault / "30 Sistema/Estado/.generation.lock", "30 Sistema/Estado/.generation.lock")


def build_outputs(vault: Path, as_of: str) -> tuple[bytes, bytes]:
    validate_as_of(as_of)
    settings = load_settings(vault / CONFIG)
    validate_preconditions(vault, settings)
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


def generate(vault: Path, as_of: str, check: bool) -> GenerationResult:
    vault = vault.resolve()
    validate_as_of(as_of)
    validate_preconditions(vault, load_settings(vault / CONFIG))
    with generation_lock(vault):
        first = build_outputs(vault, as_of)
        second = build_outputs(vault, as_of)
        if first != second:
            raise ValueError("canonical inputs changed during state build")
        catalog, snapshot = second
        paths = vault / CATALOG, vault / SNAPSHOT
        if check:
            fresh = all(path.exists() and path.read_bytes() == payload for path, payload in zip(paths, (catalog, snapshot)))
            return GenerationResult(True, fresh, False, False)
        catalog_changed, snapshot_changed = write_pair_if_changed((paths[0], catalog), (paths[1], snapshot))
        return GenerationResult(False, None, catalog_changed, snapshot_changed)


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
        result = generate(vault, args.as_of, args.check)
        if result.check:
            print("state fresh" if result.fresh else "state stale")
            return 0 if result.fresh else 1
        print(f"catalog changed={'yes' if result.catalog_changed else 'no'}")
        print(f"snapshot changed={'yes' if result.snapshot_changed else 'no'}")
        return 0
    except Exception as exc:
        print(f"generation failed: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
