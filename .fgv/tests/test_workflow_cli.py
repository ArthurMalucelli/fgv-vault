import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from fgv_workflow.cli import apply_plan, plan_for_runtime, refresh_state


class WorkflowCliTests(unittest.TestCase):
    def test_runtime_plans_have_identical_canonical_payload(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "plaud.txt"
            source.write_bytes(b"raw fixture\n")
            analysis = {
                "subject_id": "contabilidade-financeira",
                "topic": "DRE e provisões",
                "cleaned_transcript": "Texto limpo.",
                "summary": "Resumo denso.",
                "topics": ["DRE"],
                "review_questions": ["1?", "2?", "3?", "4?", "5?"],
                "concept_candidates": [],
                "task_mentions": [],
                "calendar_mentions": [],
            }
            analysis_path = root / "analysis.json"
            analysis_path.write_text(json.dumps(analysis), encoding="utf-8")
            plans = [
                plan_for_runtime(
                    runtime=runtime,
                    vault_root=root / "vault",
                    source=source,
                    analysis_path=analysis_path,
                    class_date="2026-08-28",
                )
                for runtime in ("codex", "claude")
            ]
            normalized = []
            for plan in plans:
                current = dict(plan)
                current.pop("runtime")
                normalized.append(current)
            self.assertEqual(normalized[0], normalized[1])
            self.assertEqual(plans[0]["artifacts"], plans[1]["artifacts"])
            self.assertEqual(tuple((root / "vault").rglob("*")), ())

    def test_plan_uses_the_same_sanitized_topic_as_apply(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "plaud.txt"
            source.write_text("raw", encoding="utf-8")
            analysis = {
                "subject_id": "contabilidade-financeira",
                "topic": "DRE: provisões",
                "cleaned_transcript": "Texto.",
                "summary": "Resumo.",
                "topics": ["DRE"],
                "review_questions": ["1?", "2?", "3?", "4?", "5?"],
                "concept_candidates": [],
                "task_mentions": [],
                "calendar_mentions": [],
            }
            analysis_path = root / "analysis.json"
            analysis_path.write_text(json.dumps(analysis), encoding="utf-8")
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=root / "vault",
                source=source,
                analysis_path=analysis_path,
                class_date="2026-08-28",
            )
            self.assertTrue(plan["artifacts"][0].endswith("Transcrito - DRE, provisões.md"))

    def test_refresh_state_delegates_to_canonical_generator(self) -> None:
        calls = []

        def runner(command: list[str]) -> int:
            calls.append(command)
            return 0

        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            (vault / ".fgv" / "scripts").mkdir(parents=True)
            generator = vault / ".fgv" / "scripts" / "generate_state.py"
            generator.write_text("# fixture\n", encoding="utf-8")
            self.assertEqual(refresh_state(vault, runner=runner), 0)
            self.assertEqual(calls[0][1], generator.as_posix())
            self.assertIn("--vault-root", calls[0])

    def test_apply_runs_local_actions_then_delegates_state_refresh(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            vault = root / "vault"
            scripts = vault / ".fgv" / "scripts"
            scripts.mkdir(parents=True)
            (scripts / "generate_state.py").write_text(
                "from pathlib import Path\n"
                "import sys\n"
                "root = Path(sys.argv[2])\n"
                "path = root / '30 Sistema' / 'Estado' / 'refreshed.txt'\n"
                "path.parent.mkdir(parents=True, exist_ok=True)\n"
                "path.write_text('ok\\n', encoding='utf-8')\n",
                encoding="utf-8",
            )
            source = root / "plaud.txt"
            source.write_text("raw", encoding="utf-8")
            analysis = {
                "subject_id": "contabilidade-financeira",
                "topic": "DRE e provisões",
                "cleaned_transcript": "Texto limpo.",
                "summary": "Resumo denso.",
                "topics": ["DRE"],
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
                        "tag": "#cont",
                        "priority": "",
                    }
                ],
                "calendar_mentions": [
                    {
                        "action": "reschedule",
                        "calendar_alias": "classes",
                        "payload": {"event_id": "event-1", "start": "2026-09-05"},
                    }
                ],
            }
            analysis_path = root / "analysis.json"
            analysis_path.write_text(json.dumps(analysis), encoding="utf-8")
            plan = plan_for_runtime(
                runtime="codex",
                vault_root=vault,
                source=source,
                analysis_path=analysis_path,
                class_date="2026-08-28",
            )
            plan["vault_root"] = vault.resolve().as_posix()
            receipt = apply_plan(plan, processor="test")
            self.assertTrue(receipt["created"])
            self.assertTrue(receipt["state_refreshed"])
            self.assertTrue((vault / "30 Sistema" / "Estado" / "refreshed.txt").exists())
            self.assertTrue((vault / "20 Conhecimento" / "Conceitos" / "Provisão.md").exists())
            self.assertIn(
                "Revisar provisões",
                (vault / "00 Home" / "Tasks.md").read_text(encoding="utf-8"),
            )
            intents = vault / "30 Sistema" / "Estado" / "calendar-intents.jsonl"
            self.assertTrue(json.loads(intents.read_text(encoding="utf-8"))["requires_confirmation"])


if __name__ == "__main__":
    unittest.main()
