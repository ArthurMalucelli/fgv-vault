import hashlib
import json
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class InstallOperation:
    runtime: str
    source: Path
    destination: Path
    expected_sha256: str
    backup: Path
    destination_existed: bool
    destination_observed_sha256: str | None


@dataclass(frozen=True)
class InstallPlan:
    manifest: Path
    operations: tuple[InstallOperation, ...]
    mode: str = "dry-run"


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


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
        requested_destination = destinations[runtime].expanduser()
        if requested_destination.is_symlink():
            raise ValueError(
                f"adapter destination cannot be a symlink: {requested_destination}"
            )
        destination = requested_destination.resolve(strict=False)
        if destination.exists() and (
            not destination.is_file() or destination.is_symlink()
        ):
            raise ValueError(f"adapter destination is not a regular file: {destination}")
        operations.append(
            InstallOperation(
                runtime=runtime,
                source=source,
                destination=destination,
                expected_sha256=record["sha256"],
                backup=backup_root.resolve(strict=False) / runtime / "SKILL.md",
                destination_existed=destination.exists(),
                destination_observed_sha256=(
                    _sha256(destination) if destination.is_file() else None
                ),
            )
        )
    return InstallPlan(manifest_path, tuple(operations))
