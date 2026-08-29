from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import unittest
from unittest.mock import patch


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import import_live_delta as live_delta
import rewrite_paths


ROOT = Path(__file__).resolve().parents[2]


class LiveDeltaImportTests(unittest.TestCase):
    def test_tip_tree_entry_must_match_mode_type_and_blob(self) -> None:
        record = live_delta.RECORDS[0]
        live_delta._assert_source_at_tip(
            ROOT,
            str(record["source"]),
            str(record["source_blob_oid"]),
        )
        with self.assertRaises(live_delta.ImportError):
            live_delta._assert_source_at_tip(
                ROOT,
                str(record["source"]),
                "0" * 40,
            )

    def test_hostile_git_environment_is_ignored(self) -> None:
        with patch.dict(
            live_delta.os.environ,
            {
                "GIT_DIR": "/definitely/not/the/fgv/repository",
                "GIT_WORK_TREE": "/definitely/not/the/fgv/worktree",
                "GIT_REPLACE_OBJECTS": "1",
            },
            clear=False,
        ):
            outputs, _ = live_delta.build_outputs(ROOT)
        self.assertEqual(len(outputs), 13)

    def test_pinned_blobs_build_exact_outputs(self) -> None:
        outputs, manifest_bytes = live_delta.build_outputs(ROOT)
        self.assertEqual(len(outputs), 13)
        manifest = json.loads(manifest_bytes)
        self.assertEqual(manifest["schema"], "fgv.live-delta.v1")
        self.assertEqual(
            manifest["source_tip_commit"],
            "cf8fe8c440a4dd442490afee62c0119a7db5ef9c",
        )
        self.assertEqual(manifest["record_count"], 13)
        self.assertEqual(manifest["metadata_transform_count"], 9)
        self.assertEqual(manifest["byte_identical_count"], 4)
        self.assertEqual(manifest["body_transform_count"], 0)
        self.assertEqual(
            [record["destination"] for record in manifest["records"]],
            sorted(
                (record["destination"] for record in manifest["records"]),
                key=lambda value: value.encode("utf-8"),
            ),
        )
        digest_input = dict(manifest)
        aggregate = digest_input.pop("aggregate_sha256")
        canonical = json.dumps(
            digest_input, ensure_ascii=False, sort_keys=True, separators=(",", ":")
        ).encode("utf-8")
        self.assertEqual(aggregate, hashlib.sha256(canonical).hexdigest())
        for record in manifest["records"]:
            relative = Path(record["destination"])
            payload = outputs[live_delta.PurePosixPath(record["destination"])]
            self.assertEqual(record["final_sha256"], hashlib.sha256(payload).hexdigest())
            self.assertEqual(record["original_body_sha256"], record["final_body_sha256"])
            self.assertFalse(relative.is_absolute())

        classes = {
            record["destination"]: record["content_class"]
            for record in manifest["records"]
        }
        self.assertEqual(
            sum(value == "metadata_transform" for value in classes.values()), 9
        )
        self.assertEqual(
            sum(value == "byte-identical" for value in classes.values()), 4
        )

    def test_upgrade_authority_accepts_only_the_exact_previous_generation(self) -> None:
        revision = live_delta.PurePosixPath(
            "10 Matérias/ContabilidadeFinanceira/Aulas/08.28/"
            "Revisao - Revisão de erros dos quizzes (Delícia Gelada, Sing's, "
            "Nosso Doce Amor, Lojas Paulistas).md"
        )
        previous = bytes(
            live_delta._git(
                ROOT,
                "show",
                f"47370c028d1a93d0d9d2941e4a3e148f050e8fcb:{revision}",
                binary=True,
            )
        )
        self.assertEqual(
            live_delta._classify_existing(revision, previous, b"next"), "upgrade"
        )
        with self.assertRaises(live_delta.ImportError):
            live_delta._classify_existing(revision, b"tampered", b"next")

    def test_check_is_non_mutating_or_authenticated_no_op(self) -> None:
        before = {
            relative: (ROOT / relative).read_bytes()
            for relative in (*[live_delta.PurePosixPath(item["destination"]) for item in live_delta.RECORDS], live_delta.MANIFEST)
            if (ROOT / relative).is_file()
        }
        status = live_delta.apply(ROOT, check=True)
        after = {
            relative: (ROOT / relative).read_bytes()
            for relative in (*[live_delta.PurePosixPath(item["destination"]) for item in live_delta.RECORDS], live_delta.MANIFEST)
            if (ROOT / relative).is_file()
        }
        self.assertIn(status, {"planned", "no_op"})
        self.assertEqual(before, after)

    def test_live_delta_preserves_exact_link_contract(self) -> None:
        outputs, _ = live_delta.build_outputs(ROOT)
        structural = json.loads(
            (ROOT / "30 Sistema/Estado/migration-manifest.json").read_bytes()
        )
        combined = [
            *structural,
            *({"destination": item["destination"]} for item in live_delta.RECORDS),
        ]
        _, root_fd = rewrite_paths._open_vault(ROOT)
        try:
            projected = {
                str(relative): payload
                for relative, payload in outputs.items()
                if str(relative).casefold().endswith(".md")
            }
            links = rewrite_paths.audit_projected_links(
                root_fd, combined, projected
            )
        finally:
            live_delta.os.close(root_fd)
        self.assertEqual(
            (links.total, links.resolved, links.unresolved, links.ambiguous),
            (5442, 5035, 407, 0),
        )


if __name__ == "__main__":
    unittest.main()
