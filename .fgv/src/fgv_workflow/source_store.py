import hashlib
import json
import os
from dataclasses import asdict, dataclass
from datetime import date, datetime
from pathlib import Path
import shutil
import tempfile

from . import CONTRACT_VERSION
from .models import SourceManifest


@dataclass(frozen=True)
class IngestedSource:
    transaction_id: str
    source_sha256: str
    raw_path: Path
    manifest_path: Path
    created: bool


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def make_transaction_id(
    source_sha256: str,
    subject_id: str,
    class_date: str,
) -> str:
    if len(source_sha256) != 64 or any(
        character not in "0123456789abcdef" for character in source_sha256
    ):
        raise ValueError("source_sha256 must be 64 lowercase hex characters")
    material = b"\x00".join(
        (
            f"fgv:v{CONTRACT_VERSION}".encode("utf-8"),
            source_sha256.encode("ascii"),
            subject_id.encode("utf-8"),
            class_date.encode("utf-8"),
        )
    )
    return hashlib.sha256(material).hexdigest()[:20]


def _load_manifest(path: Path) -> dict:
    if not path.exists():
        return {"schema_version": 1, "sources": []}
    payload = json.loads(path.read_text(encoding="utf-8"))
    if payload.get("schema_version") != 1 or not isinstance(payload.get("sources"), list):
        raise ValueError(f"invalid source manifest: {path}")
    return payload


def _atomic_write(path: Path, data: bytes) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(prefix=f".{path.name}.", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "wb") as handle:
            handle.write(data)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def ingest_source(
    vault_root: Path,
    source: Path,
    lesson_dir: Path,
    subject_id: str,
    class_date: date,
    ingested_at: datetime,
) -> IngestedSource:
    if not source.is_file() or source.is_symlink():
        raise ValueError(f"source must be a regular file: {source}")
    source_hash = sha256_file(source)
    transaction_id = make_transaction_id(
        source_hash,
        subject_id,
        class_date.isoformat(),
    )
    sources_dir = lesson_dir / "Fontes"
    manifest_path = sources_dir / "manifest.json"
    payload = _load_manifest(manifest_path)
    for item in payload["sources"]:
        if item.get("transaction_id") != transaction_id:
            continue
        raw_path = vault_root / item["raw_relpath"]
        if not raw_path.is_file() or sha256_file(raw_path) != source_hash:
            raise IOError("manifest raw is missing or changed")
        return IngestedSource(
            transaction_id,
            source_hash,
            raw_path,
            manifest_path,
            False,
        )

    sources_dir.mkdir(parents=True, exist_ok=True)
    suffix = source.suffix.lower() or ".txt"
    raw_path = sources_dir / f"Plaud - original{suffix}"
    sequence = 2
    while raw_path.exists():
        raw_path = sources_dir / f"Plaud - original - {sequence:02d}{suffix}"
        sequence += 1

    descriptor, temporary_name = tempfile.mkstemp(prefix=".plaud-", dir=sources_dir)
    os.close(descriptor)
    temporary = Path(temporary_name)
    try:
        shutil.copyfile(source, temporary)
        if sha256_file(temporary) != source_hash or sha256_file(source) != source_hash:
            raise IOError("raw hash changed during copy")
        try:
            os.link(temporary, raw_path)
        except FileExistsError as error:
            raise FileExistsError(f"raw destination appeared concurrently: {raw_path}") from error
    finally:
        if temporary.exists():
            temporary.unlink()

    manifest = SourceManifest(
        schema_version=1,
        transaction_id=transaction_id,
        subject_id=subject_id,
        class_date=class_date.isoformat(),
        original_name=source.name,
        raw_relpath=raw_path.relative_to(vault_root).as_posix(),
        source_sha256=source_hash,
        size_bytes=raw_path.stat().st_size,
        ingested_at=ingested_at.isoformat(),
    )
    payload["sources"].append(asdict(manifest))
    _atomic_write(
        manifest_path,
        (json.dumps(payload, ensure_ascii=False, indent=2) + "\n").encode("utf-8"),
    )
    return IngestedSource(
        transaction_id,
        source_hash,
        raw_path,
        manifest_path,
        True,
    )
