import argparse
from dataclasses import asdict
from datetime import date, datetime, timezone
import hashlib
import json
from pathlib import Path
import subprocess
import sys
from typing import Callable

from .adapters import stage_adapters
from .calendar import build_calendar_intent, queue_intent
from .concepts import ConceptCandidate, apply_concept_candidates
from .naming import clean_topic, lesson_dir
from .plaud import process_plaud, validate_analysis
from .source_store import make_transaction_id
from .subjects import SubjectRegistry
from .tasks import TaskMention, append_tasks


def _sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def plan_for_runtime(
    *,
    runtime: str,
    vault_root: Path,
    source: Path,
    analysis_path: Path,
    class_date: str,
) -> dict:
    if runtime not in {"codex", "claude"}:
        raise ValueError(f"unsupported local runtime: {runtime}")
    resolved_date = date.fromisoformat(class_date)
    analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
    validate_analysis(analysis)
    registry = SubjectRegistry.load_default()
    subject = registry.resolve(analysis["subject_id"])
    source_sha256 = _sha256(source)
    transaction_id = make_transaction_id(source_sha256, subject.id, class_date)
    lesson = lesson_dir(vault_root, subject, resolved_date)
    topic = clean_topic(analysis["topic"])
    calendar_intents = [
        asdict(
            build_calendar_intent(
                transaction_id=transaction_id,
                action=item["action"],
                calendar_alias=item["calendar_alias"],
                payload=item["payload"],
            )
        )
        for item in analysis["calendar_mentions"]
    ]
    return {
        "schema_version": 1,
        "contract_version": 1,
        "runtime": runtime,
        "transaction_id": transaction_id,
        "subject_id": subject.id,
        "class_date": class_date,
        "source": source.resolve().as_posix(),
        "analysis": analysis_path.resolve().as_posix(),
        "source_sha256": source_sha256,
        "raw_relpath": (
            lesson / "Fontes" / f"Plaud - original{source.suffix.lower() or '.txt'}"
        ).relative_to(vault_root).as_posix(),
        "artifacts": [
            (lesson / f"Transcrito - {topic}.md").relative_to(vault_root).as_posix(),
            (lesson / f"Resumo - {topic}.md").relative_to(vault_root).as_posix(),
        ],
        "concept_candidates": analysis["concept_candidates"],
        "task_mentions": analysis["task_mentions"],
        "calendar_intents": calendar_intents,
        "requires_confirmation": any(
            item["requires_confirmation"] for item in calendar_intents
        ),
    }


def refresh_state(
    vault_root: Path,
    *,
    runner: Callable[[list[str]], int] | None = None,
) -> int:
    generator = vault_root / ".fgv" / "scripts" / "generate_state.py"
    if not generator.is_file():
        raise FileNotFoundError(f"canonical state generator not found: {generator}")
    command = [sys.executable, generator.as_posix(), "--vault-root", vault_root.as_posix()]
    if runner is not None:
        return runner(command)
    return subprocess.run(command, check=False).returncode


def apply_plan(plan: dict, *, processor: str) -> dict:
    if plan.get("schema_version") != 1 or plan.get("contract_version") != 1:
        raise ValueError("unsupported ingest plan")
    vault_root = Path(plan["vault_root"]) if "vault_root" in plan else None
    if vault_root is None:
        raise ValueError("apply plan requires vault_root")
    source = Path(plan["source"])
    analysis_path = Path(plan["analysis"])
    analysis = json.loads(analysis_path.read_text(encoding="utf-8"))
    expected = plan_for_runtime(
        runtime=plan["runtime"],
        vault_root=vault_root,
        source=source,
        analysis_path=analysis_path,
        class_date=plan["class_date"],
    )
    expected["vault_root"] = vault_root.as_posix()
    if expected != plan:
        raise ValueError("ingest plan no longer matches its inputs")
    result = process_plaud(
        vault_root=vault_root,
        source=source,
        class_date=date.fromisoformat(plan["class_date"]),
        analysis=analysis,
        processor=processor,
        ingested_at=datetime.now(timezone.utc),
    )
    candidates = tuple(ConceptCandidate(**item) for item in analysis["concept_candidates"])
    apply_concept_candidates(
        candidates,
        concepts_dir=vault_root / "20 Conhecimento" / "Conceitos",
        queue_path=vault_root / "30 Sistema" / "Estado" / "concept-candidates.jsonl",
        subject_id=plan["subject_id"],
        transaction_id=result.transaction_id,
    )
    mentions = tuple(TaskMention(**item) for item in analysis["task_mentions"])
    append_tasks(vault_root / "00 Home" / "Tasks.md", mentions, result.transaction_id)
    for item in plan["calendar_intents"]:
        intent = build_calendar_intent(
            transaction_id=result.transaction_id,
            action=item["action"],
            calendar_alias=item["calendar_alias"],
            payload=item["payload"],
        )
        queue_intent(
            vault_root / "30 Sistema" / "Estado" / "calendar-intents.jsonl",
            intent,
        )
    state_exit = refresh_state(vault_root)
    if state_exit != 0:
        raise RuntimeError(f"state refresh failed with exit {state_exit}")
    return {
        "transaction_id": result.transaction_id,
        "created": result.created,
        "raw": result.raw_path.relative_to(vault_root).as_posix(),
        "artifacts": [path.relative_to(vault_root).as_posix() for path in result.artifacts],
        "calendar_status": "pending",
        "state_refreshed": True,
    }


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FGV canonical academic workflow")
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan-plaud")
    plan.add_argument("--vault-root", type=Path, required=True)
    plan.add_argument("--source", type=Path, required=True)
    plan.add_argument("--analysis", type=Path, required=True)
    plan.add_argument("--class-date", required=True)
    plan.add_argument("--runtime", choices=("codex", "claude"), required=True)
    plan.add_argument("--output", type=Path)
    apply = commands.add_parser("apply-plaud")
    apply.add_argument("--plan", type=Path, required=True)
    apply.add_argument("--processor", required=True)
    state = commands.add_parser("build-state")
    state.add_argument("--vault-root", type=Path, required=True)
    adapters = commands.add_parser("stage-adapters")
    adapters.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "plan-plaud":
        payload = plan_for_runtime(
            runtime=args.runtime,
            vault_root=args.vault_root,
            source=args.source,
            analysis_path=args.analysis,
            class_date=args.class_date,
        )
        payload["vault_root"] = args.vault_root.resolve().as_posix()
        encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(encoded, encoding="utf-8")
        else:
            print(encoded, end="")
        return 0
    if args.command == "apply-plaud":
        result = apply_plan(
            json.loads(args.plan.read_text(encoding="utf-8")),
            processor=args.processor,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0
    if args.command == "build-state":
        return refresh_state(args.vault_root)
    result = stage_adapters(args.output)
    print(f"staged adapters: {result.codex}, {result.claude}")
    print("live installations modified: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
