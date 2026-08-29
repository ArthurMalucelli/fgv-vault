import argparse
import json
from pathlib import Path
from typing import Callable

from .adapters import stage_adapters
from .locking import vault_lock
from .transaction import apply_transaction, build_plan, run_state


def plan_for_runtime(
    *,
    runtime: str,
    vault_root: Path,
    source: Path,
    analysis_path: Path,
    class_date: str,
) -> dict:
    return build_plan(
        runtime=runtime,
        vault_root=vault_root,
        source=source,
        analysis_path=analysis_path,
        class_date=class_date,
    )


def refresh_state(
    vault_root: Path,
    *,
    as_of: str,
    check: bool = False,
    runner: Callable[[list[str]], int] | None = None,
) -> int:
    with vault_lock(vault_root):
        return run_state(vault_root, as_of, check=check, runner=runner)


def apply_plan(
    plan: dict,
    *,
    vault_root: Path,
    source: Path,
    analysis_path: Path,
    processor: str,
    as_of: str,
    state_runner: Callable[[list[str]], int] | None = None,
    fault_hook: Callable[[str], None] | None = None,
) -> dict:
    return apply_transaction(
        plan,
        vault_root=vault_root,
        source=source,
        analysis_path=analysis_path,
        processor=processor,
        as_of=as_of,
        state_runner=state_runner,
        fault_hook=fault_hook,
    )


def _parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(description="FGV canonical academic workflow")
    commands = parser.add_subparsers(dest="command", required=True)
    plan = commands.add_parser("plan-plaud")
    plan.add_argument("--vault", type=Path, required=True)
    plan.add_argument("--source", type=Path, required=True)
    plan.add_argument("--analysis", type=Path, required=True)
    plan.add_argument("--class-date", required=True)
    plan.add_argument("--runtime", choices=("codex", "claude"), required=True)
    plan.add_argument("--output", type=Path)
    apply = commands.add_parser("apply-plaud")
    apply.add_argument("--plan", type=Path, required=True)
    apply.add_argument("--vault", type=Path, required=True)
    apply.add_argument("--source", type=Path, required=True)
    apply.add_argument("--analysis", type=Path, required=True)
    apply.add_argument("--processor", choices=("codex", "claude"), required=True)
    apply.add_argument("--as-of", required=True)
    state = commands.add_parser("build-state")
    state.add_argument("--vault", type=Path, required=True)
    state.add_argument("--as-of", required=True)
    state.add_argument("--check", action="store_true")
    adapters = commands.add_parser("stage-adapters")
    adapters.add_argument("--output", type=Path, required=True)
    return parser


def main(argv: list[str] | None = None) -> int:
    args = _parser().parse_args(argv)
    if args.command == "plan-plaud":
        payload = plan_for_runtime(
            runtime=args.runtime,
            vault_root=args.vault,
            source=args.source,
            analysis_path=args.analysis,
            class_date=args.class_date,
        )
        encoded = json.dumps(payload, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
        if args.output:
            args.output.write_text(encoded, encoding="utf-8")
        else:
            print(encoded, end="")
        return 0
    if args.command == "apply-plaud":
        result = apply_plan(
            json.loads(args.plan.read_text(encoding="utf-8")),
            vault_root=args.vault,
            source=args.source,
            analysis_path=args.analysis,
            processor=args.processor,
            as_of=args.as_of,
        )
        print(json.dumps(result, ensure_ascii=False, indent=2, sort_keys=True))
        return 0 if result["state"] == "complete" else 1
    if args.command == "build-state":
        return refresh_state(args.vault, as_of=args.as_of, check=args.check)
    result = stage_adapters(args.output)
    print(f"staged adapters: {result.codex}, {result.claude}")
    print("live installations modified: 0")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
