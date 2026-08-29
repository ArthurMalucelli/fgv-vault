import json
import os
from dataclasses import dataclass
from datetime import date, datetime
from pathlib import Path
from string import Template
import tempfile

from . import CONTRACT_VERSION
from .naming import artifact_path, clean_topic, lesson_dir
from .source_store import ingest_source
from .subjects import SubjectRegistry


TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "templates"
REQUIRED_ANALYSIS_KEYS = {
    "subject_id",
    "topic",
    "cleaned_transcript",
    "summary",
    "topics",
    "review_questions",
    "concept_candidates",
    "task_mentions",
    "calendar_mentions",
}


class AnalysisError(ValueError):
    pass


@dataclass(frozen=True)
class PlaudResult:
    transaction_id: str
    raw_path: Path
    manifest_path: Path
    artifacts: tuple[Path, ...]
    created: bool


def validate_analysis(analysis: dict) -> None:
    missing = sorted(REQUIRED_ANALYSIS_KEYS.difference(analysis))
    if missing:
        raise AnalysisError("missing analysis keys: " + ", ".join(missing))
    if not isinstance(analysis["review_questions"], list) or not 5 <= len(
        analysis["review_questions"]
    ) <= 10:
        raise AnalysisError("review_questions must contain 5 to 10 items")
    for key in ("subject_id", "topic", "cleaned_transcript", "summary"):
        if not isinstance(analysis[key], str) or not analysis[key].strip():
            raise AnalysisError(f"{key} must be non-empty text")
    if not isinstance(analysis["topics"], list) or not all(
        isinstance(item, str) and item.strip() for item in analysis["topics"]
    ):
        raise AnalysisError("topics must be a list of non-empty strings")
    clean_topic(analysis["topic"])


def _yaml_list(items: list[str]) -> str:
    return json.dumps(items, ensure_ascii=False, separators=(",", ":"))


def _context(
    *,
    kind: str,
    subject_id: str,
    semester: str,
    class_date: date,
    analysis: dict,
    processor: str,
    ingested_at: datetime,
    source_sha256: str,
    transaction_id: str,
    raw_relpath: str,
) -> dict[str, str]:
    topic = clean_topic(analysis["topic"])
    return {
        "artifact_id": f"{subject_id}-{class_date.isoformat()}-{kind}-{transaction_id[:8]}",
        "subject_id": subject_id,
        "semester": semester,
        "class_date": class_date.isoformat(),
        "topic": topic,
        "topics": _yaml_list(analysis["topics"]),
        "processor": processor,
        "updated_at": ingested_at.isoformat(),
        "contract_version": str(CONTRACT_VERSION),
        "source_sha256": source_sha256,
        "transaction_id": transaction_id,
        "raw_relpath": raw_relpath,
        "cleaned_transcript": analysis["cleaned_transcript"].strip(),
        "summary": analysis["summary"].strip(),
        "review_questions": "\n".join(
            f"- [ ] {question.strip()}" for question in analysis["review_questions"]
        ),
    }


def _render(kind: str, context: dict[str, str]) -> str:
    template = Template((TEMPLATE_DIR / f"{kind}.md").read_text(encoding="utf-8"))
    rendered = template.substitute(context).rstrip() + "\n"
    required = (
        f"tipo: {kind}",
        f"transaction_id: {context['transaction_id']}",
        f"source_sha256: {context['source_sha256']}",
        "contract_version: 1",
    )
    if not all(item in rendered for item in required):
        raise AnalysisError(f"invalid rendered {kind}")
    return rendered


def _existing_artifacts(lesson: Path, transaction_id: str) -> tuple[Path, ...]:
    found = []
    needle = f"transaction_id: {transaction_id}"
    for path in lesson.glob("*.md") if lesson.exists() else ():
        if needle in path.read_text(encoding="utf-8"):
            found.append(path)
    return tuple(sorted(found, key=lambda item: item.name))


def process_plaud(
    vault_root: Path,
    source: Path,
    class_date: date,
    analysis: dict,
    processor: str,
    ingested_at: datetime,
) -> PlaudResult:
    validate_analysis(analysis)
    registry = SubjectRegistry.load_default()
    subject = registry.resolve(analysis["subject_id"])
    lesson = lesson_dir(vault_root, subject, class_date)
    ingested = ingest_source(
        vault_root=vault_root,
        source=source,
        lesson_dir=lesson,
        subject_id=subject.id,
        class_date=class_date,
        ingested_at=ingested_at,
    )
    existing = _existing_artifacts(lesson, ingested.transaction_id)
    if not ingested.created and len(existing) == 2:
        return PlaudResult(
            ingested.transaction_id,
            ingested.raw_path,
            ingested.manifest_path,
            existing,
            False,
        )
    if existing:
        raise IOError("incomplete artifact set for existing transaction")

    destinations: list[Path] = []
    staged: list[Path] = []
    try:
        for kind in ("transcrito", "resumo"):
            destination = artifact_path(lesson, kind, analysis["topic"])
            context = _context(
                kind=kind,
                subject_id=subject.id,
                semester=registry.semester,
                class_date=class_date,
                analysis=analysis,
                processor=processor,
                ingested_at=ingested_at,
                source_sha256=ingested.source_sha256,
                transaction_id=ingested.transaction_id,
                raw_relpath=ingested.raw_path.relative_to(vault_root).as_posix(),
            )
            rendered = _render(kind, context)
            descriptor, temporary_name = tempfile.mkstemp(prefix=f".{kind}-", dir=lesson)
            temporary = Path(temporary_name)
            with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(rendered)
                handle.flush()
                os.fsync(handle.fileno())
            destinations.append(destination)
            staged.append(temporary)
        for temporary, destination in zip(staged, destinations, strict=True):
            try:
                os.link(temporary, destination)
            except FileExistsError as error:
                raise FileExistsError(f"artifact destination appeared: {destination}") from error
    finally:
        for temporary in staged:
            if temporary.exists():
                temporary.unlink()
    return PlaudResult(
        ingested.transaction_id,
        ingested.raw_path,
        ingested.manifest_path,
        tuple(destinations),
        True,
    )
