import hashlib
from dataclasses import dataclass
from datetime import date
import re


@dataclass(frozen=True)
class TaskMention:
    description: str
    due: str
    tag: str
    priority: str


def make_task_id(description: str, due: str, tag: str) -> str:
    normalized = " ".join(description.casefold().split())
    material = f"{normalized}\0{due}\0{tag}"
    return hashlib.sha256(material.encode("utf-8")).hexdigest()[:16]


def validate_task_fields(mention: TaskMention) -> None:
    if (
        not mention.description.strip()
        or "\n" in mention.description
        or "\r" in mention.description
    ):
        raise ValueError("task description must be single-line text")
    if not re.fullmatch(r"#[\w-]+", mention.tag):
        raise ValueError("task tag is invalid")
    try:
        parsed = date.fromisoformat(mention.due)
    except ValueError as error:
        raise ValueError("task due date is invalid") from error
    if parsed.isoformat() != mention.due:
        raise ValueError("task due date must use canonical YYYY-MM-DD")
    if mention.priority not in {"", "🔺", "⏫", "🔽"}:
        raise ValueError("task priority is invalid")
