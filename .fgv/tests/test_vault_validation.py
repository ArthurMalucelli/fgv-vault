from __future__ import annotations

import hashlib
import json
from pathlib import Path
import sys
import unittest


SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, SCRIPTS.as_posix())

import validate_vault


ROOT = Path(__file__).resolve().parents[2]


class VaultValidationTests(unittest.TestCase):
    def test_runtime_packages_are_hash_bound_and_bundle_verified(self) -> None:
        report = validate_vault.validate(ROOT, "2026-08-28")
        packages = report["packages"]
        self.assertTrue(packages["adapter_parity"])
        self.assertRegex(packages["adapter_semantic_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(packages["hermes_manifest_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(packages["hermes_prepare_bundle_sha256"], r"^[0-9a-f]{64}$")
        self.assertRegex(packages["hermes_cutover_bundle_sha256"], r"^[0-9a-f]{64}$")

    def test_integrated_content_chain_and_state_are_certifiable(self) -> None:
        report = validate_vault.validate(ROOT, "2026-08-28", require_packages=False)
        self.assertEqual(report["status"], "pass")
        self.assertEqual(report["counts"]["structural_records"], 1059)
        self.assertEqual(report["counts"]["byte_identical"], 1008)
        self.assertEqual(report["counts"]["lesson_metadata_only"], 40)
        self.assertEqual(report["counts"]["authorized_body_transforms"], 11)
        self.assertEqual(report["counts"]["live_delta_records"], 13)
        self.assertEqual(report["counts"]["files"], 1036)
        self.assertFalse(
            any("untracked" in item for item in report["known_limitations"])
        )
        digest_payload = dict(report)
        digest = digest_payload.pop("aggregate_sha256")
        canonical = json.dumps(
            digest_payload,
            ensure_ascii=False,
            sort_keys=True,
            separators=(",", ":"),
        ).encode("utf-8")
        self.assertEqual(digest, hashlib.sha256(canonical).hexdigest())

    def test_noncanonical_as_of_is_rejected(self) -> None:
        with self.assertRaises(validate_vault.ValidationError):
            validate_vault.validate(ROOT, "20260828", require_packages=False)


if __name__ == "__main__":
    unittest.main()
