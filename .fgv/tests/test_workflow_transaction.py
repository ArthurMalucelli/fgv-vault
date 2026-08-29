import hashlib
import json
from pathlib import Path
import re
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch
import unicodedata

from fgv_workflow import transaction
from fgv_workflow.cli import apply_plan as _apply_plan, plan_for_runtime
from fgv_workflow.locking import VaultLocked, vault_lock
from fgv_workflow.plaud import AnalysisError, validate_analysis
from fgv_workflow.transaction import validate_plan


def apply_plan(plan: dict, **kwargs) -> dict:
    kwargs.setdefault("as_of", "2026-08-28")
    return _apply_plan(plan, **kwargs)


def analysis_payload() -> dict:
    return {
        "schema_version": 1,
        "subject_id": "contabilidade-financeira",
        "topic": "DRE e provisões",
        "cleaned_transcript": "## Competência\n\nTexto limpo.",
        "summary": "## Conceitos essenciais\n\nResumo denso.",
        "topics": ["DRE", "provisões"],
        "review_questions": ["1?", "2?", "3?", "4?", "5?"],
        "concept_candidates": [
            {
                "title": "Provisão",
                "centrality_explicit": True,
                "used_in_assessment": False,
                "occurrence_count": 1,
                "cross_subject": False,
                "needs_own_explanation": False,
            }
        ],
        "task_mentions": [
            {
                "description": "Revisar provisões",
                "due": "2026-09-04",
                "priority": "",
            }
        ],
        "calendar_mentions": [
            {
                "action": "reschedule",
                "calendar_alias": "classes",
                "payload": {
                    "event_id": "event-1",
                    "start": "2026-09-05T11:00:00-03:00",
                },
            }
        ],
    }


class FakeState:
    def __init__(self, vault: Path, fail_build_once: bool = False) -> None:
        self.vault = vault
        self.fail_build_once = fail_build_once
        self.calls: list[list[str]] = []

    def __call__(self, command: list[str]) -> int:
        self.calls.append(command)
        is_check = "--check" in command
        state = self.vault / "30 Sistema" / "Estado"
        if is_check:
            return 0 if (state / "catalog.jsonl").exists() else 1
        if self.fail_build_once:
            self.fail_build_once = False
            return 2
        state.mkdir(parents=True, exist_ok=True)
        (state / "catalog.jsonl").write_text('{"record_type":"manifest"}\n', encoding="utf-8")
        (state / "dashboard-snapshot.md").write_text("# Snapshot\n", encoding="utf-8")
        return 0


class WorkflowTransactionTests(unittest.TestCase):
    def test_new_parent_directories_are_fsynced_for_durability(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            destination = root / "first" / "second"
            synced = []
            original = transaction._fsync_directory

            def record(path: Path) -> None:
                synced.append(path)
                original(path)

            with patch.object(transaction, "_fsync_directory", side_effect=record):
                transaction._mkdir_parents_durable(destination)

            self.assertEqual(synced, [root, root / "first"])
            self.assertTrue(destination.is_dir())

    def test_shared_append_preserves_interleaved_external_edit(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "Tasks.md"
            path.write_bytes(b"base\n")
            original_write = transaction.os.write
            interleaved = False

            def write_with_external_edit(descriptor: int, data: bytes) -> int:
                nonlocal interleaved
                if not interleaved:
                    interleaved = True
                    with path.open("ab") as handle:
                        handle.write(b"external-edit\n")
                        handle.flush()
                return original_write(descriptor, data)

            with patch.object(
                transaction.os, "write", side_effect=write_with_external_edit
            ):
                transaction._append_shared_bytes(path, b"workflow-edit\n")

            self.assertEqual(
                path.read_bytes(), b"base\nexternal-edit\nworkflow-edit\n"
            )

    def make_fixture(self, root: Path) -> tuple[Path, Path, Path]:
        vault = root / "vault"
        scripts = vault / ".fgv" / "scripts"
        scripts.mkdir(parents=True)
        (scripts / "generate_state.py").write_text("# interface fixture\n", encoding="utf-8")
        source = root / "outside" / "plaud.txt"
        source.parent.mkdir()
        source.write_bytes(b"raw fixture\r\n")
        analysis = root / "outside" / "analysis.json"
        analysis.write_text(
            json.dumps(analysis_payload(), ensure_ascii=False),
            encoding="utf-8",
        )
        return vault, source, analysis

    def test_plan_is_closed_relative_and_fixes_every_destination(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault, source, analysis = self.make_fixture(root)
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                class_date="2026-08-28",
            )
            encoded = json.dumps(plan, ensure_ascii=False)
            self.assertNotIn(root.as_posix(), encoded)
            self.assertNotIn("source", plan)
            self.assertNotIn("analysis", plan)
            self.assertEqual(
                set(plan),
                {
                    "schema_version",
                    "contract_version",
                    "runtime",
                    "transaction_id",
                    "subject_id",
                    "class_date",
                    "source_name",
                    "source_sha256",
                    "analysis_sha256",
                    "raw_relpath",
                    "manifest_relpath",
                    "artifacts",
                    "concept_actions",
                    "task_actions",
                    "calendar_intents",
                    "requires_confirmation",
                },
            )
            self.assertIn(plan["transaction_id"], plan["raw_relpath"])
            self.assertTrue(plan["raw_relpath"].startswith("10 Matérias/"))

    def test_apply_preflights_state_then_completes_durable_receipt(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault, source, analysis = self.make_fixture(root)
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                class_date="2026-08-28",
            )
            state = FakeState(vault)
            transaction_path = (
                vault
                / "30 Sistema"
                / "Estado"
                / "workflow-transactions"
                / f"{plan['transaction_id']}.json"
            )

            def state_with_preflight_assertion(command: list[str]) -> int:
                if not state.calls:
                    self.assertFalse(transaction_path.exists())
                return state(command)

            receipt = apply_plan(
                plan,
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                processor="codex",
                state_runner=state_with_preflight_assertion,
            )
            self.assertEqual(receipt["state"], "complete")
            self.assertEqual(json.loads(transaction_path.read_text(encoding="utf-8")), receipt)
            self.assertEqual(
                state.calls[0][2:],
                ["--vault", vault.resolve().as_posix(), "--as-of", "2026-08-28", "--check"],
            )
            self.assertNotIn("--check", state.calls[1])
            self.assertIn("--check", state.calls[2])
            self.assertTrue(
                {"raw", "manifest", "transcrito", "resumo", "catalog", "snapshot"}
                .issubset(receipt["file_hashes"])
            )
            self.assertEqual(receipt["actions"]["tasks"][0]["tag"], "#cont")
            self.assertTrue(receipt["actions"]["calendar"][0]["requires_confirmation"])
            self.assertEqual(
                receipt["actions"]["calendar"][0]["relpath"],
                "30 Sistema/Estado/calendar-intents.jsonl",
            )
            for relative in plan["artifacts"].values():
                text = (vault / relative).read_text(encoding="utf-8")
                self.assertIn('tema: "DRE e provisões"', text)
                self.assertIn('atualizado_por: "codex"', text)

    def test_dashboard_as_of_is_operational_not_class_date(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault, source, analysis = self.make_fixture(root)
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                class_date="2025-02-03",
            )
            state = FakeState(vault)
            receipt = apply_plan(
                plan,
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                processor="codex",
                as_of="2026-08-28",
                state_runner=state,
            )
            self.assertEqual(receipt["as_of"], "2026-08-28")
            self.assertTrue(
                all(
                    command[command.index("--as-of") + 1] == "2026-08-28"
                    for command in state.calls
                )
            )

    def test_refresh_failure_is_state_pending_and_rerun_only_finishes(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault, source, analysis = self.make_fixture(root)
            plan = plan_for_runtime(
                runtime="claude",
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                class_date="2026-08-28",
            )
            failing = FakeState(vault, fail_build_once=True)
            first = apply_plan(
                plan,
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                processor="claude",
                state_runner=failing,
            )
            self.assertEqual(first["state"], "state_pending")
            tasks_before = (vault / "00 Home" / "Tasks.md").read_bytes()
            raw_before = (vault / plan["raw_relpath"]).read_bytes()
            second = apply_plan(
                plan,
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                processor="claude",
                state_runner=FakeState(vault),
            )
            self.assertEqual(second["state"], "complete")
            self.assertEqual((vault / "00 Home" / "Tasks.md").read_bytes(), tasks_before)
            self.assertEqual((vault / plan["raw_relpath"]).read_bytes(), raw_before)
            self.assertEqual(
                (vault / "00 Home" / "Tasks.md").read_text(encoding="utf-8").count("Revisar provisões"),
                1,
            )

    def test_apply_reauthenticates_external_inputs_before_writing(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault, source, analysis = self.make_fixture(root)
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                class_date="2026-08-28",
            )
            source.write_bytes(b"changed")
            with self.assertRaisesRegex(ValueError, "source hash"):
                apply_plan(
                    plan,
                    vault_root=vault,
                    source=source,
                    analysis_path=analysis,
                    processor="codex",
                    state_runner=FakeState(vault),
                )
            transaction_dir = vault / "30 Sistema" / "Estado" / "workflow-transactions"
            self.assertFalse(transaction_dir.exists())

    def test_apply_rejects_invalid_analysis_before_first_write(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault, source, analysis = self.make_fixture(root)
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                class_date="2026-08-28",
            )
            payload = analysis_payload()
            payload["review_questions"] = [1, 2, 3, 4, 5]
            analysis_bytes = json.dumps(payload, ensure_ascii=False).encode("utf-8")
            analysis.write_bytes(analysis_bytes)
            plan["analysis_sha256"] = hashlib.sha256(analysis_bytes).hexdigest()

            with self.assertRaisesRegex(AnalysisError, "review_questions"):
                apply_plan(
                    plan,
                    vault_root=vault,
                    source=source,
                    analysis_path=analysis,
                    processor="codex",
                    state_runner=FakeState(vault),
                )

            self.assertFalse(
                (vault / "30 Sistema" / "Estado" / "workflow-transactions").exists()
            )

    def test_destination_appearing_after_plan_is_never_overwritten(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault, source, analysis = self.make_fixture(root)
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                class_date="2026-08-28",
            )
            destination = vault / plan["artifacts"]["resumo"]
            destination.parent.mkdir(parents=True)
            destination.write_text("concurrent owner\n", encoding="utf-8")
            with self.assertRaisesRegex(FileExistsError, "artifact destination"):
                apply_plan(
                    plan,
                    vault_root=vault,
                    source=source,
                    analysis_path=analysis,
                    processor="codex",
                    state_runner=FakeState(vault),
                )
            self.assertEqual(destination.read_text(encoding="utf-8"), "concurrent owner\n")

    def test_noop_authenticates_artifact_hash(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault, source, analysis = self.make_fixture(root)
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                class_date="2026-08-28",
            )
            apply_plan(
                plan,
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                processor="codex",
                state_runner=FakeState(vault),
            )
            artifact = vault / plan["artifacts"]["resumo"]
            artifact.write_text("tampered\n", encoding="utf-8")
            with self.assertRaisesRegex(IOError, "artifact hash"):
                apply_plan(
                    plan,
                    vault_root=vault,
                    source=source,
                    analysis_path=analysis,
                    processor="codex",
                    state_runner=FakeState(vault),
                )

    def test_complete_rerun_is_byte_identical_noop(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault, source, analysis = self.make_fixture(root)
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                class_date="2026-08-28",
            )
            first = apply_plan(
                plan,
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                processor="codex",
                state_runner=FakeState(vault),
            )
            receipt_path = (
                vault
                / "30 Sistema"
                / "Estado"
                / "workflow-transactions"
                / f"{plan['transaction_id']}.json"
            )
            receipt_before = receipt_path.read_bytes()
            second = apply_plan(
                plan,
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                processor="codex",
                state_runner=FakeState(vault),
            )
            self.assertEqual(receipt_path.read_bytes(), receipt_before)
            self.assertEqual(second, first)
            self.assertEqual(second["actions"]["tasks"][0]["outcome"], "appended")

    def test_complete_receipt_is_immutable_when_state_check_errors(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault, source, analysis = self.make_fixture(root)
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                class_date="2026-08-28",
            )
            apply_plan(
                plan,
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                processor="codex",
                state_runner=FakeState(vault),
            )
            receipt_path = (
                vault
                / "30 Sistema"
                / "Estado"
                / "workflow-transactions"
                / f"{plan['transaction_id']}.json"
            )
            receipt_before = receipt_path.read_bytes()
            with self.assertRaisesRegex(RuntimeError, "state check failed"):
                apply_plan(
                    plan,
                    vault_root=vault,
                    source=source,
                    analysis_path=analysis,
                    processor="codex",
                    state_runner=lambda _command: 2,
                )
            self.assertEqual(receipt_path.read_bytes(), receipt_before)

    def test_complete_rerun_never_rebuilds_stale_global_state(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault, source, analysis = self.make_fixture(root)
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                class_date="2026-08-28",
            )
            apply_plan(
                plan,
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                processor="codex",
                state_runner=FakeState(vault),
            )
            receipt_path = (
                vault
                / "30 Sistema"
                / "Estado"
                / "workflow-transactions"
                / f"{plan['transaction_id']}.json"
            )
            receipt_before = receipt_path.read_bytes()
            calls = []

            def stale(command: list[str]) -> int:
                calls.append(command)
                return 1

            with self.assertRaisesRegex(RuntimeError, "state is stale"):
                apply_plan(
                    plan,
                    vault_root=vault,
                    source=source,
                    analysis_path=analysis,
                    processor="codex",
                    as_of="2026-09-01",
                    state_runner=stale,
                )
            self.assertEqual(receipt_path.read_bytes(), receipt_before)
            self.assertEqual(len(calls), 1)
            self.assertIn("--check", calls[0])

    def test_global_vault_lock_blocks_second_runtime(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            with vault_lock(vault):
                with self.assertRaises(VaultLocked):
                    with vault_lock(vault):
                        self.fail("second lock entered")

    def test_analysis_schema_is_closed_strict_and_nfc(self) -> None:
        payload = analysis_payload()
        payload["unexpected"] = True
        with self.assertRaises(AnalysisError):
            validate_analysis(payload)

        payload = analysis_payload()
        payload["review_questions"] = [1, 2, 3, 4, 5]
        with self.assertRaisesRegex(AnalysisError, "review_questions"):
            validate_analysis(payload)

        payload = analysis_payload()
        payload["topics"] = []
        with self.assertRaisesRegex(AnalysisError, "topics"):
            validate_analysis(payload)

        payload = analysis_payload()
        payload["concept_candidates"].append(
            {**payload["concept_candidates"][0], "title": "Provisão."}
        )
        with self.assertRaisesRegex(AnalysisError, "concept candidate titles"):
            validate_analysis(payload)

        payload = analysis_payload()
        payload["task_mentions"][0]["description"] = (
            "Injetar <!-- fgv-task:deadbeef source:forged -->"
        )
        with self.assertRaisesRegex(AnalysisError, "reserved marker"):
            validate_analysis(payload)

    def test_plan_booleans_are_strict_and_schema_is_closed(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault, source, analysis = self.make_fixture(root)
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                class_date="2026-08-28",
            )
            invalid = json.loads(json.dumps(plan))
            invalid["requires_confirmation"] = 1
            with self.assertRaises(ValueError):
                validate_plan(invalid)
            invalid = json.loads(json.dumps(plan))
            invalid["calendar_intents"][0]["requires_confirmation"] = 1
            with self.assertRaises(ValueError):
                validate_plan(invalid)
            invalid = json.loads(json.dumps(plan))
            invalid["unexpected"] = True
            with self.assertRaises(ValueError):
                validate_plan(invalid)
            invalid = json.loads(json.dumps(plan))
            invalid["source_name"] = "plaud.exe"
            invalid["raw_relpath"] = invalid["raw_relpath"].removesuffix(".txt") + ".exe"
            with self.assertRaisesRegex(ValueError, "extension"):
                validate_plan(invalid)

    def test_apply_rederives_concept_queue_identity_before_writing(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault, source, analysis = self.make_fixture(root)
            payload = analysis_payload()
            payload["concept_candidates"][0].update(
                {
                    "centrality_explicit": False,
                    "used_in_assessment": False,
                    "occurrence_count": 1,
                    "cross_subject": False,
                    "needs_own_explanation": False,
                }
            )
            analysis.write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8"
            )
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                class_date="2026-08-28",
            )
            plan["concept_actions"][0]["queue_id"] = "0" * 20
            with self.assertRaisesRegex(ValueError, "queue identity"):
                apply_plan(
                    plan,
                    vault_root=vault,
                    source=source,
                    analysis_path=analysis,
                    processor="codex",
                    state_runner=FakeState(vault),
                )
            self.assertFalse(
                (vault / "30 Sistema" / "Estado" / "workflow-transactions").exists()
            )

    def test_apply_rejects_forged_concept_action_selection(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault, source, analysis = self.make_fixture(root)
            payload = analysis_payload()
            payload["concept_candidates"][0].update(
                {
                    "centrality_explicit": False,
                    "used_in_assessment": False,
                    "occurrence_count": 1,
                    "cross_subject": False,
                    "needs_own_explanation": False,
                }
            )
            analysis.write_text(
                json.dumps(payload, ensure_ascii=False), encoding="utf-8"
            )
            concept = vault / "20 Conhecimento" / "Conceitos" / "Provisão.md"
            concept.parent.mkdir(parents=True)
            concept.write_text("existing concept\n", encoding="utf-8")
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                class_date="2026-08-28",
            )
            action = plan["concept_actions"][0]
            action.clear()
            action.update(
                {
                    "title": "Provisão",
                    "action": "queue",
                    "relpath": "30 Sistema/Estado/concept-candidates.jsonl",
                    "queue_id": hashlib.sha256(
                        f"{plan['transaction_id']}\0provisão".encode("utf-8")
                    ).hexdigest()[:20],
                }
            )
            with self.assertRaisesRegex(ValueError, "concept action selection"):
                apply_plan(
                    plan,
                    vault_root=vault,
                    source=source,
                    analysis_path=analysis,
                    processor="codex",
                    state_runner=FakeState(vault),
                )
            self.assertFalse(
                (vault / "30 Sistema" / "Estado" / "workflow-transactions").exists()
            )

    def test_shared_effect_stores_are_preflighted_before_first_write(self) -> None:
        cases = ("calendar", "tasks", "concepts")
        for case in cases:
            with self.subTest(case=case), TemporaryDirectory() as temporary_directory:
                root = Path(temporary_directory)
                vault, source, analysis = self.make_fixture(root)
                if case == "concepts":
                    payload = analysis_payload()
                    payload["concept_candidates"][0].update(
                        {
                            "centrality_explicit": False,
                            "used_in_assessment": False,
                            "occurrence_count": 1,
                            "cross_subject": False,
                            "needs_own_explanation": False,
                        }
                    )
                    analysis.write_text(
                        json.dumps(payload, ensure_ascii=False), encoding="utf-8"
                    )
                plan = plan_for_runtime(
                    runtime="codex",
                    vault_root=vault,
                    source=source,
                    analysis_path=analysis,
                    class_date="2026-08-28",
                )
                if case == "calendar":
                    damaged = (
                        vault / "30 Sistema" / "Estado" / "calendar-intents.jsonl"
                    )
                    damaged.parent.mkdir(parents=True, exist_ok=True)
                    damaged.write_text("{malformed\n", encoding="utf-8")
                elif case == "concepts":
                    damaged = (
                        vault / "30 Sistema" / "Estado" / "concept-candidates.jsonl"
                    )
                    damaged.parent.mkdir(parents=True, exist_ok=True)
                    damaged.write_text("{malformed\n", encoding="utf-8")
                else:
                    damaged = vault / "00 Home" / "Tasks.md"
                    damaged.parent.mkdir(parents=True, exist_ok=True)
                    damaged.write_bytes(b"\xff\xfe")
                with self.assertRaises((IOError, UnicodeError)):
                    apply_plan(
                        plan,
                        vault_root=vault,
                        source=source,
                        analysis_path=analysis,
                        processor="codex",
                        state_runner=FakeState(vault),
                    )
                self.assertFalse((vault / plan["raw_relpath"]).exists())
                self.assertFalse(
                    (
                        vault
                        / "30 Sistema"
                        / "Estado"
                        / "workflow-transactions"
                    ).exists()
                )

    def test_complete_rerun_rejects_duplicate_calendar_identity(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault, source, analysis = self.make_fixture(root)
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                class_date="2026-08-28",
            )
            apply_plan(
                plan,
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                processor="codex",
                state_runner=FakeState(vault),
            )
            calendar_path = (
                vault / "30 Sistema" / "Estado" / "calendar-intents.jsonl"
            )
            duplicate = dict(plan["calendar_intents"][0])
            duplicate["payload"] = dict(duplicate["payload"])
            duplicate["payload"]["start"] = "2099-01-01T00:00:00-03:00"
            with calendar_path.open("a", encoding="utf-8") as handle:
                handle.write(
                    json.dumps(
                        duplicate,
                        ensure_ascii=False,
                        sort_keys=True,
                        separators=(",", ":"),
                    )
                    + "\n"
                )
            with self.assertRaisesRegex(IOError, "duplicate JSONL identity"):
                apply_plan(
                    plan,
                    vault_root=vault,
                    source=source,
                    analysis_path=analysis,
                    processor="codex",
                    state_runner=FakeState(vault),
                )

    def test_complete_rerun_rejects_noncanonical_task_marker_line(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault, source, analysis = self.make_fixture(root)
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                class_date="2026-08-28",
            )
            apply_plan(
                plan,
                vault_root=vault,
                source=source,
                analysis_path=analysis,
                processor="codex",
                state_runner=FakeState(vault),
            )
            tasks = vault / "00 Home" / "Tasks.md"
            tasks.write_text(
                tasks.read_text(encoding="utf-8").replace(
                    "- [ ] Revisar provisões",
                    "- [ ] texto injetado Revisar provisões",
                ),
                encoding="utf-8",
            )
            with self.assertRaisesRegex(IOError, "task marker content mismatch"):
                apply_plan(
                    plan,
                    vault_root=vault,
                    source=source,
                    analysis_path=analysis,
                    processor="codex",
                    state_runner=FakeState(vault),
                )

    def test_crash_after_each_local_effect_rolls_forward_without_duplicates(self) -> None:
        stages = (
            "raw",
            "manifest",
            "artifact:transcrito",
            "artifact:resumo",
            "concepts",
            "tasks",
            "calendar",
            "state_build",
            "state_check",
        )
        for stage in stages:
            with self.subTest(stage=stage), TemporaryDirectory() as temporary_directory:
                root = Path(temporary_directory)
                vault, source, analysis = self.make_fixture(root)
                plan = plan_for_runtime(
                    runtime="codex",
                    vault_root=vault,
                    source=source,
                    analysis_path=analysis,
                    class_date="2026-08-28",
                )

                def crash(current: str) -> None:
                    if current == stage:
                        raise RuntimeError(f"crash:{stage}")

                with self.assertRaisesRegex(RuntimeError, f"crash:{re.escape(stage)}"):
                    apply_plan(
                        plan,
                        vault_root=vault,
                        source=source,
                        analysis_path=analysis,
                        processor="codex",
                        state_runner=FakeState(vault),
                        fault_hook=crash,
                    )
                receipt = apply_plan(
                    plan,
                    vault_root=vault,
                    source=source,
                    analysis_path=analysis,
                    processor="codex",
                    state_runner=FakeState(vault),
                )
                self.assertEqual(receipt["state"], "complete")
                self.assertEqual(
                    (vault / "00 Home" / "Tasks.md").read_text(encoding="utf-8").count(
                        "Revisar provisões"
                    ),
                    1,
                )
                calendar = vault / "30 Sistema" / "Estado" / "calendar-intents.jsonl"
                self.assertEqual(len(calendar.read_text(encoding="utf-8").splitlines()), 1)
        payload = analysis_payload()
        payload["concept_candidates"][0]["centrality_explicit"] = 1
        with self.assertRaises(AnalysisError):
            validate_analysis(payload)
        payload = analysis_payload()
        payload["task_mentions"][0]["description"] = "linha 1\nlinha 2"
        with self.assertRaises(AnalysisError):
            validate_analysis(payload)
        payload = analysis_payload()
        payload["topic"] = unicodedata.normalize("NFD", "provisões")
        with self.assertRaises(AnalysisError):
            validate_analysis(payload)
        payload = analysis_payload()
        payload["calendar_mentions"][0]["payload"] = {"event_id": "event-1"}
        with self.assertRaises(AnalysisError):
            validate_analysis(payload)
if __name__ == "__main__":
    unittest.main()
