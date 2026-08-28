import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unicodedata
import unittest
from unittest.mock import patch


try:
    rename_lesson_notes = importlib.import_module("rename_lesson_notes")
except ModuleNotFoundError:
    rename_lesson_notes = None


ROOT = Path(__file__).resolve().parents[2]
BASE_HEAD = "dc7a1cde627e2211fa7457367c160759e6ac7993"
FINAL_TOPIC = (
    "Exercício prático (Loja da Sofia) - equação patrimonial, "
    "BP, DRE e DFC pelo método direto"
)


def _git(vault: Path, *arguments: str) -> str:
    result = subprocess.run(
        ("git", *arguments),
        cwd=vault,
        check=True,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True,
    )
    return result.stdout.strip()


def _note(kind: str, *, topic: str, body: str, professor: bool = False) -> str:
    extra = "professor: Professora Exemplo\n" if professor else ""
    return (
        "---\n"
        "materia: MatemáticaAplicada\n"
        "data: 2026-08-06\n"
        f"{extra}"
        f"tema: {topic}\n"
        "topicos: [funções, limites]\n"
        f"tags: [{kind}]\n"
        "---\n"
        f"{body}"
    )


class GitVaultFixture:
    def __init__(self, *, collision: str | None = None) -> None:
        self.temporary = TemporaryDirectory()
        self.vault = Path(self.temporary.name)
        (self.vault / ".fgv/config").mkdir(parents=True)
        (self.vault / "30 Sistema/Estado").mkdir(parents=True)
        self.class_dir = self.vault / "10 Matérias/MatemáticaAplicada/Aulas/08.06"
        self.class_dir.mkdir(parents=True)
        self.archive = self.vault / "90 Arquivo/2026.1/Legada/Aulas/01.01/Resumo.md"
        self.archive.parent.mkdir(parents=True)
        subjects = {
            "schema_version": 1,
            "semester": "2026.2",
            "timezone": "America/Sao_Paulo",
            "subjects": [
                {
                    "id": "matematica-aplicada",
                    "display_name": "Matemática Aplicada I",
                    "folder": "MatemáticaAplicada",
                    "path": "10 Matérias/MatemáticaAplicada",
                    "task_tag": "#ma1",
                    "aliases": ["MatemáticaAplicada", "ma1"],
                    "legacy_frontmatter_values": ["MatemáticaAplicada"],
                }
            ],
        }
        (self.vault / ".fgv/config/subjects.json").write_text(
            json.dumps(subjects, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        (self.class_dir / "Resumo.md").write_text(
            _note(
                "resumo",
                topic="Funções, Limites e Domínio",
                body="Resumo aponta para [[Transcrito]].\n",
            ),
            encoding="utf-8",
        )
        (self.class_dir / "Transcrito.md").write_text(
            _note(
                "transcrito",
                topic="Funções, Limites e Domínio",
                professor=True,
                body="Veja [[Resumo]] e depois [[Resumo]].\n",
            ),
            encoding="utf-8",
        )
        self.archive.write_text("arquivo legado\n", encoding="utf-8")
        if collision is not None:
            (self.class_dir / collision).write_text("collision\n", encoding="utf-8")
        _git(self.vault, "init", "-q")
        _git(self.vault, "add", "-A")
        _git(
            self.vault,
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-qm",
            "fixture",
        )
        self.head = _git(self.vault, "rev-parse", "HEAD")

    def close(self) -> None:
        self.temporary.cleanup()


class NamingUnitTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(rename_lesson_notes, "lesson renamer is missing")
        return rename_lesson_notes

    def test_topic_is_the_only_filename_source_and_date_is_not_repeated(self):
        module = self.module()
        name = module.destination_name(
            "resumo",
            "  Funções,   Limites e Domínio  ",
        )
        self.assertEqual(name, "Resumo - Funções, Limites e Domínio.md")
        self.assertNotIn("08.06", name)
        self.assertNotIn("2026", name)

    def test_portable_forbidden_characters_are_normalized_in_nfc(self):
        module = self.module()
        decomposed = unicodedata.normalize("NFD", "Café")
        name = module.destination_name(
            "transcrito",
            f'{decomposed}: BP / DRE? "Caixa" | Estoque*',
        )
        self.assertEqual(
            name,
            "Transcrito - Café - BP - DRE - Caixa - Estoque.md",
        )
        self.assertEqual(name, unicodedata.normalize("NFC", name))
        self.assertLessEqual(len(name.encode("utf-8")), 255)

    def test_valid_internal_hyphens_are_preserved_exactly(self):
        module = self.module()
        topic = (
            "Revisão pré-prova, Qui-quadrado, mente-cérebro, "
            "dado-informação-conhecimento"
        )
        self.assertEqual(
            module.destination_name("resumo", topic),
            f"Resumo - {topic}.md",
        )

    def test_empty_oversized_and_same_destination_are_rejected(self):
        module = self.module()
        with self.assertRaises(module.RenameError):
            module.destination_name("resumo", "  /:*?  ")
        with self.assertRaises(module.RenameError):
            module.destination_name("resumo", "á" * 200)
        with self.assertRaises(module.RenameError):
            module.assert_distinct_paths("A/Resumo.md", "A/Resumo.md")

    def test_metadata_normalization_preserves_body_and_allowed_fields(self):
        module = self.module()
        original = _note(
            "transcrito",
            topic="Funções, Limites e Domínio",
            professor=True,
            body="\n# Corpo\nBytes preservados.\n",
        ).encode("utf-8")
        result = module.normalize_note(
            original,
            source="10 Matérias/MatemáticaAplicada/Aulas/08.06/Transcrito.md",
            subject_id="matematica-aplicada",
            kind="transcrito",
            topic_override=None,
        )
        text = result.final_bytes.decode("utf-8")
        self.assertIn("materias: [matematica-aplicada]", text)
        self.assertIn("semestre: 2026.2", text)
        self.assertIn("data: 2026-08-06", text)
        self.assertIn("tipo: transcrito", text)
        self.assertIn("tema: Funções, Limites e Domínio", text)
        self.assertIn("status: completo", text)
        self.assertIn("contract_version: 1", text)
        self.assertIn("professor: Professora Exemplo", text)
        self.assertIn("topicos: [funções, limites]", text)
        self.assertIn("tags: [transcrito]", text)
        self.assertNotIn("\nmateria:", text)
        self.assertNotIn("source_sha256", text)
        self.assertNotIn("transaction_id", text)
        self.assertEqual(result.original_body, result.final_body)

    def test_only_the_three_authorized_short_links_change(self):
        module = self.module()
        topic = "Funções, Limites e Domínio"
        summary = module.normalize_note(
            _note(
                "resumo",
                topic=topic,
                body="Um [[Transcrito]], nenhum [[Resumo Completo]].\n",
            ).encode(),
            source="10 Matérias/MatemáticaAplicada/Aulas/08.06/Resumo.md",
            subject_id="matematica-aplicada",
            kind="resumo",
            topic_override=None,
        )
        transcript = module.normalize_note(
            _note(
                "transcrito",
                topic=topic,
                body="Dois: [[Resumo]] e [[Resumo]].\n",
            ).encode(),
            source="10 Matérias/MatemáticaAplicada/Aulas/08.06/Transcrito.md",
            subject_id="matematica-aplicada",
            kind="transcrito",
            topic_override=None,
        )
        self.assertEqual(summary.transform_occurrences, 1)
        self.assertEqual(transcript.transform_occurrences, 2)
        self.assertEqual(summary.content_class, "authorized-body-transform")
        self.assertEqual(transcript.content_class, "authorized-body-transform")
        self.assertIn(
            b"[[Transcrito - Fun\xc3\xa7\xc3\xb5es, Limites e Dom\xc3\xadnio]]",
            summary.final_body,
        )
        self.assertIn(b"[[Resumo Completo]]", summary.final_body)

    def test_invalid_utf8_and_duplicate_frontmatter_keys_fail_closed(self):
        module = self.module()
        with self.assertRaises(module.RenameError):
            module.normalize_note(
                b"---\nmateria: Matem\xfftica\ndata: 2026-08-06\ntema: Tema\n---\n",
                source="10 Matérias/MatemáticaAplicada/Aulas/08.06/Resumo.md",
                subject_id="matematica-aplicada",
                kind="resumo",
                topic_override=None,
            )
        duplicate = (
            "---\n"
            "materia: MatemáticaAplicada\n"
            "data: 2026-08-06\n"
            "tema: Primeiro\n"
            "tema: Segundo\n"
            "---\n"
            "corpo\n"
        ).encode("utf-8")
        with self.assertRaises(module.RenameError):
            module.normalize_note(
                duplicate,
                source="10 Matérias/MatemáticaAplicada/Aulas/08.06/Resumo.md",
                subject_id="matematica-aplicada",
                kind="resumo",
                topic_override=None,
            )


class TransactionFixtureTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(rename_lesson_notes, "lesson renamer is missing")
        return rename_lesson_notes

    def setUp(self) -> None:
        self.fixture = GitVaultFixture()

    def tearDown(self) -> None:
        self.fixture.close()

    def execute(self, *, apply: bool = False):
        module = self.module()
        return module.execute_rename(
            self.fixture.vault,
            self.fixture.head,
            apply=apply,
            expected_active=2,
            expected_archive=1,
        )

    def snapshot(self):
        return {
            path.relative_to(self.fixture.vault).as_posix(): path.read_bytes()
            for path in self.fixture.vault.rglob("*")
            if path.is_file() and ".git" not in path.parts
        }

    @staticmethod
    def swap_leaf(
        parent_fd: int,
        name: str,
        backup_name: str,
        replacement: bytes = b"concurrent owner\n",
    ) -> None:
        os.rename(
            name,
            backup_name,
            src_dir_fd=parent_fd,
            dst_dir_fd=parent_fd,
        )
        descriptor = os.open(
            name,
            os.O_WRONLY | os.O_CREAT | os.O_EXCL | os.O_NOFOLLOW,
            0o600,
            dir_fd=parent_fd,
        )
        try:
            os.write(descriptor, replacement)
            os.fsync(descriptor)
        finally:
            os.close(descriptor)
        os.fsync(parent_fd)

    def test_dry_run_writes_nothing_and_manifest_is_closed_deterministic(self):
        module = self.module()
        before = self.snapshot()
        first = self.execute()
        second = self.execute()
        self.assertEqual(self.snapshot(), before)
        self.assertEqual(first.plan.manifest_bytes, second.plan.manifest_bytes)
        self.assertEqual(first.status, "planned")
        self.assertEqual(first.active_generic_notes, 2)
        self.assertEqual(first.rename_operations, 2)
        self.assertEqual(first.missing_tema, 0)
        self.assertEqual(first.collisions, 0)
        self.assertEqual(first.archive_operations, 0)
        manifest = json.loads(first.plan.manifest_bytes)
        self.assertEqual(set(manifest), set(module.MANIFEST_FIELDS))
        self.assertEqual(len(manifest["records"]), 2)
        for record in manifest["records"]:
            self.assertEqual(set(record), set(module.MANIFEST_RECORD_FIELDS))
        module.validate_manifest_bytes(first.plan.manifest_bytes, self.fixture.head)

    def test_apply_is_recoverable_and_second_run_is_explicit_noop(self):
        before_archive = self.fixture.archive.read_bytes()
        applied = self.execute(apply=True)
        self.assertEqual(applied.status, "applied")
        self.assertFalse((self.fixture.class_dir / "Resumo.md").exists())
        self.assertFalse((self.fixture.class_dir / "Transcrito.md").exists())
        summary = self.fixture.class_dir / "Resumo - Funções, Limites e Domínio.md"
        transcript = self.fixture.class_dir / "Transcrito - Funções, Limites e Domínio.md"
        self.assertTrue(summary.is_file())
        self.assertTrue(transcript.is_file())
        self.assertEqual(summary.read_text(encoding="utf-8").count("[[Transcrito - "), 1)
        self.assertEqual(transcript.read_text(encoding="utf-8").count("[[Resumo - "), 2)
        self.assertEqual(self.fixture.archive.read_bytes(), before_archive)
        self.assertFalse((self.fixture.vault / ".fgv/lesson-rename-journal.json").exists())
        no_op = self.execute(apply=True)
        self.assertEqual(no_op.status, "no_op")
        self.assertEqual(no_op.rename_operations, 2)

    def test_authenticated_fresh_apply_is_noop_after_head_advances_and_preserves_mtime(self):
        applied = self.execute(apply=True)
        self.assertEqual(applied.status, "applied")
        _git(self.fixture.vault, "add", "-A")
        _git(
            self.fixture.vault,
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-qm",
            "record applied lesson names",
        )
        self.assertNotEqual(_git(self.fixture.vault, "rev-parse", "HEAD"), self.fixture.head)
        tracked = [
            self.fixture.class_dir / "Resumo - Funções, Limites e Domínio.md",
            self.fixture.class_dir / "Transcrito - Funções, Limites e Domínio.md",
            self.fixture.vault / "30 Sistema/Estado/lesson-rename-manifest.json",
        ]
        before = {path: path.stat().st_mtime_ns for path in tracked}

        no_op = self.execute(apply=True)

        self.assertEqual(no_op.status, "no_op")
        self.assertEqual({path: path.stat().st_mtime_ns for path in tracked}, before)
        self.assertFalse(
            (self.fixture.vault / ".fgv/lesson-rename-journal.json").exists()
        )

    def test_manifest_validation_rejects_wrong_exact_types_even_with_fresh_aggregate(self):
        module = self.module()
        original = json.loads(self.execute().plan.manifest_bytes)
        top_level_mutations = {
            "schema": 1,
            "schema_version": True,
            "authority_commit": 1,
            "authority_tree": 1,
            "record_count": True,
            "aggregate_sha256": True,
            "records": {},
        }
        record_string_fields = (
            "source",
            "destination",
            "subject_id",
            "class_date",
            "kind",
            "topic",
            "original_sha256",
            "original_mode",
            "final_sha256",
            "final_mode",
            "original_body_sha256",
            "final_body_sha256",
            "content_class",
            "transform_id",
        )
        record_integer_fields = (
            "original_size_bytes",
            "final_size_bytes",
            "transform_occurrences",
        )

        cases: list[tuple[str, str | None, object]] = [
            (f"top.{field}", None, replacement)
            for field, replacement in top_level_mutations.items()
        ]
        cases.extend(
            (f"record.{field}", field, True) for field in record_string_fields
        )
        cases.extend(
            (f"record.{field}", field, True) for field in record_integer_fields
        )
        for label, record_field, replacement in cases:
            with self.subTest(field=label):
                value = json.loads(json.dumps(original, ensure_ascii=False))
                if record_field is None:
                    value[label.removeprefix("top.")] = replacement
                else:
                    value["records"][0][record_field] = replacement
                if (
                    type(value.get("authority_commit")) is str
                    and type(value.get("authority_tree")) is str
                    and type(value.get("records")) is list
                    and label != "top.aggregate_sha256"
                ):
                    value["aggregate_sha256"] = module._aggregate_manifest(
                        value["authority_commit"],
                        value["authority_tree"],
                        value["records"],
                    )
                payload = module._serialize_manifest(value)
                with self.assertRaises(module.RenameError):
                    module.validate_manifest_bytes(payload, self.fixture.head)

    def test_manifest_validation_rejects_invalid_string_formats_with_fresh_aggregate(self):
        module = self.module()
        original = json.loads(self.execute().plan.manifest_bytes)
        mutations = {
            "subject_id": "Not Canonical",
            "class_date": "2026-8-6",
            "topic": "",
            "original_mode": "0644",
            "final_mode": "0644",
            "original_sha256": "g" * 64,
            "final_sha256": "g" * 64,
            "original_body_sha256": "g" * 64,
            "final_body_sha256": "g" * 64,
            "content_class": "other",
            "transform_id": "other",
        }
        for field, replacement in mutations.items():
            with self.subTest(field=field):
                value = json.loads(json.dumps(original, ensure_ascii=False))
                value["records"][0][field] = replacement
                value["aggregate_sha256"] = module._aggregate_manifest(
                    value["authority_commit"],
                    value["authority_tree"],
                    value["records"],
                )
                with self.assertRaises(module.RenameError):
                    module.validate_manifest_bytes(
                        module._serialize_manifest(value), self.fixture.head
                    )

    def test_source_delete_quarantines_and_restores_a_leaf_swapped_after_authentication(self):
        module = self.module()
        swapped = False
        source_name = "Resumo.md"
        backup_name = "authenticated-source.backup"

        def race(parent_fd, name, label):
            nonlocal swapped
            if not swapped and name == source_name:
                swapped = True
                self.swap_leaf(parent_fd, name, backup_name)

        with patch.object(
            module,
            "_before_leaf_quarantine_move",
            side_effect=race,
            create=True,
        ):
            with self.assertRaises(module.RenameError):
                self.execute(apply=True)

        self.assertTrue(swapped)
        self.assertEqual(
            (self.fixture.class_dir / source_name).read_bytes(),
            b"concurrent owner\n",
        )
        self.assertTrue((self.fixture.class_dir / backup_name).is_file())
        self.assertTrue(
            (self.fixture.vault / ".fgv/lesson-rename-journal.json").is_file()
        )
        self.assertFalse(
            any(
                path.name.startswith(".lesson-rename-quarantine-")
                for path in self.fixture.class_dir.iterdir()
            )
        )

    def test_rollback_destination_and_manifest_removal_restore_swapped_leaf(self):
        module = self.module()
        plan = self.execute().plan
        operation = plan.operations[0]
        cases = (
            ("rollback destination", operation.final, 0o644),
            ("lesson rename manifest", plan.manifest_bytes, 0o644),
        )
        for label, expected, mode in cases:
            with self.subTest(site=label), TemporaryDirectory() as raw:
                directory = Path(raw)
                name = "owned-leaf"
                backup_name = "authenticated-leaf.backup"
                (directory / name).write_bytes(expected)
                os.chmod(directory / name, mode)
                parent_fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
                swapped = False

                def race(race_fd, race_name, race_label):
                    nonlocal swapped
                    if not swapped:
                        swapped = True
                        self.swap_leaf(race_fd, race_name, backup_name)

                try:
                    with patch.object(
                        module,
                        "_before_leaf_quarantine_move",
                        side_effect=race,
                        create=True,
                    ):
                        with self.assertRaises(module.RenameError):
                            module._unlink_exact(
                                parent_fd,
                                name,
                                expected,
                                mode,
                                label,
                            )
                    self.assertTrue(swapped)
                    self.assertEqual(
                        (directory / name).read_bytes(), b"concurrent owner\n"
                    )
                    self.assertEqual((directory / backup_name).read_bytes(), expected)
                    self.assertFalse(
                        any(
                            path.name.startswith(".lesson-rename-quarantine-")
                            for path in directory.iterdir()
                        )
                    )
                finally:
                    os.close(parent_fd)

    def test_journal_checkpoint_and_cleanup_restore_swapped_leaf(self):
        module = self.module()
        actions = ("checkpoint", "cleanup")
        for action in actions:
            with self.subTest(action=action):
                fixture = GitVaultFixture()
                root_fd = journal_fd = None
                try:
                    plan = module.build_plan(
                        fixture.vault,
                        fixture.head,
                        expected_active=2,
                        expected_archive=1,
                    )
                    _, root_fd = module._open_vault(fixture.vault)
                    journal_fd = module._open_journal_directory(root_fd)
                    module._install_journal(journal_fd, plan)
                    swapped = False
                    backup_name = f"authenticated-journal-{action}.backup"

                    def race(race_fd, name, label):
                        nonlocal swapped
                        if not swapped and name == module.JOURNAL_NAME:
                            swapped = True
                            self.swap_leaf(race_fd, name, backup_name)

                    with patch.object(
                        module,
                        "_before_leaf_quarantine_move",
                        side_effect=race,
                        create=True,
                    ):
                        with self.assertRaises(module.RenameError):
                            if action == "checkpoint":
                                module._checkpoint_journal(journal_fd, plan, 1)
                            else:
                                module._delete_journal(journal_fd, plan)
                    self.assertTrue(swapped)
                    journal = fixture.vault / ".fgv" / module.JOURNAL_NAME
                    self.assertEqual(journal.read_bytes(), b"concurrent owner\n")
                    self.assertTrue((fixture.vault / ".fgv" / backup_name).is_file())
                    self.assertFalse(
                        any(
                            path.name.startswith(".lesson-rename-quarantine-")
                            for path in (fixture.vault / ".fgv").iterdir()
                        )
                    )
                finally:
                    if journal_fd is not None:
                        os.close(journal_fd)
                    if root_fd is not None:
                        os.close(root_fd)
                    fixture.close()

    def test_final_quarantine_delete_swap_never_deletes_replacement(self):
        module = self.module()
        for label in (
            "source delete",
            "rollback destination",
            "lesson rename manifest",
            "lesson rename journal cleanup",
        ):
            with self.subTest(site=label), TemporaryDirectory() as raw:
                directory = Path(raw)
                canonical = "owned-leaf"
                backup = "authenticated-quarantine.backup"
                expected = b"authenticated owner\n"
                (directory / canonical).write_bytes(expected)
                parent_fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
                swapped = False

                def race(race_fd, quarantine_name, race_label):
                    nonlocal swapped
                    if swapped:
                        return
                    swapped = True
                    self.swap_leaf(race_fd, quarantine_name, backup)

                try:
                    with patch.object(
                        module,
                        "_before_quarantine_delete",
                        side_effect=race,
                        create=True,
                    ):
                        with self.assertRaises(module.RenameError):
                            module._unlink_exact(
                                parent_fd,
                                canonical,
                                expected,
                                0o644,
                                label,
                            )
                    self.assertTrue(swapped)
                    self.assertEqual(
                        (directory / canonical).read_bytes(), b"concurrent owner\n"
                    )
                    self.assertEqual((directory / backup).read_bytes(), expected)
                    self.assertFalse(
                        any(
                            path.name.startswith(".lesson-rename-")
                            for path in directory.iterdir()
                        )
                    )
                finally:
                    os.close(parent_fd)

    def test_final_journal_checkpoint_quarantine_swap_restores_without_overwrite(self):
        module = self.module()
        plan = self.execute().plan
        _, root_fd = module._open_vault(self.fixture.vault)
        journal_fd = module._open_journal_directory(root_fd)
        backup = "authenticated-journal-quarantine.backup"
        swapped = False

        def race(race_fd, quarantine_name, label):
            nonlocal swapped
            if not swapped and label == "lesson rename journal":
                swapped = True
                self.swap_leaf(race_fd, quarantine_name, backup)

        try:
            module._install_journal(journal_fd, plan)
            with patch.object(
                module,
                "_before_quarantine_delete",
                side_effect=race,
                create=True,
            ):
                with self.assertRaises(module.RenameError):
                    module._checkpoint_journal(journal_fd, plan, 1)
            self.assertTrue(swapped)
            journal = self.fixture.vault / ".fgv" / module.JOURNAL_NAME
            self.assertEqual(journal.read_bytes(), b"concurrent owner\n")
            self.assertEqual(
                (self.fixture.vault / ".fgv" / backup).read_bytes(),
                module._journal_payload(plan, 0),
            )
            self.assertFalse(
                any(
                    path.name.startswith(".lesson-rename-")
                    for path in (self.fixture.vault / ".fgv").iterdir()
                )
            )
        finally:
            os.close(journal_fd)
            os.close(root_fd)

    def test_known_quarantine_swap_after_exchange_preserves_both_owners(self):
        module = self.module()
        with TemporaryDirectory() as raw:
            directory = Path(raw)
            canonical = "owned-leaf"
            backup = "authenticated-purge-marker.backup"
            expected = b"authenticated owner\n"
            (directory / canonical).write_bytes(expected)
            parent_fd = os.open(directory, os.O_RDONLY | os.O_DIRECTORY)
            swapped = False

            def race(race_fd, quarantine_name, purge_name, label):
                nonlocal swapped
                del purge_name, label
                if not swapped:
                    swapped = True
                    self.swap_leaf(race_fd, quarantine_name, backup)

            try:
                with patch.object(
                    module,
                    "_after_purge_exchange",
                    side_effect=race,
                    create=True,
                ):
                    with self.assertRaises(module.RenameError):
                        module._unlink_exact(
                            parent_fd,
                            canonical,
                            expected,
                            0o644,
                            "source delete",
                        )
                self.assertTrue(swapped)
                self.assertEqual(
                    (directory / canonical).read_bytes(), b"concurrent owner\n"
                )
                retained = [
                    path
                    for path in directory.iterdir()
                    if path.name.startswith(module.PURGE_PREFIX)
                    and path.name.endswith(".target")
                ]
                self.assertEqual(len(retained), 1)
                self.assertEqual(retained[0].read_bytes(), expected)
                self.assertTrue((directory / backup).is_file())
            finally:
                os.close(parent_fd)

    def test_crash_after_purge_exchange_is_recovered_for_source_and_journal(self):
        module = self.module()

        class SimulatedCrash(BaseException):
            pass

        for site in ("source", "journal-checkpoint"):
            with self.subTest(site=site):
                fixture = GitVaultFixture()

                def crash(parent_fd, quarantine_name, purge_name, label):
                    del parent_fd, quarantine_name, purge_name
                    if site == "source" and not label.endswith("/Resumo.md"):
                        return
                    if site == "journal-checkpoint" and label != "lesson rename journal":
                        return
                    raise SimulatedCrash(site)

                try:
                    with patch.object(
                        module,
                        "_after_purge_exchange",
                        side_effect=crash,
                        create=True,
                    ):
                        with self.assertRaises(SimulatedCrash):
                            module.execute_rename(
                                fixture.vault,
                                fixture.head,
                                apply=True,
                                expected_active=2,
                                expected_archive=1,
                            )
                    self.assertTrue(
                        list(fixture.vault.rglob(f"{module.PURGE_PREFIX}*"))
                    )
                    recovered = module.execute_rename(
                        fixture.vault,
                        fixture.head,
                        apply=True,
                        expected_active=2,
                        expected_archive=1,
                    )
                    self.assertEqual(recovered.status, "applied")
                    self.assertFalse(
                        list(fixture.vault.rglob(f"{module.PURGE_PREFIX}*"))
                    )
                    self.assertFalse(
                        (fixture.vault / ".fgv/lesson-rename-journal.json").exists()
                    )
                finally:
                    fixture.close()

    def test_crash_after_quarantine_move_recovers_source_and_journal_boundaries(self):
        module = self.module()

        class SimulatedCrash(BaseException):
            pass

        for site in ("source", "journal-checkpoint", "journal-cleanup"):
            with self.subTest(site=site):
                fixture = GitVaultFixture()
                armed = site != "journal-cleanup"

                def arm_cleanup(plan):
                    nonlocal armed
                    del plan
                    armed = True

                def crash_after_move(parent_fd, name, quarantine_name, label):
                    del parent_fd, name, quarantine_name
                    if not armed:
                        return
                    if site == "source" and not label.endswith("/Resumo.md"):
                        return
                    if site.startswith("journal") and label != "lesson rename journal":
                        return
                    raise SimulatedCrash(site)

                try:
                    with patch.object(
                        module,
                        "_after_leaf_quarantine_move",
                        side_effect=crash_after_move,
                        create=True,
                    ), patch.object(
                        module,
                        "_before_journal_delete",
                        side_effect=arm_cleanup,
                    ):
                        with self.assertRaises(SimulatedCrash):
                            module.execute_rename(
                                fixture.vault,
                                fixture.head,
                                apply=True,
                                expected_active=2,
                                expected_archive=1,
                            )
                    self.assertTrue(
                        list(fixture.vault.rglob(f"{module.QUARANTINE_PREFIX}*"))
                    )
                    recovered = module.execute_rename(
                        fixture.vault,
                        fixture.head,
                        apply=True,
                        expected_active=2,
                        expected_archive=1,
                    )
                    self.assertEqual(recovered.status, "applied")
                    self.assertFalse(
                        list(fixture.vault.rglob(f"{module.QUARANTINE_PREFIX}*"))
                    )
                    self.assertFalse(
                        (fixture.vault / ".fgv/lesson-rename-journal.json").exists()
                    )
                finally:
                    fixture.close()

    def test_crash_after_rollback_destination_quarantine_is_recovered(self):
        module = self.module()

        class SimulatedCrash(BaseException):
            pass

        def force_rollback(operation):
            del operation
            raise RuntimeError("force rollback")

        def crash_after_move(parent_fd, name, quarantine_name, label):
            del parent_fd, name, quarantine_name
            if label.startswith("rollback destination "):
                raise SimulatedCrash(label)

        with patch.object(
            module,
            "_after_destination_publish",
            side_effect=force_rollback,
        ), patch.object(
            module,
            "_after_leaf_quarantine_move",
            side_effect=crash_after_move,
            create=True,
        ):
            with self.assertRaises(SimulatedCrash):
                self.execute(apply=True)
        self.assertTrue(
            list(self.fixture.vault.rglob(f"{module.QUARANTINE_PREFIX}*"))
        )

        recovered = self.execute(apply=True)

        self.assertEqual(recovered.status, "applied")
        self.assertFalse(
            list(self.fixture.vault.rglob(f"{module.QUARANTINE_PREFIX}*"))
        )

    def test_crash_after_manifest_quarantine_is_recovered(self):
        module = self.module()

        class SimulatedCrash(BaseException):
            pass

        with patch.object(
            module,
            "_before_journal_delete",
            side_effect=SimulatedCrash("leave committed journal"),
        ):
            with self.assertRaises(SimulatedCrash):
                self.execute(apply=True)

        def crash_after_move(parent_fd, name, quarantine_name, label):
            del parent_fd, name, quarantine_name
            if label == "lesson rename manifest":
                raise SimulatedCrash(label)

        with patch.object(
            module,
            "_after_leaf_quarantine_move",
            side_effect=crash_after_move,
            create=True,
        ):
            with self.assertRaises(SimulatedCrash):
                self.execute(apply=True)
        self.assertTrue(
            list(self.fixture.vault.rglob(f"{module.QUARANTINE_PREFIX}*"))
        )

        recovered = self.execute(apply=True)

        self.assertEqual(recovered.status, "applied")
        self.assertFalse(
            list(self.fixture.vault.rglob(f"{module.QUARANTINE_PREFIX}*"))
        )

    def test_crash_journal_is_authenticated_recovered_and_reapplied(self):
        module = self.module()

        class SimulatedCrash(BaseException):
            pass

        calls = 0
        real_checkpoint = module._checkpoint_journal

        def crash_once(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise SimulatedCrash("power loss")
            return real_checkpoint(*args, **kwargs)

        with patch.object(module, "_checkpoint_journal", side_effect=crash_once):
            with self.assertRaises(SimulatedCrash):
                self.execute(apply=True)
        journal = self.fixture.vault / ".fgv/lesson-rename-journal.json"
        self.assertTrue(journal.is_file())

        recovered = self.execute(apply=True)
        self.assertEqual(recovered.status, "applied")
        self.assertFalse(journal.exists())

    def test_crashes_at_each_publish_delete_boundary_are_recoverable(self):
        module = self.module()

        class SimulatedCrash(BaseException):
            pass

        hooks = (
            "_after_destination_publish",
            "_after_source_delete",
            "_after_manifest_publish",
            "_before_journal_delete",
        )
        for hook in hooks:
            with self.subTest(hook=hook):
                fixture = GitVaultFixture()
                try:
                    calls = 0

                    def crash_first(*args, **kwargs):
                        nonlocal calls
                        calls += 1
                        if calls == 1:
                            raise SimulatedCrash(hook)

                    with patch.object(module, hook, side_effect=crash_first):
                        with self.assertRaises(SimulatedCrash):
                            module.execute_rename(
                                fixture.vault,
                                fixture.head,
                                apply=True,
                                expected_active=2,
                                expected_archive=1,
                            )
                    self.assertTrue(
                        (fixture.vault / ".fgv/lesson-rename-journal.json").is_file()
                    )
                    recovered = module.execute_rename(
                        fixture.vault,
                        fixture.head,
                        apply=True,
                        expected_active=2,
                        expected_archive=1,
                    )
                    self.assertEqual(recovered.status, "applied")
                    self.assertFalse(
                        (fixture.vault / ".fgv/lesson-rename-journal.json").exists()
                    )
                finally:
                    fixture.close()

    def test_journal_tamper_is_rejected_against_reconstructed_plan(self):
        module = self.module()

        class SimulatedCrash(BaseException):
            pass

        mutations = {
            "original": lambda value: value["operations"][0].update(
                original_sha256="0" * 64
            ),
            "output": lambda value: value["operations"][0].update(
                final_sha256="0" * 64
            ),
            "mode": lambda value: value["operations"][0].update(mode="100755"),
            "order": lambda value: value["operations"].reverse(),
        }
        for label, mutate in mutations.items():
            with self.subTest(label=label):
                fixture = GitVaultFixture()
                try:
                    with patch.object(
                        module,
                        "_after_destination_publish",
                        side_effect=SimulatedCrash("power loss"),
                    ):
                        with self.assertRaises(SimulatedCrash):
                            module.execute_rename(
                                fixture.vault,
                                fixture.head,
                                apply=True,
                                expected_active=2,
                                expected_archive=1,
                            )
                    journal = fixture.vault / ".fgv/lesson-rename-journal.json"
                    value = json.loads(journal.read_bytes())
                    mutate(value)
                    journal.write_text(
                        json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                        encoding="utf-8",
                    )
                    before = {
                        p.relative_to(fixture.vault).as_posix(): p.read_bytes()
                        for p in fixture.vault.rglob("*")
                        if p.is_file() and ".git" not in p.parts
                    }
                    with self.assertRaises(module.RenameError):
                        module.execute_rename(
                            fixture.vault,
                            fixture.head,
                            apply=True,
                            expected_active=2,
                            expected_archive=1,
                        )
                    after = {
                        p.relative_to(fixture.vault).as_posix(): p.read_bytes()
                        for p in fixture.vault.rglob("*")
                        if p.is_file() and ".git" not in p.parts
                    }
                    self.assertEqual(after, before)
                finally:
                    fixture.close()

    def test_exact_casefold_and_nfd_collisions_block_without_writing(self):
        module = self.module()
        for collision in (
            "Resumo - Funções, Limites e Domínio.md",
            "resumo - funções, limites e domínio.md",
            unicodedata.normalize("NFD", "Resumo - Funções, Limites e Domínio.md"),
        ):
            with self.subTest(collision=collision):
                fixture = GitVaultFixture(collision=collision)
                try:
                    before = {
                        p.relative_to(fixture.vault).as_posix(): p.read_bytes()
                        for p in fixture.vault.rglob("*")
                        if p.is_file() and ".git" not in p.parts
                    }
                    with self.assertRaises(module.RenameError):
                        module.execute_rename(
                            fixture.vault,
                            fixture.head,
                            apply=True,
                            expected_active=2,
                            expected_archive=1,
                        )
                    after = {
                        p.relative_to(fixture.vault).as_posix(): p.read_bytes()
                        for p in fixture.vault.rglob("*")
                        if p.is_file() and ".git" not in p.parts
                    }
                    self.assertEqual(after, before)
                finally:
                    fixture.close()

    def test_destination_appearing_at_publish_is_never_overwritten(self):
        module = self.module()
        real_hook = module._before_operation_publish
        created: Path | None = None

        def race(operation):
            nonlocal created
            if created is None:
                created = self.fixture.vault / operation.destination
                created.write_text("concurrent owner\n", encoding="utf-8")
            return real_hook(operation)

        with patch.object(module, "_before_operation_publish", side_effect=race):
            with self.assertRaises(module.RenameError):
                self.execute(apply=True)
        self.assertIsNotNone(created)
        self.assertEqual(created.read_text(encoding="utf-8"), "concurrent owner\n")
        self.assertTrue((self.fixture.class_dir / "Resumo.md").is_file())

    def test_source_destination_and_parent_symlinks_never_redirect(self):
        module = self.module()
        cases = ("source", "destination", "parent")
        for case in cases:
            with self.subTest(case=case):
                fixture = GitVaultFixture()
                with TemporaryDirectory() as external_raw:
                    external = Path(external_raw)
                    sentinel = external / "sentinel.md"
                    sentinel.write_text("external\n", encoding="utf-8")
                    detached = fixture.vault / "detached-class"
                    try:
                        if case == "source":
                            source = fixture.class_dir / "Resumo.md"
                            source.unlink()
                            source.symlink_to(sentinel)
                        elif case == "destination":
                            destination = (
                                fixture.class_dir
                                / "Resumo - Funções, Limites e Domínio.md"
                            )
                            destination.symlink_to(sentinel)
                        else:
                            fixture.class_dir.rename(detached)
                            fixture.class_dir.symlink_to(external, target_is_directory=True)
                        with self.assertRaises(module.RenameError):
                            module.execute_rename(
                                fixture.vault,
                                fixture.head,
                                apply=True,
                                expected_active=2,
                                expected_archive=1,
                            )
                        self.assertEqual(
                            sentinel.read_text(encoding="utf-8"), "external\n"
                        )
                    finally:
                        if fixture.class_dir.is_symlink():
                            fixture.class_dir.unlink()
                        if detached.exists():
                            detached.rename(fixture.class_dir)
                        fixture.close()

    def test_parent_swap_hook_cannot_redirect_transaction(self):
        module = self.module()
        with TemporaryDirectory() as external_raw:
            external = Path(external_raw)
            sentinel = external / "sentinel.md"
            sentinel.write_text("external\n", encoding="utf-8")
            detached = self.fixture.vault / "detached-class"
            swapped = False

            def swap(operation):
                nonlocal swapped
                if not swapped:
                    swapped = True
                    self.fixture.class_dir.rename(detached)
                    self.fixture.class_dir.symlink_to(external, target_is_directory=True)

            try:
                with patch.object(
                    module, "_before_operation_publish", side_effect=swap
                ):
                    with self.assertRaises(module.RenameError):
                        self.execute(apply=True)
                self.assertEqual(sentinel.read_text(encoding="utf-8"), "external\n")
            finally:
                if self.fixture.class_dir.is_symlink():
                    self.fixture.class_dir.unlink()
                if detached.exists():
                    detached.rename(self.fixture.class_dir)

    def test_expected_head_divergence_and_merge_state_block_apply(self):
        module = self.module()
        extra = self.fixture.vault / "extra.md"
        extra.write_text("extra\n", encoding="utf-8")
        _git(self.fixture.vault, "add", "extra.md")
        _git(
            self.fixture.vault,
            "-c",
            "user.name=Fixture",
            "-c",
            "user.email=fixture@example.invalid",
            "commit",
            "-qm",
            "diverge",
        )
        with self.assertRaises(module.RenameError):
            self.execute(apply=True)

        other = GitVaultFixture()
        try:
            (other.vault / ".git/MERGE_HEAD").write_text(
                other.head + "\n", encoding="ascii"
            )
            with self.assertRaises(module.RenameError):
                module.execute_rename(
                    other.vault,
                    other.head,
                    apply=True,
                    expected_active=2,
                    expected_archive=1,
                )
        finally:
            other.close()

    def test_hostile_git_environment_is_ignored(self):
        module = self.module()
        with patch.dict(
            os.environ,
            {
                "GIT_DIR": "/definitely/not/the/fixture",
                "GIT_WORK_TREE": "/also/not/the/fixture",
                "GIT_REPLACE_REF_BASE": "refs/evil/",
                "GIT_NO_REPLACE_OBJECTS": "0",
            },
        ):
            report = module.execute_rename(
                self.fixture.vault,
                self.fixture.head,
                apply=False,
                expected_active=2,
                expected_archive=1,
            )
        self.assertEqual(report.status, "planned")

    def test_missing_or_tampered_applied_manifest_is_rejected(self):
        module = self.module()
        for mutation in ("missing", "partial", "hash"):
            with self.subTest(mutation=mutation):
                fixture = GitVaultFixture()
                try:
                    module.execute_rename(
                        fixture.vault,
                        fixture.head,
                        apply=True,
                        expected_active=2,
                        expected_archive=1,
                    )
                    manifest = (
                        fixture.vault
                        / "30 Sistema/Estado/lesson-rename-manifest.json"
                    )
                    if mutation == "missing":
                        manifest.unlink()
                    else:
                        value = json.loads(manifest.read_bytes())
                        if mutation == "partial":
                            value["records"].pop()
                        else:
                            value["records"][0]["final_sha256"] = "0" * 64
                        manifest.write_text(
                            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
                            encoding="utf-8",
                        )
                    with self.assertRaises(module.RenameError):
                        module.execute_rename(
                            fixture.vault,
                            fixture.head,
                            apply=False,
                            expected_active=2,
                            expected_archive=1,
                        )
                finally:
                    fixture.close()

    def test_unrelated_dirty_file_blocks_apply(self):
        module = self.module()
        unrelated = self.fixture.vault / "unrelated.txt"
        unrelated.write_text("dirty\n", encoding="utf-8")
        before = self.snapshot()
        with self.assertRaises(module.RenameError):
            self.execute(apply=True)
        self.assertEqual(self.snapshot(), before)


class ProductionContractTests(unittest.TestCase):
    def module(self):
        self.assertIsNotNone(rename_lesson_notes, "lesson renamer is missing")
        return rename_lesson_notes

    def test_real_plan_or_applied_state_has_exact_contract(self):
        module = self.module()
        report = module.execute_rename(
            ROOT,
            BASE_HEAD,
            apply=False,
            expected_active=42,
            expected_archive=47,
        )
        self.assertIn(report.status, {"planned", "no_op"})
        self.assertEqual(report.active_generic_notes, 42)
        self.assertEqual(report.rename_operations, 42)
        self.assertEqual(report.missing_tema, 0)
        self.assertEqual(report.collisions, 0)
        self.assertEqual(report.archive_operations, 0)
        records = report.plan.manifest["records"]
        self.assertEqual(len(records), 42)
        self.assertEqual(
            sum(record["kind"] == "resumo" for record in records), 21
        )
        self.assertEqual(
            sum(record["kind"] == "transcrito" for record in records), 21
        )
        self.assertEqual(
            sum(record["content_class"] == "metadata-only" for record in records),
            40,
        )
        transformed = [
            record
            for record in records
            if record["content_class"] == "authorized-body-transform"
        ]
        self.assertEqual(len(transformed), 2)
        self.assertEqual(sum(record["transform_occurrences"] for record in transformed), 3)
        self.assertTrue(
            all(
                record["transform_id"]
                == "matematica-aplicada-08.06-short-links-v1"
                for record in transformed
            )
        )
        pair = [
            record
            for record in records
            if record["source"].startswith(
                "10 Matérias/ContabilidadeFinanceira/Aulas/08.10/"
            )
        ]
        self.assertEqual({record["topic"] for record in pair}, {FINAL_TOPIC})
        self.assertEqual(
            [record["source"] for record in records],
            sorted(record["source"] for record in records),
        )
        module.validate_manifest_bytes(report.plan.manifest_bytes, BASE_HEAD)


if __name__ == "__main__":
    unittest.main()
