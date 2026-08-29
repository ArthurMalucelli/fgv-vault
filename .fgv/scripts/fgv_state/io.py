from __future__ import annotations

import os
import tempfile
from pathlib import Path


def _prepare(path: Path, payload: bytes) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, name = tempfile.mkstemp(prefix=f".{path.name}.", suffix=".tmp", dir=path.parent)
    temporary = Path(name)
    with os.fdopen(descriptor, "wb") as handle:
        handle.write(payload)
        handle.flush()
        os.fsync(handle.fileno())
    return temporary


def write_if_changed(path: Path, payload: bytes) -> bool:
    if path.exists() and path.read_bytes() == payload:
        return False
    temporary = _prepare(path, payload)
    try:
        os.replace(temporary, path)
        return True
    finally:
        temporary.unlink(missing_ok=True)


def write_pair_if_changed(first: tuple[Path, bytes], second: tuple[Path, bytes]) -> tuple[bool, bool]:
    pairs = (first, second)
    changed = tuple(not path.exists() or path.read_bytes() != payload for path, payload in pairs)
    if not any(changed):
        return False, False
    old = tuple(path.read_bytes() if path.exists() else None for path, _ in pairs)
    prepared: list[Path | None] = [None, None]
    installed: list[int] = []
    try:
        for index, ((path, payload), needs_write) in enumerate(zip(pairs, changed)):
            if needs_write:
                prepared[index] = _prepare(path, payload)
        for index, ((path, _), needs_write) in enumerate(zip(pairs, changed)):
            if needs_write:
                assert prepared[index] is not None
                os.replace(prepared[index], path)
                installed.append(index)
        for directory in {path.parent for path, _ in pairs}:
            descriptor = os.open(directory, os.O_RDONLY)
            try:
                os.fsync(descriptor)
            finally:
                os.close(descriptor)
        return changed
    except Exception:
        for index in reversed(installed):
            path, _ = pairs[index]
            previous = old[index]
            if previous is None:
                path.unlink(missing_ok=True)
            else:
                restoration = _prepare(path, previous)
                os.replace(restoration, path)
        raise
    finally:
        for temporary in prepared:
            if temporary is not None:
                temporary.unlink(missing_ok=True)
