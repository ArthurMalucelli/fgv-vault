#!/usr/bin/env python3
"""Generate a deterministic migration manifest without moving vault files."""

import argparse
import json
from pathlib import Path
import sys

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


def main(arguments: list[str] | None = None) -> int:
    args = parse_args(arguments)
    vault = Path(args.vault).resolve()
    output_argument = Path(args.output)
    output = (
        output_argument.resolve()
        if output_argument.is_absolute()
        else (vault / output_argument).resolve()
    )

    try:
        try:
            output_paths = (output.relative_to(vault).as_posix(),)
        except ValueError:
            output_paths = ()
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
            if not output.parent.is_dir():
                raise InventoryError(
                    f"output parent is not a directory: {output.parent}"
                )
            output.write_bytes(payload)
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
