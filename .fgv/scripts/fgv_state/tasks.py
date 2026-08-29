from __future__ import annotations

import hashlib
import re
from datetime import date

from .config import Settings


TASK_RE = re.compile(r"^\s*-\s+\[(?P<marker>[ xX/\-])\]\s+(?P<body>.+?)\s*$")
DUE_RE = re.compile(r"📅\s*(\d{4}-\d{2}-\d{2})")
DONE_RE = re.compile(r"✅\s*\d{4}-\d{2}-\d{2}")
TAG_RE = re.compile(r"(?<!\S)#([\w/-]+)", re.UNICODE)
FENCE_RE = re.compile(r"^\s*(`{3,}|~{3,})")
STATUS = {" ": "todo", "/": "in_progress", "x": "done", "X": "done", "-": "cancelled"}
PRIORITIES = (("🔺", "highest"), ("⏫", "high"), ("🔼", "medium"), ("🔽", "low"), ("⏬", "lowest"))


def parse_tasks(text: str, source_path: str, settings: Settings) -> list[dict[str, object]]:
    records: list[dict[str, object]] = []
    tag_to_subject = {subject.task_tag: subject.id for subject in settings.subjects}
    fence_character: str | None = None
    fence_length = 0
    for line_number, raw_line in enumerate(text.splitlines(), 1):
        fence = FENCE_RE.match(raw_line)
        if fence:
            marker = fence.group(1)
            if fence_character is None:
                fence_character, fence_length = marker[0], len(marker)
            elif marker[0] == fence_character and len(marker) >= fence_length:
                fence_character, fence_length = None, 0
            continue
        if fence_character is not None:
            continue
        match = TASK_RE.match(raw_line)
        if not match:
            continue
        body = match.group("body")
        warnings: list[str] = []
        due_match = DUE_RE.search(body)
        due = due_match.group(1) if due_match else None
        if due:
            try:
                date.fromisoformat(due)
            except ValueError:
                warnings.append(f"invalid due date: {due}")
                due = None
        tags = sorted(set(TAG_RE.findall(body)))
        priority = next((value for emoji, value in PRIORITIES if emoji in body), "normal")
        description = DUE_RE.sub("", DONE_RE.sub("", body))
        for emoji, _ in PRIORITIES:
            description = description.replace(emoji, "")
        description = " ".join(TAG_RE.sub("", description).split())
        records.append({
            "description": description,
            "due": due,
            "priority": priority,
            "record_type": "task",
            "schema_version": 1,
            "scope": "active" if any(tag in tag_to_subject for tag in tags) else "unscoped",
            "source_line": line_number,
            "source_line_sha256": "sha256:" + hashlib.sha256(raw_line.encode("utf-8")).hexdigest(),
            "source_path": source_path,
            "status": STATUS[match.group("marker")],
            "subject_ids": sorted({tag_to_subject[tag] for tag in tags if tag in tag_to_subject}),
            "tags": tags,
            "warnings": sorted(warnings),
        })
    return records
