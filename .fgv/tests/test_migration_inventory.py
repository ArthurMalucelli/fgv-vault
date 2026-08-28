import hashlib
from collections import Counter
from contextlib import redirect_stdout
import io
import json
import os
from pathlib import Path, PurePosixPath
import subprocess
import sys
from tempfile import TemporaryDirectory
import unicodedata
import unittest
from unittest.mock import patch

import plan_migration
from fgv_migration.inventory import (
    InventoryEntry,
    InventoryError,
    inventory_from_filesystem,
    inventory_from_git,
    normalize_relative_path,
)
from fgv_migration.rules import (
    CollisionError,
    RuleError,
    UnclassifiedError,
    build_manifest,
    classify_path,
)


ROOT = Path(__file__).resolve().parents[2]
FIXTURE = ROOT / ".fgv/tests/fixtures/migration-mini-vault"
SCRIPT = ROOT / ".fgv/scripts/plan_migration.py"
REAL_MANIFEST = ROOT / "30 Sistema/Estado/migration-manifest.json"
REAL_BASELINE = ROOT / "30 Sistema/Estado/migration-baseline.json"
REAL_BASE_COMMIT = "a7f7d58a5fcbbee86c90a046eb30e168217b5c78"
REAL_BASE_TREE = "be1202b9388c7e927fb112d1af390a93386fae07"


def entry(path: str, data: bytes = b"fixture") -> InventoryEntry:
    return InventoryEntry(
        path=path,
        sha256=hashlib.sha256(data).hexdigest(),
        size_bytes=len(data),
    )


class FilesystemInventoryTests(unittest.TestCase):
    def test_ignores_metadata_and_generated_outputs(self) -> None:
        paths = {item.path for item in inventory_from_filesystem(FIXTURE)}
        self.assertNotIn(".obsidian/app.json", paths)
        self.assertNotIn(".fgv/private.txt", paths)
        self.assertNotIn(".gitignore", paths)
        self.assertNotIn("30 Sistema/Estado/migration-manifest.json", paths)
        self.assertNotIn("30 Sistema/Plans/generated-plan.md", paths)
        self.assertIn("Tasks.md", paths)

        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            (vault / ".git").mkdir()
            (vault / ".git/config").write_text("ignored", encoding="utf-8")
            (vault / "Tasks.md").write_text("included", encoding="utf-8")
            temporary_paths = {
                item.path for item in inventory_from_filesystem(vault)
            }
            self.assertEqual(temporary_paths, {"Tasks.md"})

    def test_hashes_exact_bytes_and_records_size(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            payload = b"\x00\xff\r\nbytes\x80"
            (vault / "Tasks.md").write_bytes(payload)

            (result,) = inventory_from_filesystem(vault)

            self.assertEqual(result.sha256, hashlib.sha256(payload).hexdigest())
            self.assertEqual(result.size_bytes, len(payload))

    def test_paths_are_relative_posix_and_nfc(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            decomposed = "Cafe\u0301.md"
            (vault / decomposed).write_text("nfc", encoding="utf-8")

            (result,) = inventory_from_filesystem(vault)

            self.assertEqual(result.path, "Caf\u00e9.md")
            self.assertFalse(Path(result.path).is_absolute())
            self.assertNotIn("\\", result.path)

    def test_rejects_nul_and_backslash_in_relative_paths(self) -> None:
        for unsafe in ("folder\\note.md", "folder/nu\x00l.md"):
            with self.subTest(path=unsafe):
                with self.assertRaisesRegex(InventoryError, "unsafe relative path"):
                    normalize_relative_path(unsafe)

    def test_rejects_symlinks_before_returning_inventory(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            vault = Path(temporary_directory)
            (vault / "Tasks.md").write_text("tasks", encoding="utf-8")
            os.symlink("Tasks.md", vault / "alias.md")

            with self.assertRaisesRegex(InventoryError, "symlink"):
                inventory_from_filesystem(vault)


class RuleTests(unittest.TestCase):
    def test_all_canonical_categories_and_special_mappings(self) -> None:
        cases = {
            "Vault/Index.md": ("00 Home/Home.md", "home"),
            "Tasks.md": ("00 Home/Tasks.md", "home"),
            "Vault/Controle de Faltas 2026.2.md": (
                "00 Home/Controle de Faltas 2026.2.md",
                "home",
            ),
            "Macro.md": ("00 Home/Inbox/Legado/Macro.md", "home"),
            "Projeto 90 Dias.md": (
                "00 Home/Inbox/Legado/Projeto 90 Dias.md",
                "home",
            ),
            "Vault/FGV Finance/Prova - T\u00f3picos cobrados.md": (
                "00 Home/Inbox/Legado/Prova - T\u00f3picos cobrados.md",
                "home",
            ),
            "Vault/Conceitos/Sem t\u00edtulo.md": (
                "00 Home/Inbox/Legado/Sem t\u00edtulo.md",
                "home",
            ),
            "Vault/Specs/rule.md": ("30 Sistema/Specs/rule.md", "system"),
            "Vault/Templates/note.md": (
                "30 Sistema/Templates/note.md",
                "system",
            ),
            "Vault/Tutor/prompt.md": ("30 Sistema/Tutor/prompt.md", "system"),
            "Vault/automation/job.py": (
                "30 Sistema/Automacoes/job.py",
                "system",
            ),
            "Vault/Conceitos/Finan\u00e7as/WACC.md": (
                "20 Conhecimento/Conceitos/Finan\u00e7as/WACC.md",
                "knowledge",
            ),
            "Vault/S1/Matem\u00e1tica/Resumo.md": (
                "90 Arquivo/2026.1/Matem\u00e1tica/Resumo.md",
                "archive",
            ),
            "ContabilidadeFinanceira/Aulas/a.md": (
                "10 Mat\u00e9rias/ContabilidadeFinanceira/Aulas/a.md",
                "subject",
            ),
            "DireitoEmpresarial/Aulas/a.md": (
                "10 Mat\u00e9rias/DireitoEmpresarial/Aulas/a.md",
                "subject",
            ),
            "Estatistica2/Aulas/a.md": (
                "10 Mat\u00e9rias/Estatistica2/Aulas/a.md",
                "subject",
            ),
            "EstudosOrganizacionais/Aulas/a.md": (
                "10 Mat\u00e9rias/EstudosOrganizacionais/Aulas/a.md",
                "subject",
            ),
            "Matem\u00e1ticaAplicada/Aulas/a.md": (
                "10 Mat\u00e9rias/Matem\u00e1ticaAplicada/Aulas/a.md",
                "subject",
            ),
            "Psicologia/Aulas/a.md": (
                "10 Mat\u00e9rias/Psicologia/Aulas/a.md",
                "subject",
            ),
            "TecnologiaDadosNegocios/Aulas/a.md": (
                "10 Mat\u00e9rias/TecnologiaDadosNegocios/Aulas/a.md",
                "subject",
            ),
        }

        for source, expected in cases.items():
            with self.subTest(source=source):
                classification = classify_path(source)
                self.assertEqual(
                    (classification.destination, classification.category), expected
                )
                self.assertEqual(classification.phase, "structural")
                self.assertTrue(classification.reason)

    def test_unknown_is_unclassified_without_explicit_allowlist(self) -> None:
        classification = classify_path("Loose Note.md")
        self.assertIsNone(classification.destination)
        self.assertEqual(classification.category, "unclassified")

        with self.assertRaisesRegex(UnclassifiedError, "Loose Note.md"):
            build_manifest((entry("Loose Note.md"),))

    def test_explicit_allowlist_can_route_unknown_to_inbox(self) -> None:
        manifest = build_manifest(
            (entry("Loose Note.md"),),
            inbox_allowlist={
                "Loose Note.md": "00 Home/Inbox/Legado/Loose Note.md"
            },
        )

        self.assertEqual(manifest[0]["destination"], "00 Home/Inbox/Legado/Loose Note.md")
        self.assertEqual(manifest[0]["category"], "home")

    def test_allowlist_rejects_unsafe_destinations(self) -> None:
        unsafe_destinations = (
            "00 Home\\Inbox\\Legado\\Loose Note.md",
            "00 Home/Inbox/Legado/nu\x00l.md",
            "00 Home/Inbox/Legado/../escape.md",
        )
        for destination in unsafe_destinations:
            with self.subTest(destination=destination):
                with self.assertRaises((InventoryError, RuleError)):
                    build_manifest(
                        (entry("Loose Note.md"),),
                        inbox_allowlist={"Loose Note.md": destination},
                    )

    def test_allowlist_stores_normalized_destination(self) -> None:
        manifest = build_manifest(
            (entry("Loose Note.md"),),
            inbox_allowlist={
                "Loose Note.md": "00 Home/Inbox/Legado/Folder/./Note.md"
            },
        )

        self.assertEqual(
            manifest[0]["destination"],
            "00 Home/Inbox/Legado/Folder/Note.md",
        )

    def test_equivalent_syntactic_destinations_collide(self) -> None:
        canonical = "00 Home/Inbox/Legado/Folder/Note.md"
        aliases = (
            "00 Home/Inbox/Legado/Folder/./Note.md",
            "00 Home/Inbox/Legado/Folder//Note.md",
            "00 Home/Inbox/Legado/Folder/Note.md/",
        )
        for alias in aliases:
            with self.subTest(alias=alias):
                with self.assertRaises(CollisionError):
                    build_manifest(
                        (entry("Loose A.md"), entry("Loose B.md")),
                        inbox_allowlist={
                            "Loose A.md": alias,
                            "Loose B.md": canonical,
                        },
                    )

    def test_exact_destination_collision_blocks_plan(self) -> None:
        allowlist = {
            "Loose A.md": "00 Home/Inbox/Legado/Duplicate.md",
            "Loose B.md": "00 Home/Inbox/Legado/Duplicate.md",
        }
        with self.assertRaisesRegex(CollisionError, "exact"):
            build_manifest(
                (entry("Loose A.md"), entry("Loose B.md")),
                inbox_allowlist=allowlist,
            )

    def test_destination_collision_after_nfc_blocks_plan(self) -> None:
        allowlist = {
            "Loose A.md": "00 Home/Inbox/Legado/Caf\u00e9.md",
            "Loose B.md": "00 Home/Inbox/Legado/Cafe\u0301.md",
        }
        with self.assertRaises(CollisionError):
            build_manifest(
                (entry("Loose A.md"), entry("Loose B.md")),
                inbox_allowlist=allowlist,
            )

    def test_manifest_is_stably_sorted_and_has_exact_schema(self) -> None:
        manifest = build_manifest((entry("Tasks.md", b"z"), entry("Macro.md", b"a")))

        self.assertEqual([record["source"] for record in manifest], ["Macro.md", "Tasks.md"])
        self.assertEqual(
            tuple(manifest[0]),
            (
                "schema_version",
                "source",
                "destination",
                "sha256",
                "size_bytes",
                "category",
                "phase",
                "reason",
            ),
        )
        self.assertEqual(manifest[0]["schema_version"], 1)
        self.assertEqual(manifest[0]["sha256"], hashlib.sha256(b"a").hexdigest())
        self.assertEqual(manifest[0]["size_bytes"], 1)


class GitInventoryTests(unittest.TestCase):
    def git(self, repository: Path, *arguments: str) -> subprocess.CompletedProcess:
        return subprocess.run(
            ("git", *arguments),
            cwd=repository,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

    def init_repository(self, repository: Path) -> None:
        self.git(repository, "init", "-q")
        self.git(repository, "config", "user.name", "Fixture")
        self.git(repository, "config", "user.email", "fixture@example.invalid")

    def test_base_ref_inventory_uses_committed_tree_bytes_and_paths(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            self.init_repository(repository)
            (repository / "Tasks.md").write_bytes(b"committed")
            (repository / "30 Sistema/Plans").mkdir(parents=True)
            (repository / "30 Sistema/Plans/new-branch-doc.md").write_bytes(
                b"generated"
            )
            (repository / ".obsidian").mkdir()
            (repository / ".obsidian/app.json").write_bytes(b"{}")
            (repository / ".gitignore").write_bytes(b".DS_Store\n")
            self.git(repository, "add", ".")
            self.git(repository, "commit", "-qm", "fixture")
            (repository / "Tasks.md").write_bytes(b"working-tree-change")
            (repository / "Loose Note.md").write_bytes(b"untracked")

            (result,) = inventory_from_git(repository, "HEAD")

            self.assertEqual(result.path, "Tasks.md")
            self.assertEqual(result.sha256, hashlib.sha256(b"committed").hexdigest())
            self.assertEqual(result.size_bytes, len(b"committed"))

    def test_git_symlink_is_rejected(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            self.init_repository(repository)
            (repository / "Tasks.md").write_text("tasks", encoding="utf-8")
            os.symlink("Tasks.md", repository / "alias.md")
            self.git(repository, "add", "Tasks.md", "alias.md")
            self.git(repository, "commit", "-qm", "fixture")

            with self.assertRaisesRegex(InventoryError, "symlink"):
                inventory_from_git(repository, "HEAD")

    def test_git_environment_cannot_redirect_inventory_to_another_repo(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            repository_a = root / "repo-a"
            repository_b = root / "repo-b"
            repository_a.mkdir()
            repository_b.mkdir()
            self.init_repository(repository_a)
            self.init_repository(repository_b)
            (repository_a / "Tasks.md").write_bytes(b"repo-a")
            (repository_b / "Tasks.md").write_bytes(b"repo-b")
            for repository in (repository_a, repository_b):
                self.git(repository, "add", "Tasks.md")
                self.git(repository, "commit", "-qm", "fixture")

            hostile_environment = {
                "GIT_DIR": str(repository_b / ".git"),
                "GIT_WORK_TREE": str(repository_b),
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "core.quotePath",
                "GIT_CONFIG_VALUE_0": "true",
            }
            with patch.dict(os.environ, hostile_environment, clear=False):
                (result,) = inventory_from_git(repository_a, "HEAD")

            self.assertEqual(result.sha256, hashlib.sha256(b"repo-a").hexdigest())

    def test_git_replace_cannot_change_base_tree_bytes(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            self.init_repository(repository)
            (repository / "Tasks.md").write_bytes(b"original")
            self.git(repository, "add", "Tasks.md")
            self.git(repository, "commit", "-qm", "original")
            original_commit = (
                self.git(repository, "rev-parse", "HEAD").stdout.decode("ascii").strip()
            )

            (repository / "Tasks.md").write_bytes(b"replacement")
            self.git(repository, "add", "Tasks.md")
            self.git(repository, "commit", "-qm", "replacement")
            replacement_commit = (
                self.git(repository, "rev-parse", "HEAD").stdout.decode("ascii").strip()
            )
            self.git(repository, "replace", original_commit, replacement_commit)

            (result,) = inventory_from_git(repository, original_commit)

            self.assertEqual(result.sha256, hashlib.sha256(b"original").hexdigest())


class PlannerCliTests(unittest.TestCase):
    def run_cli(self, *arguments: str) -> subprocess.CompletedProcess:
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        environment["PYTHONPATH"] = os.pathsep.join(
            (str(ROOT / ".fgv/src"), str(ROOT / ".fgv/scripts"))
        )
        return subprocess.run(
            (sys.executable, str(SCRIPT), *arguments),
            cwd=ROOT,
            env=environment,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
        )

    def make_git_fixture(self, repository: Path, source: str = "Tasks.md") -> None:
        subprocess.run(("git", "init", "-q"), cwd=repository, check=True)
        subprocess.run(
            ("git", "config", "user.name", "Fixture"), cwd=repository, check=True
        )
        subprocess.run(
            ("git", "config", "user.email", "fixture@example.invalid"),
            cwd=repository,
            check=True,
        )
        target = repository / source
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(b"committed")
        subprocess.run(("git", "add", source), cwd=repository, check=True)
        subprocess.run(("git", "commit", "-qm", "fixture"), cwd=repository, check=True)

    def test_help_succeeds_without_side_effects(self) -> None:
        result = self.run_cli("--help")
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertIn("--base-ref", result.stdout)
        self.assertIn("--check-only", result.stdout)

    def test_check_only_writes_nothing(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            self.make_git_fixture(repository)
            output = repository / "manifest.json"

            result = self.run_cli(
                "--vault",
                str(repository),
                "--base-ref",
                "HEAD",
                "--output",
                str(output),
                "--check-only",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertFalse(output.exists())
            self.assertIn("legacy_files=1", result.stdout)
            self.assertIn("files_written=0", result.stdout)

    def test_check_only_allows_missing_canonical_output_parents(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            self.make_git_fixture(repository)
            output = repository / "30 Sistema/Estado/migration-manifest.json"

            result = self.run_cli(
                "--vault",
                str(repository),
                "--base-ref",
                "HEAD",
                "--output",
                "30 Sistema/Estado/migration-manifest.json",
                "--check-only",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("legacy_files=1", result.stdout)
            self.assertIn("files_written=0", result.stdout)
            self.assertFalse(output.exists())
            self.assertFalse(output.parent.exists())
            self.assertFalse(output.parent.parent.exists())

    def test_normal_mode_rejects_missing_canonical_output_parent(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            self.make_git_fixture(repository)
            output = repository / "30 Sistema/Estado/migration-manifest.json"

            result = self.run_cli(
                "--vault",
                str(repository),
                "--base-ref",
                "HEAD",
                "--output",
                "30 Sistema/Estado/migration-manifest.json",
            )

            self.assertNotEqual(result.returncode, 0)
            self.assertIn("output parent", result.stderr)
            self.assertFalse(output.exists())
            self.assertFalse(output.parent.exists())
            self.assertFalse(output.parent.parent.exists())

    def test_requested_output_is_excluded_from_base_tree_and_untouched_in_check(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            self.make_git_fixture(repository)
            output = repository / "migration-manifest.json"
            output.write_text("existing output\n", encoding="utf-8")
            subprocess.run(
                ("git", "add", "migration-manifest.json"),
                cwd=repository,
                check=True,
            )
            subprocess.run(
                ("git", "commit", "-qm", "track generated output"),
                cwd=repository,
                check=True,
            )

            result = self.run_cli(
                "--vault",
                str(repository),
                "--base-ref",
                "HEAD",
                "--output",
                str(output),
                "--check-only",
            )

            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("legacy_files=1", result.stdout)
            self.assertEqual(output.read_text(encoding="utf-8"), "existing output\n")

    def test_normal_mode_writes_only_requested_output_deterministically(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            self.make_git_fixture(repository)
            sentinel = repository / "sentinel.txt"
            sentinel.write_text("unchanged", encoding="utf-8")
            output = repository / "manifest.json"

            first = self.run_cli(
                "--vault",
                str(repository),
                "--base-ref",
                "HEAD",
                "--output",
                str(output),
            )
            first_bytes = output.read_bytes()
            second = self.run_cli(
                "--vault",
                str(repository),
                "--base-ref",
                "HEAD",
                "--output",
                str(output),
            )

            self.assertEqual(first.returncode, 0, first.stderr)
            self.assertEqual(second.returncode, 0, second.stderr)
            self.assertEqual(output.read_bytes(), first_bytes)
            self.assertEqual(sentinel.read_text(encoding="utf-8"), "unchanged")
            manifest = json.loads(first_bytes)
            self.assertEqual(manifest[0]["source"], "Tasks.md")

    def test_unclassified_tree_and_invalid_ref_fail_closed_without_output(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            repository = Path(temporary_directory)
            self.make_git_fixture(repository, "Loose Note.md")
            output = repository / "manifest.json"

            unclassified = self.run_cli(
                "--vault",
                str(repository),
                "--base-ref",
                "HEAD",
                "--output",
                str(output),
            )
            invalid_ref = self.run_cli(
                "--vault",
                str(repository),
                "--base-ref",
                "missing-ref",
                "--output",
                str(output),
            )

            self.assertNotEqual(unclassified.returncode, 0)
            self.assertIn("unclassified", unclassified.stderr)
            self.assertNotEqual(invalid_ref.returncode, 0)
            self.assertIn("missing-ref", invalid_ref.stderr)
            self.assertFalse(output.exists())

    def test_output_rejects_parent_traversal_and_absolute_external_path(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            repository = root / "vault"
            repository.mkdir()
            self.make_git_fixture(repository)

            for unsafe_output in (
                "../outside.json",
                str(root / "absolute-outside.json"),
            ):
                with self.subTest(output=unsafe_output):
                    result = self.run_cli(
                        "--vault",
                        str(repository),
                        "--base-ref",
                        "HEAD",
                        "--output",
                        unsafe_output,
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("output", result.stderr)

            self.assertFalse((root / "outside.json").exists())
            self.assertFalse((root / "absolute-outside.json").exists())

    def test_output_rejects_symlink_ancestors_even_when_target_is_inside(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            repository = root / "vault"
            external = root / "external"
            repository.mkdir()
            external.mkdir()
            self.make_git_fixture(repository)
            (repository / "real").mkdir()
            os.symlink(external, repository / "external-link")
            os.symlink(repository / "real", repository / "internal-link")

            for output in (
                repository / "external-link/manifest.json",
                repository / "internal-link/manifest.json",
            ):
                with self.subTest(output=output):
                    result = self.run_cli(
                        "--vault",
                        str(repository),
                        "--base-ref",
                        "HEAD",
                        "--output",
                        str(output),
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("symlink", result.stderr)

            self.assertFalse((external / "manifest.json").exists())
            self.assertFalse((repository / "real/manifest.json").exists())

    def test_output_rejects_leaf_symlink_and_dangling_leaf(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            repository = root / "vault"
            external = root / "external"
            repository.mkdir()
            external.mkdir()
            self.make_git_fixture(repository)
            target = external / "target.json"
            target.write_bytes(b"external")
            os.symlink(target, repository / "manifest-link.json")
            os.symlink(
                external / "missing.json", repository / "dangling-manifest.json"
            )

            for output in (
                repository / "manifest-link.json",
                repository / "dangling-manifest.json",
            ):
                with self.subTest(output=output):
                    result = self.run_cli(
                        "--vault",
                        str(repository),
                        "--base-ref",
                        "HEAD",
                        "--output",
                        str(output),
                    )
                    self.assertNotEqual(result.returncode, 0)
                    self.assertIn("symlink", result.stderr)

            self.assertEqual(target.read_bytes(), b"external")
            self.assertFalse((external / "missing.json").exists())

    def test_atomic_write_preserves_previous_output_after_partial_write(self) -> None:
        writer = getattr(plan_migration, "_atomic_write_output", None)
        self.assertIsNotNone(writer, "atomic output writer is missing")
        with TemporaryDirectory() as temporary_directory:
            parent = Path(temporary_directory)
            output = parent / "manifest.json"
            output.write_bytes(b"previous")
            before = {path.name for path in parent.iterdir()}
            real_fdopen = os.fdopen

            class PartialWriter:
                def __init__(self, stream):
                    self.stream = stream

                def __enter__(self):
                    self.stream.__enter__()
                    return self

                def __exit__(self, exception_type, exception, traceback):
                    return self.stream.__exit__(exception_type, exception, traceback)

                def write(self, payload: bytes) -> None:
                    self.stream.write(payload[:4])
                    raise OSError("injected partial write")

            def partial_fdopen(file_descriptor, *arguments, **keywords):
                return PartialWriter(
                    real_fdopen(file_descriptor, *arguments, **keywords)
                )

            parent_fd = os.open(parent, plan_migration.DIRECTORY_OPEN_FLAGS)
            try:
                with patch.object(
                    plan_migration.os, "fdopen", side_effect=partial_fdopen
                ):
                    with self.assertRaisesRegex(OSError, "partial write"):
                        writer(parent_fd, output.name, b"replacement payload")
            finally:
                os.close(parent_fd)

            self.assertEqual(output.read_bytes(), b"previous")
            self.assertEqual({path.name for path in parent.iterdir()}, before)

    def test_atomic_write_preserves_previous_output_when_replace_fails(self) -> None:
        writer = getattr(plan_migration, "_atomic_write_output", None)
        self.assertIsNotNone(writer, "atomic output writer is missing")
        with TemporaryDirectory() as temporary_directory:
            parent = Path(temporary_directory)
            output = parent / "manifest.json"
            output.write_bytes(b"previous")
            before = {path.name for path in parent.iterdir()}

            parent_fd = os.open(parent, plan_migration.DIRECTORY_OPEN_FLAGS)
            try:
                with patch.object(
                    plan_migration.os,
                    "replace",
                    side_effect=OSError("injected replace failure"),
                ):
                    with self.assertRaisesRegex(OSError, "replace failure"):
                        writer(parent_fd, output.name, b"replacement payload")
            finally:
                os.close(parent_fd)

            self.assertEqual(output.read_bytes(), b"previous")
            self.assertEqual({path.name for path in parent.iterdir()}, before)

    def test_write_stays_bound_to_validated_parent_during_ancestor_swap(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            repository = root / "vault"
            repository.mkdir()
            validated_parent = repository / "validated"
            validated_parent.mkdir()
            moved_parent = repository / "validated-original"
            external = root / "external"
            external.mkdir()

            def swap_ancestor(*arguments, **keywords):
                validated_parent.rename(moved_parent)
                os.symlink(external, validated_parent)
                return (entry("Tasks.md"),)

            with patch.object(
                plan_migration,
                "inventory_from_git",
                side_effect=swap_ancestor,
            ):
                with redirect_stdout(io.StringIO()):
                    return_code = plan_migration.main(
                        [
                            "--vault",
                            str(repository),
                            "--base-ref",
                            "HEAD",
                            "--output",
                            "validated/manifest.json",
                        ]
                    )

            self.assertEqual(return_code, 0)
            self.assertFalse((external / "manifest.json").exists())
            manifest = json.loads((moved_parent / "manifest.json").read_bytes())
            self.assertEqual(manifest[0]["source"], "Tasks.md")


class RealManifestContractTests(unittest.TestCase):
    maxDiff = None

    def load_manifest(self) -> tuple[bytes, list[dict[str, object]]]:
        self.assertTrue(REAL_MANIFEST.is_file(), f"missing real manifest: {REAL_MANIFEST}")
        payload = REAL_MANIFEST.read_bytes()
        self.assertFalse(payload.startswith(b"\xef\xbb\xbf"))
        self.assertNotIn(b"\r", payload)
        self.assertTrue(payload.endswith(b"\n"))
        return payload, json.loads(payload)

    def load_baseline(self) -> dict[str, object]:
        self.assertTrue(REAL_BASELINE.is_file(), f"missing baseline: {REAL_BASELINE}")
        payload = REAL_BASELINE.read_bytes()
        self.assertNotIn(b"\r", payload)
        self.assertTrue(payload.endswith(b"\n"))
        return json.loads(payload)

    def test_real_manifest_is_complete_unique_safe_and_matches_base_tree(self) -> None:
        _, manifest = self.load_manifest()
        sources = [str(record["source"]) for record in manifest]
        destinations = [str(record["destination"]) for record in manifest]

        self.assertEqual(len(manifest), 1059)
        self.assertEqual(len(set(sources)), 1059)
        self.assertEqual(len(set(destinations)), 1059)
        self.assertEqual(
            Counter(str(record["category"]) for record in manifest),
            {"home": 7, "subject": 221, "knowledge": 505, "system": 13, "archive": 313},
        )
        self.assertNotIn("unclassified", {record["category"] for record in manifest})
        self.assertEqual(
            sources,
            sorted(sources, key=lambda value: value.encode("utf-8")),
        )
        for record in manifest:
            self.assertEqual(
                tuple(record),
                (
                    "schema_version",
                    "source",
                    "destination",
                    "sha256",
                    "size_bytes",
                    "category",
                    "phase",
                    "reason",
                ),
            )
            self.assertEqual(record["schema_version"], 1)

        for record in manifest:
            for field in ("source", "destination"):
                value = str(record[field])
                path = PurePosixPath(value)
                self.assertEqual(value, unicodedata.normalize("NFC", value))
                self.assertFalse(path.is_absolute())
                self.assertNotIn("..", path.parts)
                self.assertNotIn("\\", value)

        resolved_commit = subprocess.run(
            ("git", "rev-parse", "--verify", "origin/main^{commit}"),
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            text=True,
        ).stdout.strip()
        resolved_tree = subprocess.run(
            ("git", "rev-parse", "--verify", "origin/main^{tree}"),
            cwd=ROOT,
            check=True,
            stdout=subprocess.PIPE,
            text=True,
        ).stdout.strip()
        self.assertEqual(resolved_commit, REAL_BASE_COMMIT)
        self.assertEqual(resolved_tree, REAL_BASE_TREE)

        inventory = inventory_from_git(ROOT, REAL_BASE_COMMIT)
        expected = {
            item.path: (item.sha256, item.size_bytes) for item in inventory
        }
        actual = {
            str(record["source"]): (record["sha256"], record["size_bytes"])
            for record in manifest
        }
        self.assertEqual(actual, expected)

    def test_manifest_serialization_is_reproducible_byte_for_byte(self) -> None:
        payload, _ = self.load_manifest()
        environment = os.environ.copy()
        environment["PYTHONDONTWRITEBYTECODE"] = "1"
        environment["PYTHONPATH"] = os.pathsep.join(
            (str(ROOT / ".fgv/src"), str(ROOT / ".fgv/scripts"))
        )
        with TemporaryDirectory(dir=ROOT) as first_directory, TemporaryDirectory(
            dir=ROOT
        ) as second_directory:
            generated: list[bytes] = []
            for directory in (first_directory, second_directory):
                output = Path(directory) / "manifest.json"
                result = subprocess.run(
                    (
                        sys.executable,
                        str(SCRIPT),
                        "--vault",
                        str(ROOT),
                        "--base-ref",
                        REAL_BASE_COMMIT,
                        "--output",
                        str(output),
                    ),
                    cwd=ROOT,
                    env=environment,
                    check=False,
                    stdout=subprocess.PIPE,
                    stderr=subprocess.PIPE,
                    text=True,
                )
                self.assertEqual(result.returncode, 0, result.stderr)
                generated.append(output.read_bytes())

        self.assertEqual(generated[0], generated[1])
        self.assertEqual(generated[0], payload)

    def test_baseline_schema_and_hashes_are_reproducible(self) -> None:
        manifest_bytes, manifest = self.load_manifest()
        baseline = self.load_baseline()
        self.assertEqual(
            tuple(baseline),
            ("schema_version", "base", "manifest", "inventory", "wikilinks"),
        )
        self.assertEqual(baseline["schema_version"], 1)
        self.assertEqual(
            baseline["base"],
            {"commit": REAL_BASE_COMMIT, "tree": REAL_BASE_TREE},
        )
        self.assertEqual(
            baseline["manifest"],
            {
                "path": "30 Sistema/Estado/migration-manifest.json",
                "sha256": hashlib.sha256(manifest_bytes).hexdigest(),
                "serialization": "json-utf8-nfc-indent-2-lf-v1",
            },
        )

        inventory = baseline["inventory"]
        self.assertEqual(inventory["records"], 1059)
        self.assertEqual(inventory["unique_sources"], 1059)
        self.assertEqual(inventory["unique_destinations"], 1059)
        self.assertEqual(
            inventory["category_counts"],
            {"archive": 313, "home": 7, "knowledge": 505, "subject": 221, "system": 13},
        )

        binary = inventory["binary"]
        self.assertEqual(
            binary["method"],
            "casefolded-filename-ending-extension-allowlist-v1",
        )
        suffixes = binary["extensions"]
        self.assertEqual(
            suffixes,
            [
                ".docx",
                ".heic",
                ".jpg",
                ".pdf",
                ".pkl",
                ".png",
                ".ppt",
                ".pptx",
                ".rdata",
                ".xlsx",
            ],
        )
        binary_count = sum(
            PurePosixPath(str(record["source"]))
            .name.casefold()
            .endswith(tuple(suffixes))
            for record in manifest
        )
        self.assertEqual(binary["count"], binary_count)

        aggregate = hashlib.sha256()
        for record in sorted(
            manifest, key=lambda item: str(item["source"]).encode("utf-8")
        ):
            aggregate.update(str(record["source"]).encode("utf-8"))
            aggregate.update(b"\x00")
            aggregate.update(bytes.fromhex(str(record["sha256"])))
            aggregate.update(int(record["size_bytes"]).to_bytes(8, "big"))
        self.assertEqual(
            inventory["aggregate"],
            {
                "method": "sha256-source-utf8-nul-content-sha256-bytes-size-u64be-v1",
                "sha256": aggregate.hexdigest(),
            },
        )

        self.assertEqual(
            baseline["wikilinks"],
            {
                "method": "obsidian-wikilink-audit-v1",
                "total": 5402,
                "unresolved": 408,
                "ambiguous": 3,
                "accent_normalization_matches": {
                    "value": 161,
                    "status": "audited_estimate",
                },
            },
        )

        serialized = json.dumps(
            baseline,
            ensure_ascii=False,
            indent=2,
            separators=(",", ": "),
        ) + "\n"
        self.assertEqual(REAL_BASELINE.read_bytes(), serialized.encode("utf-8"))

        forbidden = ("hostname", "mtime", str(ROOT), str(Path.home()))
        baseline_text = REAL_BASELINE.read_text(encoding="utf-8")
        for value in forbidden:
            self.assertNotIn(value, baseline_text)


if __name__ == "__main__":
    unittest.main()
