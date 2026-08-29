from dataclasses import dataclass
from typing import Any, Literal


@dataclass(frozen=True)
class DateEvidence:
    kind: Literal["explicit", "plaud", "transcript", "calendar", "mtime"]
    value: str
    confidence: float
    source: str


@dataclass(frozen=True)
class DateResolution:
    status: Literal["resolved", "ambiguous"]
    value: str | None
    confidence: float
    evidence: tuple[DateEvidence, ...]


@dataclass(frozen=True)
class SourceManifest:
    schema_version: int
    transaction_id: str
    subject_id: str
    class_date: str
    original_name: str
    raw_relpath: str
    source_sha256: str
    size_bytes: int
    ingested_at: str


@dataclass(frozen=True)
class CalendarIntent:
    schema_version: int
    action_id: str
    transaction_id: str
    action: str
    calendar_alias: str
    payload: dict[str, Any]
    requires_confirmation: bool
    status: Literal["pending", "confirmed", "applied", "failed"]
