import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest

from fgv_workflow.adapters import LiveInstallDenied, stage_adapters
from fgv_workflow.installer import build_install_plan


def normative_lines(text: str) -> tuple[str, ...]:
    return tuple(
        line
        for line in text.splitlines()
        if line.startswith(("CONTRACT:", "CORE:", "CLI:", "GIT_ROLE:"))
    )


class WorkflowAdapterTests(unittest.TestCase):
    def test_tracked_staging_is_reproducible_from_templates(self) -> None:
        repository = Path(__file__).resolve().parents[2]
        tracked = repository / "30 Sistema" / "Estado" / "adapter-staging"
        with TemporaryDirectory() as temporary_directory:
            generated = stage_adapters(Path(temporary_directory) / "staging")
            for relative in (
                Path("codex/fgv/SKILL.md"),
                Path("claude/fgv/SKILL.md"),
                Path("manifest.json"),
            ):
                self.assertEqual(
                    (generated.root / relative).read_bytes(),
                    (tracked / relative).read_bytes(),
                )

    def test_codex_and_claude_stage_same_normative_contract(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            output = Path(temporary_directory) / "staging"
            result = stage_adapters(output)
            codex = result.codex.read_text(encoding="utf-8")
            claude = result.claude.read_text(encoding="utf-8")
            self.assertEqual(normative_lines(codex), normative_lines(claude))
            self.assertEqual(
                codex.split("\n## Ferramentas do runtime\n", 1)[0],
                claude.split("\n## Ferramentas do runtime\n", 1)[0],
            )
            self.assertIn("Nunca execute Git de rede", codex)
            self.assertIn("Nunca execute Git de rede", claude)
            self.assertIn("--as-of YYYY-MM-DD", codex)
            self.assertIn("--as-of YYYY-MM-DD", claude)
            manifest = json.loads(result.manifest.read_text(encoding="utf-8"))
            self.assertEqual(manifest["contract_version"], 1)
            self.assertTrue(manifest["parity"]["normative_contract_identical"])
            self.assertEqual(set(manifest["adapters"]), {"codex", "claude"})

    def test_stager_refuses_known_live_roots(self) -> None:
        for destination in (
            Path.home() / ".agents" / "skills",
            Path.home() / ".claude" / "skills",
            Path("/root/.hermes/skills"),
        ):
            with self.subTest(destination=destination):
                with self.assertRaises(LiveInstallDenied):
                    stage_adapters(destination)

    def test_installer_is_read_only_and_records_observed_destination(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            staged = stage_adapters(root / "staged")
            codex_destination = root / "runtime-codex" / "fgv" / "SKILL.md"
            claude_destination = root / "runtime-claude" / "fgv" / "SKILL.md"
            codex_destination.parent.mkdir(parents=True)
            claude_destination.parent.mkdir(parents=True)
            codex_destination.write_text("old codex\n", encoding="utf-8")
            claude_destination.write_text("old claude\n", encoding="utf-8")
            plan = build_install_plan(
                staged.manifest,
                {"codex": codex_destination, "claude": claude_destination},
                backup_root=root / "backup",
            )
            self.assertEqual(codex_destination.read_text(encoding="utf-8"), "old codex\n")
            self.assertEqual(plan.mode, "dry-run")
            by_runtime = {item.runtime: item for item in plan.operations}
            self.assertIsNotNone(by_runtime["codex"].destination_observed_sha256)
            self.assertEqual(codex_destination.read_text(encoding="utf-8"), "old codex\n")
            self.assertEqual(claude_destination.read_text(encoding="utf-8"), "old claude\n")

    def test_installer_cli_has_no_mutating_apply_mode(self) -> None:
        script = Path(__file__).resolve().parents[1] / "scripts" / "install_adapters.py"
        result = subprocess.run(
            [sys.executable, script.as_posix(), "--help"],
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0)
        self.assertNotIn("--apply", result.stdout)


if __name__ == "__main__":
    unittest.main()
