from contextlib import contextmanager
import fcntl
import hashlib
import os
from pathlib import Path
import tempfile
from typing import Iterator


class VaultLocked(RuntimeError):
    pass


def lock_path(vault_root: Path) -> Path:
    identity = hashlib.sha256(
        vault_root.expanduser().resolve(strict=False).as_posix().encode("utf-8")
    ).hexdigest()[:24]
    return Path(tempfile.gettempdir()) / f"fgv-workflow-{identity}.lock"


@contextmanager
def vault_lock(vault_root: Path) -> Iterator[None]:
    path = lock_path(vault_root)
    descriptor = os.open(path, os.O_RDWR | os.O_CREAT, 0o600)
    try:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError as error:
            raise VaultLocked(f"another FGV runtime owns the vault lock: {path}") from error
        yield
    finally:
        try:
            fcntl.flock(descriptor, fcntl.LOCK_UN)
        finally:
            os.close(descriptor)
