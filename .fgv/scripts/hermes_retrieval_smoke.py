#!/usr/bin/env python3
"""Exercise deterministic catalog-first Hermes retrieval without a model."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import re
import subprocess
import sys
import time

from hermes_catalog_query import MAX_CANDIDATES, MAX_OUTPUT_BYTES, query_catalog
from hermes_common import (
    CANONICAL_OPERATIONAL_TIMEZONE,
    CANONICAL_REMOTE_URL,
    CANONICAL_UPSTREAM,
    COMMIT_RE,
    HermesError,
    read_relative_file,
    require_current_operational_as_of,
    sha256_bytes,
    validate_repository_binding,
)


QUERY_TYPES = {
    "latest_class",
    "latest_transcript",
    "next_assessment",
    "eclass_material",
    "low_mastery_concept",
    "legacy_summary_name",
}
MAX_OUTPUT_LINES = 1


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--vault", required=True, type=Path)
    value.add_argument("--queries", required=True, type=Path)
    value.add_argument("--expected-commit", required=True)
    value.add_argument("--as-of", required=True)
    value.add_argument("--fixture-mode", action="store_true")
    return value


def required_payload(root: Path, relative: str) -> bytes:
    payload, issue = read_relative_file(root, relative)
    if issue or payload is None:
        raise HermesError(f"cannot trust {relative}: {issue}")
    return payload


def load_catalog_manifest(payload: bytes) -> dict[str, object]:
    lines = payload.decode("utf-8").splitlines()
    if not lines:
        raise HermesError("catalog manifest is missing or unsupported")
    first_line = lines[0]
    try:
        manifest = json.loads(first_line)
    except json.JSONDecodeError as error:
        raise HermesError("catalog manifest is invalid JSON") from error
    if (
        not isinstance(manifest, dict)
        or manifest.get("record_type") != "manifest"
        or manifest.get("schema_version") != 1
    ):
        raise HermesError("catalog manifest is missing or unsupported")
    return manifest


def run_query(vault: Path, query: dict[str, object]) -> dict[str, object]:
    started = time.perf_counter_ns()
    _, query_payload = query_catalog(
        vault,
        str(query["query_type"]),
        str(query["subject_id"]) if query.get("subject_id") else None,
        MAX_CANDIDATES,
    )
    query_output = json.loads(query_payload.decode("utf-8"))
    candidates = query_output["candidates"]
    if not isinstance(candidates, list) or len(candidates) > MAX_CANDIDATES:
        raise HermesError("catalog query candidate budget failed")
    query_bytes = len(query_payload)
    query_lines = len(query_payload.splitlines())
    if query_bytes > MAX_OUTPUT_BYTES or query_lines > MAX_OUTPUT_LINES:
        raise HermesError("catalog query output budget failed")
    steps = ["catalog_query", "dashboard_snapshot", "checkout_status", "select_exact_path"]
    selected_candidate = candidates[0] if candidates else None
    selected = selected_candidate.get("path") if isinstance(selected_candidate, dict) else None
    opened: list[str] = []
    integrity = False
    bytes_opened = 0
    if selected is not None:
        expected_hash = str(selected_candidate.get("sha256", "")).removeprefix("sha256:")
        payload = required_payload(vault, selected)
        integrity = len(expected_hash) == 64 and sha256_bytes(payload) == expected_hash
        steps.extend(("verify_sha256", "open_exact_file"))
        opened.append(selected)
        bytes_opened = len(payload)
    expected = query["expected_path"]
    elapsed_ms = max(0, (time.perf_counter_ns() - started) // 1_000_000)
    return {
        "bytes_opened": bytes_opened,
        "candidate_count": len(candidates),
        "catalog_query_bytes": query_bytes,
        "catalog_query_lines": query_lines,
        "duration_ms": elapsed_ms,
        "id": query["id"],
        "matched": selected == expected and integrity,
        "opened_files": opened,
        "selected_path": selected,
        "steps": steps,
    }


def checkout_status(vault: Path) -> tuple[str, bool, str, str]:
    root = subprocess.run(
        ["git", "-C", str(vault), "rev-parse", "--show-toplevel"],
        text=True,
        capture_output=True,
        check=False,
    )
    if root.returncode != 0 or Path(root.stdout.strip()).resolve() != vault.resolve():
        raise HermesError("vault must be the root of a Git checkout")
    head = subprocess.run(
        ["git", "-C", str(vault), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=False,
    )
    if head.returncode != 0 or COMMIT_RE.fullmatch(head.stdout.strip()) is None:
        raise HermesError("checkout HEAD is invalid")
    status = subprocess.run(
        ["git", "-C", str(vault), "status", "--porcelain=v1", "--untracked-files=all"],
        text=True,
        capture_output=True,
        check=False,
    )
    if status.returncode != 0:
        raise HermesError("cannot inspect checkout state")
    _, upstream, origin_url = validate_repository_binding(
        vault, CANONICAL_UPSTREAM, CANONICAL_REMOTE_URL
    )
    upstream_commit = subprocess.run(
        ["git", "-C", str(vault), "rev-parse", CANONICAL_UPSTREAM],
        text=True,
        capture_output=True,
        check=False,
    )
    if upstream_commit.returncode != 0 or upstream_commit.stdout.strip() != head.stdout.strip():
        raise HermesError("checkout HEAD does not match the canonical upstream commit")
    return head.stdout.strip(), bool(status.stdout), upstream, origin_url


def run_state_checks(vault: Path, as_of: str) -> str:
    environment = os.environ.copy()
    environment["PYTHONDONTWRITEBYTECODE"] = "1"
    gates = (
        ("generate_state.py", ["--vault", str(vault), "--as-of", as_of, "--check"]),
        ("validate_vault.py", ["--vault", str(vault), "--as-of", as_of]),
    )
    for name, arguments in gates:
        gate = vault / ".fgv/scripts" / name
        if not gate.is_file() or gate.is_symlink():
            raise HermesError(f"{name} is required")
        result = subprocess.run(
            ["python3", str(gate), *arguments],
            text=True,
            capture_output=True,
            check=False,
            env=environment,
        )
        if result.returncode != 0:
            raise HermesError(f"{name} failed")
        try:
            validate_repository_binding(vault, CANONICAL_UPSTREAM, CANONICAL_REMOTE_URL)
        except HermesError as error:
            raise HermesError(f"{name} changed repository binding: {error}") from error
    return "pass"


def load_queries(args: argparse.Namespace) -> bytes:
    canonical = args.vault / "30 Sistema/Hermes/retrieval-queries.json"
    if args.fixture_mode:
        if "fixtures" not in args.queries.parts or args.queries.name != "retrieval-queries.json":
            raise HermesError("fixture mode requires an explicit fixture query file")
        payload, issue = read_relative_file(args.queries.parent, args.queries.name)
    else:
        if args.queries.absolute() != canonical.absolute():
            raise HermesError("live smoke requires 30 Sistema/Hermes/retrieval-queries.json")
        payload, issue = read_relative_file(args.vault, "30 Sistema/Hermes/retrieval-queries.json")
    if issue or payload is None:
        raise HermesError(f"cannot trust queries: {issue}")
    return payload


def main() -> int:
    args = parser().parse_args()
    try:
        if not args.vault.is_absolute() or COMMIT_RE.fullmatch(args.expected_commit) is None:
            raise HermesError("vault must be absolute and expected-commit must be a lowercase full SHA")
        operational_as_of = require_current_operational_as_of(
            args.as_of, CANONICAL_OPERATIONAL_TIMEZONE
        )
        catalog_payload = required_payload(args.vault, "30 Sistema/Estado/catalog.jsonl")
        catalog_manifest = load_catalog_manifest(catalog_payload)
        if catalog_manifest.get("as_of") != operational_as_of:
            raise HermesError("catalog as_of does not match operational as_of")
        snapshot = required_payload(args.vault, "30 Sistema/Estado/dashboard-snapshot.md").decode("utf-8")
        match = re.search(r'^catalog_sha256:\s*["\']?sha256:([0-9a-f]{64})["\']?\s*$', snapshot, re.MULTILINE)
        if match is None or match.group(1) != sha256_bytes(catalog_payload):
            raise HermesError("dashboard snapshot does not authenticate the catalog")
        snapshot_as_of = re.search(
            r"^as_of:\s*['\"]?([0-9]{4}-[0-9]{2}-[0-9]{2})['\"]?\s*$",
            snapshot,
            re.MULTILINE,
        )
        if snapshot_as_of is None or snapshot_as_of.group(1) != operational_as_of:
            raise HermesError("dashboard snapshot as_of does not match operational as_of")
        actual_commit, dirty, upstream, origin_url = checkout_status(args.vault)
        state_check = run_state_checks(args.vault, operational_as_of)
        commit_after_checks, dirty_after_checks, upstream_after, origin_after = checkout_status(args.vault)
        if commit_after_checks != actual_commit:
            raise HermesError("state checks changed checkout HEAD")
        if upstream_after != upstream or origin_after != origin_url:
            raise HermesError("state checks changed checkout Git binding")
        dirty = dirty or dirty_after_checks
        query_payload = load_queries(args)
        queries = json.loads(query_payload.decode("utf-8"))
        if not isinstance(queries, list) or not queries:
            raise HermesError("queries must be a non-empty JSON list")
        results: list[dict[str, object]] = []
        seen_ids: set[str] = set()
        for query in queries:
            if not isinstance(query, dict) or set(query) not in ({"id", "question", "query_type", "expected_path"}, {"id", "question", "query_type", "subject_id", "expected_path"}):
                raise HermesError("query schema is invalid")
            if query["query_type"] not in QUERY_TYPES or not isinstance(query["id"], str) or query["id"] in seen_ids:
                raise HermesError("query id or type is invalid")
            seen_ids.add(query["id"])
            results.append(run_query(args.vault, query))
        stale = dirty or actual_commit != args.expected_commit
        passed = all(item["matched"] for item in results) and (args.fixture_mode or not stale)
        report = {
            "as_of_commit": actual_commit,
            "fixture_mode": args.fixture_mode,
            "operational_as_of": operational_as_of,
            "origin_url": origin_url,
            "queries": results,
            "stale": stale,
            "state_check": state_check,
            "sync_state": "stale" if stale else "clean",
            "status": "pass" if passed else "blocked",
            "upstream": upstream,
        }
    except (HermesError, OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        report = {"as_of_commit": None, "fixture_mode": args.fixture_mode, "operational_as_of": args.as_of, "origin_url": None, "queries": [], "stale": True, "state_check": "blocked", "sync_state": "unknown", "status": "blocked", "upstream": None, "reason": str(error)}
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if report["status"] == "pass" else 2


if __name__ == "__main__":
    sys.exit(main())
