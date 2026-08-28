import hashlib
import importlib
import io
import json
import os
from pathlib import Path
from tempfile import TemporaryDirectory
import time
import unicodedata
import unittest
from unittest.mock import patch


try:
    rewrite_paths = importlib.import_module("rewrite_paths")
except ModuleNotFoundError:
    rewrite_paths = None


ROOT = Path(__file__).resolve().parents[2]


def manifest_record(source: str, destination: str, payload: bytes = b"fixture\n"):
    return {
        "schema_version": 1,
        "source": source,
        "destination": destination,
        "sha256": hashlib.sha256(payload).hexdigest(),
        "size_bytes": len(payload),
        "category": "system",
        "phase": "structural",
        "reason": "rewrite fixture",
    }


class RewriteTextTests(unittest.TestCase):
    def require_rewriter(self):
        self.assertIsNotNone(rewrite_paths, "path rewriter is missing")
        return rewrite_paths

    def test_only_mapped_path_literals_change(self) -> None:
        module = self.require_rewriter()
        rules = (
            module.LiteralRewrite("Vault/Conceitos", "20 Conhecimento/Conceitos", 2),
        )
        source = "\n".join(
            (
                "[[Conceito Curto]]",
                "[[Vault/Conceitos/Café com Leite|café]]",
                "`Vault/Conceitos/Café com Leite.md`",
                "https://example.invalid/Vault/Conceitos/Café",
                "[externo](https://example.invalid/Vault/Conceitos/Café)",
                "obsidian://open?vault=FGV&file=Vault/Conceitos/Café",
                "file:///tmp/Vault/Conceitos/Café.md",
                "ftp://example.invalid/Vault/Conceitos/Café.md",
                "data:text/plain,Vault/Conceitos/Café",
                "urn:fgv:Vault/Conceitos/Café",
                "NotVault/Conceitos/Café.md",
                "```python",
                'path = "unrelated/legacy/file.md"',
                "```",
            )
        )

        output, occurrences = module.rewrite_markdown_text(source, rules)

        self.assertEqual(occurrences, 2)
        self.assertIn("[[Conceito Curto]]", output)
        self.assertIn("[[20 Conhecimento/Conceitos/Café com Leite|café]]", output)
        self.assertIn("`20 Conhecimento/Conceitos/Café com Leite.md`", output)
        self.assertIn("https://example.invalid/Vault/Conceitos/Café", output)
        self.assertIn("[externo](https://example.invalid/Vault/Conceitos/Café)", output)
        self.assertIn("obsidian://open?vault=FGV&file=Vault/Conceitos/Café", output)
        self.assertIn("file:///tmp/Vault/Conceitos/Café.md", output)
        self.assertIn("ftp://example.invalid/Vault/Conceitos/Café.md", output)
        self.assertIn("data:text/plain,Vault/Conceitos/Café", output)
        self.assertIn("urn:fgv:Vault/Conceitos/Café", output)
        self.assertIn("NotVault/Conceitos/Café.md", output)
        self.assertIn('path = "unrelated/legacy/file.md"', output)

    def test_spaces_and_accents_are_kept_in_nfc(self) -> None:
        module = self.require_rewriter()
        destination = "20 Conhecimento/Conceitos"
        source = "`Vault/Conceitos/Café com Leite.md`"

        output, occurrences = module.rewrite_markdown_text(
            source,
            (module.LiteralRewrite("Vault/Conceitos", destination, 1),),
        )

        self.assertEqual(occurrences, 1)
        self.assertEqual(
            output,
            "`20 Conhecimento/Conceitos/Café com Leite.md`",
        )
        self.assertEqual(output, unicodedata.normalize("NFC", output))

    def test_authorized_path_in_code_fence_changes_but_unrelated_code_does_not(self) -> None:
        module = self.require_rewriter()
        source = """```bash
cd ~/FGV/Estatistica2/Aulas/08.17
cd ~/other/Estatistica2/Aulas/08.17
```
"""

        output, occurrences = module.rewrite_markdown_text(
            source,
            (
                module.LiteralRewrite(
                    "~/FGV/Estatistica2/Aulas",
                    "~/FGV/10 Matérias/Estatistica2/Aulas",
                    1,
                ),
            ),
        )

        self.assertEqual(occurrences, 1)
        self.assertIn("cd ~/FGV/10 Matérias/Estatistica2/Aulas/08.17", output)
        self.assertIn("cd ~/other/Estatistica2/Aulas/08.17", output)

    def test_production_shell_paths_with_spaces_remain_single_arguments(self) -> None:
        module = self.require_rewriter()
        cases = (
            (
                "10 Matérias/Estatistica2/Aulas/08.17/AulaTestesHipoteseExcelR.md",
                "cd ~/FGV/Estatistica2/Aulas/08.17\n"
                "Pasta `~/FGV/Estatistica2/Aulas/08.17`\n",
                "cd ~/FGV/10\\ Matérias/Estatistica2/Aulas/08.17",
            ),
            (
                "30 Sistema/Automacoes/2026-05-25-weekly-summary-plan.md",
                "ls -la ~/FGV/Vault/automation/file.md\n"
                + "Read `~/FGV/Vault/automation/file.md`\n" * 10,
                "ls -la ~/FGV/30\\ Sistema/Automacoes/file.md",
            ),
            (
                "30 Sistema/Specs/2026-08-19-caso-marcus-dent-plan.md",
                "AULA=$VAULT/ContabilidadeFinanceira/Aulas/08.19\n"
                + "Path `ContabilidadeFinanceira/Aulas/08.19`\n" * 7
                + "Spec `~/FGV/Vault/Specs/file.md`\n"
                + "Path `Vault/Conceitos/X.md`\n" * 26
                + "Template `Vault/Templates/X.md`\n"
                + "Spec `Vault/Specs/file.md`\n",
                'AULA="$VAULT/10 Matérias/ContabilidadeFinanceira/Aulas/08.19"',
            ),
        )
        for relative, source, expected in cases:
            with self.subTest(relative=relative):
                output, _ = module.rewrite_markdown_text(
                    source, module.MARKDOWN_SPECS[relative]
                )
                self.assertIn(expected, output)


class VaultRewriteFixtureTests(unittest.TestCase):
    def require_rewriter(self):
        self.assertIsNotNone(rewrite_paths, "path rewriter is missing")
        return rewrite_paths

    def setUp(self) -> None:
        self.temporary = TemporaryDirectory()
        self.vault = Path(self.temporary.name)
        self.manifest_path = self.vault / "state/manifest.json"
        self.manifest_path.parent.mkdir(parents=True)
        records = [
            manifest_record(
                "Vault/Conceitos/Café com Leite.md",
                "20 Conhecimento/Conceitos/Café com Leite.md",
            )
        ]
        self.manifest_path.write_text(
            json.dumps(records, ensure_ascii=False) + "\n", encoding="utf-8"
        )
        (self.vault / ".fgv").mkdir()
        self.note_path = self.vault / "notes/a.md"
        self.note_path.parent.mkdir(parents=True)
        self.note_path.write_text(
            "[[Vault/Conceitos/Café com Leite]]\n"
            "`Vault/Conceitos/Café com Leite.md`\n",
            encoding="utf-8",
        )
        self.rules = {
            "notes/a.md": (
                None,
            )
        }
        self._write_stale_configs()
        module = self.require_rewriter()
        self.auth = module.ManifestAuth(
            relative_path="state/manifest.json",
            sha256=hashlib.sha256(self.manifest_path.read_bytes()).hexdigest(),
            record_count=1,
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def _literal_rules(self):
        module = self.require_rewriter()
        return {
            "notes/a.md": (
                module.LiteralRewrite(
                    "Vault/Conceitos", "20 Conhecimento/Conceitos", 2
                ),
            )
        }

    def _write_json(self, relative: str, value: object) -> None:
        path = self.vault / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(
            json.dumps(value, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )

    def _write_stale_configs(self) -> None:
        self._write_json(
            ".obsidian/app.json",
            {"attachmentFolderPath": "Vault/Attachments", "alwaysUpdateLinks": True},
        )
        self._write_json(".obsidian/templates.json", {"folder": "Vault/Templates"})
        self._write_json(
            ".obsidian/graph.json",
            {"colorGroups": [{"query": "path:Vault/Conceitos", "color": {"a": 1}}]},
        )
        self._write_json(".obsidian/core-plugins.json", {"daily-notes": True})
        self._write_json(
            ".obsidian/daily-notes.json",
            {
                "format": "YYYY-MM-DD",
                "folder": "Vault/Daily",
                "template": "Vault/Templates/Daily.md",
                "autorun": False,
            },
        )

    def _rewrite(self, *, check: bool = False, link_contract=None):
        module = self.require_rewriter()
        return module.rewrite_vault(
            self.vault,
            Path("state/manifest.json"),
            check=check,
            markdown_specs=self._literal_rules(),
            expected_markdown_occurrences=2,
            manifest_auth=self.auth,
            link_contract=link_contract,
        )

    def _snapshot(self):
        return {
            path.relative_to(self.vault).as_posix(): path.read_bytes()
            for path in self.vault.rglob("*")
            if path.is_file()
        }

    def test_check_reports_stale_without_writing_then_fresh_after_apply(self) -> None:
        before = self._snapshot()

        stale = self._rewrite(check=True)

        self.assertEqual(stale.status, "stale")
        self.assertEqual(stale.occurrences, 7)
        self.assertEqual(stale.files_changed, 6)
        self.assertEqual(self._snapshot(), before)

        applied = self._rewrite()
        fresh = self._rewrite(check=True)

        self.assertEqual(applied.status, "updated")
        self.assertEqual(applied.occurrences, 7)
        self.assertEqual(applied.files_changed, 6)
        self.assertEqual(fresh.status, "fresh")
        self.assertEqual(fresh.files_changed, 0)

    def test_configs_are_valid_and_match_the_final_contract(self) -> None:
        self._rewrite()

        app = json.loads((self.vault / ".obsidian/app.json").read_bytes())
        templates = json.loads(
            (self.vault / ".obsidian/templates.json").read_bytes()
        )
        graph = json.loads((self.vault / ".obsidian/graph.json").read_bytes())
        core = json.loads(
            (self.vault / ".obsidian/core-plugins.json").read_bytes()
        )
        daily = json.loads(
            (self.vault / ".obsidian/daily-notes.json").read_bytes()
        )
        self.assertEqual(app["attachmentFolderPath"], "30 Sistema/Anexos")
        self.assertIs(app["alwaysUpdateLinks"], True)
        self.assertEqual(templates["folder"], "30 Sistema/Templates")
        self.assertEqual(
            graph["colorGroups"][0]["query"], "path:20 Conhecimento/Conceitos"
        )
        self.assertIs(core["daily-notes"], False)
        self.assertEqual(daily["folder"], "00 Home/Daily")
        self.assertEqual(daily["template"], "")
        self.assertIs(daily["autorun"], False)

    def test_existing_daily_template_is_selected(self) -> None:
        template = self.vault / "30 Sistema/Templates/Daily.md"
        template.parent.mkdir(parents=True)
        template.write_text("# Daily\n", encoding="utf-8")

        self._rewrite()

        daily = json.loads(
            (self.vault / ".obsidian/daily-notes.json").read_bytes()
        )
        self.assertEqual(daily["template"], "30 Sistema/Templates/Daily.md")

    def test_second_execution_is_noop_and_preserves_mtimes(self) -> None:
        self._rewrite()
        paths = [self.note_path, *(self.vault / ".obsidian").glob("*.json")]
        mtimes = {path: path.stat().st_mtime_ns for path in paths}
        time.sleep(0.002)

        second = self._rewrite()

        self.assertEqual(second.status, "fresh")
        self.assertEqual(second.files_changed, 0)
        self.assertEqual(
            {path: path.stat().st_mtime_ns for path in paths},
            mtimes,
        )

    def test_partial_or_unexpected_literal_count_fails_before_first_write(self) -> None:
        module = self.require_rewriter()
        for mutation in ("partial", "unexpected"):
            with self.subTest(mutation=mutation):
                with self._fresh_fixture() as fixture:
                    text = fixture.note_path.read_text(encoding="utf-8")
                    if mutation == "partial":
                        text = text.replace(
                            "Vault/Conceitos", "20 Conhecimento/Conceitos", 1
                        )
                    else:
                        text += "Vault/Conceitos/Extra.md\n"
                    fixture.note_path.write_text(text, encoding="utf-8")
                    before = fixture._snapshot()
                    with patch.object(module, "_atomic_write_at", create=True) as atomic_write:
                        with self.assertRaises(module.RewriteError):
                            fixture._rewrite()
                    atomic_write.assert_not_called()
                    self.assertEqual(fixture._snapshot(), before)

    def test_invalid_last_config_blocks_all_writes(self) -> None:
        module = self.require_rewriter()
        daily = self.vault / ".obsidian/daily-notes.json"
        daily.write_text("{invalid\n", encoding="utf-8")
        before = self._snapshot()

        with patch.object(module, "_atomic_write_at", create=True) as atomic_write:
            with self.assertRaises(module.RewriteError):
                self._rewrite()

        atomic_write.assert_not_called()
        self.assertEqual(self._snapshot(), before)

    def test_projected_link_regression_blocks_before_journal_or_write(self) -> None:
        module = self.require_rewriter()
        before = self._snapshot()
        regressed = module.LinkAudit(
            total=1,
            resolved=0,
            unresolved=1,
            ambiguous=0,
        )
        contract = module.LinkContract(
            expected_total=1,
            max_unresolved=0,
            max_ambiguous=0,
        )

        with patch.object(
            module, "audit_projected_links", return_value=regressed
        ), patch.object(module, "_install_journal", create=True) as install:
            with self.assertRaises(module.RewriteError):
                self._rewrite(link_contract=contract)

        install.assert_not_called()
        self.assertEqual(self._snapshot(), before)

    def test_missing_projected_audit_target_blocks_all_files(self) -> None:
        module = self.require_rewriter()
        before = self._snapshot()
        contract = module.LinkContract(
            expected_total=0,
            max_unresolved=0,
            max_ambiguous=0,
        )

        with patch.object(module, "_atomic_write_at", create=True) as atomic_write:
            with self.assertRaises(module.RewriteError):
                self._rewrite(link_contract=contract)

        atomic_write.assert_not_called()
        self.assertEqual(self._snapshot(), before)

    def test_manifest_auth_is_explicit_and_fail_closed_for_custom_fixtures(self) -> None:
        module = self.require_rewriter()
        arguments = dict(
            vault=self.vault,
            manifest_path=Path("state/manifest.json"),
            markdown_specs=self._literal_rules(),
            expected_markdown_occurrences=2,
            link_contract=None,
        )
        with self.assertRaises(module.RewriteError):
            module.rewrite_vault(**arguments)

        bad_contracts = (
            module.ManifestAuth(
                "other/manifest.json", self.auth.sha256, self.auth.record_count
            ),
            module.ManifestAuth(
                self.auth.relative_path, "0" * 64, self.auth.record_count
            ),
            module.ManifestAuth(
                self.auth.relative_path, self.auth.sha256, self.auth.record_count + 1
            ),
        )
        before = self._snapshot()
        for auth in bad_contracts:
            with self.subTest(auth=auth):
                with self.assertRaises(module.RewriteError):
                    module.rewrite_vault(**arguments, manifest_auth=auth)
                self.assertEqual(self._snapshot(), before)

    def test_crash_leaves_durable_journal_and_next_run_recovers(self) -> None:
        module = self.require_rewriter()

        class SimulatedCrash(BaseException):
            pass

        calls = 0
        real_checkpoint = module._checkpoint_journal

        def crash_before_first_checkpoint(*args, **kwargs):
            nonlocal calls
            calls += 1
            if calls == 1:
                raise SimulatedCrash("power loss")
            return real_checkpoint(*args, **kwargs)

        with patch.object(
            module,
            "_checkpoint_journal",
            side_effect=crash_before_first_checkpoint,
        ):
            with self.assertRaises(SimulatedCrash):
                self._rewrite()

        journal = self.vault / ".fgv/path-rewrite-journal.json"
        self.assertTrue(journal.is_file())
        partially_written_app = json.loads(
            (self.vault / ".obsidian/app.json").read_bytes()
        )
        self.assertEqual(
            partially_written_app["attachmentFolderPath"], "30 Sistema/Anexos"
        )

        recovered = self._rewrite()

        self.assertEqual(recovered.status, "updated")
        self.assertFalse(journal.exists())
        self.assertEqual(self.note_path.read_text(encoding="utf-8").count("Vault/Conceitos"), 0)

    def test_recovery_rejects_a_divergent_journal_checkpoint(self) -> None:
        module = self.require_rewriter()

        class SimulatedCrash(BaseException):
            pass

        with patch.object(
            module,
            "_checkpoint_journal",
            side_effect=SimulatedCrash("power loss"),
        ):
            with self.assertRaises(SimulatedCrash):
                self._rewrite()

        journal = self.vault / ".fgv/path-rewrite-journal.json"
        record = json.loads(journal.read_bytes())
        record["completed_writes"] = len(record["operations"])
        journal.write_text(
            json.dumps(record, ensure_ascii=False, indent=2) + "\n",
            encoding="utf-8",
        )
        before = self._snapshot()

        with self.assertRaises(module.RewriteError):
            self._rewrite()

        self.assertEqual(self._snapshot(), before)

    def test_parent_symlink_swap_cannot_redirect_a_write(self) -> None:
        module = self.require_rewriter()
        real_atomic_write = module._atomic_write_at
        with TemporaryDirectory() as external_directory:
            external = Path(external_directory)
            sentinel = external / "app.json"
            sentinel.write_text("external\n", encoding="utf-8")
            detached = self.vault / ".obsidian-detached"
            swapped = False

            def swap_parent_then_write(operation, payload):
                nonlocal swapped
                if not swapped and operation.relative.startswith(".obsidian/"):
                    swapped = True
                    (self.vault / ".obsidian").rename(detached)
                    os.symlink(external, self.vault / ".obsidian")
                return real_atomic_write(operation, payload)

            try:
                with patch.object(
                    module, "_atomic_write_at", side_effect=swap_parent_then_write
                ):
                    with self.assertRaises(module.RewriteError):
                        self._rewrite()
                self.assertEqual(sentinel.read_text(encoding="utf-8"), "external\n")
                app = json.loads((detached / "app.json").read_bytes())
                self.assertEqual(app["attachmentFolderPath"], "Vault/Attachments")
                self.assertFalse(
                    (self.vault / ".fgv/path-rewrite-journal.json").exists()
                )
            finally:
                current = self.vault / ".obsidian"
                if current.is_symlink():
                    current.unlink()
                if detached.exists():
                    detached.rename(current)

    def test_mid_batch_failure_rolls_back_every_applied_file(self) -> None:
        module = self.require_rewriter()
        before = self._snapshot()
        real_atomic_write = module._atomic_write_at
        calls = 0

        def fail_second(operation, payload):
            nonlocal calls
            calls += 1
            if calls == 2:
                raise OSError("injected write failure")
            return real_atomic_write(operation, payload)

        with patch.object(module, "_atomic_write_at", side_effect=fail_second):
            with self.assertRaises(module.RewriteError):
                self._rewrite()

        self.assertEqual(self._snapshot(), before)

    def _fresh_fixture(self):
        return _FixtureContext(self.__class__)


class _FixtureContext:
    def __init__(self, case_class):
        self.case = case_class(methodName="runTest")

    def __enter__(self):
        self.case.setUp()
        return self.case

    def __exit__(self, exc_type, exc, traceback):
        self.case.tearDown()


class ProductionContractTests(unittest.TestCase):
    def require_rewriter(self):
        self.assertIsNotNone(rewrite_paths, "path rewriter is missing")
        return rewrite_paths

    def test_production_allowlist_has_exact_scope_and_counts(self) -> None:
        module = self.require_rewriter()

        self.assertEqual(set(module.MARKDOWN_SPECS), set(module.MARKDOWN_ALLOWLIST))
        self.assertEqual(len(module.MARKDOWN_ALLOWLIST), 9)
        self.assertEqual(len(module.CONFIG_ALLOWLIST), 5)
        self.assertEqual(
            {path: sum(rule.expected_count for rule in rules)
             for path, rules in module.MARKDOWN_SPECS.items()},
            {
                "00 Home/Home.md": 2,
                "10 Matérias/Estatistica2/Aulas/08.17/AulaTestesHipoteseExcelR.md": 2,
                "20 Conhecimento/Conceitos/Caso Marcus Dent.md": 1,
                "20 Conhecimento/Conceitos/Caso Target Canada.md": 1,
                "20 Conhecimento/Conceitos/Caso Zezinho Pipoqueiro.md": 1,
                "30 Sistema/Automacoes/2026-05-25-weekly-summary-plan.md": 11,
                "30 Sistema/Specs/2026-08-19-caso-marcus-dent-design.md": 3,
                "30 Sistema/Specs/2026-08-19-caso-marcus-dent-plan.md": 37,
                "30 Sistema/Tutor/README.md": 1,
            },
        )
        self.assertEqual(module.EXPECTED_MARKDOWN_OCCURRENCES, 59)
        self.assertEqual(module.EXPECTED_CONFIG_OCCURRENCES, 5)
        self.assertEqual(
            module.DEFAULT_MANIFEST_AUTH,
            module.ManifestAuth(
                relative_path="30 Sistema/Estado/migration-manifest.json",
                sha256="3910988998703f6a9cc01dcd4b40173241c602204ce4a4c6bc83a1a67fd29c96",
                record_count=1059,
            ),
        )

    def test_real_tree_is_exactly_stale_or_fresh_and_link_counts_do_not_regress(self) -> None:
        module = self.require_rewriter()
        manifest_path = Path("30 Sistema/Estado/migration-manifest.json")

        report = module.rewrite_vault(ROOT, manifest_path, check=True)
        manifest = json.loads(manifest_path.read_bytes())
        links = module.audit_filesystem_links(ROOT, manifest)

        self.assertIn(report.status, {"stale", "fresh"})
        self.assertEqual(report.occurrences, 64)
        self.assertIn(report.files_changed, {0, 14})
        self.assertEqual(links.total, 5402)
        self.assertLessEqual(links.unresolved, 408)
        self.assertLessEqual(links.ambiguous, 3)

    def test_hidden_superpowers_tooling_is_not_active_catalog_scope(self) -> None:
        module = self.require_rewriter()
        hidden_root = Path(
            "10 Matérias/Estatistica2/Aulas/08.17/.superpowers"
        )
        self.assertFalse(
            module.is_active_catalog_path(
                "10 Matérias/Estatistica2/Aulas/08.17/.superpowers/build/lint_md.py"
            )
        )
        hidden_occurrences = 0
        for path in (ROOT / hidden_root).rglob("*"):
            if not path.is_file():
                continue
            try:
                text = path.read_text(encoding="utf-8")
            except UnicodeDecodeError:
                continue
            hidden_occurrences += len(module.OLD_ACTIVE_PATTERN.findall(text))
        self.assertEqual(hidden_occurrences, 35)
        self.assertEqual(
            module.audit_active_old_literals(
                ROOT,
                Path(module.DEFAULT_MANIFEST_AUTH.relative_path),
                manifest_auth=module.DEFAULT_MANIFEST_AUTH,
            ),
            0,
        )

    def test_inventory_validation_error_is_controlled(self) -> None:
        module = self.require_rewriter()
        from fgv_migration.inventory import InventoryError

        with patch.object(
            module,
            "normalize_relative_path",
            side_effect=InventoryError("invalid path"),
        ):
            with self.assertRaises(module.RewriteError):
                module._safe_relative_path(ROOT, "00 Home/Home.md")

    def test_cli_fails_closed_without_traceback_on_link_regression(self) -> None:
        module = self.require_rewriter()
        regressed = module.LinkAudit(
            total=5402,
            resolved=4990,
            unresolved=409,
            ambiguous=3,
        )
        stderr = io.StringIO()

        with patch.object(
            module, "audit_projected_links", return_value=regressed
        ), patch("sys.stderr", stderr):
            result = module.main(
                [
                    "--vault",
                    str(ROOT),
                    "--manifest",
                    module.DEFAULT_MANIFEST_AUTH.relative_path,
                    "--check",
                ]
            )

        self.assertEqual(result, 1)
        self.assertIn("unresolved links regressed", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())

    def test_manifest_inventory_error_is_a_controlled_cli_failure(self) -> None:
        module = self.require_rewriter()
        from fgv_migration.inventory import InventoryError

        stderr = io.StringIO()
        with patch.object(
            module,
            "validate_manifest",
            side_effect=InventoryError("invalid manifest destination"),
        ), patch("sys.stderr", stderr):
            result = module.main(
                [
                    "--vault",
                    str(ROOT),
                    "--manifest",
                    module.DEFAULT_MANIFEST_AUTH.relative_path,
                    "--check",
                ]
            )

        self.assertEqual(result, 1)
        self.assertIn("invalid migration manifest", stderr.getvalue())
        self.assertNotIn("Traceback", stderr.getvalue())


if __name__ == "__main__":
    unittest.main()
