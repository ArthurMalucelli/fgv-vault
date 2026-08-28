import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

import apply_migration


MANIFEST_FIELDS = (
    "schema_version",
    "source",
    "destination",
    "sha256",
    "size_bytes",
    "category",
    "phase",
    "reason",
)


class MigrationApplyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        self.vault = Path(self.temporary.name)
        self.payloads = {
            "legacy/a.txt": b"alpha\n",
            "legacy/deep/b.bin": b"\x00\xffbinary\r\n",
            "solo.txt": b"solo\n",
        }
        self.destinations = {
            "legacy/a.txt": "new/one/a.txt",
            "legacy/deep/b.bin": "new/two/b.bin",
            "solo.txt": "new/three/solo.txt",
        }
        for relative, payload in self.payloads.items():
            path = self.vault / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_bytes(payload)
        self.manifest_path = self.vault / "state/manifest.json"
        self.manifest_path.parent.mkdir(parents=True)
        self.records = self._records()
        self._write_manifest(self.records)
        self._git("init", "-q")
        self._git("config", "user.email", "migration-tests@example.invalid")
        self._git("config", "user.name", "Migration Tests")
        self._git("add", ".")
        self._git("commit", "-qm", "fixture")
        self.head = self._git("rev-parse", "HEAD").stdout.decode().strip()

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _git(self, *arguments: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ("git", *arguments),
            cwd=self.vault,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def _records(self) -> list[dict[str, object]]:
        records = []
        for source in sorted(self.payloads):
            payload = self.payloads[source]
            records.append(
                dict(
                    zip(
                        MANIFEST_FIELDS,
                        (
                            1,
                            source,
                            self.destinations[source],
                            hashlib.sha256(payload).hexdigest(),
                            len(payload),
                            "home",
                            "structural",
                            "test fixture",
                        ),
                    )
                )
            )
        return records

    def _write_manifest(self, records: object, path: Path | None = None) -> None:
        target = path or self.manifest_path
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_text(json.dumps(records) + "\n", encoding="utf-8")

    def _args(self, *, dry_run: bool = False, manifest: str = "state/manifest.json") -> list[str]:
        arguments = [
            "--vault",
            str(self.vault),
            "--manifest",
            manifest,
            "--phase",
            "structural",
            "--expected-head",
            self.head,
        ]
        if dry_run:
            arguments.append("--dry-run")
        return arguments

    def _run(self, *, dry_run: bool = False, manifest: str = "state/manifest.json") -> tuple[int, str, str]:
        stdout = io.StringIO()
        stderr = io.StringIO()
        with patch("sys.stdout", stdout), patch("sys.stderr", stderr):
            result = apply_migration.main(self._args(dry_run=dry_run, manifest=manifest))
        return result, stdout.getvalue(), stderr.getvalue()

    def _snapshot(self) -> tuple[tuple[str, str, bytes | str | None], ...]:
        entries = []
        for path in sorted(self.vault.rglob("*")):
            relative = path.relative_to(self.vault).as_posix()
            if relative == ".git" or relative.startswith(".git/"):
                continue
            if path.is_symlink():
                entries.append((relative, "symlink", os.readlink(path)))
            elif path.is_dir():
                entries.append((relative, "directory", None))
            else:
                entries.append((relative, "file", path.read_bytes()))
        return tuple(entries)

    def _assert_sources_only(self) -> None:
        for source, destination in self.destinations.items():
            self.assertTrue((self.vault / source).is_file(), source)
            self.assertFalse((self.vault / destination).exists(), destination)

    def _assert_destinations_only(self) -> None:
        for source, destination in self.destinations.items():
            self.assertFalse((self.vault / source).exists(), source)
            self.assertEqual((self.vault / destination).read_bytes(), self.payloads[source])

    def test_dry_run_reports_plan_without_changing_paths_or_bytes(self) -> None:
        before = self._snapshot()

        result, stdout, stderr = self._run(dry_run=True)

        self.assertEqual(result, 0, stderr)
        self.assertEqual(
            stdout,
            "planned_moves=3\npreflight=ok\nfiles_written=0\n",
        )
        self.assertEqual(self._snapshot(), before)

    def test_divergent_head_and_invalid_expected_oid_block(self) -> None:
        (self.vault / "unrelated.txt").write_text("next", encoding="utf-8")
        self._git("add", "unrelated.txt")
        self._git("commit", "-qm", "next")
        before = self._snapshot()

        result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("HEAD does not match expected-head", stderr)
        self.assertEqual(self._snapshot(), before)

        arguments = self._args()
        arguments[arguments.index(self.head)] = "HEAD"
        with patch("sys.stderr", io.StringIO()) as error:
            self.assertEqual(apply_migration.main(arguments), 1)
            self.assertIn("full object ID", error.getvalue())

    def test_missing_source_existing_destination_and_hash_mismatch_preflight_all_moves(self) -> None:
        mutations = ("missing", "destination", "hash")
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                with self._fresh_fixture() as fixture:
                    source = fixture.vault / "legacy/deep/b.bin"
                    if mutation == "missing":
                        source.unlink()
                    elif mutation == "destination":
                        destination = fixture.vault / "new/two/b.bin"
                        destination.parent.mkdir(parents=True)
                        destination.write_bytes(b"occupied")
                    else:
                        source.write_bytes(b"tampered")
                    before = fixture._snapshot()
                    with patch("apply_migration.os.rename") as rename:
                        result, _, stderr = fixture._run()
                    self.assertEqual(result, 1)
                    self.assertTrue(stderr.startswith("error: "), stderr)
                    rename.assert_not_called()
                    self.assertEqual(fixture._snapshot(), before)

    def test_source_destination_and_ancestor_symlinks_are_rejected(self) -> None:
        mutations = ("source", "destination", "source-ancestor", "destination-ancestor")
        for mutation in mutations:
            with self.subTest(mutation=mutation):
                with self._fresh_fixture() as fixture:
                    if mutation == "source":
                        source = fixture.vault / "legacy/a.txt"
                        source.unlink()
                        os.symlink("../solo.txt", source)
                    elif mutation == "destination":
                        destination = fixture.vault / "new/one/a.txt"
                        destination.parent.mkdir(parents=True)
                        os.symlink("../../../solo.txt", destination)
                    elif mutation == "source-ancestor":
                        shutil.rmtree(fixture.vault / "legacy/deep")
                        os.symlink(".", fixture.vault / "legacy/deep")
                    else:
                        os.symlink("legacy", fixture.vault / "new")
                    before = fixture._snapshot()
                    with patch("apply_migration.os.rename") as rename:
                        result, _, stderr = fixture._run()
                    self.assertEqual(result, 1)
                    self.assertIn("symlink", stderr)
                    rename.assert_not_called()
                    self.assertEqual(fixture._snapshot(), before)

    def test_injected_midway_failure_rolls_back_moves_and_created_directories(self) -> None:
        (self.vault / "new").mkdir()
        before = self._snapshot()
        real_link = os.link
        calls = 0

        def fail_second(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected link failure")
            return real_link(*args, **kwargs)

        with patch("apply_migration.os.link", side_effect=fail_second):
            result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("injected link failure", stderr)
        self.assertEqual(self._snapshot(), before)
        self.assertTrue((self.vault / "new").is_dir())

    def test_destination_created_after_preflight_is_never_overwritten(self) -> None:
        destination = self.vault / "new/one/a.txt"
        destination.parent.mkdir(parents=True)
        real_link = os.link
        raced = False

        def race_destination(*args, **kwargs):
            nonlocal raced
            if not raced:
                raced = True
                destination.write_bytes(b"racer owns this path")
            return real_link(*args, **kwargs)

        with patch("apply_migration.os.link", side_effect=race_destination):
            result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("destination appeared after preflight", stderr)
        self.assertEqual(destination.read_bytes(), b"racer owns this path")
        for source in self.destinations:
            self.assertTrue((self.vault / source).is_file(), source)
        for other in set(self.destinations.values()) - {"new/one/a.txt"}:
            self.assertFalse((self.vault / other).exists(), other)

    def test_destination_parent_swap_before_link_never_unlinks_source(self) -> None:
        parent = self.vault / "new/one"
        parent.mkdir(parents=True)
        detached = self.vault / "detached"
        real_link = os.link
        swapped = False

        def swap_parent(*args, **kwargs):
            nonlocal swapped
            if not swapped:
                swapped = True
                parent.rename(detached)
                parent.mkdir()
            return real_link(*args, **kwargs)

        with patch("apply_migration.os.link", side_effect=swap_parent):
            result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("changed after preflight", stderr)
        for source in self.destinations:
            self.assertTrue((self.vault / source).is_file(), source)
        self.assertEqual(list(detached.iterdir()), [])

    def test_rollback_failure_is_reported_as_critical(self) -> None:
        real_link = os.link
        calls = 0

        def fail_apply_and_rollback(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls in {2, 3}:
                raise OSError(f"injected link failure {calls}")
            return real_link(*args, **kwargs)

        with patch(
            "apply_migration.os.link", side_effect=fail_apply_and_rollback
        ):
            result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("CRITICAL rollback failed", stderr)
        self.assertIn("injected link failure 2", stderr)
        self.assertIn("injected link failure 3", stderr)

    def test_complete_application_preserves_every_hash_and_count(self) -> None:
        result, stdout, stderr = self._run()

        self.assertEqual(result, 0, stderr)
        self.assertEqual(stdout, "planned_moves=3\npreflight=ok\nfiles_moved=3\n")
        self._assert_destinations_only()
        hashes = {
            hashlib.sha256((self.vault / destination).read_bytes()).hexdigest()
            for destination in self.destinations.values()
        }
        self.assertEqual(hashes, {record["sha256"] for record in self.records})
        self.assertEqual(len(hashes), len(self.records))

    def test_second_complete_application_is_explicit_no_op(self) -> None:
        first, _, first_error = self._run()
        self.assertEqual(first, 0, first_error)
        before = self._snapshot()

        second, stdout, stderr = self._run()

        self.assertEqual(second, 0, stderr)
        self.assertEqual(
            stdout,
            "planned_moves=0\npreflight=ok\nfiles_moved=0\nno_op=true\n",
        )
        self.assertEqual(self._snapshot(), before)

    def test_partially_moved_state_fails_closed_without_further_changes(self) -> None:
        source = self.vault / "legacy/a.txt"
        destination = self.vault / "new/one/a.txt"
        destination.parent.mkdir(parents=True)
        source.rename(destination)
        before = self._snapshot()

        result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("partially applied", stderr)
        self.assertEqual(self._snapshot(), before)

    def test_manifest_changed_after_preflight_cannot_redirect_moves(self) -> None:
        redirected = [dict(record) for record in self.records]
        redirected[0]["destination"] = "redirected/owned.txt"
        real_link = os.link
        changed = False

        def mutate_manifest_then_link(*args, **kwargs):
            nonlocal changed
            if not changed:
                changed = True
                self._write_manifest(redirected)
            return real_link(*args, **kwargs)

        with patch("apply_migration.os.link", side_effect=mutate_manifest_then_link):
            result, _, stderr = self._run()

        self.assertEqual(result, 0, stderr)
        self._assert_destinations_only()
        self.assertFalse((self.vault / "redirected/owned.txt").exists())

    def test_source_changed_after_preflight_is_rejected_before_link(self) -> None:
        real_hash_open_file = apply_migration._hash_open_file
        hash_calls = 0

        def mutate_before_apply(parent_fd, name, label):
            nonlocal hash_calls
            hash_calls += 1
            if hash_calls == len(self.records) + 1:
                (self.vault / "legacy/a.txt").write_bytes(b"omega\n")
            return real_hash_open_file(parent_fd, name, label)

        with patch(
            "apply_migration._hash_open_file", side_effect=mutate_before_apply
        ), patch("apply_migration.os.link") as link:
            result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("source hash mismatch", stderr)
        link.assert_not_called()
        for destination in self.destinations.values():
            self.assertFalse((self.vault / destination).exists())

    def test_manifest_must_be_regular_non_symlink_inside_vault(self) -> None:
        outside = self.vault.parent / f"{self.vault.name}-outside.json"
        self.addCleanup(outside.unlink, missing_ok=True)
        self._write_manifest(self.records, outside)
        result, _, stderr = self._run(manifest=str(outside))
        self.assertEqual(result, 1)
        self.assertIn("inside vault", stderr)

        backup = self.vault / "state/real.json"
        self.manifest_path.rename(backup)
        os.symlink("real.json", self.manifest_path)
        result, _, stderr = self._run()
        self.assertEqual(result, 1)
        self.assertIn("symlink", stderr)

    def test_manifest_ancestor_symlink_is_rejected(self) -> None:
        real_state = self.vault / "real-state"
        self.manifest_path.parent.rename(real_state)
        os.symlink("real-state", self.vault / "state")

        result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("symlink", stderr)

    def test_closed_schema_and_requested_phase_are_validated(self) -> None:
        invalid = [dict(record) for record in self.records]
        invalid[0]["extra"] = True
        self._write_manifest(invalid)
        result, _, stderr = self._run()
        self.assertEqual(result, 1)
        self.assertIn("invalid schema", stderr)

        self._write_manifest(self.records)
        arguments = self._args()
        arguments[arguments.index("structural")] = "rewrite"
        with patch("sys.stderr", io.StringIO()) as error:
            self.assertEqual(apply_migration.main(arguments), 1)
            self.assertIn("phase must be structural", error.getvalue())

    def _fresh_fixture(self):
        outer = self

        class FreshFixture:
            def __enter__(self):
                self.case = MigrationApplyTests(methodName="runTest")
                self.case.setUp()
                return self.case

            def __exit__(self, exc_type, exc_value, traceback):
                self.case.tearDown()
                return False

        return FreshFixture()


if __name__ == "__main__":
    unittest.main()
