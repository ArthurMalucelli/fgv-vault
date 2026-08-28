import hashlib
import importlib
import json
import os
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch


try:
    migration_links = importlib.import_module("fgv_migration.links")
except ModuleNotFoundError:
    migration_links = None


ROOT = Path(__file__).resolve().parents[2]
REAL_MANIFEST = ROOT / "30 Sistema/Estado/migration-manifest.json"
REAL_BASELINE = ROOT / "30 Sistema/Estado/migration-baseline.json"
REAL_BASE_COMMIT = "a7f7d58a5fcbbee86c90a046eb30e168217b5c78"


def manifest_record(path: str, data: bytes) -> dict[str, object]:
    return {
        "schema_version": 1,
        "source": path,
        "destination": f"00 Home/Inbox/Legado/{path}",
        "sha256": hashlib.sha256(data).hexdigest(),
        "size_bytes": len(data),
        "category": "home",
        "phase": "structural",
        "reason": "test fixture",
    }


class LinkAuditFixtureTests(unittest.TestCase):
    def require_auditor(self):
        self.assertIsNotNone(migration_links, "deterministic link auditor is missing")
        return migration_links

    def test_wikilink_cleaning_resolution_and_classification(self) -> None:
        auditor = self.require_auditor()
        notes = {
            "Folder/Current.md": "\n".join(
                (
                    "[[Target|alias]]",
                    "[[Target#Heading]]",
                    "[[Target#^block]]",
                    "[[Encoded%20Note]]",
                    "[[/Root/Absolute.md]]",
                    "[[Relative.md]]",
                    "[[Shared]]",
                    "[[case note]]",
                    "[[Cafe\u0301]]",
                    "![[Missing]]",
                    "[[#Heading]]",
                    "[[Missing]]",
                    "[[Sub\\Backslash.md]]",
                )
            ),
            "Folder/Target.md": "",
            "Encoded Note.md": "",
            "Root/Absolute.md": "",
            "Folder/Relative.md": "",
            "A/Shared.md": "",
            "B/Shared.md": "",
            "Case Note.md": "",
            "Caf\u00e9.md": "",
            "Sub/Backslash.md": "",
        }

        result = auditor.audit_note_contents(notes)

        self.assertEqual(
            result.as_dict(),
            {
                "total": 12,
                "resolved": 10,
                "unresolved": 1,
                "ambiguous": 1,
            },
        )

    def test_git_environment_and_unlisted_files_cannot_change_audit(self) -> None:
        auditor = self.require_auditor()
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            repository_a = root / "repo-a"
            repository_b = root / "repo-b"
            repository_a.mkdir()
            repository_b.mkdir()
            for repository in (repository_a, repository_b):
                subprocess.run(("git", "init", "-q"), cwd=repository, check=True)
                subprocess.run(
                    ("git", "config", "user.name", "Fixture"),
                    cwd=repository,
                    check=True,
                )
                subprocess.run(
                    ("git", "config", "user.email", "fixture@example.invalid"),
                    cwd=repository,
                    check=True,
                )

            source_data = b"[[Tasks]]\n"
            (repository_a / "Tasks.md").write_bytes(source_data)
            (repository_a / "Unlisted.md").write_bytes(b"[[Missing]]\n")
            (repository_b / "Tasks.md").write_bytes(b"[[Missing]]\n")
            for repository in (repository_a, repository_b):
                subprocess.run(("git", "add", "."), cwd=repository, check=True)
                subprocess.run(
                    ("git", "commit", "-qm", "fixture"),
                    cwd=repository,
                    check=True,
                )
            commit_a = subprocess.run(
                ("git", "rev-parse", "HEAD"),
                cwd=repository_a,
                check=True,
                stdout=subprocess.PIPE,
                text=True,
            ).stdout.strip()
            hostile_environment = {
                "GIT_DIR": str(repository_b / ".git"),
                "GIT_WORK_TREE": str(repository_b),
                "GIT_CONFIG_COUNT": "1",
                "GIT_CONFIG_KEY_0": "core.quotePath",
                "GIT_CONFIG_VALUE_0": "true",
            }

            with patch.dict(os.environ, hostile_environment, clear=False):
                result = auditor.audit_manifest_links(
                    repository_a,
                    commit_a,
                    [manifest_record("Tasks.md", source_data)],
                )

        self.assertEqual(
            result.as_dict(),
            {"total": 1, "resolved": 1, "unresolved": 0, "ambiguous": 0},
        )


class RealLinkAuditTests(unittest.TestCase):
    def test_fixed_commit_reproduces_the_link_integrity_baseline(self) -> None:
        self.assertIsNotNone(migration_links, "deterministic link auditor is missing")
        manifest = json.loads(REAL_MANIFEST.read_bytes())

        result = migration_links.audit_manifest_links(
            ROOT,
            REAL_BASE_COMMIT,
            manifest,
        )

        self.assertEqual(
            result.as_dict(),
            {
                "total": 5402,
                "resolved": 4991,
                "unresolved": 408,
                "ambiguous": 3,
            },
        )
        self.assertEqual(
            result.total,
            result.resolved + result.unresolved + result.ambiguous,
        )
        baseline = json.loads(REAL_BASELINE.read_bytes())
        self.assertEqual(
            baseline["wikilinks"],
            {"method": migration_links.AUDIT_METHOD, **result.as_dict()},
        )


if __name__ == "__main__":
    unittest.main()
