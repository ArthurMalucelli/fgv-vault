import json
import tempfile
import unittest
from pathlib import Path

from fgv_state.config import ConfigError, load_settings, resolve_subject_ids


class StateConfigTests(unittest.TestCase):
    def test_consumes_the_existing_registry_shape(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / "subjects.json"
            path.write_text(json.dumps({
                "schema_version": 1,
                "semester": "2026.2",
                "timezone": "America/Sao_Paulo",
                "subjects": [{
                    "id": "contabilidade-financeira",
                    "display_name": "Contabilidade Financeira",
                    "folder": "ContabilidadeFinanceira",
                    "path": "10 Matérias/ContabilidadeFinanceira",
                    "task_tag": "#cont",
                    "aliases": ["cont"],
                    "legacy_frontmatter_values": ["ContabilidadeFinanceira"],
                }],
            }, ensure_ascii=False), encoding="utf-8")
            settings = load_settings(path)
        self.assertEqual(settings.subjects[0].name, "Contabilidade Financeira")
        self.assertEqual(settings.subjects[0].task_tag, "cont")
        self.assertEqual(
            resolve_subject_ids(["ContabilidadeFinanceira"], "", settings),
            ("contabilidade-financeira",),
        )

    def test_rejects_duplicate_and_unsafe_subject_contracts(self):
        base = {
            "schema_version": 1,
            "semester": "2026.2",
            "timezone": "America/Sao_Paulo",
            "subjects": [{
                "id": "subject-a", "display_name": "A", "folder": "A",
                "path": "10 Matérias/A", "task_tag": "#a", "aliases": [],
                "legacy_frontmatter_values": [],
            }],
        }
        for mutation in ("duplicate", "unsafe"):
            with self.subTest(mutation=mutation), tempfile.TemporaryDirectory() as tmp:
                payload = json.loads(json.dumps(base))
                if mutation == "duplicate":
                    payload["subjects"].append(dict(payload["subjects"][0]))
                else:
                    payload["subjects"][0]["path"] = "../A"
                path = Path(tmp) / "subjects.json"
                path.write_text(json.dumps(payload), encoding="utf-8")
                with self.assertRaises(ConfigError):
                    load_settings(path)


if __name__ == "__main__":
    unittest.main()
