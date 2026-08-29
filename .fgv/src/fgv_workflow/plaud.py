import json
from datetime import date, datetime
from pathlib import Path
from string import Template
import unicodedata

from . import CONTRACT_VERSION
from .naming import clean_topic


TEMPLATE_DIR = Path(__file__).resolve().parents[2] / "templates"
REQUIRED_ANALYSIS_KEYS = {
    "schema_version",
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
CONCEPT_KEYS = {
    "title",
    "centrality_explicit",
    "used_in_assessment",
    "occurrence_count",
    "cross_subject",
    "needs_own_explanation",
}
TASK_KEYS = {"description", "due", "priority"}
CALENDAR_KEYS = {"action", "calendar_alias", "payload"}
CALENDAR_PAYLOAD_KEYS = {
    "append_description": {"event_id", "text"},
    "update_location": {"event_id", "location"},
    "create_assessment": {"title", "start"},
    "mark_cancelled": {"event_id"},
    "reschedule": {"event_id", "start"},
}


class AnalysisError(ValueError):
    pass


def validate_analysis(analysis: dict) -> None:
    if not isinstance(analysis, dict):
        raise AnalysisError("analysis must be an object")
    if set(analysis) != REQUIRED_ANALYSIS_KEYS:
        missing = sorted(REQUIRED_ANALYSIS_KEYS.difference(analysis))
        extra = sorted(set(analysis).difference(REQUIRED_ANALYSIS_KEYS))
        details = []
        if missing:
            details.append("missing: " + ", ".join(missing))
        if extra:
            details.append("unexpected: " + ", ".join(extra))
        raise AnalysisError("analysis schema mismatch: " + "; ".join(details))
    if type(analysis["schema_version"]) is not int or analysis["schema_version"] != 1:
        raise AnalysisError("schema_version must be integer 1")
    missing = sorted(REQUIRED_ANALYSIS_KEYS.difference(analysis))
    if missing:
        raise AnalysisError("missing analysis keys: " + ", ".join(missing))
    if not isinstance(analysis["review_questions"], list) or not 5 <= len(
        analysis["review_questions"]
    ) <= 10:
        raise AnalysisError("review_questions must contain 5 to 10 items")
    if not all(
        isinstance(question, str) and question.strip()
        for question in analysis["review_questions"]
    ):
        raise AnalysisError("review_questions must contain non-empty text")
    for key in ("subject_id", "topic", "cleaned_transcript", "summary"):
        if not isinstance(analysis[key], str) or not analysis[key].strip():
            raise AnalysisError(f"{key} must be non-empty text")
    if not isinstance(analysis["topics"], list) or not analysis["topics"] or not all(
        isinstance(item, str) and item.strip() for item in analysis["topics"]
    ):
        raise AnalysisError("topics must be a non-empty list of non-empty strings")
    for key in ("concept_candidates", "task_mentions", "calendar_mentions"):
        if not isinstance(analysis[key], list):
            raise AnalysisError(f"{key} must be a list")
    for value in _walk_strings(analysis):
        if unicodedata.normalize("NFC", value) != value:
            raise AnalysisError("all analysis strings must be NFC")
    concept_titles: set[str] = set()
    for candidate in analysis["concept_candidates"]:
        if not isinstance(candidate, dict) or set(candidate) != CONCEPT_KEYS:
            raise AnalysisError("concept candidate schema mismatch")
        if not isinstance(candidate["title"], str) or not candidate["title"].strip():
            raise AnalysisError("concept title must be non-empty text")
        title_key = " ".join(candidate["title"].casefold().split()).strip(" .")
        if title_key in concept_titles:
            raise AnalysisError("concept candidate titles must be unique")
        concept_titles.add(title_key)
        for key in (
            "centrality_explicit",
            "used_in_assessment",
            "cross_subject",
            "needs_own_explanation",
        ):
            if type(candidate[key]) is not bool:
                raise AnalysisError(f"{key} must be a strict boolean")
        if type(candidate["occurrence_count"]) is not int or candidate["occurrence_count"] < 0:
            raise AnalysisError("occurrence_count must be a non-negative integer")
    for mention in analysis["task_mentions"]:
        if not isinstance(mention, dict) or set(mention) != TASK_KEYS:
            raise AnalysisError("task mention schema mismatch")
        description = mention["description"]
        if (
            not isinstance(description, str)
            or not description.strip()
            or "\n" in description
            or "\r" in description
        ):
            raise AnalysisError("task description must be single-line text")
        if "<!-- fgv-task:" in description.casefold():
            raise AnalysisError("task description contains reserved marker namespace")
        if not isinstance(mention["priority"], str) or mention["priority"] not in {
            "",
            "🔺",
            "⏫",
            "🔽",
        }:
            raise AnalysisError("task priority is invalid")
        if not isinstance(mention["due"], str):
            raise AnalysisError("task due must be text")
        try:
            parsed_due = date.fromisoformat(mention["due"])
        except ValueError as error:
            raise AnalysisError("task due must use canonical YYYY-MM-DD") from error
        if parsed_due.isoformat() != mention["due"]:
            raise AnalysisError("task due must use canonical YYYY-MM-DD")
    for mention in analysis["calendar_mentions"]:
        if not isinstance(mention, dict) or set(mention) != CALENDAR_KEYS:
            raise AnalysisError("calendar mention schema mismatch")
        action = mention["action"]
        if not isinstance(action, str):
            raise AnalysisError("calendar action is invalid")
        if action not in CALENDAR_PAYLOAD_KEYS:
            raise AnalysisError("calendar action is invalid")
        if not isinstance(mention["calendar_alias"], str) or mention[
            "calendar_alias"
        ] not in {"classes", "assessments"}:
            raise AnalysisError("calendar alias is invalid")
        if action in {"mark_cancelled", "reschedule"} and mention["calendar_alias"] != "classes":
            raise AnalysisError(f"calendar alias must be classes for {action}")
        if action == "create_assessment" and mention["calendar_alias"] != "assessments":
            raise AnalysisError("calendar alias must be assessments for create_assessment")
        payload = mention["payload"]
        if not isinstance(payload, dict) or set(payload) != CALENDAR_PAYLOAD_KEYS[action]:
            raise AnalysisError(f"calendar payload schema mismatch for {action}")
        if not all(isinstance(value, str) and value.strip() for value in payload.values()):
            raise AnalysisError("calendar payload values must be non-empty text")
    try:
        clean_topic(analysis["topic"])
    except ValueError as error:
        raise AnalysisError(str(error)) from error


def _walk_strings(value):
    if isinstance(value, str):
        yield value
    elif isinstance(value, dict):
        for key, item in value.items():
            yield from _walk_strings(key)
            yield from _walk_strings(item)
    elif isinstance(value, list):
        for item in value:
            yield from _walk_strings(item)


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
    quote = lambda value: json.dumps(value, ensure_ascii=False)
    return {
        "artifact_id": quote(f"{subject_id}-{class_date.isoformat()}-{kind}-{transaction_id[:8]}"),
        "subject_id": quote(subject_id),
        "semester": quote(semester),
        "class_date": quote(class_date.isoformat()),
        "topic": quote(topic),
        "topics": _yaml_list(analysis["topics"]),
        "processor": quote(processor),
        "updated_at": quote(ingested_at.isoformat()),
        "contract_version": str(CONTRACT_VERSION),
        "source_sha256": quote(source_sha256),
        "transaction_id": quote(transaction_id),
        "raw_relpath": quote(raw_relpath),
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
        f'tipo: "{kind}"',
        f"transaction_id: {context['transaction_id']}",
        f"source_sha256: {context['source_sha256']}",
        "contract_version: 1",
    )
    if not all(item in rendered for item in required):
        raise AnalysisError(f"invalid rendered {kind}")
    return rendered


def render_artifact(
    *,
    kind: str,
    subject_id: str,
    semester: str,
    class_date: date,
    analysis: dict,
    processor: str,
    updated_at: datetime,
    source_sha256: str,
    transaction_id: str,
    raw_relpath: str,
) -> str:
    validate_analysis(analysis)
    return _render(
        kind,
        _context(
            kind=kind,
            subject_id=subject_id,
            semester=semester,
            class_date=class_date,
            analysis=analysis,
            processor=processor,
            ingested_at=updated_at,
            source_sha256=source_sha256,
            transaction_id=transaction_id,
            raw_relpath=raw_relpath,
        ),
    )
