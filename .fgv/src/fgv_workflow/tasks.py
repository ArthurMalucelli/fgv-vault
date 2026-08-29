import hashlib
import os
from dataclasses import dataclass
from datetime import date
from pathlib import Path
import re
import tempfile


@dataclass(frozen=True)
class TaskMention:
    description: str
    due: str
    tag: str
    priority: str


def _task_id(mention: TaskMention) -> str:
    normalized = " ".join(mention.description.casefold().split())
    material = f"{normalized}\0{mention.due}\0{mention.tag}"
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def _semantic_task_exists(text: str, mention: TaskMention) -> bool:
    expected = " ".join(
        f"{mention.description} {mention.tag} 📅 {mention.due}".casefold().split()
    )
    for line in text.splitlines():
        if not re.match(r"^- \[[ xX]\] ", line):
            continue
        normalized = " ".join(line.casefold().split())
        if expected in normalized:
            return True
    return False


def _write_atomic(path: Path, text: str) -> None:
    descriptor, temporary_name = tempfile.mkstemp(prefix=".tasks-", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(text)
            handle.flush()
            os.fsync(handle.fileno())
        os.replace(temporary, path)
    finally:
        if temporary.exists():
            temporary.unlink()


def append_tasks(
    path: Path,
    mentions: tuple[TaskMention, ...],
    transaction_id: str,
) -> int:
    path.parent.mkdir(parents=True, exist_ok=True)
    current = path.read_text(encoding="utf-8") if path.exists() else "# Tasks\n"
    heading = "## Adicionadas pela skill /fgv"
    if heading not in current:
        current = current.rstrip() + f"\n\n{heading}\n"
    additions: list[str] = []
    seen = current
    for mention in mentions:
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", mention.due):
            raise ValueError("task due date must use YYYY-MM-DD")
        try:
            date.fromisoformat(mention.due)
        except ValueError as error:
            raise ValueError("task due date is invalid") from error
        if not mention.description.strip() or not re.fullmatch(r"#[\w-]+", mention.tag):
            raise ValueError("task description and tag are required")
        task_id = _task_id(mention)
        if f"fgv-task:{task_id}" in seen or _semantic_task_exists(seen, mention):
            continue
        marker = f"<!-- fgv-task:{task_id} source:{transaction_id} -->"
        priority = f" {mention.priority}" if mention.priority else ""
        line = (
            f"- [ ] {mention.description.strip()} {mention.tag} "
            f"📅 {mention.due}{priority} {marker}"
        )
        additions.append(line)
        seen += "\n" + line
    if additions:
        _write_atomic(path, current.rstrip() + "\n\n" + "\n".join(additions) + "\n")
    return len(additions)
