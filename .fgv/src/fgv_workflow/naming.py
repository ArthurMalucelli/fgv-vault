import re
from datetime import date
from pathlib import Path
import unicodedata

from .subjects import Subject


PREFIXES = {"transcrito": "Transcrito", "resumo": "Resumo", "revisao": "Revisao"}


def lesson_dir(vault_root: Path, subject: Subject, class_date: date) -> Path:
    return vault_root / subject.path / "Aulas" / class_date.strftime("%m.%d")


def clean_topic(topic: str) -> str:
    topic = unicodedata.normalize("NFC", topic)
    topic = re.sub(r"[/\\:*?\"<>|]", ",", topic)
    topic = re.sub(r"\s+", " ", topic).strip(" .,-")
    if not 3 <= len(topic) <= 90:
        raise ValueError("topic must contain between 3 and 90 characters")
    return topic


def artifact_path(folder: Path, kind: str, topic: str) -> Path:
    try:
        prefix = PREFIXES[kind]
    except KeyError as error:
        raise ValueError(f"unknown artifact kind: {kind}") from error
    base = f"{prefix} - {clean_topic(topic)}"
    candidate = folder / f"{base}.md"
    sequence = 2
    while candidate.exists():
        candidate = folder / f"{base} - {sequence:02d}.md"
        sequence += 1
    return candidate
