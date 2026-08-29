from __future__ import annotations

import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile
import unittest


ROOT = Path(__file__).resolve().parents[2]
HERMES_DIR = ROOT / "30 Sistema/Hermes"
SCRIPTS = ROOT / ".fgv/scripts"
FIXTURES = ROOT / ".fgv/tests/fixtures"
OLD_HOME = FIXTURES / "hermes-home"
MIGRATED_HOME = FIXTURES / "hermes-home-migrated"
RETRIEVAL_VAULT = FIXTURES / "hermes-retrieval-vault"
TEST_COMMIT = "1" * 40


def run_python(script: str, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(SCRIPTS / script), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        check=False,
    )


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        if path.is_file() and not path.is_symlink():
            digest.update(path.relative_to(root).as_posix().encode())
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


class HermesPackageContractTests(unittest.TestCase):
    def setUp(self) -> None:
        self.contract = (HERMES_DIR / "HERMES-CONTRACT.md").read_text(encoding="utf-8")
        self.manifest = json.loads(
            (HERMES_DIR / "hermes-manifest.json").read_text(encoding="utf-8")
        )

    def test_catalog_and_snapshot_precede_exact_artifact(self) -> None:
        self.assertEqual(
            self.manifest["retrieval_order"],
            [
                "30 Sistema/Estado/catalog.jsonl",
                "30 Sistema/Estado/dashboard-snapshot.md",
                "exact_catalog_path",
            ],
        )
        self.assertIn("catalog-first", self.contract)
        self.assertIn("um único arquivo exato", self.contract)

    def test_canonical_paths_and_response_provenance_are_mandatory(self) -> None:
        self.assertEqual(
            self.manifest["canonical_paths"]["subjects_root"], "10 Matérias/"
        )
        self.assertEqual(self.manifest["canonical_paths"]["tasks"], "00 Home/Tasks.md")
        self.assertEqual(self.manifest["canonical_paths"]["state_root"], "30 Sistema/Estado/")
        self.assertEqual(
            self.manifest["required_response_fields"], ["as_of_commit", "sync_state"]
        )

    def test_fgv_sync_is_the_only_vps_git_owner(self) -> None:
        self.assertEqual(self.manifest["vps_git_owner"], "fgv-sync")
        self.assertIn("único owner", self.contract)

    def test_audited_components_are_closed_and_complete(self) -> None:
        ids = {component["id"] for component in self.manifest["components"]}
        self.assertEqual(
            ids,
            {
                "eclass-scan.py",
                "eclass",
                "fgv-eclass-api",
                "fgv-briefing",
                "academic-reading-notes",
                "memory",
                "cronjobs",
            },
        )
        self.assertTrue(all(c["classification"] == "required" for c in self.manifest["components"]))


class HermesAuditTests(unittest.TestCase):
    def audit(self, home: Path, output: Path) -> subprocess.CompletedProcess[str]:
        return run_python(
            "audit_hermes.py",
            "--hermes-home",
            str(home),
            "--vault",
            "/root/vault",
            "--manifest",
            str(HERMES_DIR / "hermes-manifest.json"),
            "--json-out",
            str(output),
        )

    def test_detects_legacy_paths_git_and_material_folder_without_mutation(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / ".hermes"
            shutil.copytree(OLD_HOME, home)
            before = tree_digest(home)
            output = Path(tmp) / "audit.json"
            result = self.audit(home, output)
            self.assertEqual(result.returncode, 2, result.stderr)
            self.assertEqual(tree_digest(home), before)
            report = json.loads(output.read_text(encoding="utf-8"))
            self.assertEqual(report["status"], "blocked")
            rules = {finding["rule"] for finding in report["findings"]}
            self.assertTrue({"legacy_path", "unauthorized_git", "legacy_materials"} <= rules)
            self.assertNotIn("secret-value", output.read_text(encoding="utf-8"))

    def test_output_is_byte_deterministic_and_sorted(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            first = Path(tmp) / "first.json"
            second = Path(tmp) / "second.json"
            self.audit(OLD_HOME, first)
            self.audit(OLD_HOME, second)
            self.assertEqual(first.read_bytes(), second.read_bytes())
            report = json.loads(first.read_text(encoding="utf-8"))
            keys = [(item["file"], item["line"], item["rule"]) for item in report["findings"]]
            self.assertEqual(keys, sorted(keys))

    def test_refuses_symlink_escape(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / ".hermes"
            shutil.copytree(MIGRATED_HOME, home)
            target = home / "scripts/eclass-scan.py"
            target.unlink()
            target.symlink_to("/etc/hosts")
            result = self.audit(home, Path(tmp) / "audit.json")
            self.assertEqual(result.returncode, 2)
            report = json.loads((Path(tmp) / "audit.json").read_text(encoding="utf-8"))
            self.assertIn("unsafe_path", {f["rule"] for f in report["findings"]})

    def test_detects_tilde_relative_roots_and_git_with_directory_option(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / ".hermes"
            shutil.copytree(MIGRATED_HOME, home)
            target = home / "skills/productivity/fgv-briefing/SKILL.md"
            target.write_text(
                "Leia ~/FGV/Psicologia/Aulas/ e Psicologia/Aulas/.\n"
                "Rode git -C /root/vault pull.\n",
                encoding="utf-8",
            )
            output = Path(tmp) / "audit.json"
            result = self.audit(home, output)
            self.assertEqual(result.returncode, 2)
            rules = {finding["rule"] for finding in json.loads(output.read_text(encoding="utf-8"))["findings"]}
            self.assertTrue({"legacy_path", "unauthorized_git"} <= rules)


class HermesCutoverValidationTests(unittest.TestCase):
    def validate(self, home: Path) -> subprocess.CompletedProcess[str]:
        return run_python(
            "validate_hermes_cutover.py",
            "--hermes-home",
            str(home),
            "--vault",
            "/root/vault-plan-b-test",
            "--manifest",
            str(HERMES_DIR / "hermes-manifest.json"),
        )

    def test_old_fixture_is_blocked_and_migrated_fixture_is_ready(self) -> None:
        self.assertNotEqual(self.validate(OLD_HOME).returncode, 0)
        migrated = self.validate(MIGRATED_HOME)
        self.assertEqual(migrated.returncode, 0, migrated.stdout + migrated.stderr)
        self.assertEqual(json.loads(migrated.stdout)["status"], "ready")

    def test_missing_required_component_is_blocked(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / ".hermes"
            shutil.copytree(MIGRATED_HOME, home)
            (home / "cron/jobs.json").unlink()
            result = self.validate(home)
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("missing_component", result.stdout)


class HermesSyncTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.remote = self.base / "origin.git"
        subprocess.run(["git", "init", "--bare", str(self.remote)], check=True, capture_output=True)
        seed = self.base / "seed"
        subprocess.run(["git", "clone", str(self.remote), str(seed)], check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=seed, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=seed, check=True)
        (seed / "note.md").write_text("one\n", encoding="utf-8")
        subprocess.run(["git", "add", "note.md"], cwd=seed, check=True)
        subprocess.run(["git", "commit", "-m", "seed"], cwd=seed, check=True, capture_output=True)
        subprocess.run(["git", "push", "-u", "origin", "HEAD"], cwd=seed, check=True, capture_output=True)
        self.vault = self.base / "vault"
        subprocess.run(["git", "clone", str(self.remote), str(self.vault)], check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=self.vault, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=self.vault, check=True)
        self.lock = self.base / "sync.lock"

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def sync(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env.update(FGV_VAULT_ROOT=str(self.vault), FGV_SYNC_LOCK=str(self.lock))
        return subprocess.run(
            [str(HERMES_DIR / "fgv-sync"), *args],
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def test_status_reports_commit_sync_and_dirty_state(self) -> None:
        report = json.loads(self.sync("status").stdout)
        self.assertRegex(report["as_of_commit"], r"^[0-9a-f]{40}$")
        self.assertEqual(report["sync_state"], "clean")
        self.assertFalse(report["dirty"])

    def test_dirty_refresh_fails_without_modifying_files(self) -> None:
        target = self.vault / "note.md"
        target.write_text("dirty\n", encoding="utf-8")
        before = target.read_bytes()
        result = self.sync("refresh")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(target.read_bytes(), before)
        self.assertEqual(json.loads(result.stdout)["reason"], "working_tree_not_clean")

    def test_existing_lock_blocks_second_writer(self) -> None:
        self.lock.mkdir()
        result = self.sync("refresh")
        self.assertEqual(result.returncode, 75)
        self.assertEqual(json.loads(result.stdout)["reason"], "lock_busy")

    def test_refresh_accepts_only_remote_fast_forward(self) -> None:
        writer = self.base / "writer"
        subprocess.run(["git", "clone", str(self.remote), str(writer)], check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=writer, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=writer, check=True)
        (writer / "remote.md").write_text("remote\n", encoding="utf-8")
        subprocess.run(["git", "add", "remote.md"], cwd=writer, check=True)
        subprocess.run(["git", "commit", "-m", "remote update"], cwd=writer, check=True, capture_output=True)
        subprocess.run(["git", "push"], cwd=writer, check=True, capture_output=True)

        result = self.sync("refresh")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual((self.vault / "remote.md").read_text(encoding="utf-8"), "remote\n")
        self.assertEqual(json.loads(result.stdout)["sync_state"], "clean")

    def test_refresh_blocks_divergence_without_changing_head(self) -> None:
        writer = self.base / "writer"
        subprocess.run(["git", "clone", str(self.remote), str(writer)], check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=writer, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=writer, check=True)
        (self.vault / "local.md").write_text("local\n", encoding="utf-8")
        subprocess.run(["git", "add", "local.md"], cwd=self.vault, check=True)
        subprocess.run(["git", "commit", "-m", "local update"], cwd=self.vault, check=True, capture_output=True)
        before = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.vault, text=True, capture_output=True, check=True).stdout.strip()
        (writer / "remote.md").write_text("remote\n", encoding="utf-8")
        subprocess.run(["git", "add", "remote.md"], cwd=writer, check=True)
        subprocess.run(["git", "commit", "-m", "remote update"], cwd=writer, check=True, capture_output=True)
        subprocess.run(["git", "push"], cwd=writer, check=True, capture_output=True)

        result = self.sync("refresh")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["reason"], "branch_diverged_or_ahead")
        after = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.vault, text=True, capture_output=True, check=True).stdout.strip()
        self.assertEqual(after, before)
        self.assertFalse((self.vault / "remote.md").exists())

    def test_publish_commits_only_explicit_clean_scope(self) -> None:
        (self.vault / "note.md").write_text("two\n", encoding="utf-8")
        result = self.sync("publish", "--message", "update note", "--path", "note.md")
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        changed = subprocess.run(
            ["git", "show", "--pretty=format:", "--name-only", "HEAD"],
            cwd=self.vault,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.splitlines()
        self.assertEqual(changed, ["note.md"])

    def test_publish_rejects_unrelated_changes(self) -> None:
        (self.vault / "note.md").write_text("two\n", encoding="utf-8")
        (self.vault / "other.md").write_text("other\n", encoding="utf-8")
        result = self.sync("publish", "--message", "update note", "--path", "note.md")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["reason"], "changes_outside_scope")

    def test_publish_rebuilds_state_and_requires_generated_output_in_scope(self) -> None:
        script = self.vault / ".fgv/scripts/generate_state.py"
        script.parent.mkdir(parents=True)
        state = self.vault / "30 Sistema/Estado/catalog.fixture"
        state.parent.mkdir(parents=True)
        state.write_text("initial\n", encoding="utf-8")
        script.write_text(
            "from pathlib import Path\n"
            "import sys\n"
            "root = Path(sys.argv[sys.argv.index('--vault') + 1])\n"
            "target = root / '30 Sistema/Estado/catalog.fixture'\n"
            "if '--check' in sys.argv:\n"
            "    raise SystemExit(0 if target.read_text() == 'rebuilt\\n' else 2)\n"
            "target.write_text('rebuilt\\n')\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", ".fgv/scripts/generate_state.py", "30 Sistema/Estado/catalog.fixture"], cwd=self.vault, check=True)
        subprocess.run(["git", "commit", "-m", "add state fixture"], cwd=self.vault, check=True, capture_output=True)
        subprocess.run(["git", "push"], cwd=self.vault, check=True, capture_output=True)
        (self.vault / "note.md").write_text("two\n", encoding="utf-8")

        blocked = self.sync("publish", "--message", "update note", "--path", "note.md")
        self.assertNotEqual(blocked.returncode, 0)
        self.assertEqual(json.loads(blocked.stdout)["reason"], "changes_outside_scope")
        self.assertEqual(state.read_text(encoding="utf-8"), "rebuilt\n")

        result = self.sync(
            "publish", "--message", "update note and state",
            "--path", "note.md",
            "--path", "30 Sistema/Estado/catalog.fixture",
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        changed = subprocess.run(
            ["git", "show", "--pretty=format:", "--name-only", "HEAD"], cwd=self.vault,
            text=True, capture_output=True, check=True,
        ).stdout.splitlines()
        self.assertEqual(changed, ["30 Sistema/Estado/catalog.fixture", "note.md"])

    def test_script_contains_no_destructive_git_primitive(self) -> None:
        script = (HERMES_DIR / "fgv-sync").read_text(encoding="utf-8")
        for forbidden in ("reset --hard", "clean -f", "push --force", "force-with-lease"):
            self.assertNotIn(forbidden, script)


class HermesReadinessTests(unittest.TestCase):
    def manifest_hash(self) -> str:
        return hashlib.sha256(
            (HERMES_DIR / "hermes-manifest.json").read_bytes()
        ).hexdigest()

    def valid_report(self) -> dict[str, object]:
        return {
            "schema_version": 1,
            "timestamp_utc": "2026-08-28T12:00:00Z",
            "host_role": "hermes-vps",
            "recommendation": "READY",
            "production_commit": "0" * 40,
            "tested_commit": TEST_COMMIT,
            "package_manifest_sha256": self.manifest_hash(),
            "backup": {"path": "/root/backups/fgv-hermes-20260828", "sha256": "2" * 64},
            "untracked": {"inventory_sha256": "3" * 64, "backup_sha256": "4" * 64, "preserved": True, "classified": True},
            "findings": {"required_remaining": 0, "warnings": 0},
            "component_results": {name: "pass" for name in (
                "eclass-scan.py", "eclass", "fgv-eclass-api", "fgv-briefing",
                "academic-reading-notes", "memory", "cronjobs"
            )},
            "smoke_tests": {"academic_retrieval": "pass", "eclass": "pass", "whatsapp": "pass"},
            "retrieval_fixture_mode": False,
            "retrieval_sync_state": "clean",
            "query_timings": [{"id": "latest_class", "duration_ms": 4}],
            "context_tokens": 1200,
            "diff_summary": ["staged configuration only"],
        }

    def validate(self, payload: dict[str, object]) -> subprocess.CompletedProcess[str]:
        with tempfile.NamedTemporaryFile("w", encoding="utf-8", suffix=".json", delete=False) as handle:
            json.dump(payload, handle)
            path = handle.name
        try:
            return run_python(
                "validate_hermes_readiness.py",
                "--report", path,
                "--tested-commit", TEST_COMMIT,
                "--manifest", str(HERMES_DIR / "hermes-manifest.json"),
            )
        finally:
            Path(path).unlink()

    def test_ready_exact_sha_and_checksums_pass(self) -> None:
        result = self.validate(self.valid_report())
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "ready")

    def test_non_ready_mismatched_commit_or_manifest_is_blocked(self) -> None:
        mutations = (
            ("recommendation", "BLOCKED"),
            ("tested_commit", "4" * 40),
            ("package_manifest_sha256", "5" * 64),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                report = self.valid_report()
                report[field] = value
                self.assertNotEqual(self.validate(report).returncode, 0)

    def test_fixture_mode_or_stale_retrieval_is_blocked(self) -> None:
        for field, value in (("retrieval_fixture_mode", True), ("retrieval_sync_state", "stale")):
            with self.subTest(field=field):
                report = self.valid_report()
                report[field] = value
                self.assertNotEqual(self.validate(report).returncode, 0)


class HermesPromptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.prepare = (HERMES_DIR / "PROMPT-HERMES-PREPARAR.md").read_text(encoding="utf-8")
        self.cutover = (HERMES_DIR / "PROMPT-HERMES-CUTOVER.md").read_text(encoding="utf-8")
        self.template = (HERMES_DIR / "READINESS-REPORT-TEMPLATE.md").read_text(encoding="utf-8")

    def test_prepare_is_staging_only_and_evidence_complete(self) -> None:
        for marker in (
            "não altere produção", "SHA-256", "untracked", "clone separado", "cópia",
            "audit_hermes.py", "Eclass", "WhatsApp", "busca acadêmica", "READY", "BLOCKED"
        ):
            self.assertIn(marker, self.prepare)

    def test_cutover_is_blocked_without_ready_exact_commit(self) -> None:
        for marker in (
            "validate_hermes_readiness.py", "tested_commit", "READY", "working tree",
            "fgv-sync", "smoke", "rollback", "cron", "nunca use force push"
        ):
            self.assertIn(marker, self.cutover)
        self.assertLess(self.cutover.index("validate_hermes_readiness.py"), self.cutover.index("Primeira mutação"))

    def test_report_template_has_required_evidence(self) -> None:
        for marker in (
            "timestamp_utc", "production_commit", "tested_commit", "backup", "untracked",
            "component_results", "query_timings", "context_tokens", "recommendation"
        ):
            self.assertIn(marker, self.template)


class HermesBundleTests(unittest.TestCase):
    def verify(self, root: Path, bundle: str) -> subprocess.CompletedProcess[str]:
        return run_python(
            "verify_hermes_bundle.py",
            "--root", str(root),
            "--bundle", bundle,
        )

    def test_prepare_and_cutover_bundles_have_valid_checksums(self) -> None:
        for name in ("PREPARAR-BUNDLE.json", "CUTOVER-BUNDLE.json"):
            with self.subTest(name=name):
                result = self.verify(ROOT, f"30 Sistema/Hermes/{name}")
                self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
                self.assertEqual(json.loads(result.stdout)["status"], "pass")

    def test_tampered_bundle_file_is_blocked(self) -> None:
        bundle_relative = Path("30 Sistema/Hermes/PREPARAR-BUNDLE.json")
        source_manifest = ROOT / bundle_relative
        manifest = json.loads(source_manifest.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as tmp:
            target_root = Path(tmp)
            for record in manifest["files"]:
                source = ROOT / record["path"]
                target = target_root / record["path"]
                target.parent.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(source, target)
            target_manifest = target_root / bundle_relative
            target_manifest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source_manifest, target_manifest)
            first = target_root / manifest["files"][0]["path"]
            first.write_bytes(first.read_bytes() + b"tampered\n")
            result = self.verify(target_root, bundle_relative.as_posix())
            self.assertNotEqual(result.returncode, 0)
            self.assertEqual(json.loads(result.stdout)["status"], "blocked")


class HermesRetrievalSmokeTests(unittest.TestCase):
    def test_queries_are_catalog_first_exact_and_provenanced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            shutil.copytree(RETRIEVAL_VAULT, vault)
            subprocess.run(["git", "init"], cwd=vault, check=True, capture_output=True)
            subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=vault, check=True)
            subprocess.run(["git", "config", "user.name", "Fixture"], cwd=vault, check=True)
            subprocess.run(["git", "add", "."], cwd=vault, check=True)
            subprocess.run(["git", "commit", "-m", "fixture"], cwd=vault, check=True, capture_output=True)
            actual_commit = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=vault, text=True, capture_output=True, check=True
            ).stdout.strip()
            result = run_python(
                "hermes_retrieval_smoke.py",
                "--vault", str(vault),
                "--queries", str(FIXTURES / "retrieval-queries.json"),
                "--expected-commit", TEST_COMMIT,
                "--fixture-mode",
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["status"], "pass")
            self.assertEqual(report["as_of_commit"], actual_commit)
            self.assertTrue(report["stale"])
            self.assertEqual(report["state_check"], "pass")
            self.assertTrue(report["fixture_mode"])
            for query in report["queries"]:
                self.assertEqual(query["steps"][:2], ["catalog", "dashboard_snapshot"])
                self.assertLessEqual(len(query["opened_files"]), 1)
                self.assertNotIn("filesystem_scan", query["steps"])
                self.assertTrue(query["matched"])


if __name__ == "__main__":
    unittest.main()
