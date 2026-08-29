from collections import defaultdict
from datetime import date

from .models import DateEvidence, DateResolution


MIN_AUTO_CONFIDENCE = 0.90


def resolve_class_date(evidence: tuple[DateEvidence, ...]) -> DateResolution:
    by_value: dict[str, list[DateEvidence]] = defaultdict(list)
    for item in evidence:
        try:
            date.fromisoformat(item.value)
        except ValueError as error:
            raise ValueError(f"invalid evidence date: {item.value}") from error
        if not 0.0 <= item.confidence <= 1.0:
            raise ValueError("evidence confidence must be between 0 and 1")
        by_value[item.value].append(item)
    strong = {
        value: items
        for value, items in by_value.items()
        if max(item.confidence for item in items) >= MIN_AUTO_CONFIDENCE
    }
    if len(strong) != 1:
        return DateResolution(
            status="ambiguous",
            value=None,
            confidence=max((item.confidence for item in evidence), default=0.0),
            evidence=evidence,
        )
    value, items = next(iter(strong.items()))
    return DateResolution(
        status="resolved",
        value=value,
        confidence=max(item.confidence for item in items),
        evidence=evidence,
    )
