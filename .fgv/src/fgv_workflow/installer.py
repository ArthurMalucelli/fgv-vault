import hashlib
import json
import os
from dataclasses import dataclass
from pathlib import Path
import shutil
import tempfile


@dataclass(frozen=True)
class InstallOperation:
    runtime: str
    source: Path
    destination: Path
    expected_sha256: str
    backup: Path
    destination_existed: bool


@dataclass(frozen=True)
class InstallPlan:
    manifest: Path
    operations: tuple[InstallOperation, ...]
    mode: str = "dry-run"


@dataclass(frozen=True)
class InstallReceipt:
    operations: tuple[InstallOperation, ...]


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _copy_atomic(source: Path, destination: Path) -> None:
    destination.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{destination.name}.", dir=destination.parent
    )
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        shutil.copyfile(source, temporary)
        os.replace(temporary, destination)
    finally:
        if temporary.exists():
            temporary.unlink()


def build_install_plan(
    manifest_path: Path,
    destinations: dict[str, Path],
    *,
    backup_root: Path,
) -> InstallPlan:
    payload = json.loads(manifest_path.read_text(encoding="utf-8"))
    if payload.get("contract_version") != 1 or payload.get("install_performed") is not False:
        raise ValueError("invalid adapter staging manifest")
    if set(destinations) != set(payload.get("adapters", {})):
        raise ValueError("destinations must match staged adapters")
    operations = []
    for runtime in sorted(destinations):
        record = payload["adapters"][runtime]
        source = manifest_path.parent / record["path"]
        if _sha256(source) != record["sha256"]:
            raise ValueError(f"staged adapter hash mismatch: {runtime}")
        destination = destinations[runtime].expanduser().resolve(strict=False)
        operations.append(
            InstallOperation(
                runtime=runtime,
                source=source,
                destination=destination,
                expected_sha256=record["sha256"],
                backup=backup_root.resolve(strict=False) / runtime / "SKILL.md",
                destination_existed=destination.exists(),
            )
        )
    return InstallPlan(manifest_path, tuple(operations))


def apply_install(plan: InstallPlan) -> InstallReceipt:
    completed: list[InstallOperation] = []
    try:
        for operation in plan.operations:
            if _sha256(operation.source) != operation.expected_sha256:
                raise ValueError(f"staged adapter changed: {operation.runtime}")
            if operation.destination_existed:
                _copy_atomic(operation.destination, operation.backup)
            _copy_atomic(operation.source, operation.destination)
            if _sha256(operation.destination) != operation.expected_sha256:
                raise IOError(f"installed adapter hash mismatch: {operation.runtime}")
            completed.append(operation)
    except Exception:
        rollback_install(InstallReceipt(tuple(completed)))
        raise
    return InstallReceipt(tuple(completed))


def rollback_install(receipt: InstallReceipt) -> None:
    for operation in reversed(receipt.operations):
        if operation.destination_existed:
            if not operation.backup.is_file():
                raise IOError(f"missing adapter backup: {operation.backup}")
            _copy_atomic(operation.backup, operation.destination)
        elif operation.destination.exists():
            operation.destination.unlink()
