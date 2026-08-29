import json
import os
from dataclasses import dataclass
from pathlib import Path
from string import Template
import tempfile
from typing import Literal


TEMPLATE_PATH = Path(__file__).resolve().parents[2] / "templates" / "conceito.md"


@dataclass(frozen=True)
class ConceptCandidate:
    title: str
    centrality_explicit: bool
    used_in_assessment: bool
    occurrence_count: int
    cross_subject: bool
    needs_own_explanation: bool


@dataclass(frozen=True)
class ConceptAction:
    title: str
    action: Literal["queue", "create", "link_existing"]
    path: Path | None


def should_promote(candidate: ConceptCandidate) -> bool:
    return any(
        (
            candidate.centrality_explicit,
            candidate.used_in_assessment,
            candidate.occurrence_count >= 2,
            candidate.cross_subject,
            candidate.needs_own_explanation,
        )
    )


def _validated_title(title: str) -> str:
    title = " ".join(title.split()).strip(" .")
    if not title or len(title) > 100 or any(character in title for character in "/\\"):
        raise ValueError(f"unsafe concept title: {title}")
    return title


def _append_candidate(
    queue_path: Path,
    candidate: ConceptCandidate,
    subject_id: str,
    transaction_id: str,
) -> None:
    queue_path.parent.mkdir(parents=True, exist_ok=True)
    key = f"{transaction_id}\0{candidate.title.casefold()}"
    rows = []
    if queue_path.exists():
        rows = [json.loads(line) for line in queue_path.read_text(encoding="utf-8").splitlines()]
    if any(row.get("dedupe_key") == key for row in rows):
        return
    row = {
        "schema_version": 1,
        "dedupe_key": key,
        "transaction_id": transaction_id,
        "subject_id": subject_id,
        "title": candidate.title,
        "criteria": {
            "centrality_explicit": candidate.centrality_explicit,
            "used_in_assessment": candidate.used_in_assessment,
            "occurrence_count": candidate.occurrence_count,
            "cross_subject": candidate.cross_subject,
            "needs_own_explanation": candidate.needs_own_explanation,
        },
        "status": "pending",
    }
    with queue_path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(row, ensure_ascii=False, sort_keys=True) + "\n")


def _create_concept(
    path: Path,
    title: str,
    subject_id: str,
    transaction_id: str,
) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    rendered = Template(TEMPLATE_PATH.read_text(encoding="utf-8")).substitute(
        title=title,
        subject_id=subject_id,
        transaction_id=transaction_id,
    )
    descriptor, temporary_name = tempfile.mkstemp(prefix=".concept-", dir=path.parent)
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="\n") as handle:
            handle.write(rendered.rstrip() + "\n")
            handle.flush()
            os.fsync(handle.fileno())
        try:
            os.link(temporary, path)
        except FileExistsError:
            return False
        return True
    finally:
        if temporary.exists():
            temporary.unlink()


def apply_concept_candidates(
    candidates: tuple[ConceptCandidate, ...],
    *,
    concepts_dir: Path,
    queue_path: Path,
    subject_id: str,
    transaction_id: str,
) -> tuple[ConceptAction, ...]:
    actions: list[ConceptAction] = []
    for candidate in candidates:
        title = _validated_title(candidate.title)
        path = concepts_dir / f"{title}.md"
        if path.exists():
            actions.append(ConceptAction(title, "link_existing", path))
        elif should_promote(candidate):
            created = _create_concept(path, title, subject_id, transaction_id)
            actions.append(
                ConceptAction(title, "create" if created else "link_existing", path)
            )
        else:
            _append_candidate(queue_path, candidate, subject_id, transaction_id)
            actions.append(ConceptAction(title, "queue", None))
    return tuple(actions)
