#!/usr/bin/env python3
"""Return a deterministic bounded candidate set from the FGV catalog."""

from __future__ import annotations

import argparse
import json
from pathlib import Path, PurePosixPath
import re
import sys

from hermes_common import HermesError, read_relative_file, sha256_bytes


MAX_CANDIDATES = 5
MAX_OUTPUT_BYTES = 16_384
QUERY_TYPES = {
    "latest_class",
    "latest_transcript",
    "next_assessment",
    "eclass_material",
    "low_mastery_concept",
    "legacy_summary_name",
}
LESSON_DATE_RE = re.compile(r"^[0-9]{2}\.[0-9]{2}$")
PRIMARY_MATERIAL_SUFFIXES = {
    ".doc",
    ".docx",
    ".pdf",
    ".ppt",
    ".pptx",
    ".xls",
    ".xlsx",
}


def parser() -> argparse.ArgumentParser:
    value = argparse.ArgumentParser(description=__doc__)
    value.add_argument("--vault", required=True, type=Path)
    value.add_argument("--query-type", required=True, choices=sorted(QUERY_TYPES))
    value.add_argument("--subject-id")
    value.add_argument("--limit", type=int, default=MAX_CANDIDATES)
    value.add_argument("--expected-catalog-sha256", required=True)
    return value


def is_direct_lesson_note(path: object, prefix: str) -> bool:
    if not isinstance(path, str):
        return False
    pure = PurePosixPath(path)
    if not pure.name.startswith(prefix):
        return False
    return (
        len(pure.parts) == 5
        and pure.parts[0] == "10 Matérias"
        and pure.parts[1] != ""
        and pure.parts[2] == "Aulas"
        and LESSON_DATE_RE.fullmatch(pure.parts[3]) is not None
    )


def is_direct_material(path: object) -> bool:
    if not isinstance(path, str):
        return False
    pure = PurePosixPath(path)
    return (
        len(pure.parts) == 6
        and pure.parts[0] == "10 Matérias"
        and pure.parts[1] != ""
        and pure.parts[2] == "Aulas"
        and LESSON_DATE_RE.fullmatch(pure.parts[3]) is not None
        and pure.parts[4] == "Material"
    )


def material_priority(path: object) -> int:
    if not isinstance(path, str):
        return 0
    return 1 if PurePosixPath(path).suffix.casefold() in PRIMARY_MATERIAL_SUFFIXES else 0


def load_records(
    vault: Path, expected_catalog_sha256: str | None = None
) -> tuple[dict[str, object], list[dict[str, object]]]:
    if not vault.is_absolute() or not vault.is_dir() or vault.is_symlink():
        raise HermesError("vault must be an absolute non-symlink directory")
    payload, issue = read_relative_file(vault, "30 Sistema/Estado/catalog.jsonl")
    if issue or payload is None:
        raise HermesError(f"catalog cannot be trusted: {issue}")
    if expected_catalog_sha256 is not None and sha256_bytes(payload) != expected_catalog_sha256:
        raise HermesError("catalog changed after snapshot authentication")
    records: list[dict[str, object]] = []
    for number, line in enumerate(payload.decode("utf-8").splitlines(), 1):
        try:
            record = json.loads(line)
        except json.JSONDecodeError as error:
            raise HermesError(f"catalog line {number} is invalid JSON") from error
        if not isinstance(record, dict) or record.get("schema_version") != 1:
            raise HermesError(f"catalog line {number} has an unsupported schema")
        records.append(record)
    if (
        not records
        or records[0].get("record_type") != "manifest"
        or sum(item.get("record_type") == "manifest" for item in records) != 1
    ):
        raise HermesError("catalog must start with exactly one manifest")
    return records[0], records[1:]


def select_records(
    records: list[dict[str, object]], query_type: str, subject_id: str | None
) -> list[dict[str, object]]:
    files = [item for item in records if item.get("record_type") == "file"]
    if subject_id:
        files = [item for item in files if subject_id in item.get("subject_ids", [])]
    if query_type in {"latest_class", "legacy_summary_name"}:
        selected = [item for item in files if is_direct_lesson_note(item.get("path"), "Resumo")]
        return sorted(selected, key=lambda item: (str(item.get("date") or ""), str(item["path"])), reverse=True)
    if query_type == "latest_transcript":
        selected = [item for item in files if is_direct_lesson_note(item.get("path"), "Transcrito")]
        return sorted(selected, key=lambda item: (str(item.get("date") or ""), str(item["path"])), reverse=True)
    if query_type == "eclass_material":
        selected = [
            item
            for item in files
            if is_direct_material(item.get("path"))
            and not PurePosixPath(str(item.get("path"))).name.startswith(("Resumo", "Transcrito"))
        ]
        return sorted(
            selected,
            key=lambda item: (
                str(item.get("date") or ""),
                material_priority(item.get("path")),
                str(item["path"]),
            ),
            reverse=True,
        )
    if query_type == "next_assessment":
        selected = [
            item
            for item in records
            if item.get("record_type") == "task"
            and item.get("status") in {"todo", "in_progress"}
            and item.get("due")
            and (not subject_id or subject_id in item.get("subject_ids", []))
        ]
        return sorted(selected, key=lambda item: (str(item["due"]), str(item.get("description", ""))))
    selected = [
        item
        for item in records
        if item.get("record_type") == "learning_state"
        and item.get("last_status") in {"gap", "nao_sabe", "parcial"}
        and item.get("concept_path")
        and (not subject_id or item.get("subject") == subject_id)
    ]
    return sorted(selected, key=lambda item: (str(item.get("last_status")), str(item.get("concept"))))


def candidate_record(
    record: dict[str, object], all_records: list[dict[str, object]]
) -> dict[str, object]:
    keys_by_type = {
        "file": ("record_type", "path", "sha256", "date", "note_type", "subject_ids"),
        "task": ("record_type", "source_path", "due", "status", "description", "subject_ids"),
        "learning_state": ("record_type", "concept_path", "concept", "last_status", "subject"),
    }
    keys = keys_by_type.get(str(record.get("record_type")))
    if keys is None:
        raise HermesError("selected candidate has an unsupported record type")
    candidate = {key: record[key] for key in keys if key in record}
    selected_path = record.get("path") or record.get("source_path") or record.get("concept_path")
    if isinstance(selected_path, str):
        candidate["path"] = selected_path
        linked = [
            item
            for item in all_records
            if item.get("record_type") == "file" and item.get("path") == selected_path
        ]
        if len(linked) == 1 and isinstance(linked[0].get("sha256"), str):
            candidate["sha256"] = linked[0]["sha256"]
    return candidate


def query_catalog(
    vault: Path,
    query_type: str,
    subject_id: str | None,
    limit: int,
    expected_catalog_sha256: str | None = None,
) -> tuple[dict[str, object], bytes]:
    if limit < 1 or limit > MAX_CANDIDATES:
        raise HermesError(f"limit must be between 1 and {MAX_CANDIDATES}")
    manifest, records = load_records(vault, expected_catalog_sha256)
    selected = select_records(records, query_type, subject_id)[:limit]
    report = {
        "candidates": [candidate_record(item, records) for item in selected],
        "manifest": manifest,
        "schema_version": 1,
    }
    payload = (
        json.dumps(report, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
    ).encode("utf-8")
    if len(payload) > MAX_OUTPUT_BYTES or payload.count(b"\n") > 1:
        raise HermesError("bounded catalog query exceeded its output budget")
    return report, payload


def main() -> int:
    args = parser().parse_args()
    try:
        _, payload = query_catalog(
            args.vault,
            args.query_type,
            args.subject_id,
            args.limit,
            args.expected_catalog_sha256,
        )
        sys.stdout.buffer.write(payload)
        return 0
    except (HermesError, OSError, UnicodeDecodeError, KeyError, TypeError) as error:
        print(
            json.dumps(
                {"reason": str(error), "schema_version": 1, "status": "blocked"},
                ensure_ascii=False,
                sort_keys=True,
                separators=(",", ":"),
            )
        )
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
