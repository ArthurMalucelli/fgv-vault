#!/usr/bin/env python3
"""Exercise deterministic catalog-first Hermes retrieval without a model."""

from __future__ import annotations

import argparse
import json
import os
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys
import time

from hermes_common import COMMIT_RE, HermesError, read_relative_file, sha256_bytes


QUERY_TYPES = {
    "latest_class",
    "latest_transcript",
    "next_assessment",
    "eclass_material",
    "low_mastery_concept",
    "legacy_summary_name",
}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--vault", required=True, type=Path)
    value.add_argument("--queries", required=True, type=Path)
    value.add_argument("--expected-commit", required=True)
    value.add_argument("--fixture-mode", action="store_true")
    return value


def required_payload(root: Path, relative: str) -> bytes:
    payload, issue = read_relative_file(root, relative)
    if issue or payload is None:
        raise HermesError(f"cannot trust {relative}: {issue}")
    return payload


def load_catalog(payload: bytes) -> tuple[bytes, list[dict[str, object]]]:
    records: list[dict[str, object]] = []
    for number, line in enumerate(payload.decode("utf-8").splitlines(), 1):
        try:
            value = json.loads(line)
        except json.JSONDecodeError as error:
            raise HermesError(f"catalog line {number} is invalid JSON") from error
        if not isinstance(value, dict):
            raise HermesError(f"catalog line {number} is not an object")
        records.append(value)
    if not records or records[0].get("record_type") != "manifest" or records[0].get("schema_version") != 1:
        raise HermesError("catalog manifest is missing or unsupported")
    if sum(record.get("record_type") == "manifest" for record in records) != 1:
        raise HermesError("catalog must contain exactly one manifest")
    paths: set[str] = set()
    for record in records[1:]:
        if record.get("schema_version") != 1 or record.get("record_type") not in {"file", "task", "learning_state"}:
            raise HermesError("catalog contains unsupported record")
        if record.get("record_type") == "file":
            value = record.get("path")
            if not isinstance(value, str):
                raise HermesError("file record path is missing")
            pure = PurePosixPath(value)
            if pure.is_absolute() or ".." in pure.parts or pure.as_posix() != value or value in paths:
                raise HermesError("file record path is unsafe or duplicated")
            paths.add(value)
    return payload, records


def select_path(query: dict[str, object], records: list[dict[str, object]]) -> str | None:
    query_type = query["query_type"]
    subject_id = query.get("subject_id")
    files = [record for record in records if record.get("record_type") == "file"]
    if subject_id:
        files = [record for record in files if subject_id in record.get("subject_ids", [])]

    if query_type in {"latest_class", "legacy_summary_name"}:
        candidates = [record for record in files if PurePosixPath(str(record["path"])).name.startswith("Resumo")]
        candidates.sort(key=lambda item: (str(item.get("date") or ""), str(item["path"])), reverse=True)
        return str(candidates[0]["path"]) if candidates else None
    if query_type == "latest_transcript":
        candidates = [record for record in files if PurePosixPath(str(record["path"])).name.startswith("Transcrito")]
        candidates.sort(key=lambda item: (str(item.get("date") or ""), str(item["path"])), reverse=True)
        return str(candidates[0]["path"]) if candidates else None
    if query_type == "eclass_material":
        candidates = [record for record in files if "/Material/" in str(record["path"])]
        candidates.sort(key=lambda item: str(item["path"]))
        candidates.sort(key=lambda item: str(item.get("date") or ""), reverse=True)
        return str(candidates[0]["path"]) if candidates else None
    if query_type == "next_assessment":
        tasks = [
            record for record in records
            if record.get("record_type") == "task"
            and record.get("status") in {"todo", "in_progress"}
            and (not subject_id or subject_id in record.get("subject_ids", []))
            and record.get("due")
        ]
        tasks.sort(key=lambda item: (str(item["due"]), str(item.get("description", ""))))
        return str(tasks[0]["source_path"]) if tasks else None
    if query_type == "low_mastery_concept":
        learning = [
            record for record in records
            if record.get("record_type") == "learning_state"
            and record.get("last_status") in {"gap", "nao_sabe", "parcial"}
            and record.get("concept_path")
        ]
        learning.sort(key=lambda item: (str(item.get("last_status")), str(item.get("concept"))))
        return str(learning[0]["concept_path"]) if learning else None
    return None


def run_query(vault: Path, query: dict[str, object], records: list[dict[str, object]]) -> dict[str, object]:
    started = time.perf_counter_ns()
    steps = ["catalog", "dashboard_snapshot", "checkout_status", "select_exact_path"]
    selected = select_path(query, records)
    opened: list[str] = []
    integrity = False
    bytes_opened = 0
    if selected is not None:
        file_records = [item for item in records if item.get("record_type") == "file" and item.get("path") == selected]
        if len(file_records) != 1:
            raise HermesError(f"catalog does not have one file record for {selected}")
        expected_hash = str(file_records[0].get("sha256", "")).removeprefix("sha256:")
        payload = required_payload(vault, selected)
        integrity = len(expected_hash) == 64 and sha256_bytes(payload) == expected_hash
        steps.extend(("verify_sha256", "open_exact_file"))
        opened.append(selected)
        bytes_opened = len(payload)
    expected = query["expected_path"]
    elapsed_ms = max(0, (time.perf_counter_ns() - started) // 1_000_000)
    return {
        "bytes_opened": bytes_opened,
        "duration_ms": elapsed_ms,
        "id": query["id"],
        "matched": selected == expected and integrity,
        "opened_files": opened,
        "selected_path": selected,
        "steps": steps,
    }


def checkout_status(vault: Path) -> tuple[str, bool]:
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
    return head.stdout.strip(), bool(status.stdout)


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
        catalog_payload, records = load_catalog(required_payload(args.vault, "30 Sistema/Estado/catalog.jsonl"))
        snapshot = required_payload(args.vault, "30 Sistema/Estado/dashboard-snapshot.md").decode("utf-8")
        match = re.search(r'^catalog_sha256:\s*["\']?sha256:([0-9a-f]{64})["\']?\s*$', snapshot, re.MULTILINE)
        if match is None or match.group(1) != sha256_bytes(catalog_payload):
            raise HermesError("dashboard snapshot does not authenticate the catalog")
        actual_commit, dirty = checkout_status(args.vault)
        state_check = run_state_checks(args.vault, str(records[0].get("as_of", "")))
        commit_after_checks, dirty_after_checks = checkout_status(args.vault)
        if commit_after_checks != actual_commit:
            raise HermesError("state checks changed checkout HEAD")
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
            results.append(run_query(args.vault, query, records))
        stale = dirty or actual_commit != args.expected_commit
        passed = all(item["matched"] for item in results) and (args.fixture_mode or not stale)
        report = {
            "as_of_commit": actual_commit,
            "fixture_mode": args.fixture_mode,
            "queries": results,
            "stale": stale,
            "state_check": state_check,
            "sync_state": "stale" if stale else "clean",
            "status": "pass" if passed else "blocked",
        }
    except (HermesError, OSError, UnicodeDecodeError, json.JSONDecodeError, KeyError, TypeError) as error:
        report = {"as_of_commit": None, "fixture_mode": args.fixture_mode, "queries": [], "stale": True, "state_check": "blocked", "sync_state": "unknown", "status": "blocked", "reason": str(error)}
    print(json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0 if report["status"] == "pass" else 2


if __name__ == "__main__":
    sys.exit(main())
