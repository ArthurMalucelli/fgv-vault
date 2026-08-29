from __future__ import annotations

import ast
from contextlib import redirect_stdout
import hashlib
import io
import json
import os
from datetime import date, datetime, timedelta, timezone
from pathlib import Path
import shutil
import shlex
import subprocess
import tempfile
import unittest
from unittest import mock
from zoneinfo import ZoneInfo

import hermes_channel_smoke
from hermes_catalog_query import query_catalog, select_records
from hermes_channel_smoke import audit_channel_entrypoint
from hermes_common import HermesError


ROOT = Path(__file__).resolve().parents[2]
HERMES_DIR = ROOT / "30 Sistema/Hermes"
SCRIPTS = ROOT / ".fgv/scripts"
FIXTURES = ROOT / ".fgv/tests/fixtures"
OLD_HOME = FIXTURES / "hermes-home"
MIGRATED_HOME = FIXTURES / "hermes-home-migrated"
RETRIEVAL_VAULT = FIXTURES / "hermes-retrieval-vault"
TEST_COMMIT = "1" * 40
EXPECTED_UPSTREAM = "origin/codex/vault-plan-b"
EXPECTED_BRANCH = "codex/vault-plan-b"
EXPECTED_FETCH_REFSPEC = "+refs/heads/codex/vault-plan-b:refs/remotes/origin/codex/vault-plan-b"
EXPECTED_REMOTE_URL = "https://github.com/ArthurMalucelli/fgv-vault.git"
OPERATIONAL_TIMEZONE = "America/Sao_Paulo"
LIVE_QUERY_EXPECTED = {
    "ultima-aula-matematica": "10 Matérias/MatemáticaAplicada/Aulas/08.20/Resumo - Introdução a derivadas.md",
    "transcrito-matematica": "10 Matérias/MatemáticaAplicada/Aulas/08.20/Transcrito - Introdução a derivadas.md",
    "proxima-avaliacao": "00 Home/Tasks.md",
    "material-eclass": "10 Matérias/Estatistica2/Aulas/08.18/Material/Exercicios_Aula05.docx",
    "conceito-gap": "20 Conhecimento/Conceitos/Dividend Yield.md",
    "compat-resumo": "10 Matérias/MatemáticaAplicada/Aulas/08.20/Resumo - Introdução a derivadas.md",
}
LIVE_QUERY_STEPS = [
    "dashboard_snapshot", "catalog_query", "dashboard_snapshot_recheck", "checkout_status", "select_exact_path",
    "verify_sha256", "open_exact_file",
]
MAX_CATALOG_QUERY_BYTES = 16_384
MAX_CATALOG_QUERY_LINES = 1
MAX_CATALOG_CANDIDATES = 5


def run_python(
    script: str, *args: str, env: dict[str, str] | None = None
) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["python3", str(SCRIPTS / script), *args],
        cwd=ROOT,
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )


def tree_digest(root: Path) -> str:
    digest = hashlib.sha256()
    for path in sorted(root.rglob("*")):
        relative = path.relative_to(root)
        if ".git" in relative.parts:
            continue
        if path.is_file() and not path.is_symlink():
            digest.update(relative.as_posix().encode())
            digest.update(b"\0")
            digest.update(path.read_bytes())
            digest.update(b"\0")
    return digest.hexdigest()


def current_operational_as_of() -> str:
    return datetime.now(ZoneInfo(OPERATIONAL_TIMEZONE)).date().isoformat()


def install_git_transport_wrapper(directory: Path) -> Path:
    real_git = shutil.which("git")
    if real_git is None:
        raise RuntimeError("git is required")
    directory.mkdir(parents=True)
    wrapper = directory / "git"
    wrapper.write_text(
        "#!/usr/bin/env bash\n"
        "set -eu\n"
        "if [ \"$#\" -eq 4 ] && [ \"$1\" = fetch ] && [ \"$2\" = --prune ] && [ \"$3\" = origin ]; then\n"
        f"  exec {shlex.quote(real_git)} fetch --prune \"$FGV_TEST_REMOTE_PATH\" \"$4\"\n"
        "fi\n"
        "if [ \"$#\" -eq 6 ] && [ \"$1\" = -C ] && [ \"$3\" = ls-remote ] && [ \"$4\" = --exit-code ] && [ \"$5\" = origin ]; then\n"
        f"  exec {shlex.quote(real_git)} -C \"$2\" ls-remote --exit-code \"$FGV_TEST_REMOTE_PATH\" \"$6\"\n"
        "fi\n"
        "if [ \"$#\" -ge 2 ] && [ \"$1\" = push ] && [ \"$2\" = origin ]; then\n"
        "  shift 2\n"
        f"  exec {shlex.quote(real_git)} push \"$FGV_TEST_REMOTE_PATH\" \"$@\"\n"
        "fi\n"
        f"exec {shlex.quote(real_git)} \"$@\"\n",
        encoding="utf-8",
    )
    wrapper.chmod(0o755)
    return directory


def configure_canonical_fetch_binding(repository: Path) -> None:
    subprocess.run(
        ["git", "config", f"branch.{EXPECTED_BRANCH}.remote", "origin"],
        cwd=repository,
        check=True,
    )
    subprocess.run(
        ["git", "config", f"branch.{EXPECTED_BRANCH}.merge", f"refs/heads/{EXPECTED_BRANCH}"],
        cwd=repository,
        check=True,
    )
    subprocess.run(
        ["git", "config", "--unset-all", "remote.origin.fetch"],
        cwd=repository,
        check=False,
    )
    subprocess.run(
        ["git", "config", "--add", "remote.origin.fetch", EXPECTED_FETCH_REFSPEC],
        cwd=repository,
        check=True,
    )


def set_fixture_as_of(vault: Path, as_of: str) -> None:
    catalog = vault / "30 Sistema/Estado/catalog.jsonl"
    lines = catalog.read_text(encoding="utf-8").splitlines()
    manifest = json.loads(lines[0])
    manifest["as_of"] = as_of
    lines[0] = json.dumps(manifest, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
    catalog_payload = ("\n".join(lines) + "\n").encode("utf-8")
    catalog.write_bytes(catalog_payload)
    snapshot = vault / "30 Sistema/Estado/dashboard-snapshot.md"
    snapshot_lines = snapshot.read_text(encoding="utf-8").splitlines()
    for index, line in enumerate(snapshot_lines):
        if line.startswith("as_of:"):
            snapshot_lines[index] = f"as_of: {as_of}"
        if line.startswith("catalog_sha256:"):
            snapshot_lines[index] = f'catalog_sha256: "sha256:{hashlib.sha256(catalog_payload).hexdigest()}"'
    snapshot.write_text("\n".join(snapshot_lines) + "\n", encoding="utf-8")


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
                "30 Sistema/Estado/dashboard-snapshot.md",
                ".fgv/scripts/hermes_catalog_query.py",
                "dashboard_snapshot_recheck",
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
            self.manifest["canonical_paths"]["catalog_query"],
            ".fgv/scripts/hermes_catalog_query.py",
        )
        self.assertEqual(
            self.manifest["canonical_paths"]["channel_smoke"],
            ".fgv/scripts/hermes_channel_smoke.py",
        )
        self.assertEqual(self.manifest["canonical_paths"]["materials_segment"], "Material/")
        self.assertEqual(
            self.manifest["required_response_fields"], ["as_of_commit", "sync_state"]
        )

    def test_fgv_sync_is_the_only_vps_git_owner(self) -> None:
        self.assertEqual(self.manifest["vps_git_owner"], "fgv-sync")
        self.assertIn("único owner", self.contract)

    def test_operational_timezone_and_upstream_are_canonical(self) -> None:
        self.assertEqual(self.manifest["operational_timezone"], OPERATIONAL_TIMEZONE)
        self.assertEqual(self.manifest["expected_branch"], EXPECTED_BRANCH)
        self.assertEqual(self.manifest["expected_upstream"], EXPECTED_UPSTREAM)
        self.assertEqual(self.manifest["expected_fetch_refspec"], EXPECTED_FETCH_REFSPEC)
        self.assertEqual(self.manifest["expected_remote_url"], EXPECTED_REMOTE_URL)
        self.assertIn(OPERATIONAL_TIMEZONE, self.contract)
        self.assertIn(EXPECTED_BRANCH, self.contract)
        self.assertIn(EXPECTED_UPSTREAM, self.contract)
        self.assertIn(EXPECTED_FETCH_REFSPEC, self.contract)
        self.assertIn(EXPECTED_REMOTE_URL, self.contract)

    def test_audited_components_are_closed_and_complete(self) -> None:
        ids = {component["id"] for component in self.manifest["components"]}
        self.assertEqual(
            ids,
            {
                "eclass-scan.py",
                "whatsapp-fgv.py",
                "eclass",
                "fgv-eclass-api",
                "fgv-briefing",
                "academic-reading-notes",
                "memory",
                "cronjobs",
            },
        )
        self.assertTrue(all(c["classification"] == "required" for c in self.manifest["components"]))
        self.assertEqual(
            {component["format"] for component in self.manifest["components"]},
            {"python", "markdown", "cron_json"},
        )

    def test_components_use_bounded_catalog_query_not_full_catalog_context(self) -> None:
        query_marked = 0
        for component in self.manifest["components"]:
            if component["id"] == "cronjobs":
                continue
            payload = (MIGRATED_HOME / component["path"]).read_text(encoding="utf-8")
            self.assertIn("hermes_catalog_query.py", payload, component["id"])
            self.assertNotIn("carregue o catálogo completo", payload.lower())
            query_marked += 1
        self.assertEqual(query_marked, 7)

    def test_live_query_expectations_match_current_catalog(self) -> None:
        queries = json.loads(
            (HERMES_DIR / "retrieval-queries.json").read_text(encoding="utf-8")
        )
        catalog_sha256 = hashlib.sha256(
            (ROOT / "30 Sistema/Estado/catalog.jsonl").read_bytes()
        ).hexdigest()
        for query in queries:
            with self.subTest(query=query["id"]):
                result, _ = query_catalog(
                    ROOT,
                    query["query_type"],
                    query.get("subject_id"),
                    MAX_CATALOG_CANDIDATES,
                    catalog_sha256,
                )
                self.assertTrue(result["candidates"])
                self.assertEqual(
                    result["candidates"][0]["path"],
                    query["expected_path"],
                )

    def test_eclass_material_prefers_primary_document_over_code_on_same_date(self) -> None:
        prefix = "10 Matérias/Estatistica2/Aulas/08.18/Material/"
        records = [
            {
                "date": "2026-08-18",
                "path": prefix + "Script_Aula05.R",
                "record_type": "file",
                "subject_ids": ["estatistica-2"],
            },
            {
                "date": "2026-08-18",
                "path": prefix + "Exercicios_Aula05.docx",
                "record_type": "file",
                "subject_ids": ["estatistica-2"],
            },
        ]

        selected = select_records(records, "eclass_material", "estatistica-2")

        self.assertEqual(selected[0]["path"], prefix + "Exercicios_Aula05.docx")

    def test_eclass_material_prefers_extracted_markdown_and_deduplicates_pdf(self) -> None:
        prefix = "10 Matérias/Estatistica2/Aulas/08.18/Material/"
        records = [
            {
                "date": "2026-08-19",
                "path": prefix + "Slides_Aula05.pdf",
                "record_type": "file",
                "subject_ids": ["estatistica-2"],
            },
            {
                "date": "2026-08-20",
                "path": prefix + "Slides_Aula05.extracted.md",
                "record_type": "file",
                "subject_ids": ["estatistica-2"],
            },
            {
                "date": "2026-08-18",
                "path": prefix + "Slides_Aula05.pdf.extracted.md",
                "record_type": "file",
                "subject_ids": ["estatistica-2"],
            },
            {
                "date": "2026-08-18",
                "path": prefix + "Script_Aula05.R",
                "record_type": "file",
                "subject_ids": ["estatistica-2"],
            },
        ]

        selected = select_records(records, "eclass_material", "estatistica-2")
        selected_paths = [record["path"] for record in selected]

        self.assertEqual(selected_paths[0], prefix + "Slides_Aula05.extracted.md")
        self.assertNotIn(prefix + "Slides_Aula05.pdf", selected_paths)
        self.assertNotIn(prefix + "Slides_Aula05.pdf.extracted.md", selected_paths)
        self.assertEqual(selected_paths[1], prefix + "Script_Aula05.R")


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
            self.assertTrue({"legacy_path", "unauthorized_git", "legacy_materials", "destructive_command"} <= rules)
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

    def test_format_aware_audit_ignores_comments_and_blocks_executable_commands(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / ".hermes"
            shutil.copytree(MIGRATED_HOME, home)
            python_component = home / "scripts/eclass-scan.py"
            python_component.write_text(
                "import os\n"
                "import subprocess as sp\n"
                "from os import system as shell\n"
                "# git pull and rm -rf /root/vault are comments\n"
                "sp.run(['/usr/bin/git', '-C', '/root/vault', 'pull'])\n"
                "shell('/bin/rm -rf /root/.hermes')\n",
                encoding="utf-8",
            )
            markdown = home / "skills/productivity/eclass/SKILL.md"
            markdown.write_text(
                "# Commands\n\n```bash\nenv X=1 git pull\nfgv-sync status\n/usr/local/bin/fgv-sync status\n/bin/rm -rf /root/vault\n```\n",
                encoding="utf-8",
            )
            cron = home / "cron/jobs.json"
            cron.write_text(
                json.dumps({"jobs": [{"name": "bad", "command": "sh -c '/usr/bin/git reset --hard'"}]}),
                encoding="utf-8",
            )
            output = Path(tmp) / "audit.json"
            result = self.audit(home, output)
            self.assertEqual(result.returncode, 2)
            findings = json.loads(output.read_text(encoding="utf-8"))["findings"]
            rules = [finding["rule"] for finding in findings]
            self.assertGreaterEqual(rules.count("unauthorized_git"), 3)
            self.assertGreaterEqual(rules.count("destructive_command"), 2)
            self.assertIn("nonliteral_sync", rules)
            self.assertFalse(
                any(
                    finding["line"] == 4
                    and finding["file"] == "scripts/eclass-scan.py"
                    and finding["rule"] in {"unauthorized_git", "destructive_command"}
                    for finding in findings
                )
            )

    def test_audit_blocks_nested_assignment_cron_python_and_pathlib_bypasses(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / ".hermes"
            shutil.copytree(MIGRATED_HOME, home)
            python_component = home / "scripts/eclass-scan.py"
            python_component.write_text(
                "import subprocess\n"
                "from pathlib import Path\n"
                "runner = subprocess.run\n"
                "def nested():\n"
                "    from subprocess import run as nested_runner\n"
                "    nested_runner(['git', 'reset', '--hard'])\n"
                "runner(['/usr/bin/git', 'clean', '-fd'])\n"
                "Path('/root/vault').unlink()\n",
                encoding="utf-8",
            )
            cron = home / "cron/jobs.json"
            cron.write_text(
                json.dumps({
                    "jobs": [{
                        "name": "python-bypass",
                        "command": "python3 -c 'import os; os.system(\"git reset --hard\")'",
                    }]
                }),
                encoding="utf-8",
            )
            output = Path(tmp) / "audit.json"
            result = self.audit(home, output)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            findings = json.loads(output.read_text(encoding="utf-8"))["findings"]
            rules = [finding["rule"] for finding in findings]
            self.assertGreaterEqual(rules.count("unauthorized_git"), 3)
            self.assertGreaterEqual(rules.count("destructive_command"), 4)

    def test_audit_fails_closed_on_dynamic_process_and_path_callables(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / ".hermes"
            shutil.copytree(MIGRATED_HOME, home)
            target = home / "scripts/eclass-scan.py"
            target.write_text(
                "import os\n"
                "import subprocess\n"
                "from pathlib import Path\n"
                "process = getattr(subprocess, os.environ['PROCESS_METHOD'])\n"
                "shell = getattr(os, os.environ['OS_METHOD'])\n"
                "deleter = getattr(Path('/root/vault'), os.environ['PATH_METHOD'])\n"
                "process(['fgv-sync', 'status'])\n"
                "shell('fgv-sync status')\n"
                "deleter()\n",
                encoding="utf-8",
            )
            output = Path(tmp) / "audit.json"
            result = self.audit(home, output)
            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            rules = [
                finding["rule"]
                for finding in json.loads(output.read_text(encoding="utf-8"))["findings"]
            ]
            self.assertGreaterEqual(rules.count("dynamic_command"), 2)
            self.assertIn("dynamic_destructive_path", rules)

    def test_bounded_query_marker_cannot_hide_direct_catalog_access(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / ".hermes"
            shutil.copytree(MIGRATED_HOME, home)
            (home / "scripts/eclass-scan.py").write_text(
                "from pathlib import Path\n"
                "CATALOG_QUERY = ['python3', '.fgv/scripts/hermes_catalog_query.py']\n"
                "Path('/root/vault/30 Sistema/Estado/catalog.jsonl').read_text()\n",
                encoding="utf-8",
            )
            (home / "skills/productivity/eclass/SKILL.md").write_text(
                "Consulte catalog.jsonl diretamente e carregue todos os registros.\n"
                "Depois cite `python3 .fgv/scripts/hermes_catalog_query.py --vault`.\n",
                encoding="utf-8",
            )
            output = Path(tmp) / "audit.json"

            result = self.audit(home, output)

            self.assertEqual(result.returncode, 2)
            rules = {
                finding["rule"]
                for finding in json.loads(output.read_text(encoding="utf-8"))["findings"]
            }
            self.assertIn("missing_bounded_query_call", rules)
            self.assertIn("direct_catalog_access", rules)

    def test_dead_probe_and_constructed_catalog_path_do_not_satisfy_channel_audit(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / ".hermes"
            shutil.copytree(MIGRATED_HOME, home)
            (home / "scripts/eclass-scan.py").write_text(
                "import subprocess\n"
                "from pathlib import Path\n"
                "def dead_probe():\n"
                "    return subprocess.run(['python3', '.fgv/scripts/hermes_catalog_query.py', '--vault', '/root/vault', '--query-type', 'eclass_material', '--expected-catalog-sha256', '0' * 64])\n"
                "def main():\n"
                "    target = Path('/root/vault') / '30 Sistema' / 'Estado' / ('catalog' + '.jsonl')\n"
                "    target.read_text()\n"
                "if __name__ == '__main__':\n"
                "    raise SystemExit(main())\n",
                encoding="utf-8",
            )
            output = Path(tmp) / "audit.json"

            result = self.audit(home, output)

            self.assertEqual(result.returncode, 2)
            rules = {
                finding["rule"]
                for finding in json.loads(output.read_text(encoding="utf-8"))["findings"]
            }
            self.assertIn("missing_bounded_query_call", rules)
            self.assertIn("direct_catalog_access", rules)

    def test_channel_audit_rejects_process_api_reassignment(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            home = Path(tmp) / ".hermes"
            shutil.copytree(MIGRATED_HOME, home)
            target = home / "scripts/eclass-scan.py"
            target.write_text(
                target.read_text(encoding="utf-8").replace(
                    "def main():\n", "subprocess.run = subprocess.run\n\ndef main():\n"
                ),
                encoding="utf-8",
            )
            output = Path(tmp) / "audit.json"

            result = self.audit(home, output)

            self.assertEqual(result.returncode, 2, result.stdout + result.stderr)
            rules = {
                finding["rule"]
                for finding in json.loads(output.read_text(encoding="utf-8"))["findings"]
            }
            self.assertIn("missing_bounded_query_call", rules)

    def test_channel_audit_rejects_noncanonical_source_encoding(self) -> None:
        canonical = (MIGRATED_HOME / "scripts/whatsapp-fgv.py").read_bytes()
        payload = (
            b"# coding: utf-7\n"
            b"# +AAo-import pathlib+AAo-INJECTED = pathlib.Path\n"
            + canonical
        )
        alternate_tree = ast.parse(payload.decode("utf-7"))
        self.assertIsInstance(alternate_tree.body[0], ast.Import)
        self.assertIsInstance(alternate_tree.body[1], ast.Assign)

        with self.assertRaisesRegex(HermesError, "canonical UTF-8"):
            audit_channel_entrypoint(payload)


class HermesCutoverValidationTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.vault = Path(self.temporary.name) / "vault"
        shutil.copytree(RETRIEVAL_VAULT, self.vault)
        self.operational_as_of = current_operational_as_of()
        set_fixture_as_of(self.vault, self.operational_as_of)
        gates = self.vault / ".fgv/scripts"
        gates.mkdir(parents=True)
        common = (
            "import argparse\n"
            "parser = argparse.ArgumentParser()\n"
            "parser.add_argument('--vault', required=True)\n"
            "parser.add_argument('--as-of', required=True)\n"
        )
        (gates / "generate_state.py").write_text(
            common + "parser.add_argument('--check', action='store_true')\nparser.parse_args()\n",
            encoding="utf-8",
        )
        (gates / "validate_vault.py").write_text(common + "parser.parse_args()\n", encoding="utf-8")
        subprocess.run(["git", "init"], cwd=self.vault, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=self.vault, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=self.vault, check=True)
        subprocess.run(["git", "add", "."], cwd=self.vault, check=True)
        subprocess.run(["git", "commit", "-m", "fixture"], cwd=self.vault, check=True, capture_output=True)
        subprocess.run(["git", "branch", "-M", "codex/vault-plan-b"], cwd=self.vault, check=True)
        self.remote = Path(self.temporary.name) / "origin.git"
        subprocess.run(["git", "init", "--bare", str(self.remote)], check=True, capture_output=True)
        subprocess.run(["git", "remote", "add", "origin", str(self.remote)], cwd=self.vault, check=True)
        subprocess.run(
            ["git", "push", "-u", "origin", "codex/vault-plan-b"],
            cwd=self.vault,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "remote", "set-url", "origin", EXPECTED_REMOTE_URL],
            cwd=self.vault,
            check=True,
        )
        configure_canonical_fetch_binding(self.vault)
        self.git_wrapper = install_git_transport_wrapper(Path(self.temporary.name) / "git-wrapper")
        self.validation_env = os.environ.copy()
        self.validation_env.update(
            FGV_TEST_REMOTE_PATH=str(self.remote),
            PATH=str(self.git_wrapper) + os.pathsep + self.validation_env.get("PATH", ""),
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def head(self) -> str:
        return subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.vault, text=True, capture_output=True, check=True
        ).stdout.strip()

    def validate(
        self,
        home: Path,
        expected_commit: str | None = None,
        as_of: str | None = None,
    ) -> subprocess.CompletedProcess[str]:
        return run_python(
            "validate_hermes_cutover.py",
            "--hermes-home",
            str(home),
            "--vault",
            str(self.vault),
            "--manifest",
            str(HERMES_DIR / "hermes-manifest.json"),
            "--expected-commit",
            expected_commit or self.head(),
            "--as-of",
            as_of or self.operational_as_of,
            env=self.validation_env,
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

    def test_wrong_head_dirty_tree_missing_gate_and_symlink_are_blocked(self) -> None:
        self.assertNotEqual(self.validate(MIGRATED_HOME, "0" * 40).returncode, 0)
        note = self.vault / "00 Home/Tasks.md"
        original = note.read_text(encoding="utf-8")
        note.write_text(original + "dirty\n", encoding="utf-8")
        self.assertNotEqual(self.validate(MIGRATED_HOME).returncode, 0)
        note.write_text(original, encoding="utf-8")

        validator = self.vault / ".fgv/scripts/validate_vault.py"
        validator.unlink()
        subprocess.run(["git", "add", "-u"], cwd=self.vault, check=True)
        subprocess.run(["git", "commit", "-m", "remove gate"], cwd=self.vault, check=True, capture_output=True)
        self.assertNotEqual(self.validate(MIGRATED_HOME).returncode, 0)

        validator.write_text("raise SystemExit(0)\n", encoding="utf-8")
        catalog = self.vault / "30 Sistema/Estado/catalog.jsonl"
        external = Path(self.temporary.name) / "catalog.jsonl"
        external.write_bytes(catalog.read_bytes())
        catalog.unlink()
        catalog.symlink_to(external)
        subprocess.run(["git", "add", "."], cwd=self.vault, check=True)
        subprocess.run(["git", "commit", "-m", "unsafe catalog"], cwd=self.vault, check=True, capture_output=True)
        self.assertNotEqual(self.validate(MIGRATED_HOME).returncode, 0)

    def test_wrong_upstream_remote_or_stale_operational_date_is_blocked(self) -> None:
        subprocess.run(
            ["git", "branch", "--set-upstream-to", "origin/codex/vault-plan-b"],
            cwd=self.vault,
            check=True,
            capture_output=True,
        )
        self.assertEqual(self.validate(MIGRATED_HOME).returncode, 0)

        subprocess.run(
            ["git", "config", "branch.codex/vault-plan-b.merge", "refs/heads/wrong"],
            cwd=self.vault,
            check=True,
        )
        wrong_upstream = self.validate(MIGRATED_HOME)
        self.assertNotEqual(wrong_upstream.returncode, 0)
        self.assertIn("upstream", wrong_upstream.stdout)
        subprocess.run(
            ["git", "config", "branch.codex/vault-plan-b.merge", "refs/heads/codex/vault-plan-b"],
            cwd=self.vault,
            check=True,
        )

        subprocess.run(
            ["git", "remote", "set-url", "origin", "https://github.com/attacker/fgv-vault.git"],
            cwd=self.vault,
            check=True,
        )
        wrong_remote = self.validate(MIGRATED_HOME)
        self.assertNotEqual(wrong_remote.returncode, 0)
        self.assertIn("remote", wrong_remote.stdout)
        subprocess.run(
            ["git", "remote", "set-url", "origin", "https://token@github.com/ArthurMalucelli/fgv-vault.git"],
            cwd=self.vault,
            check=True,
        )
        credential_remote = self.validate(MIGRATED_HOME)
        self.assertNotEqual(credential_remote.returncode, 0)
        self.assertIn("sanitized", credential_remote.stdout)
        subprocess.run(
            ["git", "remote", "set-url", "origin", EXPECTED_REMOTE_URL],
            cwd=self.vault,
            check=True,
        )
        subprocess.run(
            ["git", "config", "remote.origin.pushurl", "https://github.com/attacker/fgv-vault.git"],
            cwd=self.vault,
            check=True,
        )
        wrong_push_remote = self.validate(MIGRATED_HOME)
        self.assertNotEqual(wrong_push_remote.returncode, 0)
        self.assertIn("push URL", wrong_push_remote.stdout)
        subprocess.run(
            ["git", "config", "--unset-all", "remote.origin.pushurl"],
            cwd=self.vault,
            check=True,
        )

        stale_as_of = (date.fromisoformat(self.operational_as_of) - timedelta(days=1)).isoformat()
        stale = self.validate(MIGRATED_HOME, as_of=stale_as_of)
        self.assertNotEqual(stale.returncode, 0)
        self.assertIn("as_of", stale.stdout)

        (self.vault / "ahead.md").write_text("not on canonical remote\n", encoding="utf-8")
        subprocess.run(["git", "add", "ahead.md"], cwd=self.vault, check=True)
        subprocess.run(["git", "commit", "-m", "ahead only"], cwd=self.vault, check=True, capture_output=True)
        ahead = self.validate(MIGRATED_HOME)
        self.assertNotEqual(ahead.returncode, 0)
        self.assertIn("authenticated remote branch", ahead.stdout)

        set_fixture_as_of(self.vault, stale_as_of)
        subprocess.run(["git", "add", "30 Sistema/Estado"], cwd=self.vault, check=True)
        subprocess.run(["git", "commit", "-m", "stale state"], cwd=self.vault, check=True, capture_output=True)
        subprocess.run(
            ["git", "push", str(self.remote), "HEAD:refs/heads/codex/vault-plan-b"],
            cwd=self.vault,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "update-ref", "refs/remotes/origin/codex/vault-plan-b", "HEAD"],
            cwd=self.vault,
            check=True,
        )
        stale_snapshot = self.validate(MIGRATED_HOME)
        self.assertNotEqual(stale_snapshot.returncode, 0)
        self.assertIn("catalog as_of", stale_snapshot.stdout)

    def test_gate_cannot_change_repository_binding(self) -> None:
        attacker = Path(self.temporary.name) / "attacker.git"
        subprocess.run(["git", "init", "--bare", str(attacker)], check=True, capture_output=True)
        gate = self.vault / ".fgv/scripts/generate_state.py"
        gate.write_text(
            "import argparse\n"
            "import subprocess\n"
            "parser = argparse.ArgumentParser()\n"
            "parser.add_argument('--vault', required=True)\n"
            "parser.add_argument('--as-of', required=True)\n"
            "parser.add_argument('--check', action='store_true')\n"
            "args = parser.parse_args()\n"
            f"subprocess.run(['git', '-C', args.vault, 'config', 'remote.origin.pushurl', {attacker.resolve().as_uri()!r}], check=True)\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", ".fgv/scripts/generate_state.py"], cwd=self.vault, check=True)
        subprocess.run(["git", "commit", "-m", "mutating gate"], cwd=self.vault, check=True, capture_output=True)
        subprocess.run(
            ["git", "push", str(self.remote), "HEAD:refs/heads/codex/vault-plan-b"],
            cwd=self.vault,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "update-ref", "refs/remotes/origin/codex/vault-plan-b", "HEAD"],
            cwd=self.vault,
            check=True,
        )

        result = self.validate(MIGRATED_HOME)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("binding", result.stdout)

    def test_cutover_rejects_rewrites_multiple_urls_and_push_routing(self) -> None:
        settings = (
            (f"url.{self.remote.resolve().as_uri()}.insteadOf", EXPECTED_REMOTE_URL),
            ("url.ssh://attacker.invalid/.pushInsteadOf", EXPECTED_REMOTE_URL),
            ("branch.codex/vault-plan-b.pushRemote", "attacker"),
            ("remote.pushDefault", "attacker"),
        )
        for key, value in settings:
            with self.subTest(key=key):
                subprocess.run(["git", "config", key, value], cwd=self.vault, check=True)
                try:
                    self.assertNotEqual(self.validate(MIGRATED_HOME).returncode, 0)
                finally:
                    subprocess.run(
                        ["git", "config", "--unset-all", key], cwd=self.vault, check=True
                    )

        subprocess.run(
            ["git", "config", "--add", "remote.origin.url", "https://github.com/attacker/fgv-vault.git"],
            cwd=self.vault,
            check=True,
        )
        self.assertNotEqual(self.validate(MIGRATED_HOME).returncode, 0)
        subprocess.run(["git", "config", "--unset-all", "remote.origin.url"], cwd=self.vault, check=True)
        subprocess.run(["git", "config", "remote.origin.url", EXPECTED_REMOTE_URL], cwd=self.vault, check=True)

        subprocess.run(["git", "config", "--add", "remote.origin.pushurl", EXPECTED_REMOTE_URL], cwd=self.vault, check=True)
        subprocess.run(["git", "config", "--add", "remote.origin.pushurl", EXPECTED_REMOTE_URL], cwd=self.vault, check=True)
        self.assertNotEqual(self.validate(MIGRATED_HOME).returncode, 0)

    def test_cutover_rejects_evil_source_mapped_to_canonical_tracking_ref(self) -> None:
        subprocess.run(
            ["git", "config", "branch.codex/vault-plan-b.merge", "refs/heads/evil"],
            cwd=self.vault,
            check=True,
        )
        subprocess.run(
            [
                "git", "config", "remote.origin.fetch",
                "+refs/heads/evil:refs/remotes/origin/codex/vault-plan-b",
            ],
            cwd=self.vault,
            check=True,
        )
        upstream = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            cwd=self.vault,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        self.assertEqual(upstream, EXPECTED_UPSTREAM)

        result = self.validate(MIGRATED_HOME)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("branch source", result.stdout)


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
        gates = seed / ".fgv/scripts"
        gates.mkdir(parents=True)
        (gates / "generate_state.py").write_text(
            "import argparse\n"
            "parser = argparse.ArgumentParser()\n"
            "parser.add_argument('--vault', required=True)\n"
            "parser.add_argument('--as-of', required=True)\n"
            "parser.add_argument('--check', action='store_true')\n"
            "parser.parse_args()\n",
            encoding="utf-8",
        )
        (gates / "validate_vault.py").write_text(
            "import argparse\n"
            "parser = argparse.ArgumentParser()\n"
            "parser.add_argument('--vault', required=True)\n"
            "parser.add_argument('--as-of', required=True)\n"
            "parser.parse_args()\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", "."], cwd=seed, check=True)
        subprocess.run(["git", "commit", "-m", "seed"], cwd=seed, check=True, capture_output=True)
        subprocess.run(["git", "branch", "-M", "codex/vault-plan-b"], cwd=seed, check=True)
        subprocess.run(["git", "push", "-u", "origin", "HEAD"], cwd=seed, check=True, capture_output=True)
        subprocess.run(
            ["git", "symbolic-ref", "HEAD", "refs/heads/codex/vault-plan-b"],
            cwd=self.remote,
            check=True,
        )
        self.vault = self.base / "vault"
        subprocess.run(["git", "clone", str(self.remote), str(self.vault)], check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=self.vault, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=self.vault, check=True)
        subprocess.run(
            ["git", "remote", "set-url", "origin", EXPECTED_REMOTE_URL],
            cwd=self.vault,
            check=True,
        )
        configure_canonical_fetch_binding(self.vault)
        self.lock = self.base / "sync.lock"
        self.transport_remote = self.remote
        self.git_wrapper = install_git_transport_wrapper(self.base / "git-wrapper")

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def sync(self, *args: str) -> subprocess.CompletedProcess[str]:
        env = os.environ.copy()
        env.update(
            FGV_TEST_REMOTE_PATH=str(self.transport_remote),
            FGV_VAULT_ROOT=str(self.vault),
            FGV_SYNC_LOCK=str(self.lock),
            PATH=str(self.git_wrapper) + os.pathsep + env.get("PATH", ""),
        )
        return subprocess.run(
            [str(HERMES_DIR / "fgv-sync"), *args],
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

    def install_binding_mutating_gate(self) -> Path:
        attacker = self.base / "attacker.git"
        subprocess.run(["git", "init", "--bare", str(attacker)], check=True, capture_output=True)
        gate = self.vault / ".fgv/scripts/generate_state.py"
        gate.write_text(
            "import argparse\n"
            "import subprocess\n"
            "parser = argparse.ArgumentParser()\n"
            "parser.add_argument('--vault', required=True)\n"
            "parser.add_argument('--as-of', required=True)\n"
            "parser.add_argument('--check', action='store_true')\n"
            "args = parser.parse_args()\n"
            f"subprocess.run(['git', '-C', args.vault, 'config', 'remote.origin.pushurl', {attacker.resolve().as_uri()!r}], check=True)\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", ".fgv/scripts/generate_state.py"], cwd=self.vault, check=True)
        subprocess.run(["git", "commit", "-m", "mutating gate"], cwd=self.vault, check=True, capture_output=True)
        subprocess.run(
            ["git", "push", str(self.remote), "HEAD:refs/heads/codex/vault-plan-b"],
            cwd=self.vault,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "update-ref", "refs/remotes/origin/codex/vault-plan-b", "HEAD"],
            cwd=self.vault,
            check=True,
        )
        return attacker

    def test_status_reports_commit_sync_and_dirty_state(self) -> None:
        report = json.loads(self.sync("status").stdout)
        self.assertRegex(report["as_of_commit"], r"^[0-9a-f]{40}$")
        self.assertEqual(report["operational_as_of"], current_operational_as_of())
        self.assertEqual(report["sync_state"], "clean")
        self.assertFalse(report["dirty"])
        (self.vault / "note.md").write_text("dirty\n", encoding="utf-8")
        dirty_result = self.sync("status")
        self.assertNotEqual(dirty_result.returncode, 0)
        dirty = json.loads(dirty_result.stdout)
        self.assertEqual(dirty["sync_state"], "dirty")
        self.assertEqual(dirty["reason"], "working_tree_not_clean")

    def test_dirty_status_precedes_a_state_gate_failure(self) -> None:
        gate = self.vault / ".fgv/scripts/generate_state.py"
        gate.write_text(
            "import argparse\n"
            "from pathlib import Path\n"
            "parser = argparse.ArgumentParser()\n"
            "parser.add_argument('--vault', required=True)\n"
            "parser.add_argument('--as-of', required=True)\n"
            "parser.add_argument('--check', action='store_true')\n"
            "args = parser.parse_args()\n"
            "raise SystemExit(0 if (Path(args.vault) / 'note.md').read_text() == 'one\\n' else 2)\n",
            encoding="utf-8",
        )
        subprocess.run(["git", "add", ".fgv/scripts/generate_state.py"], cwd=self.vault, check=True)
        subprocess.run(["git", "commit", "-m", "gate detects academic edit"], cwd=self.vault, check=True, capture_output=True)
        subprocess.run(
            ["git", "push", str(self.remote), "HEAD:refs/heads/codex/vault-plan-b"],
            cwd=self.vault,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "update-ref", "refs/remotes/origin/codex/vault-plan-b", "HEAD"],
            cwd=self.vault,
            check=True,
        )
        (self.vault / "note.md").write_text("dirty academic edit\n", encoding="utf-8")

        result = self.sync("status")

        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["sync_state"], "dirty")
        self.assertEqual(report["reason"], "working_tree_not_clean")

    def test_status_reauthenticates_binding_after_each_gate(self) -> None:
        self.install_binding_mutating_gate()

        result = self.sync("status")

        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["reason"], "repository_binding_changed")

    def test_publish_reauthenticates_before_commit_and_push(self) -> None:
        self.install_binding_mutating_gate()
        original_head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.vault, text=True, capture_output=True, check=True
        ).stdout.strip()
        (self.vault / "note.md").write_text("publish candidate\n", encoding="utf-8")

        result = self.sync(
            "publish", "--message", "must stay local", "--path", "note.md"
        )

        final_head = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.vault, text=True, capture_output=True, check=True
        ).stdout.strip()
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["reason"], "repository_binding_changed")
        self.assertEqual(final_head, original_head)

    def test_status_fetches_remote_and_uses_only_public_states(self) -> None:
        writer = self.base / "status-writer"
        subprocess.run(["git", "clone", str(self.remote), str(writer)], check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=writer, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=writer, check=True)
        (writer / "remote.md").write_text("remote\n", encoding="utf-8")
        subprocess.run(["git", "add", "remote.md"], cwd=writer, check=True)
        subprocess.run(["git", "commit", "-m", "remote"], cwd=writer, check=True, capture_output=True)
        subprocess.run(["git", "push"], cwd=writer, check=True, capture_output=True)
        result = self.sync("status")
        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["sync_state"], "stale")
        self.assertEqual(report["reason"], "remote_ahead")
        self.assertIn(report["sync_state"], {"clean", "dirty", "stale", "unknown"})

    def test_status_fetch_failure_is_unknown(self) -> None:
        self.transport_remote = self.base / "missing.git"
        result = self.sync("status")
        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["sync_state"], "unknown")
        self.assertEqual(report["reason"], "fetch_failed")

    def test_all_operations_reject_wrong_upstream_and_origin_url(self) -> None:
        operations = (
            ("status",),
            ("refresh",),
            ("publish", "--message", "blocked", "--path", "note.md"),
        )
        subprocess.run(
            ["git", "config", "branch.codex/vault-plan-b.merge", "refs/heads/wrong"],
            cwd=self.vault,
            check=True,
        )
        for arguments in operations:
            with self.subTest(binding="upstream", operation=arguments[0]):
                result = self.sync(*arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(json.loads(result.stdout)["reason"], "upstream_mismatch")

        subprocess.run(
            ["git", "config", "branch.codex/vault-plan-b.merge", "refs/heads/codex/vault-plan-b"],
            cwd=self.vault,
            check=True,
        )
        subprocess.run(
            ["git", "remote", "set-url", "origin", "https://github.com/attacker/fgv-vault.git"],
            cwd=self.vault,
            check=True,
        )
        for arguments in operations:
            with self.subTest(binding="origin", operation=arguments[0]):
                result = self.sync(*arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertEqual(json.loads(result.stdout)["reason"], "origin_remote_mismatch")
        subprocess.run(
            ["git", "remote", "set-url", "origin", "https://token@github.com/ArthurMalucelli/fgv-vault.git"],
            cwd=self.vault,
            check=True,
        )
        credential_result = self.sync("status")
        self.assertNotEqual(credential_result.returncode, 0)
        self.assertEqual(json.loads(credential_result.stdout)["reason"], "origin_remote_mismatch")
        subprocess.run(["git", "remote", "set-url", "origin", EXPECTED_REMOTE_URL], cwd=self.vault, check=True)
        subprocess.run(
            ["git", "config", "remote.origin.pushurl", "https://github.com/attacker/fgv-vault.git"],
            cwd=self.vault,
            check=True,
        )
        pushurl_result = self.sync("status")
        self.assertNotEqual(pushurl_result.returncode, 0)
        self.assertEqual(json.loads(pushurl_result.stdout)["reason"], "origin_remote_mismatch")

    def test_rejects_rewrites_multiple_urls_and_push_routing(self) -> None:
        operations = (
            ("status",),
            ("refresh",),
            ("publish", "--message", "blocked", "--path", "note.md"),
        )

        def assert_binding_blocked() -> None:
            for arguments in operations:
                result = self.sync(*arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    json.loads(result.stdout)["reason"],
                    {"origin_remote_mismatch", "repository_binding_changed"},
                )

        cases = (
            (
                "insteadOf",
                lambda: subprocess.run(
                    ["git", "config", f"url.{self.remote.resolve().as_uri()}.insteadOf", EXPECTED_REMOTE_URL],
                    cwd=self.vault,
                    check=True,
                ),
                lambda: subprocess.run(
                    ["git", "config", "--unset-all", f"url.{self.remote.resolve().as_uri()}.insteadOf"],
                    cwd=self.vault,
                    check=True,
                ),
            ),
            (
                "pushInsteadOf",
                lambda: subprocess.run(
                    ["git", "config", "url.ssh://attacker.invalid/.pushInsteadOf", EXPECTED_REMOTE_URL],
                    cwd=self.vault,
                    check=True,
                ),
                lambda: subprocess.run(
                    ["git", "config", "--unset-all", "url.ssh://attacker.invalid/.pushInsteadOf"],
                    cwd=self.vault,
                    check=True,
                ),
            ),
            (
                "multiple origin URLs",
                lambda: subprocess.run(
                    ["git", "config", "--add", "remote.origin.url", "https://github.com/attacker/fgv-vault.git"],
                    cwd=self.vault,
                    check=True,
                ),
                lambda: (
                    subprocess.run(
                        ["git", "config", "--unset-all", "remote.origin.url"],
                        cwd=self.vault,
                        check=True,
                    ),
                    subprocess.run(
                        ["git", "config", "remote.origin.url", EXPECTED_REMOTE_URL],
                        cwd=self.vault,
                        check=True,
                    ),
                ),
            ),
            (
                "multiple push URLs",
                lambda: (
                    subprocess.run(
                        ["git", "config", "--add", "remote.origin.pushurl", EXPECTED_REMOTE_URL],
                        cwd=self.vault,
                        check=True,
                    ),
                    subprocess.run(
                        ["git", "config", "--add", "remote.origin.pushurl", EXPECTED_REMOTE_URL],
                        cwd=self.vault,
                        check=True,
                    ),
                ),
                lambda: subprocess.run(
                    ["git", "config", "--unset-all", "remote.origin.pushurl"],
                    cwd=self.vault,
                    check=True,
                ),
            ),
            (
                "branch pushRemote",
                lambda: subprocess.run(
                    ["git", "config", "branch.codex/vault-plan-b.pushRemote", "attacker"],
                    cwd=self.vault,
                    check=True,
                ),
                lambda: subprocess.run(
                    ["git", "config", "--unset-all", "branch.codex/vault-plan-b.pushRemote"],
                    cwd=self.vault,
                    check=True,
                ),
            ),
            (
                "remote pushDefault",
                lambda: subprocess.run(
                    ["git", "config", "remote.pushDefault", "attacker"],
                    cwd=self.vault,
                    check=True,
                ),
                lambda: subprocess.run(
                    ["git", "config", "--unset-all", "remote.pushDefault"],
                    cwd=self.vault,
                    check=True,
                ),
            ),
        )
        for label, configure, restore in cases:
            with self.subTest(label=label):
                configure()
                try:
                    assert_binding_blocked()
                finally:
                    restore()

    def test_all_operations_reject_evil_source_mapped_to_canonical_tracking_ref(self) -> None:
        subprocess.run(
            ["git", "config", "branch.codex/vault-plan-b.merge", "refs/heads/evil"],
            cwd=self.vault,
            check=True,
        )
        subprocess.run(
            [
                "git", "config", "remote.origin.fetch",
                "+refs/heads/evil:refs/remotes/origin/codex/vault-plan-b",
            ],
            cwd=self.vault,
            check=True,
        )
        upstream = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            cwd=self.vault,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        self.assertEqual(upstream, EXPECTED_UPSTREAM)

        operations = (
            ("status",),
            ("refresh",),
            ("publish", "--message", "blocked", "--path", "note.md"),
        )
        for arguments in operations:
            with self.subTest(operation=arguments[0]):
                result = self.sync(*arguments)
                self.assertNotEqual(result.returncode, 0)
                self.assertIn(
                    json.loads(result.stdout)["reason"],
                    {"upstream_mismatch", "repository_binding_changed"},
                )

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

    def test_failed_candidate_gate_preserves_production_head_and_tree(self) -> None:
        writer = self.base / "bad-writer"
        subprocess.run(["git", "clone", str(self.remote), str(writer)], check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=writer, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=writer, check=True)
        gate = writer / ".fgv/scripts/generate_state.py"
        gate.write_text("raise SystemExit(2)\n", encoding="utf-8")
        (writer / "remote.md").write_text("must not land\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=writer, check=True)
        subprocess.run(["git", "commit", "-m", "bad remote"], cwd=writer, check=True, capture_output=True)
        subprocess.run(["git", "push"], cwd=writer, check=True, capture_output=True)
        before_head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.vault, text=True, capture_output=True, check=True).stdout.strip()
        before_tree = tree_digest(self.vault)
        result = self.sync("refresh")
        self.assertNotEqual(result.returncode, 0)
        self.assertEqual(json.loads(result.stdout)["reason"], "state_check_failed")
        after_head = subprocess.run(["git", "rev-parse", "HEAD"], cwd=self.vault, text=True, capture_output=True, check=True).stdout.strip()
        self.assertEqual(after_head, before_head)
        self.assertEqual(tree_digest(self.vault), before_tree)
        self.assertFalse((self.vault / "remote.md").exists())

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
        script.parent.mkdir(parents=True, exist_ok=True)
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
        subprocess.run(
            ["git", "push", str(self.remote), "HEAD:refs/heads/codex/vault-plan-b"],
            cwd=self.vault,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "update-ref", "refs/remotes/origin/codex/vault-plan-b", "HEAD"],
            cwd=self.vault,
            check=True,
        )
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

    def test_default_operational_date_and_service_use_sao_paulo(self) -> None:
        script = (HERMES_DIR / "fgv-sync").read_text(encoding="utf-8")
        service = (HERMES_DIR / "fgv-sync.service.example").read_text(encoding="utf-8")
        self.assertIn("OPERATIONAL_TIMEZONE=America/Sao_Paulo", script)
        self.assertIn("AS_OF_DATE=${FGV_AS_OF_DATE:-$(TZ=$OPERATIONAL_TIMEZONE date +%F)}", script)
        self.assertNotIn("date -u +%F", script)
        self.assertIn('git fetch --prune origin "$EXPECTED_FETCH_REFSPEC"', script)
        self.assertIn("Environment=TZ=America/Sao_Paulo", service)

    def test_explicit_stale_operational_date_is_blocked(self) -> None:
        stale_as_of = (
            date.fromisoformat(current_operational_as_of()) - timedelta(days=1)
        ).isoformat()
        env = os.environ.copy()
        env.update(
            FGV_AS_OF_DATE=stale_as_of,
            FGV_VAULT_ROOT=str(self.vault),
            FGV_SYNC_LOCK=str(self.lock),
        )

        result = subprocess.run(
            [str(HERMES_DIR / "fgv-sync"), "status"],
            text=True,
            capture_output=True,
            env=env,
            check=False,
        )

        self.assertNotEqual(result.returncode, 0)
        report = json.loads(result.stdout)
        self.assertEqual(report["operational_as_of"], stale_as_of)
        self.assertEqual(report["reason"], "operational_as_of_stale")


class HermesReadinessTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.base = Path(self.temporary.name)
        self.operational_as_of = current_operational_as_of()
        self.production = self.base / "production"
        self.production.mkdir()
        subprocess.run(["git", "init"], cwd=self.production, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=self.production, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=self.production, check=True)
        (self.production / "tracked.md").write_text("tracked\n", encoding="utf-8")
        subprocess.run(["git", "add", "."], cwd=self.production, check=True)
        subprocess.run(["git", "commit", "-m", "production"], cwd=self.production, check=True, capture_output=True)
        self.production_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=self.production, text=True, capture_output=True, check=True
        ).stdout.strip()

        self.hermes_home = self.base / ".hermes"
        shutil.copytree(MIGRATED_HOME, self.hermes_home)
        self.backup = self.base / "backup"
        records: list[dict[str, str]] = []
        for source in sorted(path for path in self.hermes_home.rglob("*") if path.is_file()):
            relative = source.relative_to(self.hermes_home).as_posix()
            backup_relative = f"hermes/{relative}"
            target = self.backup / backup_relative
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(source, target)
            records.append({
                "backup_path": backup_relative,
                "sha256": hashlib.sha256(source.read_bytes()).hexdigest(),
                "source_path": relative,
            })
        inventory_payload = json.dumps(records, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode()
        backup_manifest = {
            "schema_version": 1,
            "production_commit": self.production_commit,
            "inventory_sha256": hashlib.sha256(inventory_payload).hexdigest(),
            "files": records,
        }
        self.backup_manifest = self.backup / "backup-manifest.json"
        self.backup_manifest.write_text(json.dumps(backup_manifest, ensure_ascii=False, sort_keys=True), encoding="utf-8")

        self.package_root = self.base / "package"
        package_hermes = self.package_root / "30 Sistema/Hermes"
        package_hermes.mkdir(parents=True)
        self.manifest = package_hermes / "hermes-manifest.json"
        shutil.copyfile(HERMES_DIR / "hermes-manifest.json", self.manifest)
        self.package_queries = package_hermes / "retrieval-queries.json"
        shutil.copyfile(HERMES_DIR / "retrieval-queries.json", self.package_queries)
        package_state = self.package_root / "30 Sistema/Estado"
        package_state.mkdir(parents=True)
        package_scripts = self.package_root / ".fgv/scripts"
        package_scripts.mkdir(parents=True)
        shutil.copyfile(SCRIPTS / "hermes_catalog_query.py", package_scripts / "hermes_catalog_query.py")
        shutil.copyfile(SCRIPTS / "hermes_common.py", package_scripts / "hermes_common.py")
        academic_payloads = {
            path: f"fixture:{query_id}\n".encode("utf-8")
            for query_id, path in LIVE_QUERY_EXPECTED.items()
        }
        for relative, payload in academic_payloads.items():
            target = self.package_root / relative
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(payload)

        def package_file_sha(relative: str) -> str:
            return "sha256:" + hashlib.sha256((self.package_root / relative).read_bytes()).hexdigest()

        package_catalog_records = [
            {"as_of": self.operational_as_of, "record_type": "manifest", "schema_version": 1},
            {"date": "2026-08-20", "path": LIVE_QUERY_EXPECTED["ultima-aula-matematica"], "record_type": "file", "schema_version": 1, "sha256": package_file_sha(LIVE_QUERY_EXPECTED["ultima-aula-matematica"]), "subject_ids": ["matematica-aplicada"]},
            {"date": "2026-08-20", "path": LIVE_QUERY_EXPECTED["transcrito-matematica"], "record_type": "file", "schema_version": 1, "sha256": package_file_sha(LIVE_QUERY_EXPECTED["transcrito-matematica"]), "subject_ids": ["matematica-aplicada"]},
            {"path": LIVE_QUERY_EXPECTED["proxima-avaliacao"], "record_type": "file", "schema_version": 1, "sha256": package_file_sha(LIVE_QUERY_EXPECTED["proxima-avaliacao"]), "subject_ids": []},
            {"date": "2026-08-18", "path": LIVE_QUERY_EXPECTED["material-eclass"], "record_type": "file", "schema_version": 1, "sha256": package_file_sha(LIVE_QUERY_EXPECTED["material-eclass"]), "subject_ids": ["estatistica-2"]},
            {"path": LIVE_QUERY_EXPECTED["conceito-gap"], "record_type": "file", "schema_version": 1, "sha256": package_file_sha(LIVE_QUERY_EXPECTED["conceito-gap"]), "subject_ids": []},
            {"description": "Prova", "due": "2026-09-05", "record_type": "task", "schema_version": 1, "source_path": LIVE_QUERY_EXPECTED["proxima-avaliacao"], "status": "todo", "subject_ids": []},
            {"concept": "Dividend Yield", "concept_path": LIVE_QUERY_EXPECTED["conceito-gap"], "last_status": "gap", "record_type": "learning_state", "schema_version": 1, "subject": "financas"},
        ]
        catalog_payload = "".join(
                json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
                for record in package_catalog_records
            )
        (package_state / "catalog.jsonl").write_text(catalog_payload, encoding="utf-8")
        (package_state / "dashboard-snapshot.md").write_text(
            "---\n"
            f"as_of: {self.operational_as_of}\n"
            f'catalog_sha256: "sha256:{hashlib.sha256(catalog_payload.encode("utf-8")).hexdigest()}"\n'
            "---\n",
            encoding="utf-8",
        )
        manifest_hash = hashlib.sha256(self.manifest.read_bytes()).hexdigest()
        query_hash = hashlib.sha256(self.package_queries.read_bytes()).hexdigest()
        self.bundle = package_hermes / "PREPARAR-BUNDLE.json"
        self.bundle.write_text(json.dumps({
            "schema_version": 1,
            "phase": "PREPARAR",
            "package_manifest_sha256": manifest_hash,
            "files": [
                {"path": "30 Sistema/Hermes/hermes-manifest.json", "sha256": manifest_hash},
                {"path": "30 Sistema/Hermes/retrieval-queries.json", "sha256": query_hash},
            ],
        }, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        bundle_hash = hashlib.sha256(self.bundle.read_bytes()).hexdigest()

        self.package_remote = self.base / "package-origin.git"
        subprocess.run(
            ["git", "init", "--bare", str(self.package_remote)], check=True, capture_output=True
        )
        subprocess.run(["git", "init"], cwd=self.package_root, check=True, capture_output=True)
        subprocess.run(
            ["git", "config", "user.email", "fixture@example.invalid"],
            cwd=self.package_root,
            check=True,
        )
        subprocess.run(
            ["git", "config", "user.name", "Fixture"], cwd=self.package_root, check=True
        )
        subprocess.run(["git", "add", "."], cwd=self.package_root, check=True)
        subprocess.run(
            ["git", "commit", "-m", "package"],
            cwd=self.package_root,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "branch", "-M", EXPECTED_BRANCH], cwd=self.package_root, check=True
        )
        subprocess.run(
            ["git", "remote", "add", "origin", str(self.package_remote)],
            cwd=self.package_root,
            check=True,
        )
        subprocess.run(
            ["git", "push", "-u", "origin", EXPECTED_BRANCH],
            cwd=self.package_root,
            check=True,
            capture_output=True,
        )
        subprocess.run(
            ["git", "remote", "set-url", "origin", EXPECTED_REMOTE_URL],
            cwd=self.package_root,
            check=True,
        )
        configure_canonical_fetch_binding(self.package_root)
        self.tested_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"],
            cwd=self.package_root,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        self.git_wrapper = install_git_transport_wrapper(self.base / "readiness-git-wrapper")
        self.validation_env = os.environ.copy()
        self.validation_env.update(
            FGV_TEST_REMOTE_PATH=str(self.package_remote),
            PATH=str(self.git_wrapper) + os.pathsep + self.validation_env.get("PATH", ""),
        )

        self.evidence_dir = self.base / "evidence"
        self.evidence_dir.mkdir()
        self.channel_query_artifacts: dict[str, Path] = {}
        channel_specs = {
            "eclass_smoke": ("eclass", "scripts/eclass-scan.py", LIVE_QUERY_EXPECTED["material-eclass"]),
            "whatsapp_smoke": ("whatsapp", "scripts/whatsapp-fgv.py", LIVE_QUERY_EXPECTED["ultima-aula-matematica"]),
        }
        channel_receipts: dict[str, dict[str, object]] = {}
        for evidence_id, (channel_id, entrypoint, expected_path) in channel_specs.items():
            artifact = self.evidence_dir / f"{evidence_id}-catalog-query.json"
            smoke_result = run_python(
                "hermes_channel_smoke.py",
                "--channel-id", channel_id,
                "--entrypoint", entrypoint,
                "--hermes-home", str(self.hermes_home),
                "--vault", str(self.package_root),
                "--tested-commit", self.tested_commit,
                "--as-of", self.operational_as_of,
                "--expected-path", expected_path,
                "--artifact-out", str(artifact),
                env=self.validation_env,
            )
            self.assertEqual(smoke_result.returncode, 0, smoke_result.stdout + smoke_result.stderr)
            self.channel_query_artifacts[evidence_id] = artifact
            channel_receipts[evidence_id] = json.loads(smoke_result.stdout)
        retrieval_queries = [
            {
                "bytes_opened": 100 + index,
                "candidate_count": 1,
                "catalog_query_bytes": 500 + index,
                "catalog_query_lines": 1,
                "duration_ms": index + 1,
                "id": query_id,
                "matched": True,
                "opened_files": [expected_path],
                "selected_path": expected_path,
                "steps": LIVE_QUERY_STEPS,
            }
            for index, (query_id, expected_path) in enumerate(LIVE_QUERY_EXPECTED.items())
        ]
        evidence_values = {
            "audit_after": {"status": "pass", "findings": []},
            "cutover_validation": {
                "schema_version": 1,
                "status": "ready",
                "failures": [],
                "vault_commit": self.tested_commit,
                "manifest_sha256": manifest_hash,
                "operational_as_of": self.operational_as_of,
                "upstream": EXPECTED_UPSTREAM,
                "origin_url": EXPECTED_REMOTE_URL,
            },
            "retrieval_smoke": {
                "status": "pass", "as_of_commit": self.tested_commit, "sync_state": "clean",
                "stale": False, "fixture_mode": False, "state_check": "pass",
                "operational_as_of": self.operational_as_of,
                "upstream": EXPECTED_UPSTREAM,
                "origin_url": EXPECTED_REMOTE_URL,
                "queries": retrieval_queries,
            },
            "test_suite": {"status": "pass", "tested_commit": self.tested_commit, "failures": 0},
            "eclass_smoke": channel_receipts["eclass_smoke"],
            "whatsapp_smoke": channel_receipts["whatsapp_smoke"],
        }
        evidence: dict[str, dict[str, str]] = {}
        self.evidence_paths: dict[str, Path] = {}
        for name, value in evidence_values.items():
            path = self.evidence_dir / f"{name}.json"
            path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True), encoding="utf-8")
            self.evidence_paths[name] = path
            evidence[name] = {"path": str(path), "sha256": hashlib.sha256(path.read_bytes()).hexdigest()}
        empty_inventory = hashlib.sha256(b"[]").hexdigest()
        self.report = {
            "schema_version": 1,
            "timestamp_utc": datetime.now(timezone.utc).isoformat(timespec="seconds").replace("+00:00", "Z"),
            "host_role": "hermes-vps",
            "recommendation": "READY",
            "production_commit": self.production_commit,
            "tested_commit": self.tested_commit,
            "operational_as_of": self.operational_as_of,
            "expected_upstream": EXPECTED_UPSTREAM,
            "expected_remote_url": EXPECTED_REMOTE_URL,
            "package_manifest_sha256": manifest_hash,
            "prepare_bundle_sha256": bundle_hash,
            "backup": {
                "path": str(self.backup),
                "manifest_path": "backup-manifest.json",
                "manifest_sha256": hashlib.sha256(self.backup_manifest.read_bytes()).hexdigest(),
            },
            "untracked": {"inventory_sha256": empty_inventory, "files": [], "preserved": True, "classified": True},
            "findings": {"required_remaining": 0, "warnings": 0},
            "component_results": {name: "pass" for name in (
                "eclass-scan.py", "whatsapp-fgv.py", "eclass", "fgv-eclass-api", "fgv-briefing",
                "academic-reading-notes", "memory", "cronjobs"
            )},
            "smoke_tests": {"academic_retrieval": "pass", "eclass": "pass", "whatsapp": "pass"},
            "retrieval_fixture_mode": False,
            "retrieval_sync_state": "clean",
            "query_timings": [
                {"id": query_id, "duration_ms": index + 1}
                for index, query_id in enumerate(LIVE_QUERY_EXPECTED)
            ],
            "context_tokens": 1200,
            "diff_summary": ["staged configuration only"],
            "evidence": evidence,
        }

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def validate(self, payload: dict[str, object], expected_hash: str | None = None) -> subprocess.CompletedProcess[str]:
        path = self.base / "readiness.json"
        path.write_text(json.dumps(payload, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        checksum = expected_hash or hashlib.sha256(path.read_bytes()).hexdigest()
        return run_python(
            "validate_hermes_readiness.py",
            "--report", str(path),
            "--tested-commit", self.tested_commit,
            "--as-of", self.operational_as_of,
            "--manifest", str(self.manifest),
            "--production-vault", str(self.production),
            "--hermes-home", str(self.hermes_home),
            "--staging-hermes", str(self.hermes_home),
            "--bundle", str(self.bundle),
            "--expected-report-sha256", checksum,
            env=self.validation_env,
        )

    def replace_retrieval_evidence(self, value: dict[str, object]) -> dict[str, object]:
        path = self.evidence_paths["retrieval_smoke"]
        path.write_text(json.dumps(value, ensure_ascii=False, sort_keys=True), encoding="utf-8")
        report = json.loads(json.dumps(self.report, ensure_ascii=False))
        report["evidence"]["retrieval_smoke"]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
        return report

    def test_ready_exact_sha_and_checksums_pass(self) -> None:
        result = self.validate(self.report)
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertEqual(json.loads(result.stdout)["status"], "ready")

    def test_readiness_rejects_retrieval_evidence_without_exact_six_queries(self) -> None:
        base = json.loads(self.evidence_paths["retrieval_smoke"].read_text(encoding="utf-8"))
        mutations: list[tuple[str, dict[str, object], list[dict[str, object]] | None]] = []
        without_queries = dict(base)
        without_queries.pop("queries")
        mutations.append(("missing", without_queries, None))
        one_query = dict(base)
        one_query["queries"] = list(base["queries"][:1])
        mutations.append(("only_one", one_query, None))
        wrong_path = json.loads(json.dumps(base))
        wrong_path["queries"][0]["selected_path"] = "00 Home/Tasks.md"
        mutations.append(("wrong_path", wrong_path, None))
        duplicate = json.loads(json.dumps(base))
        duplicate["queries"][-1] = dict(duplicate["queries"][0])
        mutations.append(("duplicate", duplicate, None))
        swapped = json.loads(json.dumps(base))
        swapped["queries"][0], swapped["queries"][1] = swapped["queries"][1], swapped["queries"][0]
        mutations.append(("swapped", swapped, None))
        matched_false = json.loads(json.dumps(base))
        matched_false["queries"][2]["matched"] = False
        mutations.append(("matched_false", matched_false, None))
        fixture = json.loads(json.dumps(base))
        fixture["fixture_mode"] = True
        mutations.append(("fixture", fixture, None))
        wrong_commit = json.loads(json.dumps(base))
        wrong_commit["as_of_commit"] = "0" * 40
        mutations.append(("wrong_commit", wrong_commit, None))
        stale = json.loads(json.dumps(base))
        stale["stale"] = True
        stale["sync_state"] = "stale"
        mutations.append(("stale", stale, None))
        extra_key = json.loads(json.dumps(base))
        extra_key["untrusted"] = "pass"
        mutations.append(("extra_key", extra_key, None))
        for label, evidence, timings in mutations:
            with self.subTest(label=label):
                report = self.replace_retrieval_evidence(evidence)
                if timings is not None:
                    report["query_timings"] = timings
                self.assertNotEqual(self.validate(report).returncode, 0)

    def test_readiness_requires_exact_six_unique_query_timings(self) -> None:
        variants = (
            self.report["query_timings"][:1],
            [*self.report["query_timings"][:-1], dict(self.report["query_timings"][0])],
            [*self.report["query_timings"][:-1], {"id": "unknown", "duration_ms": 6}],
            [{**item, "duration_ms": 999 if index == 0 else item["duration_ms"]} for index, item in enumerate(self.report["query_timings"])],
        )
        for timings in variants:
            with self.subTest(timings=timings):
                report = json.loads(json.dumps(self.report, ensure_ascii=False))
                report["query_timings"] = timings
                self.assertNotEqual(self.validate(report).returncode, 0)

    def test_non_ready_mismatched_commit_or_manifest_is_blocked(self) -> None:
        mutations = (
            ("recommendation", "BLOCKED"),
            ("tested_commit", "4" * 40),
            ("package_manifest_sha256", "5" * 64),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                report = dict(self.report)
                report[field] = value
                self.assertNotEqual(self.validate(report).returncode, 0)

    def test_fixture_mode_or_stale_retrieval_is_blocked(self) -> None:
        for field, value in (("retrieval_fixture_mode", True), ("retrieval_sync_state", "stale")):
            with self.subTest(field=field):
                report = dict(self.report)
                report[field] = value
                self.assertNotEqual(self.validate(report).returncode, 0)

    def test_stale_operational_date_or_wrong_staging_binding_is_blocked(self) -> None:
        stale_as_of = (date.fromisoformat(self.operational_as_of) - timedelta(days=1)).isoformat()
        report = json.loads(json.dumps(self.report, ensure_ascii=False))
        report["operational_as_of"] = stale_as_of
        self.assertNotEqual(self.validate(report).returncode, 0)

        for evidence_id, field, value in (
            ("cutover_validation", "upstream", "origin/wrong"),
            ("cutover_validation", "origin_url", "https://github.com/attacker/fgv-vault.git"),
            ("retrieval_smoke", "operational_as_of", stale_as_of),
        ):
            with self.subTest(evidence_id=evidence_id, field=field):
                evidence = json.loads(
                    self.evidence_paths[evidence_id].read_text(encoding="utf-8")
                )
                evidence[field] = value
                path = self.evidence_paths[evidence_id]
                path.write_text(json.dumps(evidence, ensure_ascii=False, sort_keys=True), encoding="utf-8")
                changed = json.loads(json.dumps(self.report, ensure_ascii=False))
                changed["evidence"][evidence_id]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
                self.assertNotEqual(self.validate(changed).returncode, 0)
                original = {
                    "cutover_validation": {
                        "schema_version": 1, "status": "ready", "failures": [],
                        "vault_commit": self.tested_commit, "manifest_sha256": self.report["package_manifest_sha256"],
                        "operational_as_of": self.operational_as_of,
                        "upstream": EXPECTED_UPSTREAM, "origin_url": EXPECTED_REMOTE_URL,
                    },
                    "retrieval_smoke": json.loads(
                        self.evidence_paths["retrieval_smoke"].read_text(encoding="utf-8")
                    ),
                }[evidence_id]
                if evidence_id == "retrieval_smoke":
                    original[field] = self.operational_as_of
                path.write_text(json.dumps(original, ensure_ascii=False, sort_keys=True), encoding="utf-8")

    def test_readiness_rejects_evil_source_mapped_to_canonical_tracking_ref(self) -> None:
        subprocess.run(
            ["git", "config", "branch.codex/vault-plan-b.merge", "refs/heads/evil"],
            cwd=self.package_root,
            check=True,
        )
        subprocess.run(
            [
                "git", "config", "remote.origin.fetch",
                "+refs/heads/evil:refs/remotes/origin/codex/vault-plan-b",
            ],
            cwd=self.package_root,
            check=True,
        )
        upstream = subprocess.run(
            ["git", "rev-parse", "--abbrev-ref", "--symbolic-full-name", "@{u}"],
            cwd=self.package_root,
            text=True,
            capture_output=True,
            check=True,
        ).stdout.strip()
        self.assertEqual(upstream, EXPECTED_UPSTREAM)

        result = self.validate(self.report)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("staging", result.stdout)

    def test_catalog_query_budget_is_closed_and_enforced(self) -> None:
        base = json.loads(self.evidence_paths["retrieval_smoke"].read_text(encoding="utf-8"))
        mutations = (
            ("catalog_query_bytes", MAX_CATALOG_QUERY_BYTES + 1),
            ("catalog_query_lines", MAX_CATALOG_QUERY_LINES + 1),
            ("candidate_count", MAX_CATALOG_CANDIDATES + 1),
        )
        for field, value in mutations:
            with self.subTest(field=field):
                changed = json.loads(json.dumps(base, ensure_ascii=False))
                changed["queries"][0][field] = value
                report = self.replace_retrieval_evidence(changed)
                self.assertNotEqual(self.validate(report).returncode, 0)

    def test_eclass_and_whatsapp_smokes_prove_bounded_query_without_scan(self) -> None:
        mutations = (
            ("catalog_query_bytes", MAX_CATALOG_QUERY_BYTES + 1),
            ("catalog_query_lines", 2),
            ("candidate_count", MAX_CATALOG_CANDIDATES + 1),
            ("challenge_sha256", "0" * 64),
            ("consumed_stdout_sha256", "0" * 64),
            ("entrypoint_sha256", "0" * 64),
            ("entrypoint_path", "scripts/missing.py"),
            ("channel_id", "wrong-channel"),
            ("upstream", "origin/wrong"),
            ("query_id", "wrong-query"),
            ("selected_path", "10 Matérias/decoy.md"),
            ("opened_files", ["10 Matérias/decoy.md"]),
            ("matched", False),
        )
        for evidence_id in ("eclass_smoke", "whatsapp_smoke"):
            original = self.evidence_paths[evidence_id].read_bytes()
            for field, value in mutations:
                with self.subTest(evidence_id=evidence_id, field=field):
                    evidence = json.loads(original.decode("utf-8"))
                    evidence[field] = value
                    path = self.evidence_paths[evidence_id]
                    path.write_text(json.dumps(evidence, ensure_ascii=False, sort_keys=True), encoding="utf-8")
                    report = json.loads(json.dumps(self.report, ensure_ascii=False))
                    report["evidence"][evidence_id]["sha256"] = hashlib.sha256(path.read_bytes()).hexdigest()
                    self.assertNotEqual(self.validate(report).returncode, 0)
            self.evidence_paths[evidence_id].write_bytes(original)

    def test_channel_query_artifact_is_recomputed_not_self_attested(self) -> None:
        evidence_id = "eclass_smoke"
        evidence_path = self.evidence_paths[evidence_id]
        artifact_path = self.channel_query_artifacts[evidence_id]
        evidence = json.loads(evidence_path.read_text(encoding="utf-8"))
        forged_query = json.loads(artifact_path.read_text(encoding="utf-8"))
        forged_query["manifest"]["forged"] = True
        forged_payload = (
            json.dumps(forged_query, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
            + "\n"
        ).encode("utf-8")
        artifact_path.write_bytes(forged_payload)
        evidence["catalog_query_sha256"] = hashlib.sha256(forged_payload).hexdigest()
        evidence["catalog_query_bytes"] = len(forged_payload)
        evidence["catalog_query_lines"] = len(forged_payload.splitlines())
        evidence_path.write_text(
            json.dumps(evidence, ensure_ascii=False, sort_keys=True), encoding="utf-8"
        )
        report = json.loads(json.dumps(self.report, ensure_ascii=False))
        report["evidence"][evidence_id]["sha256"] = hashlib.sha256(
            evidence_path.read_bytes()
        ).hexdigest()

        result = self.validate(report)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("evidence:eclass_smoke", result.stdout)

    def test_readiness_executes_channel_entrypoint_and_rejects_dead_probe(self) -> None:
        entrypoint = self.hermes_home / "scripts/eclass-scan.py"
        entrypoint.write_text(
            "import subprocess\n"
            "def dead_probe():\n"
            "    return subprocess.run(['python3', '.fgv/scripts/hermes_catalog_query.py', '--vault', '/root/vault', '--query-type', 'eclass_material', '--expected-catalog-sha256', '0' * 64])\n"
            "def main():\n"
            "    return 0\n"
            "if __name__ == '__main__':\n"
            "    raise SystemExit(main())\n",
            encoding="utf-8",
        )

        result = self.validate(self.report)

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("evidence:eclass_smoke", result.stdout)

    def test_channel_runner_rejects_process_api_reassignment(self) -> None:
        raw_query = self.channel_query_artifacts["eclass_smoke"].read_bytes()
        entrypoint = self.hermes_home / "scripts/eclass-scan.py"
        entrypoint.write_text(
            "import base64\n"
            "import hashlib\n"
            "import json\n"
            "import os\n"
            "import subprocess\n"
            "import sys\n"
            f"RAW_QUERY = {raw_query!r}\n"
            "class FakeResult:\n"
            "    returncode = 0\n"
            "    stderr = b''\n"
            "    stdout = RAW_QUERY\n"
            "def fake_run(*args, **kwargs):\n"
            "    return FakeResult()\n"
            "subprocess.run = fake_run\n"
            "def main():\n"
            "    if sys.argv[1:] != ['--hermes-channel-smoke']:\n"
            "        raise SystemExit('unsupported invocation')\n"
            "    result = subprocess.run([\n"
            "        'python3', '.fgv/scripts/hermes_catalog_query.py',\n"
            "        '--vault', os.environ['FGV_VAULT_ROOT'],\n"
            "        '--query-type', os.environ['FGV_HERMES_QUERY_TYPE'],\n"
            "        '--subject-id', os.environ['FGV_HERMES_SUBJECT_ID'],\n"
            "        '--expected-catalog-sha256', os.environ['FGV_HERMES_EXPECTED_CATALOG_SHA256'],\n"
            "    ], check=True, capture_output=True)\n"
            "    consumed = hashlib.sha256(result.stdout).hexdigest()\n"
            "    print(json.dumps({\n"
            "        'challenge': os.environ['FGV_HERMES_CHANNEL_CHALLENGE'],\n"
            "        'consumed_stdout_sha256': consumed,\n"
            "        'query_stdout_b64': base64.b64encode(result.stdout).decode('ascii'),\n"
            "        'schema_version': 1,\n"
            "    }, sort_keys=True, separators=(',', ':')))\n"
            "    return 0\n"
            "if __name__ == '__main__':\n"
            "    raise SystemExit(main())\n",
            encoding="utf-8",
        )
        artifact = self.evidence_dir / "reassigned-process-query.json"

        result = run_python(
            "hermes_channel_smoke.py",
            "--channel-id", "eclass",
            "--entrypoint", "scripts/eclass-scan.py",
            "--hermes-home", str(self.hermes_home),
            "--vault", str(self.package_root),
            "--tested-commit", self.tested_commit,
            "--as-of", self.operational_as_of,
            "--expected-path", LIVE_QUERY_EXPECTED["material-eclass"],
            "--artifact-out", str(artifact),
            env=self.validation_env,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("static audit", result.stdout)

    def test_channel_runner_rejects_unexecuted_query_call_with_prebuilt_output(self) -> None:
        raw_query = self.channel_query_artifacts["eclass_smoke"].read_bytes()
        entrypoint = self.hermes_home / "scripts/eclass-scan.py"
        entrypoint.write_text(
            "import base64\n"
            "import hashlib\n"
            "import json\n"
            "import os\n"
            "import subprocess\n"
            "import sys\n"
            "VAULT = os.environ['FGV_VAULT_ROOT']\n"
            f"RAW_QUERY = {raw_query!r}\n"
            "def main():\n"
            "    if sys.argv[1:] != ['--hermes-channel-smoke']:\n"
            "        raise SystemExit('unsupported invocation')\n"
            "    if False:\n"
            "        subprocess.run([\n"
            "            'python3', '.fgv/scripts/hermes_catalog_query.py',\n"
            "            '--vault', VAULT,\n"
            "            '--query-type', os.environ['FGV_HERMES_QUERY_TYPE'],\n"
            "            '--subject-id', os.environ['FGV_HERMES_SUBJECT_ID'],\n"
            "            '--expected-catalog-sha256', os.environ['FGV_HERMES_EXPECTED_CATALOG_SHA256'],\n"
            "        ], check=True, capture_output=True)\n"
            "    consumed = hashlib.sha256(RAW_QUERY).hexdigest()\n"
            "    print(json.dumps({\n"
            "        'challenge': os.environ['FGV_HERMES_CHANNEL_CHALLENGE'],\n"
            "        'consumed_stdout_sha256': consumed,\n"
            "        'query_stdout_b64': base64.b64encode(RAW_QUERY).decode('ascii'),\n"
            "        'schema_version': 1,\n"
            "    }, sort_keys=True, separators=(',', ':')))\n"
            "    return 0\n"
            "if __name__ == '__main__':\n"
            "    raise SystemExit(main())\n",
            encoding="utf-8",
        )
        artifact = self.evidence_dir / "prebuilt-process-query.json"

        result = run_python(
            "hermes_channel_smoke.py",
            "--channel-id", "eclass",
            "--entrypoint", "scripts/eclass-scan.py",
            "--hermes-home", str(self.hermes_home),
            "--vault", str(self.package_root),
            "--tested-commit", self.tested_commit,
            "--as-of", self.operational_as_of,
            "--expected-path", LIVE_QUERY_EXPECTED["material-eclass"],
            "--artifact-out", str(artifact),
            env=self.validation_env,
        )

        self.assertNotEqual(result.returncode, 0)
        self.assertIn("authenticated bounded-query template", result.stdout)

    def test_channel_runner_uses_isolated_standard_library_imports(self) -> None:
        (self.hermes_home / "scripts/subprocess.py").write_text(
            "raise RuntimeError('local module must not load')\n", encoding="utf-8"
        )
        artifact = self.evidence_dir / "isolated-import-query.json"

        result = run_python(
            "hermes_channel_smoke.py",
            "--channel-id", "eclass",
            "--entrypoint", "scripts/eclass-scan.py",
            "--hermes-home", str(self.hermes_home),
            "--vault", str(self.package_root),
            "--tested-commit", self.tested_commit,
            "--as-of", self.operational_as_of,
            "--expected-path", LIVE_QUERY_EXPECTED["material-eclass"],
            "--artifact-out", str(artifact),
            env=self.validation_env,
        )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_channel_flow_executes_audited_bytes_after_path_swap(self) -> None:
        entrypoint = self.hermes_home / "scripts/eclass-scan.py"
        audited_payload = entrypoint.read_bytes()
        replacement = b"raise RuntimeError('swapped pathname executed')\n"
        captured: dict[str, bytes] = {}
        swap_state = {"done": False}
        real_catalog_pin = hermes_channel_smoke._catalog_pin
        real_runner = hermes_channel_smoke._run_pinned_channel_payload

        def catalog_pin_with_swap(vault: Path, operational_as_of: str) -> tuple[str, bytes]:
            result = real_catalog_pin(vault, operational_as_of)
            if not swap_state["done"]:
                entrypoint.write_bytes(replacement)
                swap_state["done"] = True
            return result

        def capture_runner(
            payload: bytes, *, vault: Path, environment: dict[str, str]
        ) -> subprocess.CompletedProcess[bytes]:
            captured["payload"] = payload
            return real_runner(payload, vault=vault, environment=environment)

        with (
            mock.patch.dict(os.environ, self.validation_env, clear=True),
            mock.patch.object(
                hermes_channel_smoke,
                "_catalog_pin",
                side_effect=catalog_pin_with_swap,
            ),
            mock.patch.object(
                hermes_channel_smoke,
                "_run_pinned_channel_payload",
                side_effect=capture_runner,
            ),
        ):
            receipt, _ = hermes_channel_smoke.execute_channel_flow(
                channel_id="eclass",
                entrypoint_relative="scripts/eclass-scan.py",
                hermes_home=self.hermes_home,
                vault=self.package_root,
                tested_commit=self.tested_commit,
                operational_as_of=self.operational_as_of,
                expected_path=LIVE_QUERY_EXPECTED["material-eclass"],
            )

        self.assertEqual(entrypoint.read_bytes(), replacement)
        self.assertEqual(captured["payload"], audited_payload)
        self.assertEqual(receipt["entrypoint_sha256"], hashlib.sha256(audited_payload).hexdigest())
        self.assertEqual(receipt["status"], "pass")

    def test_stale_report_untracked_production_or_tampered_evidence_is_blocked(self) -> None:
        report = dict(self.report)
        report["timestamp_utc"] = "2026-08-28T12:00:00Z"
        self.assertNotEqual(self.validate(report).returncode, 0)

        (self.production / "unexpected.bin").write_bytes(b"unexpected")
        self.assertNotEqual(self.validate(self.report).returncode, 0)
        (self.production / "unexpected.bin").unlink()

        self.evidence_paths["whatsapp_smoke"].write_bytes(b"tampered")
        self.assertNotEqual(self.validate(self.report).returncode, 0)

    def test_report_bundle_and_backup_hashes_are_enforced(self) -> None:
        self.assertNotEqual(self.validate(self.report, "0" * 64).returncode, 0)
        backup_file = next(path for path in self.backup.rglob("*") if path.is_file() and path != self.backup_manifest)
        backup_file.write_bytes(backup_file.read_bytes() + b"tampered")
        self.assertNotEqual(self.validate(self.report).returncode, 0)

    def test_canonical_live_query_set_is_loaded_and_bundle_pinned(self) -> None:
        queries = json.loads(self.package_queries.read_text(encoding="utf-8"))
        queries[0]["id"] = "substituted"
        self.package_queries.write_text(json.dumps(queries, ensure_ascii=False), encoding="utf-8")
        self.assertNotEqual(self.validate(self.report).returncode, 0)


class HermesPromptTests(unittest.TestCase):
    def setUp(self) -> None:
        self.prepare = (HERMES_DIR / "PROMPT-HERMES-PREPARAR.md").read_text(encoding="utf-8")
        self.cutover = (HERMES_DIR / "PROMPT-HERMES-CUTOVER.md").read_text(encoding="utf-8")
        self.template = (HERMES_DIR / "READINESS-REPORT-TEMPLATE.md").read_text(encoding="utf-8")

    def test_prepare_is_staging_only_and_evidence_complete(self) -> None:
        for marker in (
            "não altere produção", "SHA-256", "untracked", "clone separado", "cópia",
            "audit_hermes.py", "Eclass", "WhatsApp", "busca acadêmica", "READY", "BLOCKED",
            "OPERATIONAL_AS_OF", EXPECTED_UPSTREAM, EXPECTED_REMOTE_URL,
            EXPECTED_FETCH_REFSPEC, "hermes_catalog_query.py", "hermes_channel_smoke.py",
            "--staging-hermes", "catálogo completo",
        ):
            self.assertIn(marker, self.prepare)

    def test_cutover_is_blocked_without_ready_exact_commit(self) -> None:
        for marker in (
            "validate_hermes_readiness.py", "tested_commit", "READY", "working tree",
            "fgv-sync", "smoke", "rollback", "cron", "nunca use force push",
            "OPERATIONAL_AS_OF", EXPECTED_UPSTREAM, EXPECTED_REMOTE_URL,
            EXPECTED_FETCH_REFSPEC, "hermes_channel_smoke.py", "--staging-hermes",
        ):
            self.assertIn(marker, self.cutover)
        self.assertLess(self.cutover.index("validate_hermes_readiness.py"), self.cutover.index("Primeira mutação"))

    def test_report_template_has_required_evidence(self) -> None:
        for marker in (
            "timestamp_utc", "production_commit", "tested_commit", "backup", "untracked",
            "component_results", "query_timings", "context_tokens", "recommendation",
            "operational_as_of", "expected_upstream", "expected_remote_url",
            "catalog_query_bytes", "catalog_query_lines", "candidate_count",
            "catalog_query_artifact", "catalog_query_sha256", "byte a byte",
            "entrypoint_sha256", "challenge_sha256", "consumed_stdout_sha256",
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
    def make_vault(self, parent: Path, live_queries: bool) -> tuple[Path, str, Path]:
        vault = parent / "vault"
        shutil.copytree(RETRIEVAL_VAULT, vault)
        operational_as_of = current_operational_as_of()
        decoy_relative = (
            "10 Matérias/ContabilidadeFinanceira/Aulas/08.28/Material/"
            "Resumo - Decoy aninhado.md"
        )
        decoy = vault / decoy_relative
        decoy.parent.mkdir(parents=True, exist_ok=True)
        decoy.write_text("# Decoy\n", encoding="utf-8")
        catalog = vault / "30 Sistema/Estado/catalog.jsonl"
        with catalog.open("a", encoding="utf-8") as handle:
            handle.write(json.dumps({
                "date": "2099-12-31",
                "kind": "note",
                "note_type": "resumo",
                "path": decoy_relative,
                "record_type": "file",
                "schema_version": 1,
                "sha256": f"sha256:{hashlib.sha256(decoy.read_bytes()).hexdigest()}",
                "subject_ids": ["contabilidade-financeira"],
                "title": "Decoy aninhado",
            }, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
        set_fixture_as_of(vault, operational_as_of)
        gates = vault / ".fgv/scripts"
        gates.mkdir(parents=True)
        common = (
            "import argparse\n"
            "parser = argparse.ArgumentParser()\n"
            "parser.add_argument('--vault', required=True)\n"
            "parser.add_argument('--as-of', required=True)\n"
        )
        (gates / "generate_state.py").write_text(
            common + "parser.add_argument('--check', action='store_true')\nparser.parse_args()\n",
            encoding="utf-8",
        )
        (gates / "validate_vault.py").write_text(common + "parser.parse_args()\n", encoding="utf-8")
        if live_queries:
            query_target = vault / "30 Sistema/Hermes/retrieval-queries.json"
            query_target.parent.mkdir(parents=True)
            shutil.copyfile(FIXTURES / "retrieval-queries.json", query_target)
        subprocess.run(["git", "init"], cwd=vault, check=True, capture_output=True)
        subprocess.run(["git", "config", "user.email", "fixture@example.invalid"], cwd=vault, check=True)
        subprocess.run(["git", "config", "user.name", "Fixture"], cwd=vault, check=True)
        subprocess.run(["git", "add", "."], cwd=vault, check=True)
        subprocess.run(["git", "commit", "-m", "fixture"], cwd=vault, check=True, capture_output=True)
        subprocess.run(["git", "branch", "-M", "codex/vault-plan-b"], cwd=vault, check=True)
        remote = parent / "origin.git"
        subprocess.run(["git", "init", "--bare", str(remote)], check=True, capture_output=True)
        subprocess.run(["git", "remote", "add", "origin", str(remote)], cwd=vault, check=True)
        subprocess.run(
            ["git", "push", "-u", "origin", "codex/vault-plan-b"],
            cwd=vault,
            check=True,
            capture_output=True,
        )
        subprocess.run(["git", "remote", "set-url", "origin", EXPECTED_REMOTE_URL], cwd=vault, check=True)
        configure_canonical_fetch_binding(vault)
        actual_commit = subprocess.run(
            ["git", "rev-parse", "HEAD"], cwd=vault, text=True, capture_output=True, check=True
        ).stdout.strip()
        return vault, actual_commit, remote

    def smoke_env(self, parent: Path, remote: Path) -> dict[str, str]:
        wrapper = install_git_transport_wrapper(parent / "smoke-git-wrapper")
        environment = os.environ.copy()
        environment.update(
            FGV_TEST_REMOTE_PATH=str(remote),
            PATH=str(wrapper) + os.pathsep + environment.get("PATH", ""),
        )
        return environment

    def test_queries_are_catalog_first_exact_and_provenanced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            vault, actual_commit, remote = self.make_vault(parent, live_queries=False)
            result = run_python(
                "hermes_retrieval_smoke.py",
                "--vault", str(vault),
                "--queries", str(FIXTURES / "retrieval-queries.json"),
                "--expected-commit", TEST_COMMIT,
                "--as-of", current_operational_as_of(),
                "--fixture-mode",
                env=self.smoke_env(parent, remote),
            )
            self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
            report = json.loads(result.stdout)
            self.assertEqual(report["status"], "pass")
            self.assertEqual(report["as_of_commit"], actual_commit)
            self.assertTrue(report["stale"])
            self.assertEqual(report["state_check"], "pass")
            self.assertTrue(report["fixture_mode"])
            self.assertEqual(report["operational_as_of"], current_operational_as_of())
            for query in report["queries"]:
                self.assertEqual(
                    query["steps"][:3],
                    ["dashboard_snapshot", "catalog_query", "dashboard_snapshot_recheck"],
                )
                self.assertLessEqual(len(query["opened_files"]), 1)
                self.assertNotIn("filesystem_scan", query["steps"])
                self.assertTrue(query["matched"])
                self.assertLessEqual(query["catalog_query_bytes"], MAX_CATALOG_QUERY_BYTES)
                self.assertLessEqual(query["catalog_query_lines"], MAX_CATALOG_QUERY_LINES)
                self.assertLessEqual(query["candidate_count"], MAX_CATALOG_CANDIDATES)

    def test_live_queries_are_distinct_existing_and_require_fresh_commit(self) -> None:
        live_path = HERMES_DIR / "retrieval-queries.json"
        self.assertNotEqual(live_path.read_bytes(), (FIXTURES / "retrieval-queries.json").read_bytes())
        live_queries = json.loads(live_path.read_text(encoding="utf-8"))
        self.assertEqual(
            {query["id"]: query["expected_path"] for query in live_queries},
            LIVE_QUERY_EXPECTED,
        )
        self.assertEqual([query["id"] for query in live_queries], list(LIVE_QUERY_EXPECTED))
        for query in live_queries:
            self.assertTrue((ROOT / query["expected_path"]).is_file(), query["expected_path"])
        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            vault, actual_commit, remote = self.make_vault(parent, live_queries=True)
            smoke_env = self.smoke_env(parent, remote)
            canonical_queries = vault / "30 Sistema/Hermes/retrieval-queries.json"
            fresh = run_python(
                "hermes_retrieval_smoke.py",
                "--vault", str(vault),
                "--queries", str(canonical_queries),
                "--expected-commit", actual_commit,
                "--as-of", current_operational_as_of(),
                env=smoke_env,
            )
            self.assertEqual(fresh.returncode, 0, fresh.stdout + fresh.stderr)
            self.assertEqual(json.loads(fresh.stdout)["sync_state"], "clean")

            subprocess.run(
                ["git", "config", "remote.origin.pushurl", "https://github.com/attacker/fgv-vault.git"],
                cwd=vault,
                check=True,
            )
            wrong_push_remote = run_python(
                "hermes_retrieval_smoke.py",
                "--vault", str(vault),
                "--queries", str(canonical_queries),
                "--expected-commit", actual_commit,
                "--as-of", current_operational_as_of(),
                env=smoke_env,
            )
            self.assertNotEqual(wrong_push_remote.returncode, 0)
            self.assertIn("push URL", wrong_push_remote.stdout)
            subprocess.run(
                ["git", "config", "--unset-all", "remote.origin.pushurl"],
                cwd=vault,
                check=True,
            )

            rewrite_key = f"url.{(Path(tmp) / 'origin.git').resolve().as_uri()}.insteadOf"
            subprocess.run(
                ["git", "config", rewrite_key, EXPECTED_REMOTE_URL], cwd=vault, check=True
            )
            rewritten_remote = run_python(
                "hermes_retrieval_smoke.py",
                "--vault", str(vault),
                "--queries", str(canonical_queries),
                "--expected-commit", actual_commit,
                "--as-of", current_operational_as_of(),
                env=smoke_env,
            )
            self.assertNotEqual(rewritten_remote.returncode, 0)
            self.assertIn("rewrite", rewritten_remote.stdout)
            subprocess.run(
                ["git", "config", "--unset-all", rewrite_key], cwd=vault, check=True
            )

            subprocess.run(
                ["git", "config", "branch.codex/vault-plan-b.merge", "refs/heads/evil"],
                cwd=vault,
                check=True,
            )
            subprocess.run(
                [
                    "git", "config", "remote.origin.fetch",
                    "+refs/heads/evil:refs/remotes/origin/codex/vault-plan-b",
                ],
                cwd=vault,
                check=True,
            )
            evil_source = run_python(
                "hermes_retrieval_smoke.py",
                "--vault", str(vault),
                "--queries", str(canonical_queries),
                "--expected-commit", actual_commit,
                "--as-of", current_operational_as_of(),
                env=smoke_env,
            )
            self.assertNotEqual(evil_source.returncode, 0)
            self.assertIn("branch source", evil_source.stdout)
            subprocess.run(
                [
                    "git", "config", "branch.codex/vault-plan-b.merge",
                    "refs/heads/codex/vault-plan-b",
                ],
                cwd=vault,
                check=True,
            )
            subprocess.run(
                ["git", "config", "remote.origin.fetch", EXPECTED_FETCH_REFSPEC],
                cwd=vault,
                check=True,
            )

            stale = run_python(
                "hermes_retrieval_smoke.py",
                "--vault", str(vault),
                "--queries", str(canonical_queries),
                "--expected-commit", TEST_COMMIT,
                "--as-of", current_operational_as_of(),
                env=smoke_env,
            )
            self.assertNotEqual(stale.returncode, 0)
            stale_report = json.loads(stale.stdout)
            self.assertEqual(stale_report["status"], "blocked")
            self.assertTrue(stale_report["stale"])

            stale_date = (
                date.fromisoformat(current_operational_as_of()) - timedelta(days=1)
            ).isoformat()
            stale_snapshot = run_python(
                "hermes_retrieval_smoke.py",
                "--vault", str(vault),
                "--queries", str(canonical_queries),
                "--expected-commit", actual_commit,
                "--as-of", stale_date,
                env=smoke_env,
            )
            self.assertNotEqual(stale_snapshot.returncode, 0)
            self.assertIn("as_of", stale_snapshot.stdout)

            set_fixture_as_of(vault, stale_date)
            subprocess.run(["git", "add", "30 Sistema/Estado"], cwd=vault, check=True)
            subprocess.run(["git", "commit", "-m", "stale catalog"], cwd=vault, check=True, capture_output=True)
            subprocess.run(
                ["git", "push", str(Path(tmp) / "origin.git"), "HEAD:refs/heads/codex/vault-plan-b"],
                cwd=vault,
                check=True,
                capture_output=True,
            )
            subprocess.run(
                ["git", "update-ref", "refs/remotes/origin/codex/vault-plan-b", "HEAD"],
                cwd=vault,
                check=True,
            )
            stale_commit = subprocess.run(
                ["git", "rev-parse", "HEAD"], cwd=vault, text=True, capture_output=True, check=True
            ).stdout.strip()
            stale_current = run_python(
                "hermes_retrieval_smoke.py",
                "--vault", str(vault),
                "--queries", str(canonical_queries),
                "--expected-commit", stale_commit,
                "--as-of", current_operational_as_of(),
                env=smoke_env,
            )
            self.assertNotEqual(stale_current.returncode, 0)
            self.assertIn("catalog as_of", stale_current.stdout)

    def test_smoke_rejects_catalog_swap_after_snapshot_authentication(self) -> None:
        import hermes_retrieval_smoke as smoke_module

        with tempfile.TemporaryDirectory() as tmp:
            parent = Path(tmp)
            vault, actual_commit, remote = self.make_vault(parent, live_queries=True)
            canonical_queries = vault / "30 Sistema/Hermes/retrieval-queries.json"
            query_payload = canonical_queries.read_bytes()
            target_relative = str(json.loads(query_payload)[0]["expected_path"])

            def swap_catalog(_args: object) -> bytes:
                target = vault / target_relative
                target.write_text("# conteúdo trocado após autenticação\n", encoding="utf-8")
                catalog = vault / "30 Sistema/Estado/catalog.jsonl"
                records = [json.loads(line) for line in catalog.read_text(encoding="utf-8").splitlines()]
                for record in records:
                    if record.get("record_type") == "file" and record.get("path") == target_relative:
                        record["sha256"] = "sha256:" + hashlib.sha256(target.read_bytes()).hexdigest()
                catalog.write_text(
                    "".join(
                        json.dumps(record, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n"
                        for record in records
                    ),
                    encoding="utf-8",
                )
                return query_payload

            argv = [
                "hermes_retrieval_smoke.py",
                "--vault", str(vault),
                "--queries", str(canonical_queries),
                "--expected-commit", actual_commit,
                "--as-of", current_operational_as_of(),
            ]
            output = io.StringIO()
            environment = self.smoke_env(parent, remote)
            with (
                mock.patch.object(smoke_module, "load_queries", side_effect=swap_catalog),
                mock.patch.object(smoke_module.sys, "argv", argv),
                mock.patch.dict(os.environ, environment, clear=True),
                redirect_stdout(output),
            ):
                returncode = smoke_module.main()

        report = json.loads(output.getvalue())
        self.assertNotEqual(returncode, 0)
        self.assertEqual(report["status"], "blocked")
        self.assertIn("catalog", report["reason"])


class HermesCatalogQueryTests(unittest.TestCase):
    def test_query_rejects_catalog_hash_mismatch(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            shutil.copytree(RETRIEVAL_VAULT, vault)
            result = run_python(
                "hermes_catalog_query.py",
                "--vault", str(vault),
                "--query-type", "latest_class",
                "--expected-catalog-sha256", "0" * 64,
            )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("changed after snapshot", result.stdout)

    def test_query_returns_only_manifest_and_bounded_direct_lesson_candidates(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            shutil.copytree(RETRIEVAL_VAULT, vault)
            set_fixture_as_of(vault, current_operational_as_of())
            catalog = vault / "30 Sistema/Estado/catalog.jsonl"
            with catalog.open("a", encoding="utf-8") as handle:
                for decoy_path in (
                    "10 Matérias/ContabilidadeFinanceira/Aulas/Material/Resumo - Decoy.md",
                    "10 Matérias/Grupo/ContabilidadeFinanceira/Aulas/08.29/Resumo - Decoy profundo.md",
                ):
                    handle.write(json.dumps({
                        "date": "2099-12-31",
                        "path": decoy_path,
                        "record_type": "file",
                        "schema_version": 1,
                        "sha256": "sha256:" + "0" * 64,
                        "subject_ids": ["contabilidade-financeira"],
                    }, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
            result = run_python(
                "hermes_catalog_query.py",
                "--vault", str(vault),
                "--query-type", "latest_class",
                "--subject-id", "contabilidade-financeira",
                "--limit", str(MAX_CATALOG_CANDIDATES),
                "--expected-catalog-sha256", hashlib.sha256(catalog.read_bytes()).hexdigest(),
            )

        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)
        self.assertLessEqual(len(result.stdout.encode("utf-8")), MAX_CATALOG_QUERY_BYTES)
        self.assertLessEqual(len(result.stdout.splitlines()), MAX_CATALOG_QUERY_LINES)
        payload = json.loads(result.stdout)
        self.assertEqual(set(payload), {"candidates", "manifest", "schema_version"})
        self.assertLessEqual(len(payload["candidates"]), MAX_CATALOG_CANDIDATES)
        self.assertEqual(payload["manifest"]["as_of"], current_operational_as_of())
        self.assertEqual(
            payload["candidates"][0]["path"],
            "10 Matérias/ContabilidadeFinanceira/Aulas/08.28/Resumo - DRE e provisões.md",
        )
        self.assertNotIn("records", payload)

    def test_material_depth_and_low_mastery_subject_are_exact(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            vault = Path(tmp) / "vault"
            shutil.copytree(RETRIEVAL_VAULT, vault)
            catalog = vault / "30 Sistema/Estado/catalog.jsonl"
            with catalog.open("a", encoding="utf-8") as handle:
                handle.write(json.dumps({
                    "date": "2099-12-31",
                    "path": "10 Matérias/Grupo/ContabilidadeFinanceira/Aulas/08.29/Material/Decoy.pdf",
                    "record_type": "file",
                    "schema_version": 1,
                    "sha256": "sha256:" + "0" * 64,
                    "subject_ids": ["contabilidade-financeira"],
                }, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")
                handle.write(json.dumps({
                    "concept": "Target",
                    "concept_path": "20 Conhecimento/Conceitos/Target.md",
                    "last_status": "parcial",
                    "record_type": "learning_state",
                    "schema_version": 1,
                    "subject": "estatistica-2",
                }, ensure_ascii=False, sort_keys=True, separators=(",", ":")) + "\n")

            material = run_python(
                "hermes_catalog_query.py",
                "--vault", str(vault),
                "--query-type", "eclass_material",
                "--subject-id", "contabilidade-financeira",
                "--expected-catalog-sha256", hashlib.sha256(catalog.read_bytes()).hexdigest(),
            )
            mastery = run_python(
                "hermes_catalog_query.py",
                "--vault", str(vault),
                "--query-type", "low_mastery_concept",
                "--subject-id", "estatistica-2",
                "--expected-catalog-sha256", hashlib.sha256(catalog.read_bytes()).hexdigest(),
            )

        self.assertEqual(material.returncode, 0, material.stdout + material.stderr)
        self.assertEqual(
            json.loads(material.stdout)["candidates"][0]["path"],
            "10 Matérias/ContabilidadeFinanceira/Aulas/08.28/Material/Slides - DRE.extracted.md",
        )
        self.assertEqual(mastery.returncode, 0, mastery.stdout + mastery.stderr)
        self.assertEqual(
            json.loads(mastery.stdout)["candidates"][0]["subject"],
            "estatistica-2",
        )


if __name__ == "__main__":
    unittest.main()
