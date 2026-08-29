#!/usr/bin/env python3
"""Execute a staged Hermes channel entrypoint and authenticate its query consumption."""

from __future__ import annotations

import argparse
import ast
import base64
import hashlib
import json
import os
from pathlib import Path
import re
import subprocess
import sys

from hermes_catalog_query import MAX_CANDIDATES, MAX_OUTPUT_BYTES, query_catalog
from hermes_common import (
    CANONICAL_BRANCH,
    CANONICAL_FETCH_REFSPEC,
    CANONICAL_OPERATIONAL_TIMEZONE,
    CANONICAL_REMOTE_URL,
    CANONICAL_UPSTREAM,
    COMMIT_RE,
    HermesError,
    authenticated_remote_branch_commit,
    read_relative_file,
    require_current_operational_as_of,
    safe_relative,
    sha256_bytes,
    validate_repository_binding,
    _python_command_findings,
)


CHANNEL_SPECS = {
    "eclass": ("material-eclass", "eclass_material", "estatistica-2"),
    "whatsapp": ("ultima-aula-matematica", "latest_class", "matematica-aplicada"),
}
MAX_OUTPUT_LINES = 1
ENTRYPOINT_ENVELOPE_KEYS = {
    "challenge",
    "consumed_stdout_sha256",
    "query_stdout_b64",
    "schema_version",
}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--channel-id", required=True, choices=sorted(CHANNEL_SPECS))
    value.add_argument("--entrypoint", required=True)
    value.add_argument("--hermes-home", required=True, type=Path)
    value.add_argument("--vault", required=True, type=Path)
    value.add_argument("--tested-commit", required=True)
    value.add_argument("--as-of", required=True)
    value.add_argument("--expected-path", required=True)
    value.add_argument("--artifact-out", required=True, type=Path)
    return value


def _call_name(node: ast.AST) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        prefix = _call_name(node.value)
        return f"{prefix}.{node.attr}" if prefix else node.attr
    return ""


def _literal_tokens(node: ast.AST | None) -> list[str | None] | None:
    if not isinstance(node, (ast.List, ast.Tuple)):
        return None
    return [item.value if isinstance(item, ast.Constant) and isinstance(item.value, str) else None for item in node.elts]


def _reachable_function_nodes(tree: ast.Module) -> tuple[set[str], dict[str, ast.FunctionDef | ast.AsyncFunctionDef]]:
    functions = {
        node.name: node
        for node in tree.body
        if isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef))
    }
    module_calls_main = any(
        any(isinstance(call, ast.Call) and _call_name(call.func) == "main" for call in ast.walk(node))
        for node in tree.body
        if not isinstance(node, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef))
    )
    if "main" not in functions or not module_calls_main:
        raise HermesError("channel entrypoint must call a local main function")
    reachable = {"main"}
    pending = ["main"]
    while pending:
        current = pending.pop()
        for call in (node for node in ast.walk(functions[current]) if isinstance(node, ast.Call)):
            name = _call_name(call.func)
            if name in functions and name not in reachable:
                reachable.add(name)
                pending.append(name)
    return reachable, functions


def audit_channel_entrypoint(payload: bytes) -> None:
    try:
        text = payload.decode("utf-8")
        tree = ast.parse(text)
    except (UnicodeDecodeError, SyntaxError) as error:
        raise HermesError(f"channel entrypoint is not valid UTF-8 Python: {error}") from error
    static_findings = _python_command_findings(text)
    if static_findings:
        raise HermesError(f"channel entrypoint static audit failed: {static_findings[0][1]}")
    reachable, functions = _reachable_function_nodes(tree)
    reachable_nodes = [functions[name] for name in sorted(reachable)]
    all_process_calls = [
        node
        for node in ast.walk(tree)
        if isinstance(node, ast.Call) and _call_name(node.func) == "subprocess.run"
    ]
    reachable_process_calls = [
        node
        for function in reachable_nodes
        for node in ast.walk(function)
        if isinstance(node, ast.Call) and _call_name(node.func) == "subprocess.run"
    ]
    if len(all_process_calls) != 1 or len(reachable_process_calls) != 1:
        raise HermesError("channel entrypoint needs one reachable bounded query call and no dead probes")
    tokens = _literal_tokens(
        reachable_process_calls[0].args[0] if reachable_process_calls[0].args else None
    )
    required_tokens = {
        ".fgv/scripts/hermes_catalog_query.py",
        "--vault",
        "--query-type",
        "--expected-catalog-sha256",
    }
    if tokens is None or not required_tokens <= set(tokens):
        raise HermesError("channel entrypoint query invocation is not a closed bounded command")
    forbidden_scan_calls = {"os.listdir", "os.scandir", "os.walk", "glob.glob", "Path.glob", "Path.rglob"}
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _call_name(node.func)
        if name in forbidden_scan_calls or name.endswith((".glob", ".rglob")):
            raise HermesError("channel entrypoint may not scan the filesystem")
        if name in {"open", "Path.open"} or name.endswith((".read_text", ".read_bytes", ".open")):
            source = ast.get_source_segment(text, node) or ""
            fragments = "".join(
                child.value
                for child in ast.walk(node)
                if isinstance(child, ast.Constant) and isinstance(child.value, str)
            )
            normalized = (source + fragments).replace("'", "").replace('"', "").replace(" ", "")
            if "catalog.jsonl" in normalized or "catalog+.jsonl" in normalized:
                raise HermesError("channel entrypoint may not read catalog.jsonl directly")


def _checkout(vault: Path, tested_commit: str) -> tuple[str, str]:
    head = subprocess.run(
        ["git", "-C", str(vault), "rev-parse", "HEAD"],
        text=True,
        capture_output=True,
        check=False,
    )
    status = subprocess.run(
        ["git", "-C", str(vault), "status", "--porcelain=v1", "--untracked-files=all"],
        text=True,
        capture_output=True,
        check=False,
    )
    if head.returncode != 0 or head.stdout.strip() != tested_commit or status.returncode != 0 or status.stdout:
        raise HermesError("channel smoke requires the exact clean tested commit")
    _, upstream, origin_url = validate_repository_binding(
        vault,
        CANONICAL_BRANCH,
        CANONICAL_UPSTREAM,
        CANONICAL_FETCH_REFSPEC,
        CANONICAL_REMOTE_URL,
    )
    if authenticated_remote_branch_commit(vault, CANONICAL_BRANCH) != tested_commit:
        raise HermesError("channel smoke tested commit is not the authenticated remote branch")
    validate_repository_binding(
        vault,
        CANONICAL_BRANCH,
        CANONICAL_UPSTREAM,
        CANONICAL_FETCH_REFSPEC,
        CANONICAL_REMOTE_URL,
    )
    return upstream, origin_url


def _catalog_pin(vault: Path, operational_as_of: str) -> tuple[str, bytes]:
    catalog, issue = read_relative_file(vault, "30 Sistema/Estado/catalog.jsonl")
    if issue or catalog is None:
        raise HermesError(f"channel smoke cannot trust catalog: {issue}")
    snapshot_payload, snapshot_issue = read_relative_file(
        vault, "30 Sistema/Estado/dashboard-snapshot.md"
    )
    if snapshot_issue or snapshot_payload is None:
        raise HermesError(f"channel smoke cannot trust dashboard snapshot: {snapshot_issue}")
    catalog_sha256 = sha256_bytes(catalog)
    snapshot = snapshot_payload.decode("utf-8")
    hash_match = re.search(
        r'^catalog_sha256:\s*["\']?sha256:([0-9a-f]{64})["\']?\s*$', snapshot, re.MULTILINE
    )
    as_of_match = re.search(
        r'^as_of:\s*["\']?([0-9]{4}-[0-9]{2}-[0-9]{2})["\']?\s*$', snapshot, re.MULTILINE
    )
    if (
        hash_match is None
        or hash_match.group(1) != catalog_sha256
        or as_of_match is None
        or as_of_match.group(1) != operational_as_of
    ):
        raise HermesError("channel smoke snapshot does not pin the current catalog and date")
    first = json.loads(catalog.decode("utf-8").splitlines()[0])
    if not isinstance(first, dict) or first.get("as_of") != operational_as_of:
        raise HermesError("channel smoke catalog as_of is stale")
    return catalog_sha256, snapshot_payload


def execute_channel_flow(
    *,
    channel_id: str,
    entrypoint_relative: str,
    hermes_home: Path,
    vault: Path,
    tested_commit: str,
    operational_as_of: str,
    expected_path: str,
) -> tuple[dict[str, object], bytes]:
    if channel_id not in CHANNEL_SPECS or COMMIT_RE.fullmatch(tested_commit) is None:
        raise HermesError("channel smoke inputs are invalid")
    entrypoint_relative = safe_relative(entrypoint_relative, "channel entrypoint")
    entrypoint_payload, issue = read_relative_file(hermes_home, entrypoint_relative)
    if issue or entrypoint_payload is None:
        raise HermesError(f"channel entrypoint cannot be trusted: {issue}")
    audit_channel_entrypoint(entrypoint_payload)
    entrypoint_sha256 = sha256_bytes(entrypoint_payload)
    upstream, origin_url = _checkout(vault, tested_commit)
    catalog_sha256, snapshot_payload = _catalog_pin(vault, operational_as_of)
    query_id, query_type, subject_id = CHANNEL_SPECS[channel_id]
    challenge = hashlib.sha256(
        f"fgv-hermes-channel-v1\0{channel_id}\0{tested_commit}\0{operational_as_of}\0{entrypoint_sha256}".encode()
    ).hexdigest()
    environment = os.environ.copy()
    environment.update(
        FGV_VAULT_ROOT=str(vault),
        FGV_HERMES_CHANNEL_CHALLENGE=challenge,
        FGV_HERMES_QUERY_TYPE=query_type,
        FGV_HERMES_SUBJECT_ID=subject_id,
        FGV_HERMES_EXPECTED_CATALOG_SHA256=catalog_sha256,
        PYTHONDONTWRITEBYTECODE="1",
    )
    result = subprocess.run(
        [sys.executable, str(hermes_home / entrypoint_relative), "--hermes-channel-smoke"],
        cwd=vault,
        capture_output=True,
        check=False,
        env=environment,
    )
    if result.returncode != 0 or result.stderr:
        raise HermesError("channel entrypoint smoke execution failed")
    try:
        envelope = json.loads(result.stdout.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise HermesError("channel entrypoint returned an invalid envelope") from error
    if not isinstance(envelope, dict) or set(envelope) != ENTRYPOINT_ENVELOPE_KEYS:
        raise HermesError("channel entrypoint envelope schema is closed and invalid")
    if envelope.get("schema_version") != 1 or envelope.get("challenge") != challenge:
        raise HermesError("channel entrypoint did not answer the runtime challenge")
    try:
        raw_query = base64.b64decode(str(envelope["query_stdout_b64"]), validate=True)
    except (ValueError, TypeError) as error:
        raise HermesError("channel entrypoint raw query encoding is invalid") from error
    raw_sha256 = sha256_bytes(raw_query)
    if envelope.get("consumed_stdout_sha256") != raw_sha256:
        raise HermesError("channel entrypoint did not bind consumption to raw query stdout")
    expected_query, expected_raw = query_catalog(
        vault, query_type, subject_id, MAX_CANDIDATES, catalog_sha256
    )
    if raw_query != expected_raw:
        raise HermesError("channel entrypoint did not consume the pinned bounded query stdout")
    candidates = expected_query.get("candidates")
    selected = candidates[0] if isinstance(candidates, list) and candidates else None
    selected_path = selected.get("path") if isinstance(selected, dict) else None
    if selected_path != expected_path:
        raise HermesError("channel entrypoint selected path does not match the canonical query")
    selected_payload, selected_issue = read_relative_file(vault, expected_path)
    expected_sha = str(selected.get("sha256", "")).removeprefix("sha256:") if isinstance(selected, dict) else ""
    if selected_issue or selected_payload is None or sha256_bytes(selected_payload) != expected_sha:
        raise HermesError("channel entrypoint selected artifact cannot be authenticated")
    if len(raw_query) > MAX_OUTPUT_BYTES or len(raw_query.splitlines()) != MAX_OUTPUT_LINES:
        raise HermesError("channel entrypoint query exceeded its output budget")
    if _catalog_pin(vault, operational_as_of) != (catalog_sha256, snapshot_payload):
        raise HermesError("channel catalog or snapshot changed during execution")
    final_upstream, final_origin = _checkout(vault, tested_commit)
    if (final_upstream, final_origin) != (upstream, origin_url):
        raise HermesError("channel entrypoint changed repository binding")
    receipt = {
        "candidate_count": len(candidates),
        "catalog_query_bytes": len(raw_query),
        "catalog_query_lines": len(raw_query.splitlines()),
        "catalog_query_sha256": raw_sha256,
        "challenge_sha256": sha256_bytes(challenge.encode()),
        "channel_id": channel_id,
        "consumed_stdout_sha256": raw_sha256,
        "entrypoint_path": entrypoint_relative,
        "entrypoint_sha256": entrypoint_sha256,
        "matched": True,
        "opened_files": [expected_path],
        "operational_as_of": operational_as_of,
        "origin_url": origin_url,
        "query_id": query_id,
        "selected_path": expected_path,
        "schema_version": 1,
        "status": "pass",
        "steps": [
            "entrypoint_challenge",
            "catalog_query",
            "consume_raw_stdout",
            "dashboard_snapshot",
            "checkout_status",
            "select_exact_path",
            "verify_sha256",
            "open_exact_file",
        ],
        "tested_commit": tested_commit,
        "upstream": upstream,
    }
    return receipt, raw_query


def write_new_artifact(path: Path, payload: bytes) -> None:
    if not path.is_absolute():
        raise HermesError("channel artifact path must be absolute")
    flags = os.O_WRONLY | os.O_CREAT | os.O_EXCL
    if hasattr(os, "O_NOFOLLOW"):
        flags |= os.O_NOFOLLOW
    descriptor = os.open(path, flags, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=False) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
    finally:
        os.close(descriptor)


def main() -> int:
    args = parser().parse_args()
    try:
        operational_as_of = require_current_operational_as_of(
            args.as_of, CANONICAL_OPERATIONAL_TIMEZONE
        )
        receipt, raw_query = execute_channel_flow(
            channel_id=args.channel_id,
            entrypoint_relative=args.entrypoint,
            hermes_home=args.hermes_home,
            vault=args.vault,
            tested_commit=args.tested_commit,
            operational_as_of=operational_as_of,
            expected_path=args.expected_path,
        )
        write_new_artifact(args.artifact_out, raw_query)
        receipt["catalog_query_artifact"] = str(args.artifact_out)
        print(json.dumps(receipt, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 0
    except (HermesError, OSError, KeyError, TypeError, json.JSONDecodeError) as error:
        print(json.dumps({"reason": str(error), "schema_version": 1, "status": "blocked"}, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
