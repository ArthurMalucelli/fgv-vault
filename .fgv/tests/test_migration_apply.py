import hashlib
import io
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
from tempfile import TemporaryDirectory
from types import SimpleNamespace
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
SCRIPT = Path(__file__).resolve().parents[1] / "scripts/apply_migration.py"


def _is_runtime_rename(source_name: str, destination_name: str = "") -> bool:
    prefixes = (
        ".migration-apply-journal",
        ".migration-apply-directory.",
        ".migration-apply-removed.",
    )
    return source_name.startswith(prefixes) or destination_name.startswith(prefixes)


class MigrationApplyTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        self.vault = Path(self.temporary.name)
        (self.vault / ".fgv").mkdir()
        self.journal_path = self.vault / ".fgv/migration-apply-journal.json"
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

    def _commit_fixture(self, message: str = "fixture update") -> None:
        self._git("add", ".")
        self._git("commit", "-qm", message)
        self.head = self._git("rev-parse", "HEAD").stdout.decode().strip()

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

    def test_valid_uncommitted_manifest_is_rejected_before_any_change(self) -> None:
        altered = [dict(record) for record in self.records]
        altered[0]["destination"] = "redirected/uncommitted.txt"
        self._write_manifest(altered)
        before = self._snapshot()

        result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("manifest does not match expected-head blob", stderr)
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
                    with patch("apply_migration._rename_noreplace") as rename:
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
                    with patch("apply_migration._rename_noreplace") as rename:
                        result, _, stderr = fixture._run()
                    self.assertEqual(result, 1)
                    self.assertIn("symlink", stderr)
                    rename.assert_not_called()
                    self.assertEqual(fixture._snapshot(), before)

    def test_injected_midway_failure_rolls_back_moves_and_created_directories(self) -> None:
        (self.vault / "new").mkdir()
        before = self._snapshot()
        real_move = apply_migration._rename_noreplace
        calls = 0

        def fail_second(*args, **kwargs):
            nonlocal calls
            if _is_runtime_rename(args[0], args[1]):
                return real_move(*args, **kwargs)
            calls += 1
            if calls == 2:
                raise OSError("injected rename failure")
            return real_move(*args, **kwargs)

        with patch("apply_migration._rename_noreplace", side_effect=fail_second):
            result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("injected rename failure", stderr)
        self.assertEqual(self._snapshot(), before)
        self.assertTrue((self.vault / "new").is_dir())

    def test_destination_created_after_preflight_is_never_overwritten(self) -> None:
        destination = self.vault / "new/one/a.txt"
        destination.parent.mkdir(parents=True)
        real_move = apply_migration._rename_noreplace
        raced = False

        def race_destination(*args, **kwargs):
            nonlocal raced
            if _is_runtime_rename(args[0], args[1]):
                return real_move(*args, **kwargs)
            if not raced:
                raced = True
                destination.write_bytes(b"racer owns this path")
            return real_move(*args, **kwargs)

        with patch(
            "apply_migration._rename_noreplace", side_effect=race_destination
        ):
            result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("destination appeared after preflight", stderr)
        self.assertEqual(destination.read_bytes(), b"racer owns this path")
        for source in self.destinations:
            self.assertTrue((self.vault / source).is_file(), source)
        for other in set(self.destinations.values()) - {"new/one/a.txt"}:
            self.assertFalse((self.vault / other).exists(), other)

    def test_destination_parent_swap_before_move_never_loses_source(self) -> None:
        parent = self.vault / "new/one"
        parent.mkdir(parents=True)
        detached = self.vault / "detached"
        real_move = apply_migration._rename_noreplace
        swapped = False

        def swap_parent(*args, **kwargs):
            nonlocal swapped
            if _is_runtime_rename(args[0], args[1]):
                return real_move(*args, **kwargs)
            if not swapped:
                swapped = True
                parent.rename(detached)
                parent.mkdir()
            return real_move(*args, **kwargs)

        with patch("apply_migration._rename_noreplace", side_effect=swap_parent):
            result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("changed after preflight", stderr)
        for source in self.destinations:
            self.assertTrue((self.vault / source).is_file(), source)
        self.assertEqual(list(detached.iterdir()), [])

    def test_rollback_failure_is_reported_as_critical(self) -> None:
        real_move = apply_migration._rename_noreplace
        calls = 0

        def fail_apply_and_rollback(*args, **kwargs):
            nonlocal calls
            if _is_runtime_rename(args[0], args[1]):
                return real_move(*args, **kwargs)
            calls += 1
            if calls in {2, 3}:
                raise OSError(f"injected rename failure {calls}")
            return real_move(*args, **kwargs)

        with patch(
            "apply_migration._rename_noreplace",
            side_effect=fail_apply_and_rollback,
        ):
            result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("CRITICAL rollback failed", stderr)
        self.assertIn("injected rename failure 2", stderr)
        self.assertIn("injected rename failure 3", stderr)
        self.assertTrue(self.journal_path.is_file())

        recovered, _, recovery_error = self._run()

        self.assertEqual(recovered, 0, recovery_error)
        self._assert_destinations_only()
        self.assertFalse(self.journal_path.exists())

    def test_corrupt_recovery_journal_blocks_without_mutation(self) -> None:
        self.journal_path.write_bytes(b"{not-json")
        before = self._snapshot()

        result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("CRITICAL recovery journal", stderr)
        self.assertEqual(self._snapshot(), before)

    def test_incompatible_recovery_journal_blocks_without_mutation(self) -> None:
        real_move = apply_migration._rename_noreplace
        calls = 0

        def leave_partial_state(*args, **kwargs):
            nonlocal calls
            if _is_runtime_rename(args[0], args[1]):
                return real_move(*args, **kwargs)
            calls += 1
            if calls in {2, 3}:
                raise OSError(f"injected rename failure {calls}")
            return real_move(*args, **kwargs)

        with patch(
            "apply_migration._rename_noreplace", side_effect=leave_partial_state
        ):
            result, _, _ = self._run()
        self.assertEqual(result, 1)
        journal = json.loads(self.journal_path.read_text(encoding="utf-8"))
        journal["expected_head"] = "0" * 40
        self.journal_path.write_text(
            json.dumps(journal) + "\n", encoding="utf-8"
        )
        before = self._snapshot()

        blocked, _, stderr = self._run()

        self.assertEqual(blocked, 1)
        self.assertIn("CRITICAL recovery journal is incompatible", stderr)
        self.assertEqual(self._snapshot(), before)

    def test_all_complete_recovery_finalizes_as_no_op(self) -> None:
        with patch(
            "apply_migration._delete_journal",
            side_effect=OSError("injected journal delete failure"),
        ):
            result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("injected journal delete failure", stderr)
        self._assert_destinations_only()
        self.assertTrue(self.journal_path.is_file())

        recovered, stdout, recovery_error = self._run()

        self.assertEqual(recovered, 0, recovery_error)
        self.assertIn("no_op=true", stdout)
        self.assertFalse(self.journal_path.exists())

    def test_all_pending_recovery_clears_journal_and_restarts(self) -> None:
        with patch(
            "apply_migration._create_planned_directories",
            side_effect=OSError("injected pre-move failure"),
        ), patch(
            "apply_migration._delete_journal",
            side_effect=OSError("injected journal retention"),
        ):
            result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("CRITICAL rollback failed", stderr)
        self._assert_sources_only()
        self.assertTrue(self.journal_path.is_file())

        recovered, _, recovery_error = self._run()

        self.assertEqual(recovered, 0, recovery_error)
        self._assert_destinations_only()
        self.assertFalse(self.journal_path.exists())

    def test_recovery_stabilizes_observed_prefix_before_rollback(self) -> None:
        moves = tuple(
            apply_migration.Move(
                source=record["source"],
                destination=record["destination"],
                sha256=record["sha256"],
                size_bytes=record["size_bytes"],
            )
            for record in self.records
        )
        first = moves[0]
        destination = self.vault / first.destination
        destination.parent.mkdir(parents=True)
        (self.vault / first.source).rename(destination)
        payload = self.manifest_path.read_bytes()
        journal = apply_migration.RecoveryJournal(
            expected_head=self.head,
            manifest_path="state/manifest.json",
            manifest_sha256=hashlib.sha256(payload).hexdigest(),
            move_set_sha256=apply_migration._move_set_sha256(moves),
            phase="structural",
            move_count=len(moves),
            completed_moves=1,
            planned_directories=(),
            created_directories=[],
            directory_intent=None,
        )
        self.journal_path.write_bytes(apply_migration._journal_payload(journal))
        events: list[tuple[str, str]] = []
        real_hash = apply_migration._hash_open_file
        real_rollback = apply_migration._rollback_entry

        def record_hash(parent_fd, name, label, **kwargs):
            if kwargs.get("sync"):
                events.append(("sync", label))
            return real_hash(parent_fd, name, label, **kwargs)

        def record_rollback(*args, **kwargs):
            events.append(("rollback", args[1].move.source))
            return real_rollback(*args, **kwargs)

        with patch(
            "apply_migration._hash_open_file", side_effect=record_hash
        ), patch(
            "apply_migration._rollback_entry", side_effect=record_rollback
        ):
            result, _, stderr = self._run()

        self.assertEqual(result, 0, stderr)
        first_rollback = next(
            index for index, event in enumerate(events) if event[0] == "rollback"
        )
        stabilized = [label for kind, label in events[:first_rollback] if kind == "sync"]
        self.assertTrue(
            any(first.destination in label for label in stabilized),
            stabilized,
        )
        self.assertTrue(
            any(moves[1].source in label for label in stabilized),
            stabilized,
        )

    def test_directory_creation_crash_recovers_automatically(self) -> None:
        moves = tuple(
            apply_migration.Move(
                source=record["source"],
                destination=record["destination"],
                sha256=record["sha256"],
                size_bytes=record["size_bytes"],
            )
            for record in self.records
        )
        payload = self.manifest_path.read_bytes()
        root_fd = os.open(self.vault, apply_migration.DIRECTORY_OPEN_FLAGS)
        journal_directory_fd = apply_migration._open_journal_directory(root_fd)
        journal = apply_migration.RecoveryJournal(
            expected_head=self.head,
            manifest_path="state/manifest.json",
            manifest_sha256=hashlib.sha256(payload).hexdigest(),
            move_set_sha256=apply_migration._move_set_sha256(moves),
            phase="structural",
            move_count=len(moves),
            completed_moves=0,
            planned_directories=apply_migration._planned_destination_directories(
                root_fd, moves
            ),
            created_directories=[],
            directory_intent=None,
        )
        apply_migration._install_initial_journal(journal_directory_fd, journal)
        real_write = apply_migration._write_journal
        writes = 0

        def crash_before_ownership_checkpoint(*args, **kwargs):
            nonlocal writes
            writes += 1
            if writes == 2:
                raise OSError("injected directory checkpoint crash")
            return real_write(*args, **kwargs)

        try:
            with patch(
                "apply_migration._write_journal",
                side_effect=crash_before_ownership_checkpoint,
            ):
                with self.assertRaisesRegex(
                    OSError, "injected directory checkpoint crash"
                ):
                    apply_migration._create_planned_directories(
                        root_fd,
                        journal_directory_fd,
                        journal,
                    )
        finally:
            os.close(journal_directory_fd)
            os.close(root_fd)

        orphaned = tuple(
            path
            for path in (self.vault / ".fgv").iterdir()
            if path.name.startswith(apply_migration.DIRECTORY_TEMPORARY_PREFIX)
        )
        self.assertEqual(len(orphaned), 1)
        orphan_identity = orphaned[0].stat().st_ino

        recovered, _, recovery_error = self._run()

        self.assertEqual(recovered, 0, recovery_error)
        self._assert_destinations_only()
        self.assertFalse(self.journal_path.exists())
        self.assertTrue(orphaned[0].is_dir())
        self.assertEqual(orphaned[0].stat().st_ino, orphan_identity)

    def test_published_directory_without_checkpoint_recovers_automatically(self) -> None:
        real_write = apply_migration._write_journal
        writes = 0

        def crash_before_created_checkpoint(*args, **kwargs):
            nonlocal writes
            writes += 1
            if writes == 3:
                raise OSError("injected created-directory checkpoint crash")
            return real_write(*args, **kwargs)

        with patch(
            "apply_migration._write_journal",
            side_effect=crash_before_created_checkpoint,
        ), patch(
            "apply_migration._rollback",
            return_value=["injected abrupt process termination"],
        ):
            interrupted, _, interrupted_error = self._run()

        self.assertEqual(interrupted, 1)
        self.assertIn("CRITICAL rollback failed", interrupted_error)
        self.assertTrue((self.vault / "new").is_dir())
        self.assertTrue(self.journal_path.is_file())
        self._assert_sources_only()

        recovered, _, recovery_error = self._run()

        self.assertEqual(recovered, 0, recovery_error)
        self._assert_destinations_only()
        self.assertFalse(self.journal_path.exists())

    def test_missing_owned_intent_is_idempotent_cleanup(self) -> None:
        real_write = apply_migration._write_journal
        writes = 0

        def crash_before_created_checkpoint(*args, **kwargs):
            nonlocal writes
            writes += 1
            if writes == 3:
                raise OSError("injected created-directory checkpoint crash")
            return real_write(*args, **kwargs)

        with patch(
            "apply_migration._write_journal",
            side_effect=crash_before_created_checkpoint,
        ), patch(
            "apply_migration._rollback",
            return_value=["injected abrupt process termination"],
        ):
            interrupted, _, _ = self._run()

        self.assertEqual(interrupted, 1)
        (self.vault / "new").rmdir()

        recovered, _, recovery_error = self._run()

        self.assertEqual(recovered, 0, recovery_error)
        self._assert_destinations_only()
        self.assertFalse(self.journal_path.exists())

    def test_directory_cleanup_race_never_removes_replacement(self) -> None:
        owned = self.vault / "owned"
        replacement = self.vault / "replacement"
        displaced = self.vault / "displaced-owned"
        owned.mkdir()
        replacement.mkdir()
        owned_metadata = owned.stat()
        replacement_inode = replacement.stat().st_ino
        directory = apply_migration.CreatedDirectory(
            "owned",
            owned_metadata.st_dev,
            owned_metadata.st_ino,
        )
        root_fd = os.open(self.vault, apply_migration.DIRECTORY_OPEN_FLAGS)
        real_move = apply_migration._rename_noreplace
        real_rmdir = os.rmdir
        raced = False

        def inject_race(parent_fd: int) -> None:
            nonlocal raced
            if raced:
                return
            raced = True
            os.rename(
                "owned",
                "displaced-owned",
                src_dir_fd=parent_fd,
                dst_dir_fd=parent_fd,
            )
            os.rename(
                "replacement",
                "owned",
                src_dir_fd=parent_fd,
                dst_dir_fd=parent_fd,
            )

        def race_before_quarantine(source_name, destination_name, **kwargs):
            if source_name == "owned":
                inject_race(kwargs["src_dir_fd"])
            return real_move(source_name, destination_name, **kwargs)

        def race_before_legacy_rmdir(name, *args, **kwargs):
            if name == "owned":
                inject_race(kwargs["dir_fd"])
            return real_rmdir(name, *args, **kwargs)

        try:
            with patch(
                "apply_migration._rename_noreplace",
                side_effect=race_before_quarantine,
            ), patch(
                "apply_migration.os.rmdir",
                side_effect=race_before_legacy_rmdir,
            ):
                with self.assertRaisesRegex(
                    apply_migration.MigrationApplyError,
                    "ownership changed",
                ):
                    apply_migration._remove_created_directory(root_fd, directory)
        finally:
            os.close(root_fd)

        self.assertTrue(raced)
        self.assertEqual(owned.stat().st_ino, replacement_inode)
        self.assertEqual(displaced.stat().st_ino, owned_metadata.st_ino)

    def test_directory_race_is_not_removed_without_recorded_ownership(self) -> None:
        real_move = apply_migration._rename_noreplace
        raced = False

        def create_racer_before_publish(*args, **kwargs):
            nonlocal raced
            if args[0].startswith(".migration-apply-directory.") and not raced:
                raced = True
                os.mkdir(args[1], dir_fd=kwargs["dst_dir_fd"])
            return real_move(*args, **kwargs)

        with patch(
            "apply_migration._rename_noreplace",
            side_effect=create_racer_before_publish,
        ):
            result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("destination directory appeared after preflight", stderr)
        self.assertTrue((self.vault / "new").is_dir())
        self.assertFalse(self.journal_path.exists())
        self._assert_sources_only()

    def test_directory_parent_swap_is_rejected_before_ownership_checkpoint(self) -> None:
        parent = self.vault / "new"
        detached = self.vault / "detached-new"
        real_move = apply_migration._rename_noreplace
        real_write = apply_migration._write_journal
        swapped = False
        checkpointed_detached_path = False

        def swap_parent_before_publish(*args, **kwargs):
            nonlocal swapped
            if (
                args[0].startswith(".migration-apply-directory.")
                and args[1] == "one"
                and not swapped
            ):
                swapped = True
                parent.rename(detached)
                parent.mkdir()
            return real_move(*args, **kwargs)

        def record_checkpoint(*args, **kwargs):
            nonlocal checkpointed_detached_path
            journal = args[1]
            if any(
                directory.path == "new/one"
                for directory in journal.created_directories
            ):
                checkpointed_detached_path = True
            return real_write(*args, **kwargs)

        with patch(
            "apply_migration._rename_noreplace",
            side_effect=swap_parent_before_publish,
        ), patch(
            "apply_migration._write_journal",
            side_effect=record_checkpoint,
        ):
            result, _, stderr = self._run()

        self.assertTrue(swapped)
        self.assertEqual(result, 1)
        self.assertIn("CRITICAL", stderr)
        self.assertFalse(checkpointed_detached_path)
        self._assert_sources_only()

    def test_each_atomic_file_move_is_fsynced_before_checkpoint(self) -> None:
        events: list[str] = []
        real_move = apply_migration._rename_noreplace
        real_write = apply_migration._write_journal

        def record_move(source_name, destination_name, **kwargs):
            if not _is_runtime_rename(source_name, destination_name):
                events.append("move")
            return real_move(source_name, destination_name, **kwargs)

        def record_sync(*args, **kwargs):
            events.append("sync")

        def record_checkpoint(*args, **kwargs):
            events.append("checkpoint")
            return real_write(*args, **kwargs)

        with patch(
            "apply_migration._rename_noreplace", side_effect=record_move
        ), patch(
            "apply_migration._fsync_move_directories",
            side_effect=record_sync,
            create=True,
        ), patch(
            "apply_migration._write_journal", side_effect=record_checkpoint
        ):
            result, _, stderr = self._run()

        self.assertEqual(result, 0, stderr)
        move_positions = [
            index for index, event in enumerate(events) if event == "move"
        ]
        self.assertEqual(len(move_positions), len(self.records))
        for position in move_positions:
            checkpoint = events.index("checkpoint", position + 1)
            self.assertIn("sync", events[position + 1 : checkpoint])

    def test_move_directory_fsync_persists_target_before_origin(self) -> None:
        synced: list[int] = []
        metadata = {
            41: SimpleNamespace(st_dev=1, st_ino=10),
            42: SimpleNamespace(st_dev=1, st_ino=20),
        }

        with patch(
            "apply_migration.os.fstat", side_effect=lambda fd: metadata[fd]
        ), patch("apply_migration.os.fsync", side_effect=synced.append):
            apply_migration._fsync_move_directories(
                origin_parent_fd=41,
                target_parent_fd=42,
            )

        self.assertEqual(synced, [42, 41])

    def test_missing_owned_directory_still_fsyncs_existing_parent(self) -> None:
        parent = self.vault / "durable-parent"
        child = parent / "child"
        child.mkdir(parents=True)
        parent_metadata = parent.stat()
        child_metadata = child.stat()
        created = [
            apply_migration.CreatedDirectory(
                "durable-parent",
                parent_metadata.st_dev,
                parent_metadata.st_ino,
            ),
            apply_migration.CreatedDirectory(
                "durable-parent/child",
                child_metadata.st_dev,
                child_metadata.st_ino,
            ),
        ]
        child.rmdir()
        parent.rmdir()
        root_fd = os.open(self.vault, apply_migration.DIRECTORY_OPEN_FLAGS)
        synced: list[tuple[int, int]] = []

        def record_sync(fd: int) -> None:
            metadata = os.fstat(fd)
            synced.append((metadata.st_dev, metadata.st_ino))

        try:
            with patch("apply_migration.os.fsync", side_effect=record_sync):
                apply_migration._remove_journal_directories(root_fd, created)
        finally:
            os.close(root_fd)

        vault_metadata = self.vault.stat()
        self.assertEqual(
            synced,
            [(vault_metadata.st_dev, vault_metadata.st_ino)],
        )

    def test_initial_journal_race_is_not_overwritten(self) -> None:
        sentinel = b"external journal owner\n"
        invoked = False

        def race_initial_install(*args, **kwargs):
            nonlocal invoked
            invoked = True
            self.journal_path.write_bytes(sentinel)
            raise FileExistsError("injected journal race")

        with patch(
            "apply_migration._install_initial_journal",
            side_effect=race_initial_install,
            create=True,
        ):
            result, _, _ = self._run()

        self.assertTrue(invoked)
        self.assertEqual(result, 1)
        self.assertEqual(self.journal_path.read_bytes(), sentinel)
        self._assert_sources_only()

    def test_manifest_cannot_use_recovery_journal_namespace(self) -> None:
        reserved = [dict(record) for record in self.records]
        reserved[0]["destination"] = ".fgv/migration-apply-journal.json"
        self._write_manifest(reserved)
        self._commit_fixture("reserved journal destination")
        before = self._snapshot()

        result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("reserved migration runtime path", stderr)
        self.assertEqual(self._snapshot(), before)

    def test_manifest_cannot_use_descendant_of_recovery_journal(self) -> None:
        reserved = [dict(record) for record in self.records]
        reserved[0]["destination"] = ".fgv/migration-apply-journal.json/child"
        self._write_manifest(reserved)
        self._commit_fixture("reserved journal descendant")
        before = self._snapshot()

        result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("reserved migration runtime path", stderr)
        self.assertEqual(self._snapshot(), before)

    def test_non_local_filesystem_is_rejected_before_mutation(self) -> None:
        before = self._snapshot()

        with patch(
            "apply_migration._is_local_filesystem",
            return_value=False,
            create=True,
        ):
            result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("local filesystem", stderr)
        self.assertEqual(self._snapshot(), before)

    def test_complete_application_preserves_every_hash_and_count(self) -> None:
        result, stdout, stderr = self._run()

        self.assertEqual(result, 0, stderr)
        self.assertEqual(stdout, "planned_moves=3\npreflight=ok\nfiles_moved=3\n")
        self._assert_destinations_only()
        self.assertFalse(self.journal_path.exists())
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
        self.assertFalse(self.journal_path.exists())

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
        real_move = apply_migration._rename_noreplace
        changed = False

        def mutate_manifest_then_move(*args, **kwargs):
            nonlocal changed
            if _is_runtime_rename(args[0], args[1]):
                return real_move(*args, **kwargs)
            if not changed:
                changed = True
                self._write_manifest(redirected)
            return real_move(*args, **kwargs)

        with patch(
            "apply_migration._rename_noreplace",
            side_effect=mutate_manifest_then_move,
        ):
            result, _, stderr = self._run()

        self.assertEqual(result, 0, stderr)
        self._assert_destinations_only()
        self.assertFalse((self.vault / "redirected/owned.txt").exists())

    def test_source_changed_after_preflight_is_rejected_before_move(self) -> None:
        real_hash_open_file = apply_migration._hash_open_file
        real_move = apply_migration._rename_noreplace
        hash_calls = 0
        file_move_calls = 0

        def mutate_before_apply(parent_fd, name, label, **kwargs):
            nonlocal hash_calls
            hash_calls += 1
            if hash_calls == len(self.records) + 1:
                (self.vault / "legacy/a.txt").write_bytes(b"omega\n")
            return real_hash_open_file(parent_fd, name, label, **kwargs)

        def record_file_move(*args, **kwargs):
            nonlocal file_move_calls
            if not _is_runtime_rename(args[0], args[1]):
                file_move_calls += 1
            return real_move(*args, **kwargs)

        with patch(
            "apply_migration._hash_open_file", side_effect=mutate_before_apply
        ), patch(
            "apply_migration._rename_noreplace", side_effect=record_file_move
        ):
            result, _, stderr = self._run()

        self.assertEqual(result, 1)
        self.assertIn("source hash mismatch", stderr)
        self.assertEqual(file_move_calls, 0)
        for destination in self.destinations.values():
            self.assertFalse((self.vault / destination).exists())

    def test_source_substituted_at_move_window_is_never_deleted(self) -> None:
        source = self.vault / "legacy/a.txt"
        saved_original = self.vault / "saved-original.txt"
        replacement = b"replacement survives\n"
        invoked = False
        real_move = getattr(apply_migration, "_rename_noreplace", None)

        def substitute_source_then_move(*args, **kwargs):
            nonlocal invoked
            if _is_runtime_rename(args[0], args[1]):
                if real_move is not None:
                    return real_move(*args, **kwargs)
                return None
            if not invoked:
                invoked = True
                source.rename(saved_original)
                source.write_bytes(replacement)
            if real_move is not None:
                return real_move(*args, **kwargs)
            return None

        with patch(
            "apply_migration._rename_noreplace",
            side_effect=substitute_source_then_move,
            create=True,
        ):
            result, _, stderr = self._run()

        self.assertTrue(invoked)
        self.assertEqual(result, 1)
        self.assertIn("source hash mismatch", stderr)
        self.assertEqual(source.read_bytes(), replacement)
        self.assertEqual(saved_original.read_bytes(), self.payloads["legacy/a.txt"])
        self.assertFalse((self.vault / "new/one/a.txt").exists())

    def test_source_parent_swap_is_rejected_and_reversed_by_original_dirfds(self) -> None:
        record = dict(self.records[0])
        self.records = [record]
        self._write_manifest(self.records)
        self._commit_fixture("single move source parent race")
        source_parent = self.vault / "legacy"
        detached_parent = self.vault / "detached-legacy"
        replacement = b"replacement survives source parent swap\n"
        real_move = apply_migration._rename_noreplace
        swapped = False

        def swap_source_parent_then_move(*args, **kwargs):
            nonlocal swapped
            if not _is_runtime_rename(args[0], args[1]) and not swapped:
                swapped = True
                source_parent.rename(detached_parent)
                source_parent.mkdir()
                (source_parent / "a.txt").write_bytes(replacement)
            return real_move(*args, **kwargs)

        with patch(
            "apply_migration._rename_noreplace",
            side_effect=swap_source_parent_then_move,
        ):
            result, _, stderr = self._run()

        self.assertTrue(swapped)
        self.assertEqual(result, 1)
        self.assertIn("changed after preflight", stderr)
        self.assertEqual((source_parent / "a.txt").read_bytes(), replacement)
        self.assertEqual(
            (detached_parent / "a.txt").read_bytes(),
            self.payloads["legacy/a.txt"],
        )
        self.assertFalse((self.vault / record["destination"]).exists())
        self.assertFalse(self.journal_path.exists())

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

    def test_dot_manifest_path_is_a_controlled_cli_error(self) -> None:
        environment = dict(os.environ)
        environment["PYTHONPATH"] = str(SCRIPT.parent)
        environment["PYTHONDONTWRITEBYTECODE"] = "1"

        result = subprocess.run(
            (
                sys.executable,
                str(SCRIPT),
                "--vault",
                str(self.vault),
                "--manifest",
                ".",
                "--phase",
                "structural",
                "--expected-head",
                self.head,
            ),
            check=False,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            env=environment,
        )

        stderr = result.stderr.decode("utf-8", errors="replace")
        self.assertEqual(result.returncode, 1)
        self.assertIn("unsafe manifest path", stderr)
        self.assertNotIn("Traceback", stderr)

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
        self._commit_fixture("invalid manifest schema")
        result, _, stderr = self._run()
        self.assertEqual(result, 1)
        self.assertIn("invalid schema", stderr)

        self._write_manifest(self.records)
        self._commit_fixture("restore manifest schema")
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
