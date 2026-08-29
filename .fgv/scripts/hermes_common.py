#!/usr/bin/env python3
"""Shared validation primitives for the versioned Hermes package."""

from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re
import stat
from typing import Any


class HermesError(ValueError):
    """Input cannot be trusted by the Hermes package."""


MANIFEST_KEYS = {
    "schema_version",
    "package_id",
    "contract_version",
    "vps_git_owner",
    "canonical_paths",
    "retrieval_order",
    "required_response_fields",
    "components",
    "legacy_subject_folders",
    "forbidden_scan_roots",
}
COMPONENT_KEYS = {"id", "path", "classification", "required_markers"}
SHA256_RE = re.compile(r"^[0-9a-f]{64}$")
COMMIT_RE = re.compile(r"^[0-9a-f]{40}$")


def canonical_json(value: object) -> str:
    return json.dumps(value, ensure_ascii=False, sort_keys=True, separators=(",", ":"))


def sha256_bytes(payload: bytes) -> str:
    return hashlib.sha256(payload).hexdigest()


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
        (
            "legacy_materials",
            re.compile(r"(?:Slides/Material|(?<!Materiais)/Material(?:/|\b))"),
            "legacy material folder",
        ),
        (
            "legacy_fixed_name",
            re.compile(r"(?<![-\w])(?:Resumo|Transcrito)\.md\b"),
            "fixed legacy lesson filename",
        ),
        (
            "unauthorized_git",
            re.compile(r"\bgit(?:\s+(?:-C|--git-dir|--work-tree)\s+\S+)*\s+(?:add|checkout|commit|fetch|merge|pull|push|rebase)\b"),
            "Git command outside fgv-sync",
        ),
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
        for number, line in enumerate(text.splitlines(), 1):
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
    findings.sort(key=lambda item: (str(item["file"]), int(item["line"]), str(item["rule"])))
    blocked = any(item["severity"] == "error" for item in findings)
    return {
        "schema_version": 1,
        "status": "blocked" if blocked else "pass",
        "components": component_states,
        "findings": findings,
    }
