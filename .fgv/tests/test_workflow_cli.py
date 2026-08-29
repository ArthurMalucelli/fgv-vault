from contextlib import redirect_stderr
from io import StringIO
import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from fgv_workflow.cli import _parser, plan_for_runtime, refresh_state
from fgv_workflow.locking import VaultLocked, vault_lock


class WorkflowCliTests(unittest.TestCase):
    def test_apply_cli_requires_explicit_operational_as_of(self) -> None:
        with redirect_stderr(StringIO()), self.assertRaises(SystemExit):
            _parser().parse_args(
                [
                    "apply-plaud",
                    "--plan",
                    "plan.json",
                    "--vault",
                    "vault",
                    "--source",
                    "plaud.txt",
                    "--analysis",
                    "analysis.json",
                    "--processor",
                    "codex",
                ]
            )
        parsed = _parser().parse_args(
            [
                "apply-plaud",
                "--plan",
                "plan.json",
                "--vault",
                "vault",
                "--source",
                "plaud.txt",
                "--analysis",
                "analysis.json",
                "--processor",
                "codex",
                "--as-of",
                "2026-08-28",
            ]
        )
        self.assertEqual(parsed.as_of, "2026-08-28")

    def test_dashboard_interface_fixture_matches_delegate(self) -> None:
        fixture = (
            Path(__file__).parent
            / "fixtures"
            / "dashboard"
            / "generate-state-interface.json"
        )
        payload = json.loads(fixture.read_text(encoding="utf-8"))
        self.assertEqual(payload["check_flag"], "--check")
        self.assertEqual(payload["command"][2:4], ["--vault", "<vault>"])
        self.assertEqual(payload["command"][4:6], ["--as-of", "YYYY-MM-DD"])

    def test_runtime_plans_have_identical_canonical_payload(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "plaud.txt"
            source.write_bytes(b"raw fixture\n")
            analysis = {
                "schema_version": 1,
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
                "schema_version": 1,
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
            self.assertTrue(
                plan["artifacts"]["transcrito"].endswith(
                    "Transcrito - DRE, provisões.md"
                )
            )

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
            self.assertEqual(
                refresh_state(vault, as_of="2026-08-28", check=True, runner=runner),
                0,
            )
            self.assertEqual(calls[0][1], generator.resolve().as_posix())
            self.assertEqual(
                calls[0][2:],
                ["--vault", vault.resolve().as_posix(), "--as-of", "2026-08-28", "--check"],
            )

    def test_refresh_state_uses_the_same_global_vault_lock(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            (vault / ".fgv" / "scripts").mkdir(parents=True)
            (vault / ".fgv" / "scripts" / "generate_state.py").write_text(
                "# fixture\n", encoding="utf-8"
            )
            calls = []
            with vault_lock(vault):
                with self.assertRaises(VaultLocked):
                    refresh_state(
                        vault,
                        as_of="2026-08-28",
                        check=True,
                        runner=lambda command: calls.append(command) or 0,
                    )
            self.assertEqual(calls, [])


if __name__ == "__main__":
    unittest.main()
