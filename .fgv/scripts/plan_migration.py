#!/usr/bin/env python3
"""Generate a deterministic migration manifest without moving vault files."""

import argparse
import json
import os
from pathlib import Path
import stat
import sys
import tempfile

from fgv_migration.inventory import InventoryError, inventory_from_git
from fgv_migration.rules import RuleError, build_manifest


def parse_args(arguments: list[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Plan the FGV vault migration from an immutable Git tree."
    )
    parser.add_argument("--vault", required=True, help="path to the Git-backed vault")
    parser.add_argument(
        "--base-ref", required=True, help="Git tree used as the migration source"
    )
    parser.add_argument(
        "--output", required=True, help="destination path for the JSON manifest"
    )
    parser.add_argument(
        "--check-only",
        action="store_true",
        help="validate and report without writing the manifest",
    )
    return parser.parse_args(arguments)


def _resolve_output_path(
    vault: Path, lexical_vault: Path, value: str, *, require_parent: bool
) -> Path:
    raw_output = Path(value)
    if "\x00" in value or "\\" in value or ".." in raw_output.parts:
        raise InventoryError(f"unsafe output path: {value!r}")

    if raw_output.is_absolute():
        lexical_output = Path(os.path.abspath(raw_output))
        try:
            relative_output = lexical_output.relative_to(lexical_vault)
        except ValueError as error:
            raise InventoryError(f"output must be inside vault: {value!r}") from error
    else:
        relative_output = raw_output
    if not relative_output.parts:
        raise InventoryError("output must name a file inside vault")
    output = vault / relative_output

    current = vault
    existing_ancestor = vault
    parent_missing = False
    for part in relative_output.parts[:-1]:
        current = current / part
        try:
            metadata = os.lstat(current)
        except FileNotFoundError as error:
            if require_parent:
                raise InventoryError(
                    f"output parent is not a directory: {output.parent}"
                ) from error
            parent_missing = True
            break
        if stat.S_ISLNK(metadata.st_mode):
            raise InventoryError(f"output ancestor is a symlink: {current}")
        if not stat.S_ISDIR(metadata.st_mode):
            raise InventoryError(
                f"output parent is not a directory: {output.parent}"
            )
        existing_ancestor = current

    resolved_ancestor = existing_ancestor.resolve(strict=True)
    try:
        resolved_ancestor.relative_to(vault)
    except ValueError as error:
        raise InventoryError(f"resolved output must be inside vault: {value!r}") from error

    if not parent_missing:
        try:
            leaf_metadata = os.lstat(output)
        except FileNotFoundError:
            pass
        else:
            if stat.S_ISLNK(leaf_metadata.st_mode):
                raise InventoryError(f"output leaf is a symlink: {output}")
            if not stat.S_ISREG(leaf_metadata.st_mode):
                raise InventoryError(f"output is not a regular file: {output}")
    return output


def _atomic_write_output(output: Path, payload: bytes) -> None:
    file_descriptor: int | None = None
    temporary_name: str | None = None
    try:
        file_descriptor, temporary_name = tempfile.mkstemp(
            prefix=f".{output.name}.", suffix=".tmp", dir=output.parent
        )
        stream = os.fdopen(file_descriptor, "wb")
        file_descriptor = None
        with stream:
            stream.write(payload)
            stream.flush()
            os.fsync(stream.fileno())
        os.replace(temporary_name, output)
        temporary_name = None
    finally:
        if file_descriptor is not None:
            os.close(file_descriptor)
        if temporary_name is not None:
            try:
                os.unlink(temporary_name)
            except FileNotFoundError:
                pass


def main(arguments: list[str] | None = None) -> int:
    args = parse_args(arguments)

    try:
        lexical_vault = Path(os.path.abspath(args.vault))
        vault = lexical_vault.resolve(strict=True)
        if not vault.is_dir():
            raise InventoryError(f"vault is not a directory: {vault}")
        output = _resolve_output_path(
            vault,
            lexical_vault,
            args.output,
            require_parent=not args.check_only,
        )
        output_paths = (output.relative_to(vault).as_posix(),)
        inventory = inventory_from_git(
            vault, args.base_ref, output_paths=output_paths
        )
        manifest = build_manifest(inventory)
        payload = (
            json.dumps(manifest, ensure_ascii=False, indent=2, separators=(",", ": "))
            + "\n"
        ).encode("utf-8")

        files_written = 0
        if not args.check_only:
            _atomic_write_output(output, payload)
            files_written = 1
    except (InventoryError, RuleError, OSError, ValueError) as error:
        print(f"error: {error}", file=sys.stderr)
        return 1

    print(f"legacy_files={len(manifest)}")
    print(f"unique_destinations={len(manifest)}")
    print("collisions=0")
    print("unclassified=0")
    print(f"files_written={files_written}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
