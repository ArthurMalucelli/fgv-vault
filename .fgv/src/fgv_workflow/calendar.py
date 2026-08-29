import hashlib
import json
from dataclasses import asdict
from pathlib import Path

from .models import CalendarIntent


ALLOWED_ACTIONS = {
    "append_description",
    "update_location",
    "create_assessment",
    "mark_cancelled",
    "reschedule",
}
DESTRUCTIVE_ACTIONS = {"mark_cancelled", "reschedule"}
CALENDAR_ALIASES = {"classes", "assessments"}


def make_action_id(
    transaction_id: str,
    action: str,
    calendar_alias: str,
    payload: dict,
) -> str:
    canonical = json.dumps(payload, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    material = f"{transaction_id}\0{action}\0{calendar_alias}\0{canonical}"
    return "cal-" + hashlib.sha256(material.encode("utf-8")).hexdigest()[:20]


def build_calendar_intent(
    *,
    transaction_id: str,
    action: str,
    calendar_alias: str,
    payload: dict,
) -> CalendarIntent:
    if action not in ALLOWED_ACTIONS:
        raise ValueError(f"unsupported calendar action: {action}")
    if calendar_alias not in CALENDAR_ALIASES:
        raise ValueError(f"unsupported calendar alias: {calendar_alias}")
    return CalendarIntent(
        schema_version=1,
        action_id=make_action_id(transaction_id, action, calendar_alias, payload),
        transaction_id=transaction_id,
        action=action,
        calendar_alias=calendar_alias,
        payload=payload,
        requires_confirmation=action in DESTRUCTIVE_ACTIONS,
        status="pending",
    )


def queue_intent(path: Path, intent: CalendarIntent) -> bool:
    path.parent.mkdir(parents=True, exist_ok=True)
    if path.exists():
        rows = [json.loads(line) for line in path.read_text(encoding="utf-8").splitlines()]
        if any(row.get("action_id") == intent.action_id for row in rows):
            return False
    with path.open("a", encoding="utf-8", newline="\n") as handle:
        handle.write(json.dumps(asdict(intent), ensure_ascii=False, sort_keys=True) + "\n")
    return True
