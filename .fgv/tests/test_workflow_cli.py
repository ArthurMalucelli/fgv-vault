from contextlib import redirect_stderr
from io import StringIO
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from fgv_workflow import cli
from fgv_workflow.cli import _parser, plan_for_runtime, refresh_state
from fgv_workflow.locking import VaultLocked, vault_lock


class WorkflowCliTests(unittest.TestCase):
    def test_scripts_path_cannot_shadow_the_workflow_package(self) -> None:
        fgv_root = Path(__file__).resolve().parents[1]
        environment = dict(os.environ)
        environment["PYTHONPATH"] = os.pathsep.join(
            ((fgv_root / "scripts").as_posix(), (fgv_root / "src").as_posix())
        )
        result = subprocess.run(
            [
                sys.executable,
                "-c",
                "import fgv_workflow; import fgv_workflow.cli; print(fgv_workflow.__file__)",
            ],
            cwd=fgv_root.parent,
            env=environment,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("/.fgv/src/fgv_workflow/__init__.py", result.stdout)

    def make_output_fixture(self, root: Path) -> tuple[Path, Path, Path]:
        source = root / "plaud.txt"
        source.write_bytes(b"raw source\n")
        analysis = root / "analysis.json"
        analysis.write_text("{}\n", encoding="utf-8")
        return source, analysis, root / "plan.json"

    def test_plan_output_rejects_existing_file_and_symlink(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory).resolve()
            source, analysis, output = self.make_output_fixture(root)
            output.write_bytes(b"existing owner\n")

            with self.assertRaises(FileExistsError):
                cli._write_plan_output(
                    output,
                    b"replacement\n",
                    source=source,
                    analysis_path=analysis,
                )
            self.assertEqual(output.read_bytes(), b"existing owner\n")

            output.unlink()
            target = root / "other-owner.json"
            target.write_bytes(b"symlink owner\n")
            output.symlink_to(target)
            with self.assertRaises(FileExistsError):
                cli._write_plan_output(
                    output,
                    b"replacement\n",
                    source=source,
                    analysis_path=analysis,
                )
            self.assertTrue(output.is_symlink())
            self.assertEqual(target.read_bytes(), b"symlink owner\n")

    def test_plan_output_cannot_alias_source_or_analysis(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory).resolve()
            source, analysis, _output = self.make_output_fixture(root)

            for label, output in (("source", source), ("analysis", analysis)):
                with self.subTest(label=label), self.assertRaisesRegex(
                    ValueError, label
                ):
                    cli._write_plan_output(
                        output,
                        b"replacement\n",
                        source=source,
                        analysis_path=analysis,
                    )
            self.assertEqual(source.read_bytes(), b"raw source\n")
            self.assertEqual(analysis.read_text(encoding="utf-8"), "{}\n")

    def test_plan_output_requires_existing_nonsymlink_directory_parent(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory).resolve()
            source, analysis, _output = self.make_output_fixture(root)
            real_parent = root / "real-parent"
            real_parent.mkdir()
            linked_parent = root / "linked-parent"
            linked_parent.symlink_to(real_parent, target_is_directory=True)
            file_parent = root / "file-parent"
            file_parent.write_text("owner\n", encoding="utf-8")
            outputs = (
                root / "missing-parent" / "plan.json",
                linked_parent / "plan.json",
                file_parent / "plan.json",
            )

            for output in outputs:
                with self.subTest(output=output), self.assertRaises(
                    (FileNotFoundError, NotADirectoryError, ValueError)
                ):
                    cli._write_plan_output(
                        output,
                        b"payload\n",
                        source=source,
                        analysis_path=analysis,
                    )
                self.assertFalse(output.exists())

    def test_plan_cli_exclusively_writes_all_bytes_and_fsyncs(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory).resolve()
            source, analysis, output = self.make_output_fixture(root)
            original_write = os.write
            writes = []

            def short_write(descriptor: int, data: bytes) -> int:
                writes.append(len(data))
                return original_write(descriptor, data[:3])

            with (
                patch.object(cli, "plan_for_runtime", return_value={"ok": True}),
                patch.object(cli.os, "write", side_effect=short_write),
                patch.object(cli.os, "fsync", wraps=os.fsync) as fsync,
            ):
                exit_code = cli.main(
                    [
                        "plan-plaud",
                        "--vault",
                        str(root / "vault"),
                        "--source",
                        str(source),
                        "--analysis",
                        str(analysis),
                        "--class-date",
                        "2026-08-28",
                        "--runtime",
                        "codex",
                        "--output",
                        str(output),
                    ]
                )

            expected = json.dumps(
                {"ok": True}, ensure_ascii=False, indent=2, sort_keys=True
            ).encode("utf-8") + b"\n"
            self.assertEqual(exit_code, 0)
            self.assertEqual(output.read_bytes(), expected)
            self.assertGreater(len(writes), 1)
            self.assertGreaterEqual(fsync.call_count, 2)
            self.assertEqual(tuple(root.glob(".fgv-plan-*")), ())

    def test_plan_output_publication_is_bound_to_the_written_descriptor(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory).resolve()
            source, analysis, output = self.make_output_fixture(root)
            original_fsync = os.fsync
            swapped = False

            def swap_named_source_after_fsync(descriptor: int) -> None:
                nonlocal swapped
                original_fsync(descriptor)
                if swapped or not stat.S_ISREG(os.fstat(descriptor).st_mode):
                    return
                candidates = tuple(root.glob(".fgv-plan-*.tmp"))
                if candidates:
                    swapped = True
                    candidates[0].unlink()
                    candidates[0].write_bytes(b"foreign owner\n")

            with patch.object(cli.os, "fsync", side_effect=swap_named_source_after_fsync):
                cli._write_plan_output(
                    output,
                    b"owned descriptor\n",
                    source=source,
                    analysis_path=analysis,
                )

            self.assertEqual(output.read_bytes(), b"owned descriptor\n")
            self.assertEqual(tuple(root.glob(".fgv-plan-*")), ())

    def test_success_leaves_git_status_clean_except_for_declared_output(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory).resolve()
            subprocess.run(
                ["git", "init", "--quiet", str(root)],
                check=True,
                capture_output=True,
                text=True,
            )
            (root / ".gitignore").write_text(
                ".gitignore\nplaud.txt\nanalysis.json\nplan.json\n",
                encoding="utf-8",
            )
            source, analysis, output = self.make_output_fixture(root)

            cli._write_plan_output(
                output,
                b"owned descriptor\n",
                source=source,
                analysis_path=analysis,
            )

            status = subprocess.run(
                [
                    "git",
                    "-C",
                    str(root),
                    "status",
                    "--porcelain",
                    "--untracked-files=all",
                ],
                check=True,
                capture_output=True,
                text=True,
            )
            self.assertEqual(status.stdout, "")

    def test_plan_output_failure_removes_only_the_owned_partial_file(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory).resolve()
            source, analysis, output = self.make_output_fixture(root)
            original_write = os.write
            original_unlink = os.unlink
            original_open = os.open
            calls = 0
            unsafe_cleanup_attempts = []

            def fail_after_partial(descriptor: int, data: bytes) -> int:
                nonlocal calls
                calls += 1
                if calls == 1:
                    return original_write(descriptor, data[:3])
                raise OSError("injected write failure")

            def replace_in_unlink_window(
                name: str,
                *,
                dir_fd: int | None = None,
            ) -> None:
                if name.startswith(".fgv-plan-"):
                    unsafe_cleanup_attempts.append(name)
                    original_unlink(name, dir_fd=dir_fd)
                    replacement = original_open(
                        name,
                        os.O_WRONLY | os.O_CREAT | os.O_EXCL,
                        0o600,
                        dir_fd=dir_fd,
                    )
                    try:
                        original_write(replacement, b"replacement owner\n")
                    finally:
                        os.close(replacement)
                original_unlink(name, dir_fd=dir_fd)

            with (
                patch.object(cli.os, "write", side_effect=fail_after_partial),
                patch.object(cli.os, "unlink", side_effect=replace_in_unlink_window),
                patch.object(
                    cli, "_secure_nofollow_flag", return_value=os.O_NOFOLLOW
                ),
            ):
                with self.assertRaisesRegex(OSError, "injected write failure"):
                    cli._write_plan_output(
                        output,
                        b"complete payload\n",
                        source=source,
                        analysis_path=analysis,
                    )
            self.assertFalse(output.exists())
            self.assertEqual(unsafe_cleanup_attempts, [])
            self.assertEqual(tuple(root.glob(".fgv-plan-*")), ())

            calls = 0

            def competing_owner_appears(descriptor: int, data: bytes) -> int:
                nonlocal calls
                calls += 1
                if calls == 1:
                    if output.exists():
                        output.unlink()
                    output.write_bytes(b"replacement owner\n")
                return original_write(descriptor, data)

            with patch.object(cli.os, "write", side_effect=competing_owner_appears):
                with self.assertRaises(FileExistsError):
                    cli._write_plan_output(
                        output,
                        b"complete payload\n",
                        source=source,
                        analysis_path=analysis,
                    )
            self.assertEqual(output.read_bytes(), b"replacement owner\n")
            self.assertEqual(tuple(root.glob(".fgv-plan-*")), ())

    def test_plan_output_fails_closed_without_nofollow_support(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory).resolve()
            source, analysis, output = self.make_output_fixture(root)

            with patch.object(cli.os, "O_NOFOLLOW", None):
                with self.assertRaisesRegex(RuntimeError, "O_NOFOLLOW"):
                    cli._write_plan_output(
                        output,
                        b"payload\n",
                        source=source,
                        analysis_path=analysis,
                    )
            self.assertFalse(output.exists())

    def test_linux_descriptor_publication_uses_proc_fd_without_capability(self) -> None:
        calls = []

        class FakeFunction:
            argtypes = None
            restype = None

            def __call__(self, *arguments: object) -> int:
                calls.append(arguments)
                return 0

        class FakeLibrary:
            linkat = FakeFunction()

        with (
            patch.object(cli.sys, "platform", "linux"),
            patch.object(cli.ctypes, "CDLL", return_value=FakeLibrary()),
        ):
            cli._publish_descriptor_exclusive(9, 11, "plan.json")

        self.assertEqual(
            calls,
            [
                (
                    -100,
                    b"/proc/self/fd/9",
                    11,
                    b"plan.json",
                    0x00000400,
                )
            ],
        )

    def test_plan_output_setup_unlink_failure_retries_private_cleanup(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory).resolve()
            source, analysis, output = self.make_output_fixture(root)
            original_unlink = os.unlink
            payload_unlinks = 0

            def fail_first_payload_unlink(
                name: str,
                *,
                dir_fd: int | None = None,
            ) -> None:
                nonlocal payload_unlinks
                if name == "payload":
                    payload_unlinks += 1
                    if payload_unlinks == 1:
                        raise OSError("injected first unlink failure")
                original_unlink(name, dir_fd=dir_fd)

            with (
                patch.object(
                    cli.os, "unlink", side_effect=fail_first_payload_unlink
                ),
                patch.object(
                    cli, "_secure_nofollow_flag", return_value=os.O_NOFOLLOW
                ),
            ):
                with self.assertRaisesRegex(OSError, "first unlink failure"):
                    cli._write_plan_output(
                        output,
                        b"payload\n",
                        source=source,
                        analysis_path=analysis,
                    )

            self.assertEqual(payload_unlinks, 2)
            self.assertFalse(output.exists())
            self.assertEqual(tuple(root.glob(".fgv-plan-*")), ())

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
