from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import import_live_delta as live_delta
import rewrite_paths


ROOT = Path(__file__).resolve().parents[2]


class LiveDeltaImportTests(unittest.TestCase):
    def test_pinned_blobs_build_exact_outputs(self) -> None:
        outputs, manifest_bytes = live_delta.build_outputs(ROOT)
        self.assertEqual(len(outputs), 5)
        manifest = json.loads(manifest_bytes)
        self.assertEqual(manifest["schema"], "fgv.live-delta.v1")
        self.assertEqual(manifest["record_count"], 5)
        self.assertEqual(manifest["metadata_transform_count"], 5)
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
        structural = json.loads(
            (ROOT / "30 Sistema/Estado/migration-manifest.json").read_bytes()
        )
        combined = [
            *structural,
            *({"destination": item["destination"]} for item in live_delta.RECORDS),
        ]
        _, root_fd = rewrite_paths._open_vault(ROOT)
        try:
            links = rewrite_paths.audit_projected_links(root_fd, combined, {})
        finally:
            live_delta.os.close(root_fd)
        self.assertEqual(
            (links.total, links.resolved, links.unresolved, links.ambiguous),
            (5442, 5035, 407, 0),
        )


if __name__ == "__main__":
    unittest.main()
