import hashlib
from pathlib import Path

from . import CONTRACT_VERSION


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
