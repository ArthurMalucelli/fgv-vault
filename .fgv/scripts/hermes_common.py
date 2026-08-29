#!/usr/bin/env python3
"""Shared validation primitives for the versioned Hermes package."""

from __future__ import annotations

import ast
from datetime import date, datetime
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import shlex
import stat
import subprocess
from typing import Any
from urllib.parse import urlsplit, urlunsplit
from zoneinfo import ZoneInfo, ZoneInfoNotFoundError


class HermesError(ValueError):
    """Input cannot be trusted by the Hermes package."""


MANIFEST_KEYS = {
    "schema_version",
    "package_id",
    "contract_version",
    "vps_git_owner",
    "operational_timezone",
    "expected_branch",
    "expected_upstream",
    "expected_fetch_refspec",
    "expected_remote_url",
    "canonical_paths",
    "retrieval_order",
    "required_response_fields",
    "components",
    "legacy_subject_folders",
    "forbidden_scan_roots",
}
COMPONENT_KEYS = {"id", "path", "classification", "format", "required_markers"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")
CANONICAL_OPERATIONAL_TIMEZONE = "America/Sao_Paulo"
CANONICAL_BRANCH = "codex/vault-plan-b"
CANONICAL_UPSTREAM = "origin/codex/vault-plan-b"
CANONICAL_FETCH_REFSPEC = "+refs/heads/codex/vault-plan-b:refs/remotes/origin/codex/vault-plan-b"
CANONICAL_REMOTE_URL = "https://github.com/ArthurMalucelli/fgv-vault.git"


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


def current_operational_as_of(timezone_name: str = CANONICAL_OPERATIONAL_TIMEZONE) -> str:
    try:
        zone = ZoneInfo(timezone_name)
    except ZoneInfoNotFoundError as error:
        raise HermesError("operational timezone is unavailable") from error
    return datetime.now(zone).date().isoformat()


def require_current_operational_as_of(value: object, timezone_name: str) -> str:
    if not isinstance(value, str):
        raise HermesError("operational as_of must be an ISO date")
    try:
        parsed = date.fromisoformat(value)
    except ValueError as error:
        raise HermesError("operational as_of must be an ISO date") from error
    normalized = parsed.isoformat()
    if normalized != current_operational_as_of(timezone_name):
        raise HermesError("operational as_of is stale for America/Sao_Paulo")
    return normalized


def normalize_remote_url(value: object) -> str:
    if not isinstance(value, str) or not value or any(character in value for character in "\r\n\x00"):
        raise HermesError("origin remote URL is invalid")
    try:
        parsed = urlsplit(value)
        parsed_port = parsed.port
    except ValueError as error:
        raise HermesError("origin remote URL is invalid") from error
    if (
        parsed.scheme.lower() != "https"
        or (parsed.hostname or "").lower() != "github.com"
        or parsed_port is not None
        or parsed.username is not None
        or parsed.password is not None
        or parsed.query
        or parsed.fragment
    ):
        raise HermesError("origin remote URL is not a sanitized GitHub HTTPS URL")
    path = parsed.path.rstrip("/")
    if not path.endswith(".git"):
        path += ".git"
    return urlunsplit(("https", "github.com", path, "", ""))


def _git(vault: Path, *arguments: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(vault), *arguments],
        text=True,
        capture_output=True,
        check=False,
    )


def _git_config_values(vault: Path, key: str) -> list[str]:
    result = _git(vault, "config", "--null", "--get-all", key)
    if result.returncode == 1:
        return []
    if result.returncode != 0:
        raise HermesError(f"Git config {key} is unavailable")
    values = result.stdout.split("\0")
    if values and values[-1] == "":
        values.pop()
    if not values or any(not value for value in values):
        raise HermesError(f"Git config {key} is invalid")
    return values


def validate_repository_binding(
    vault: Path,
    expected_branch: str,
    expected_upstream: str,
    expected_fetch_refspec: str,
    expected_remote_url: str,
) -> tuple[str, str, str]:
    branch_result = _git(vault, "symbolic-ref", "--quiet", "--short", "HEAD")
    branch = branch_result.stdout.strip()
    if branch_result.returncode != 0 or branch != expected_branch:
        raise HermesError("checkout branch does not match the canonical branch")
    branch_remotes = _git_config_values(vault, f"branch.{expected_branch}.remote")
    if branch_remotes != ["origin"]:
        raise HermesError("checkout branch remote does not match origin")
    branch_merges = _git_config_values(vault, f"branch.{expected_branch}.merge")
    expected_merge = f"refs/heads/{expected_branch}"
    if branch_merges != [expected_merge]:
        raise HermesError("checkout branch source does not match the canonical branch")
    fetch_refspecs = _git_config_values(vault, "remote.origin.fetch")
    if fetch_refspecs != [expected_fetch_refspec]:
        raise HermesError("origin fetch refspec is not uniquely canonical")
    if expected_upstream != f"origin/{expected_branch}":
        raise HermesError("expected upstream is inconsistent with the canonical branch")
    expected_refspec = f"+refs/heads/{expected_branch}:refs/remotes/{expected_upstream}"
    if expected_fetch_refspec != expected_refspec:
        raise HermesError("expected fetch refspec is inconsistent with the canonical upstream")
    upstream_result = _git(
        vault, "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"
    )
    upstream = upstream_result.stdout.strip()
    if upstream_result.returncode != 0 or upstream != expected_upstream:
        raise HermesError("checkout upstream does not match the canonical upstream")

    origin_urls = _git_config_values(vault, "remote.origin.url")
    if len(origin_urls) != 1:
        raise HermesError("origin must have exactly one fetch URL")
    origin_url = normalize_remote_url(origin_urls[0])
    if origin_url != expected_remote_url:
        raise HermesError("origin remote URL does not match the canonical remote")
    push_urls = _git_config_values(vault, "remote.origin.pushurl")
    if len(push_urls) > 1:
        raise HermesError("origin must have at most one push URL")
    if push_urls and normalize_remote_url(push_urls[0]) != expected_remote_url:
        raise HermesError("origin push URL does not match the canonical remote")

    rewrites = _git(vault, "config", "--null", "--get-regexp", r"^url\.")
    if rewrites.returncode not in {0, 1}:
        raise HermesError("Git URL rewrite configuration is unavailable")
    for record in rewrites.stdout.split("\0"):
        key = record.partition("\n")[0].casefold()
        if key.endswith(".insteadof") or key.endswith(".pushinsteadof"):
            raise HermesError("Git URL rewrites are forbidden")

    for key in (f"branch.{branch}.pushRemote", "remote.pushDefault"):
        if _git_config_values(vault, key):
            raise HermesError("Git push routing overrides are forbidden")

    for arguments, label in (
        (("remote", "get-url", "--all", "origin"), "fetch"),
        (("remote", "get-url", "--push", "--all", "origin"), "push"),
    ):
        result = _git(vault, *arguments)
        urls = result.stdout.splitlines()
        if (
            result.returncode != 0
            or len(urls) != 1
            or normalize_remote_url(urls[0]) != expected_remote_url
        ):
            raise HermesError(f"origin effective {label} URL is not canonical")
    return branch, upstream, origin_url


def authenticated_remote_branch_commit(vault: Path, expected_branch: str) -> str:
    reference = f"refs/heads/{expected_branch}"
    result = _git(vault, "ls-remote", "--exit-code", "origin", reference)
    if result.returncode != 0:
        raise HermesError("canonical remote branch is unavailable")
    lines = result.stdout.splitlines()
    if len(lines) != 1:
        raise HermesError("canonical remote branch response is ambiguous")
    fields = lines[0].split()
    if len(fields) != 2 or COMMIT_RE.fullmatch(fields[0]) is None or fields[1] != reference:
        raise HermesError("canonical remote branch response is invalid")
    return fields[0]


def safe_relative(value: object, label: str) -> str:
    if not isinstance(value, str) or not value or "\\" in value or "\x00" in value:
        raise HermesError(f"{label} must be a non-empty POSIX relative path")
    path = PurePosixPath(value)
    if path.is_absolute() or path.as_posix() != value or ".." in path.parts or "." in path.parts:
        raise HermesError(f"{label} is unsafe")
    return value


def load_manifest(path: Path) -> tuple[dict[str, Any], str]:
    payload, issue = read_relative_file(path.parent, path.name)
    if issue or payload is None:
        raise HermesError(f"manifest must be a stable regular non-symlink file: {issue}")
    try:
        value = json.loads(payload.decode("utf-8"))
    except (UnicodeDecodeError, json.JSONDecodeError) as error:
        raise HermesError(f"manifest is not valid UTF-8 JSON: {error}") from error
    if not isinstance(value, dict) or set(value) != MANIFEST_KEYS:
        raise HermesError("manifest root schema is closed and invalid")
    if type(value["schema_version"]) is not int or value["schema_version"] != 1:
        raise HermesError("manifest schema_version must be 1")
    if type(value["contract_version"]) is not int or value["contract_version"] != 1:
        raise HermesError("manifest contract_version must be 1")
    if value["vps_git_owner"] != "fgv-sync":
        raise HermesError("manifest vps_git_owner must be fgv-sync")
    if value["operational_timezone"] != CANONICAL_OPERATIONAL_TIMEZONE:
        raise HermesError("manifest operational_timezone is not canonical")
    if value["expected_branch"] != CANONICAL_BRANCH:
        raise HermesError("manifest expected_branch is not canonical")
    if value["expected_upstream"] != CANONICAL_UPSTREAM:
        raise HermesError("manifest expected_upstream is not canonical")
    if value["expected_fetch_refspec"] != CANONICAL_FETCH_REFSPEC:
        raise HermesError("manifest expected_fetch_refspec is not canonical")
    if (
        value["expected_remote_url"] != CANONICAL_REMOTE_URL
        or normalize_remote_url(value["expected_remote_url"]) != CANONICAL_REMOTE_URL
    ):
        raise HermesError("manifest expected_remote_url is not canonical")
    components = value["components"]
    if not isinstance(components, list) or not components:
        raise HermesError("manifest components must be a non-empty list")
    ids: set[str] = set()
    paths: set[str] = set()
    for component in components:
        if not isinstance(component, dict) or set(component) != COMPONENT_KEYS:
            raise HermesError("component schema is closed and invalid")
        component_id = component["id"]
        if not isinstance(component_id, str) or not component_id or component_id in ids:
            raise HermesError("component id is invalid or duplicated")
        ids.add(component_id)
        relative = safe_relative(component["path"], "component path")
        if relative in paths:
            raise HermesError("component path is duplicated")
        paths.add(relative)
        if component["classification"] not in {"required", "optional", "discovered"}:
            raise HermesError("component classification is invalid")
        if component["format"] not in {"python", "markdown", "cron_json"}:
            raise HermesError("component format is invalid")
        markers = component["required_markers"]
        if not isinstance(markers, list) or any(not isinstance(item, str) or not item for item in markers):
            raise HermesError("component required_markers are invalid")
    for field in ("retrieval_order", "required_response_fields", "legacy_subject_folders", "forbidden_scan_roots"):
        values = value[field]
        if not isinstance(values, list) or any(not isinstance(item, str) or not item for item in values):
            raise HermesError(f"manifest {field} is invalid")
    if not isinstance(value["canonical_paths"], dict):
        raise HermesError("manifest canonical_paths must be an object")
    return value, sha256_bytes(payload)


def component_path(root: Path, relative: str) -> tuple[Path | None, str | None]:
    """Resolve a listed component without following any symlink."""
    safe_relative(relative, "component path")
    try:
        root_resolved = root.resolve(strict=True)
    except OSError:
        return None, "missing_root"
    current = root_resolved
    parts = PurePosixPath(relative).parts
    for index, part in enumerate(parts):
        current = current / part
        try:
            mode = current.lstat().st_mode
        except FileNotFoundError:
            return None, "missing_component"
        except OSError:
            return None, "unreadable_component"
        if stat.S_ISLNK(mode):
            return None, "unsafe_path"
        if index < len(parts) - 1 and not stat.S_ISDIR(mode):
            return None, "unsafe_path"
    if not current.is_file():
        return None, "unsafe_path"
    try:
        if not current.resolve(strict=True).is_relative_to(root_resolved):
            return None, "unsafe_path"
    except OSError:
        return None, "unsafe_path"
    return current, None


def read_relative_file(root: Path, relative: str) -> tuple[bytes | None, str | None]:
    """Read through pinned directory descriptors and reject concurrent changes."""
    try:
        safe_relative(relative, "component path")
    except HermesError:
        return None, "unsafe_path"
    directory_flags = os.O_RDONLY | os.O_DIRECTORY | os.O_NOFOLLOW
    file_flags = os.O_RDONLY | os.O_NOFOLLOW
    descriptor = -1
    try:
        descriptor = os.open(root, directory_flags)
        for part in PurePosixPath(relative).parts[:-1]:
            child = os.open(part, directory_flags, dir_fd=descriptor)
            os.close(descriptor)
            descriptor = child
        file_descriptor = os.open(PurePosixPath(relative).name, file_flags, dir_fd=descriptor)
        os.close(descriptor)
        descriptor = file_descriptor
        before = os.fstat(descriptor)
        if not stat.S_ISREG(before.st_mode):
            return None, "unsafe_path"
        chunks: list[bytes] = []
        while True:
            chunk = os.read(descriptor, 1024 * 1024)
            if not chunk:
                break
            chunks.append(chunk)
        after = os.fstat(descriptor)
        identity_before = (before.st_dev, before.st_ino, before.st_size, before.st_mtime_ns, before.st_ctime_ns)
        identity_after = (after.st_dev, after.st_ino, after.st_size, after.st_mtime_ns, after.st_ctime_ns)
        if identity_before != identity_after:
            return None, "concurrent_change"
        return b"".join(chunks), None
    except FileNotFoundError:
        return None, "missing_component"
    except (NotADirectoryError, PermissionError, OSError):
        return None, "unsafe_path"
    finally:
        if descriptor >= 0:
            os.close(descriptor)


def atomic_json_write(path: Path, value: object) -> None:
    payload = (json.dumps(value, ensure_ascii=False, sort_keys=True, indent=2) + "\n").encode("utf-8")
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.parent / f".{path.name}.{os.getpid()}.tmp"
    descriptor = os.open(temporary, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    try:
        with os.fdopen(descriptor, "wb", closefd=True) as handle:
            handle.write(payload)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        try:
            temporary.unlink()
        except FileNotFoundError:
            pass


def _call_name(node: ast.AST) -> str:
    parts: list[str] = []
    current = node
    while isinstance(current, ast.Attribute):
        parts.append(current.attr)
        current = current.value
    if isinstance(current, ast.Name):
        parts.append(current.id)
    return ".".join(reversed(parts))


def _literal_string(node: ast.AST | None) -> str | None:
    if isinstance(node, ast.Constant) and isinstance(node.value, str):
        return node.value
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Add):
        left = _literal_string(node.left)
        right = _literal_string(node.right)
        return left + right if left is not None and right is not None else None
    if isinstance(node, ast.JoinedStr):
        values = [_literal_string(value) for value in node.values]
        return "".join(str(value) for value in values) if all(value is not None for value in values) else None
    return None


def _shell_tokens(command: str) -> list[str]:
    lexer = shlex.shlex(command, posix=True, punctuation_chars=";&|()")
    lexer.commenters = ""
    lexer.whitespace_split = True
    return list(lexer)


def _command_segments(tokens: list[str]) -> list[list[str]]:
    separators = {";", "&&", "||", "|", "&", "(", ")"}
    segments: list[list[str]] = []
    current: list[str] = []
    for token in tokens:
        if token in separators:
            if current:
                segments.append(current)
                current = []
        else:
            current.append(token)
    if current:
        segments.append(current)
    return segments


def _command_index(tokens: list[str]) -> int | None:
    index = 0
    if tokens and tokens[0] == "$":
        index = 1
    while index < len(tokens):
        token = tokens[index]
        if re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", token):
            index += 1
            continue
        if token == "env":
            index += 1
            while index < len(tokens) and (
                tokens[index].startswith("-")
                or re.fullmatch(r"[A-Za-z_][A-Za-z0-9_]*=.*", tokens[index])
            ):
                index += 1
            continue
        if token in {"command", "exec"}:
            index += 1
            continue
        if token == "sudo":
            index += 1
            while index < len(tokens) and tokens[index].startswith("-"):
                index += 1
            continue
        return index
    return None


def _git_subcommand(tokens: list[str], index: int) -> str | None:
    cursor = index + 1
    while cursor < len(tokens):
        token = tokens[cursor]
        if token in {"-C", "--git-dir", "--work-tree"}:
            cursor += 2
            continue
        if token.startswith("-"):
            cursor += 1
            continue
        return token
    return None


def _sensitive_delete_target(token: str) -> bool:
    lowered = token.casefold()
    return any(
        marker in lowered
        for marker in (
            "/root/vault",
            "/root/.hermes",
            "fgv_vault_root",
            "hermes_home",
            "${vault",
            "$vault",
        )
    )


def _inspect_command_tokens(tokens: list[str]) -> list[tuple[str, str]]:
    findings: list[tuple[str, str]] = []
    for segment in _command_segments(tokens):
        index = _command_index(segment)
        if index is None:
            continue
        executable = segment[index]
        executable_name = PurePosixPath(executable).name
        if executable != "fgv-sync" and executable_name == "fgv-sync":
            findings.append(("nonliteral_sync", "sync command must be the literal fgv-sync executable"))
        if executable in {"sh", "bash", "zsh"} and "-c" in segment[index + 1 :]:
            command_index = segment.index("-c", index + 1) + 1
            if command_index < len(segment):
                try:
                    findings.extend(_inspect_command_tokens(_shell_tokens(segment[command_index])))
                except ValueError:
                    findings.append(("invalid_shell", "nested shell command is not tokenizable"))
        if re.fullmatch(r"python(?:3(?:\.\d+)?)?", executable_name) and "-c" in segment[index + 1 :]:
            code_index = segment.index("-c", index + 1) + 1
            if code_index >= len(segment):
                findings.append(("dynamic_command", "python -c code is missing"))
            else:
                findings.extend(
                    (rule, f"python -c: {detail}")
                    for _, rule, detail in _python_command_findings(segment[code_index])
                )
        if executable_name == "git":
            findings.append(("unauthorized_git", "Git command outside literal fgv-sync"))
            if _git_subcommand(segment, index) in {"reset", "clean"}:
                findings.append(("destructive_command", "destructive Git command"))
        if executable_name in {"rm", "rmdir", "unlink"} and any(
            _sensitive_delete_target(token) for token in segment[index + 1 :]
        ):
            findings.append(("destructive_command", "destructive command targets vault or Hermes"))
    return findings


def _resolve_symbol(name: str, symbols: dict[str, str]) -> str:
    current = name
    seen: set[str] = set()
    while current and current not in seen:
        seen.add(current)
        if current in symbols:
            current = symbols[current]
            continue
        first, separator, rest = current.partition(".")
        if first in symbols:
            current = symbols[first] + (separator + rest if separator else "")
            continue
        break
    return current


def _callable_expression_name(node: ast.AST, symbols: dict[str, str]) -> str:
    raw = _call_name(node)
    if isinstance(node, ast.Call) and _call_name(node.func) == "getattr" and len(node.args) >= 2:
        owner = _resolve_symbol(_call_name(node.args[0]), symbols)
        attribute = _literal_string(node.args[1])
        if owner and attribute:
            raw = f"{owner}.{attribute}"
    if isinstance(node, ast.Attribute) and isinstance(node.value, ast.Call):
        importer = node.value
        if _call_name(importer.func) == "__import__" and importer.args:
            module = _literal_string(importer.args[0])
            if module in {"os", "pathlib", "shutil", "subprocess"}:
                raw = f"{module}.{node.attr}"
    return _resolve_symbol(raw, symbols)


def _assigned_names(node: ast.AST) -> list[str]:
    if isinstance(node, ast.Name):
        return [node.id]
    if isinstance(node, ast.Attribute):
        name = _call_name(node)
        return [name] if name else []
    if isinstance(node, (ast.Tuple, ast.List)):
        return [name for item in node.elts for name in _assigned_names(item)]
    return []


def _path_expression(
    node: ast.AST | None,
    symbols: dict[str, str],
    path_values: dict[str, str | None],
) -> tuple[bool, str | None]:
    literal = _literal_string(node)
    if literal is not None:
        return True, literal
    if isinstance(node, ast.Name) and node.id in path_values:
        return True, path_values[node.id]
    if isinstance(node, ast.Call):
        constructor = _callable_expression_name(node.func, symbols)
        if constructor in {"pathlib.Path", "pathlib.PurePath", "pathlib.PurePosixPath"}:
            if not node.args:
                return True, None
            return _path_expression(node.args[0], symbols, path_values)
    if isinstance(node, ast.BinOp) and isinstance(node.op, ast.Div):
        left_is_path, left = _path_expression(node.left, symbols, path_values)
        right = _literal_string(node.right)
        if left_is_path:
            if left is None or right is None:
                return True, None
            return True, str(PurePosixPath(left) / right)
    return False, None


def _dynamic_callable_kind(node: ast.AST, symbols: dict[str, str]) -> str | None:
    if not isinstance(node, ast.Call) or _call_name(node.func) != "getattr" or len(node.args) < 2:
        return None
    owner = _resolve_symbol(_call_name(node.args[0]), symbols)
    attribute = _literal_string(node.args[1])
    if owner in {"os", "shutil", "subprocess"}:
        return "process"
    is_path, _ = _path_expression(node.args[0], symbols, {})
    if is_path and (attribute is None or attribute in {"unlink", "rmdir", "rename", "replace"}):
        return "path"
    return None


def _bounded_catalog_query_command(node: ast.AST | None) -> list[str] | None:
    if not isinstance(node, (ast.List, ast.Tuple)):
        return None
    elements = node.elts
    if len(elements) not in {8, 10}:
        return None
    literal_at = {index: _literal_string(value) for index, value in enumerate(elements)}
    if literal_at.get(0) not in {"python3", "python"} or literal_at.get(1) != ".fgv/scripts/hermes_catalog_query.py":
        return None
    flags = [literal_at.get(index) for index in range(2, len(elements), 2)]
    required = {"--vault", "--query-type", "--expected-catalog-sha256"}
    if not required <= set(flags) or any(flag not in required | {"--subject-id"} for flag in flags):
        return None
    for index in range(3, len(elements), 2):
        value = elements[index]
        if isinstance(value, ast.Constant) and isinstance(value.value, str):
            continue
        if isinstance(value, ast.Name):
            continue
        if (
            isinstance(value, ast.Subscript)
            and _call_name(value.value) in {"os.environ", "environ"}
            and _literal_string(value.slice) is not None
        ):
            continue
        return None
    return [
        str(literal_at.get(index) if index % 2 == 0 else "__runtime_value__")
        for index in range(len(elements))
    ]


def _python_command_findings(text: str) -> list[tuple[int, str, str]]:
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return [(0, "invalid_format", "Python component does not parse")]
    findings: list[tuple[int, str, str]] = []
    symbols: dict[str, str] = {}
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for alias in node.names:
                if alias.name in {"os", "pathlib", "shutil", "subprocess"}:
                    symbols.setdefault(alias.asname or alias.name, alias.name)
        elif isinstance(node, ast.ImportFrom) and node.module in {"os", "pathlib", "shutil", "subprocess"}:
            for alias in node.names:
                symbols.setdefault(alias.asname or alias.name, f"{node.module}.{alias.name}")
    assignments: list[tuple[list[str], ast.AST]] = []
    for node in ast.walk(tree):
        if isinstance(node, ast.Assign):
            names = [name for target in node.targets for name in _assigned_names(target)]
            assignments.append((names, node.value))
        elif isinstance(node, ast.AnnAssign):
            assignments.append((_assigned_names(node.target), node.value))
    for _ in range(len(assignments) + 1):
        changed = False
        for names, value in assignments:
            dynamic_kind = _dynamic_callable_kind(value, symbols)
            if dynamic_kind == "process":
                resolved = "__hermes_dynamic_process__"
            elif dynamic_kind == "path":
                resolved = "__hermes_dynamic_path__"
            else:
                resolved = _callable_expression_name(value, symbols)
            if not resolved:
                continue
            for name in names:
                if name not in symbols:
                    symbols[name] = resolved
                    changed = True
        if not changed:
            break
    path_values: dict[str, str | None] = {}
    for names, value in assignments:
        is_path, path_value = _path_expression(value, symbols, path_values)
        if is_path:
            for name in names:
                path_values.setdefault(name, path_value)
    process_calls = {
        "subprocess.call",
        "subprocess.check_call",
        "subprocess.check_output",
        "subprocess.Popen",
        "subprocess.run",
        "os.popen",
        "os.system",
    }
    destructive_calls = {
        "os.remove",
        "os.removedirs",
        "os.rmdir",
        "os.unlink",
        "shutil.rmtree",
    }
    for node in ast.walk(tree):
        if not isinstance(node, ast.Call):
            continue
        name = _callable_expression_name(node.func, symbols)
        line = int(getattr(node, "lineno", 0))
        if name in {"open", "pathlib.Path.open"} or name.endswith((".read_text", ".read_bytes", ".open")):
            fragments = "".join(
                child.value
                for child in ast.walk(node)
                if isinstance(child, ast.Constant) and isinstance(child.value, str)
            ).replace(" ", "")
            if "catalog.jsonl" in fragments or ("catalog" in fragments and ".jsonl" in fragments):
                findings.append((line, "direct_catalog_access", "direct catalog.jsonl access is forbidden"))
            receiver = node.func.value if isinstance(node.func, ast.Attribute) else (node.args[0] if node.args else None)
            is_path, read_target = _path_expression(receiver, symbols, path_values)
            if is_path and read_target is not None and str(read_target).endswith("catalog.jsonl"):
                findings.append((line, "direct_catalog_access", "direct catalog.jsonl access is forbidden"))
        dynamic_kind = _dynamic_callable_kind(node.func, symbols)
        if name == "__hermes_dynamic_process__" or dynamic_kind == "process":
            findings.append((line, "dynamic_command", "dynamic Python process callable is not allowed"))
        if name == "__hermes_dynamic_path__" or dynamic_kind == "path":
            findings.append((line, "dynamic_destructive_path", "dynamic pathlib callable is not allowed"))
        if name in process_calls or name.startswith("os.exec") or name.startswith("os.spawn"):
            argument_offset = 1 if name.startswith("os.spawn") else 0
            argument = node.args[argument_offset] if len(node.args) > argument_offset else None
            if argument is None:
                argument = next(
                    (keyword.value for keyword in node.keywords if keyword.arg in {"args", "command"}),
                    None,
                )
            tokens: list[str] | None = None
            literal = _literal_string(argument)
            if literal is not None:
                try:
                    tokens = _shell_tokens(literal)
                except ValueError:
                    findings.append((line, "invalid_shell", "Python command string is not tokenizable"))
            elif isinstance(argument, (ast.List, ast.Tuple)):
                values = [_literal_string(item) for item in argument.elts]
                if all(item is not None for item in values):
                    tokens = [str(item) for item in values]
                else:
                    tokens = _bounded_catalog_query_command(argument)
            if tokens is None:
                findings.append((line, "dynamic_command", "Python process command is not a closed literal"))
            else:
                findings.extend((line, rule, detail) for rule, detail in _inspect_command_tokens(tokens))
        if name in destructive_calls:
            is_path, target = _path_expression(node.args[0] if node.args else None, symbols, path_values)
            if not is_path or target is None:
                findings.append((line, "dynamic_destructive_path", "Python destructive path is not a closed literal"))
            elif _sensitive_delete_target(target):
                findings.append((line, "destructive_command", "Python call deletes vault or Hermes path"))
        if isinstance(node.func, ast.Attribute) and node.func.attr in {"unlink", "rmdir", "rename", "replace"}:
            is_path, target = _path_expression(node.func.value, symbols, path_values)
            if is_path:
                targets = [target]
                if node.func.attr in {"rename", "replace"}:
                    _, destination = _path_expression(node.args[0] if node.args else None, symbols, path_values)
                    targets.append(destination)
                if any(item is None for item in targets):
                    findings.append((line, "dynamic_destructive_path", "pathlib destructive path is not a closed literal"))
                elif any(_sensitive_delete_target(str(item)) for item in targets):
                    findings.append((line, "destructive_command", "pathlib call mutates vault or Hermes path"))
    return findings


def _markdown_command_findings(text: str) -> list[tuple[int, str, str]]:
    findings: list[tuple[int, str, str]] = []
    in_shell_fence = False
    for number, line in enumerate(text.splitlines(), 1):
        stripped = line.strip()
        if stripped.startswith("```"):
            language = stripped[3:].strip().casefold()
            if in_shell_fence:
                in_shell_fence = False
            else:
                in_shell_fence = language in {"bash", "sh", "shell", "zsh"}
            continue
        candidates: list[str] = []
        if in_shell_fence and stripped and not stripped.startswith("#"):
            candidates.append(stripped)
        candidates.extend(re.findall(r"`([^`\n]+)`", line))
        prose_command = re.search(r"(?<![-\w/])(?:git\b|fgv-sync\b|(?:rm|rmdir|unlink)\s).*$", line)
        if prose_command is not None:
            candidates.append(prose_command.group(0))
        for command in dict.fromkeys(candidates):
            try:
                tokens = _shell_tokens(command)
            except ValueError:
                findings.append((number, "invalid_shell", "Markdown shell command is not tokenizable"))
                continue
            findings.extend((number, rule, detail) for rule, detail in _inspect_command_tokens(tokens))
    return findings


_CHANNEL_ADAPTER_IMPORTS = {"base64", "hashlib", "json", "os", "subprocess", "sys"}
_CHANNEL_MAIN_TEMPLATE = ast.parse(
    """def main():
    if sys.argv[1:] != ["--hermes-channel-smoke"]:
        raise SystemExit("unsupported invocation")
    result = subprocess.run(
        [
            "python3",
            ".fgv/scripts/hermes_catalog_query.py",
            "--vault",
            VAULT,
            "--query-type",
            os.environ["FGV_HERMES_QUERY_TYPE"],
            "--subject-id",
            os.environ["FGV_HERMES_SUBJECT_ID"],
            "--expected-catalog-sha256",
            os.environ["FGV_HERMES_EXPECTED_CATALOG_SHA256"],
        ],
        check=True,
        capture_output=True,
    )
    consumed_sha256 = hashlib.sha256(result.stdout).hexdigest()
    print(json.dumps({
        "challenge": os.environ["FGV_HERMES_CHANNEL_CHALLENGE"],
        "consumed_stdout_sha256": consumed_sha256,
        "query_stdout_b64": base64.b64encode(result.stdout).decode("ascii"),
        "schema_version": 1,
    }, ensure_ascii=False, sort_keys=True, separators=(",", ":")))
    return 0
"""
).body[0]
_CHANNEL_GUARD_TEMPLATE = ast.parse(
    """if __name__ == "__main__":
    raise SystemExit(main())
"""
).body[0]
_CHANNEL_VAULT_VALUE_TEMPLATE = ast.parse(
    'VAULT = os.environ["FGV_VAULT_ROOT"]'
).body[0].value


def python_channel_entrypoint_findings(text: str) -> list[tuple[int, str, str]]:
    """Validate the complete executable schema of a thin channel adapter."""
    try:
        tree = ast.parse(text)
    except SyntaxError:
        return [(0, "channel_schema", "channel adapter does not parse")]
    findings: list[tuple[int, str, str]] = []
    imports: list[str] = []
    assignments: list[ast.Assign] = []
    functions: list[ast.FunctionDef] = []
    guards: list[ast.If] = []
    phase = 0
    for node in tree.body:
        line = int(getattr(node, "lineno", 0))
        if isinstance(node, ast.Import) and phase == 0:
            if len(node.names) != 1 or node.names[0].asname is not None:
                findings.append((line, "channel_schema", "channel imports must be exact and unaliased"))
            else:
                imports.append(node.names[0].name)
            continue
        if isinstance(node, ast.Assign) and phase <= 1:
            phase = 1
            assignments.append(node)
            continue
        if isinstance(node, ast.FunctionDef) and phase <= 2:
            phase = 2
            functions.append(node)
            continue
        if isinstance(node, ast.If) and phase <= 3:
            phase = 3
            guards.append(node)
            continue
        findings.append((line, "channel_schema", "channel module contains executable statements outside its closed adapter schema"))
    if len(imports) != len(_CHANNEL_ADAPTER_IMPORTS) or set(imports) != _CHANNEL_ADAPTER_IMPORTS:
        findings.append((0, "channel_schema", "channel adapter imports are not the exact standard-library allowlist"))
    seen_assignments: set[str] = set()
    for node in assignments:
        line = int(getattr(node, "lineno", 0))
        if len(node.targets) != 1 or not isinstance(node.targets[0], ast.Name):
            findings.append((line, "channel_schema", "channel assignments may target one constant name only"))
            continue
        name = node.targets[0].id
        if not name.isupper() or name in seen_assignments or name in _CHANNEL_ADAPTER_IMPORTS:
            findings.append((line, "channel_schema", "channel adapter assignment target is not an immutable unique constant"))
            continue
        seen_assignments.add(name)
        if name == "VAULT":
            if ast.dump(node.value, include_attributes=False) != ast.dump(
                _CHANNEL_VAULT_VALUE_TEMPLATE, include_attributes=False
            ):
                findings.append((line, "channel_schema", "VAULT must come from the pinned FGV_VAULT_ROOT environment value"))
            continue
        try:
            ast.literal_eval(node.value)
        except (ValueError, TypeError):
            findings.append((line, "channel_schema", "channel constants must be closed literal values"))
    if "VAULT" not in seen_assignments:
        findings.append((0, "channel_schema", "channel adapter is missing its pinned VAULT binding"))
    if len(functions) != 1 or ast.dump(functions[0], include_attributes=False) != ast.dump(
        _CHANNEL_MAIN_TEMPLATE, include_attributes=False
    ):
        findings.append((0, "channel_schema", "channel main function does not match the authenticated bounded-query template"))
    if len(guards) != 1 or ast.dump(guards[0], include_attributes=False) != ast.dump(
        _CHANNEL_GUARD_TEMPLATE, include_attributes=False
    ):
        findings.append((0, "channel_schema", "channel main guard does not match the authenticated template"))
    return findings


def _python_has_bounded_catalog_query_call(text: str) -> bool:
    return not python_channel_entrypoint_findings(text)


def _cron_command_findings(text: str) -> list[tuple[int, str, str]]:
    try:
        payload = json.loads(text)
    except json.JSONDecodeError:
        return [(0, "invalid_format", "cron component is not valid JSON")]
    if not isinstance(payload, dict) or set(payload) != {"jobs"} or not isinstance(payload["jobs"], list):
        return [(0, "invalid_format", "cron JSON root schema is closed and invalid")]
    findings: list[tuple[int, str, str]] = []
    allowed_keys = {"command", "description", "enabled", "name", "schedule"}
    for index, job in enumerate(payload["jobs"], 1):
        if (
            not isinstance(job, dict)
            or not {"name", "command"} <= set(job)
            or not set(job) <= allowed_keys
            or not isinstance(job["name"], str)
            or not isinstance(job["command"], str)
        ):
            findings.append((index, "invalid_format", "cron job schema is closed and invalid"))
            continue
        try:
            tokens = _shell_tokens(job["command"])
        except ValueError:
            findings.append((index, "invalid_shell", "cron command is not tokenizable"))
            continue
        findings.extend((index, rule, detail) for rule, detail in _inspect_command_tokens(tokens))
    return findings


def audit_components(home: Path, manifest: dict[str, Any]) -> dict[str, object]:
    findings: list[dict[str, object]] = []
    legacy_subjects = "|".join(re.escape(item) for item in manifest["legacy_subject_folders"])
    rules = (
        (
            "legacy_path",
            re.compile(
                rf"(?:(?:/root/vault|~/FGV)/(?:Tasks\.md(?:\b|$)|Vault(?:/|\b)|S1(?:/|\b)|(?:{legacy_subjects})(?:/|\b))"
                rf"|(?<![\w/])(?:{legacy_subjects})/Aulas(?:/|\b))"
            ),
            "legacy vault path",
        ),
        ("legacy_materials", re.compile(r"(?:Slides/Material|Materiais(?:/|\b))"), "legacy material folder"),
        (
            "legacy_fixed_name",
            re.compile(r"(?<![-\w])(?:Resumo|Transcrito)\.md\b"),
            "fixed legacy lesson filename",
        ),
    )
    direct_catalog_access = re.compile(
        r"\b(?:consulte|leia|carregue|abra|read|load|open|cat|head|tail|less)\b[^\n]{0,100}\bcatalog\.jsonl\b",
        re.IGNORECASE,
    )
    component_states: list[dict[str, object]] = []
    for component in manifest["components"]:
        relative = component["path"]
        payload, issue = read_relative_file(home, relative)
        if issue:
            severity = "error" if component["classification"] == "required" or issue == "unsafe_path" else "warning"
            findings.append(
                {
                    "detail": issue.replace("_", " "),
                    "file": relative,
                    "line": 0,
                    "rule": issue,
                    "severity": severity,
                }
            )
            component_states.append({"id": component["id"], "path": relative, "state": issue})
            continue
        try:
            text = payload.decode("utf-8")
        except UnicodeDecodeError:
            findings.append(
                {
                    "detail": "component is not readable UTF-8 text",
                    "file": relative,
                    "line": 0,
                    "rule": "unreadable_component",
                    "severity": "error",
                }
            )
            component_states.append({"id": component["id"], "path": relative, "state": "unreadable"})
            continue
        component_states.append({"id": component["id"], "path": relative, "state": "found"})
        if (
            component["format"] == "python"
            and "catalog.jsonl" in text
            and re.search(r"\b(?:open|read_text|read_bytes)\b", text)
        ):
            findings.append(
                {
                    "detail": "Python component reads catalog.jsonl directly",
                    "file": relative,
                    "line": 0,
                    "rule": "direct_catalog_access",
                    "severity": "error",
                }
            )
        for number, line in enumerate(text.splitlines(), 1):
            if direct_catalog_access.search(line):
                findings.append(
                    {
                        "detail": "component accesses catalog.jsonl directly instead of the bounded query",
                        "file": relative,
                        "line": number,
                        "rule": "direct_catalog_access",
                        "severity": "error",
                    }
                )
            for rule, pattern, detail in rules:
                if pattern.search(line):
                    findings.append(
                        {
                            "detail": detail,
                            "file": relative,
                            "line": number,
                            "rule": rule,
                            "severity": "error",
                        }
                    )
            for forbidden in manifest["forbidden_scan_roots"]:
                if forbidden in line and re.search(r"\b(?:find|grep|rg|rglob|walk)\b", line):
                    findings.append(
                        {
                            "detail": "forbidden broad scan root",
                            "file": relative,
                            "line": number,
                            "rule": "forbidden_scan_root",
                            "severity": "error",
                        }
                    )
        format_scanners = {
            "python": _python_command_findings,
            "markdown": _markdown_command_findings,
            "cron_json": _cron_command_findings,
        }
        for number, rule, detail in format_scanners[component["format"]](text):
            findings.append(
                {
                    "detail": detail,
                    "file": relative,
                    "line": number,
                    "rule": rule,
                    "severity": "error",
                }
            )
        if (
            component["format"] == "python"
            and "hermes_catalog_query.py" in component["required_markers"]
            and not _python_has_bounded_catalog_query_call(text)
        ):
            findings.append(
                {
                    "detail": "Python component does not invoke the bounded catalog query",
                    "file": relative,
                    "line": 0,
                    "rule": "missing_bounded_query_call",
                    "severity": "error",
                }
            )
    findings.sort(key=lambda item: (str(item["file"]), int(item["line"]), str(item["rule"])))
    blocked = any(item["severity"] == "error" for item in findings)
    return {
        "schema_version": 1,
        "status": "blocked" if blocked else "pass",
        "components": component_states,
        "findings": findings,
    }
