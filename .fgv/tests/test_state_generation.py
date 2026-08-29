import hashlib
import json
import multiprocessing
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


def _delayed_generation(vault: str, as_of: str, catalog_installed, release) -> None:
    from unittest.mock import patch

    import fgv_state.io as state_io
    from generate_state import generate

    real_replace = state_io.os.replace
    delayed = False

    def replace_then_pause(source, destination):
        nonlocal delayed
        result = real_replace(source, destination)
        if Path(destination).name == "catalog.jsonl" and not delayed:
            delayed = True
            catalog_installed.set()
            if not release.wait(10):
                raise TimeoutError("test release was not signalled")
        return result

    with patch("fgv_state.io.os.replace", side_effect=replace_then_pause):
        generate(Path(vault), as_of, check=False)


def _normal_generation(vault: str, as_of: str) -> None:
    from generate_state import generate

    generate(Path(vault), as_of, check=False)


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

    def test_missing_required_inputs_preserve_both_outputs(self):
        cases = (
            ("00 Home/Tasks.md", "required regular file"),
            ("90 Arquivo", "required regular directory"),
            ("10 Matérias/ContabilidadeFinanceira", "required regular directory"),
        )
        for relative, message in cases:
            with self.subTest(relative=relative), tempfile.TemporaryDirectory() as tmp:
                vault = CatalogTests().make_vault(Path(tmp))
                self.assertEqual(self.run_cli(vault).returncode, 0)
                outputs = [vault / "30 Sistema/Estado/catalog.jsonl", vault / "30 Sistema/Estado/dashboard-snapshot.md"]
                before = [path.read_bytes() for path in outputs]
                target = vault / relative
                target.rename(target.with_name(target.name + ".missing"))
                failed = self.run_cli(vault)
                self.assertEqual(failed.returncode, 2)
                self.assertIn(message, failed.stderr)
                self.assertEqual(before, [path.read_bytes() for path in outputs])

    def test_revalidation_mismatch_preserves_both_outputs(self):
        from unittest.mock import patch

        from generate_state import generate

        with tempfile.TemporaryDirectory() as tmp:
            vault = CatalogTests().make_vault(Path(tmp))
            self.assertEqual(self.run_cli(vault).returncode, 0)
            outputs = [vault / "30 Sistema/Estado/catalog.jsonl", vault / "30 Sistema/Estado/dashboard-snapshot.md"]
            before = [path.read_bytes() for path in outputs]
            with patch("generate_state.build_outputs", side_effect=[(b"first", b"pair"), (b"changed", b"pair")]):
                with self.assertRaisesRegex(ValueError, "changed during state build"):
                    generate(vault, "2026-08-28", check=False)
            self.assertEqual(before, [path.read_bytes() for path in outputs])

    def test_as_of_must_be_canonical_yyyy_mm_dd(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = CatalogTests().make_vault(Path(tmp))
            env = dict(os.environ)
            env["PYTHONPATH"] = str(ROOT / ".fgv/scripts")
            for value in ("2026-8-28", "2026-08-28T00:00:00", "２０２６-０８-２８"):
                completed = subprocess.run(
                    [sys.executable, str(SCRIPT), "--vault", str(vault), "--as-of", value],
                    text=True, capture_output=True, env=env, check=False,
                )
                self.assertEqual(completed.returncode, 2, (value, completed.stderr))
                self.assertIn("canonical YYYY-MM-DD", completed.stderr)

    def test_interprocess_lock_serializes_build_revalidation_and_pair_publication(self):
        if "fork" not in multiprocessing.get_all_start_methods():
            self.skipTest("requires POSIX fork")
        with tempfile.TemporaryDirectory() as tmp:
            vault = CatalogTests().make_vault(Path(tmp))
            self.assertEqual(self.run_cli(vault).returncode, 0)
            context = multiprocessing.get_context("fork")
            installed = context.Event()
            release = context.Event()
            first = context.Process(target=_delayed_generation, args=(str(vault), "2026-08-29", installed, release))
            first.start()
            self.assertTrue(installed.wait(10), "first writer never installed catalog")
            second = context.Process(target=_normal_generation, args=(str(vault), "2026-08-30"))
            second.start()
            time.sleep(0.25)
            self.assertTrue(second.is_alive(), "second writer bypassed the interprocess lock")
            release.set()
            first.join(10)
            second.join(10)
            self.assertEqual(first.exitcode, 0)
            self.assertEqual(second.exitcode, 0)
            catalog = (vault / "30 Sistema/Estado/catalog.jsonl").read_bytes()
            snapshot = (vault / "30 Sistema/Estado/dashboard-snapshot.md").read_text(encoding="utf-8")
            manifest = json.loads(catalog.splitlines()[0])
            expected = "sha256:" + hashlib.sha256(catalog).hexdigest()
            self.assertEqual(manifest["as_of"], "2026-08-30")
            self.assertIn("as_of: 2026-08-30", snapshot)
            self.assertIn(f'catalog_sha256: "{expected}"', snapshot)


if __name__ == "__main__":
    unittest.main()
