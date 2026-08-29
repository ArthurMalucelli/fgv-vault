import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time
import unittest
from pathlib import Path

from test_catalog import CatalogTests


ROOT = Path(__file__).resolve().parents[2]
SCRIPT = ROOT / ".fgv/scripts/generate_state.py"


class StateGenerationTests(unittest.TestCase):
    def run_cli(self, vault: Path, *extra: str):
        env = dict(os.environ)
        env["PYTHONPATH"] = str(ROOT / ".fgv/scripts")
        return subprocess.run([sys.executable, str(SCRIPT), "--vault", str(vault), "--as-of", "2026-08-28", *extra],
                              text=True, capture_output=True, env=env, check=False)

    def test_generate_check_write_if_changed_and_cross_hash(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = CatalogTests().make_vault(Path(tmp))
            first = self.run_cli(vault)
            self.assertEqual(first.returncode, 0, first.stderr)
            catalog = vault / "30 Sistema/Estado/catalog.jsonl"
            snapshot = vault / "30 Sistema/Estado/dashboard-snapshot.md"
            before = (catalog.read_bytes(), snapshot.read_bytes(), catalog.stat().st_mtime_ns, snapshot.stat().st_mtime_ns)
            time.sleep(0.01)
            second = self.run_cli(vault)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(before, (catalog.read_bytes(), snapshot.read_bytes(), catalog.stat().st_mtime_ns, snapshot.stat().st_mtime_ns))
            self.assertEqual(self.run_cli(vault, "--check").returncode, 0)
            expected = "sha256:" + hashlib.sha256(catalog.read_bytes()).hexdigest()
            self.assertIn(expected, snapshot.read_text(encoding="utf-8"))

    def test_failure_leaves_both_outputs_unchanged(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = CatalogTests().make_vault(Path(tmp))
            self.assertEqual(self.run_cli(vault).returncode, 0)
            outputs = [vault / "30 Sistema/Estado/catalog.jsonl", vault / "30 Sistema/Estado/dashboard-snapshot.md"]
            before = [path.read_bytes() for path in outputs]
            (vault / "30 Sistema/Tutor/concepts-history.json").write_text("{broken", encoding="utf-8")
            self.assertEqual(self.run_cli(vault).returncode, 2)
            self.assertEqual(before, [path.read_bytes() for path in outputs])

    def test_check_reports_stale_without_writing_and_environment_does_not_change_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = CatalogTests().make_vault(Path(tmp))
            self.assertEqual(self.run_cli(vault).returncode, 0)
            outputs = [vault / "30 Sistema/Estado/catalog.jsonl", vault / "30 Sistema/Estado/dashboard-snapshot.md"]
            first = [path.read_bytes() for path in outputs]
            env = dict(os.environ)
            env.update(PYTHONPATH=str(ROOT / ".fgv/scripts"), TZ="UTC", LC_ALL="C")
            rerun = subprocess.run(
                [sys.executable, str(SCRIPT), "--vault", str(vault), "--as-of", "2026-08-28"],
                text=True, capture_output=True, env=env, check=False,
            )
            self.assertEqual(rerun.returncode, 0, rerun.stderr)
            self.assertEqual(first, [path.read_bytes() for path in outputs])
            home = vault / "00 Home/Home.md"
            home.write_text(home.read_text(encoding="utf-8") + "changed\n", encoding="utf-8")
            stale = self.run_cli(vault, "--check")
            self.assertEqual(stale.returncode, 1)
            self.assertIn("state stale", stale.stdout)
            self.assertEqual(first, [path.read_bytes() for path in outputs])


if __name__ == "__main__":
    unittest.main()
