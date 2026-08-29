from dataclasses import dataclass


@dataclass(frozen=True)
class ConceptCandidate:
    title: str
    centrality_explicit: bool
    used_in_assessment: bool
    occurrence_count: int
    cross_subject: bool
    needs_own_explanation: bool


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
