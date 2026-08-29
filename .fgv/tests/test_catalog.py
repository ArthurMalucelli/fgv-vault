import json
import tempfile
import unittest
from pathlib import Path

from fgv_state.catalog import _ensure_unique_normalized_paths, build_catalog, serialize_catalog
from fgv_state.config import load_settings


class CatalogTests(unittest.TestCase):
    def make_vault(self, root: Path) -> Path:
        vault = root / "vault"
        files = {
            ".fgv/config/subjects.json": json.dumps({
                "schema_version": 1, "semester": "2026.2", "timezone": "America/Sao_Paulo",
                "subjects": [{"id": "contabilidade-financeira", "display_name": "Contabilidade Financeira",
                              "folder": "ContabilidadeFinanceira", "path": "10 Matérias/ContabilidadeFinanceira",
                              "task_tag": "#cont", "aliases": ["cont"],
                              "legacy_frontmatter_values": ["ContabilidadeFinanceira"]}],
            }, ensure_ascii=False),
            "00 Home/Home.md": "# Home\n",
            "00 Home/Tasks.md": "```\n- [ ] exemplo #cont\n```\n- [ ] Prova #cont 📅 2026-08-28\n",
            "10 Matérias/ContabilidadeFinanceira/Aulas/08.27/Resumo - DRE.md": "---\nmateria: ContabilidadeFinanceira\nstatus: completo\n---\n# DRE\n",
            "10 Matérias/ContabilidadeFinanceira/Aulas/08.28/Materiais/Slides.pdf": "today material",
            "10 Matérias/ContabilidadeFinanceira/Aulas/08.29/Transcrito - Futuro.md": "# Futuro\n",
            "20 Conhecimento/Conceitos/DRE.md": "---\nmaterias: [ContabilidadeFinanceira]\n---\n# DRE\n",
            "30 Sistema/Tutor/concepts-history.json": json.dumps({"DRE": {"subject": "ContabilidadeFinanceira", "times_probed": 1, "last_status": "parcial"}}),
            "30 Sistema/Plans/secret.md": "never index",
            "30 Sistema/Estado/old.md": "never index",
            "30 Sistema/Estado/.generation.lock": "",
            "90 Arquivo/2026.1/ProdutosFinanceiros/Aulas/05.20/Resumo.md": "---\nmateria: ProdutosFinanceiros\n---\n# RF\n",
        }
        for relative, content in files.items():
            path = vault / relative
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(content, encoding="utf-8")
        return vault

    def test_allowlist_indexes_academic_roots_and_separates_archive(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = self.make_vault(Path(tmp))
            settings = load_settings(vault / ".fgv/config/subjects.json")
            build = build_catalog(vault, settings, "2026-08-28")
        files = [r for r in build.records if r["record_type"] == "file"]
        paths = {r["path"] for r in files}
        self.assertIn("90 Arquivo/2026.1/ProdutosFinanceiros/Aulas/05.20/Resumo.md", paths)
        self.assertNotIn("30 Sistema/Plans/secret.md", paths)
        self.assertNotIn("30 Sistema/Estado/old.md", paths)
        archived = next(r for r in files if r["path"].startswith("90 Arquivo/"))
        self.assertEqual(archived["scope"], "archive")
        self.assertEqual(archived["semester"], "2026.1")

    def test_serialization_is_deterministic_and_manifest_first(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = self.make_vault(Path(tmp))
            settings = load_settings(vault / ".fgv/config/subjects.json")
            first = serialize_catalog(build_catalog(vault, settings, "2026-08-28"), settings)
            second = serialize_catalog(build_catalog(vault, settings, "2026-08-28", reverse_walk_for_test=True), settings)
        self.assertEqual(first, second)
        records = [json.loads(line) for line in first.decode().splitlines()]
        self.assertEqual(records[0]["record_type"], "manifest")
        self.assertEqual(sum(r["record_type"] == "task" for r in records), 1)

    def test_nfc_collision_is_fatal(self):
        with self.assertRaises(ValueError):
            _ensure_unique_normalized_paths(["Café.md", "Cafe\u0301.md"])


if __name__ == "__main__":
    unittest.main()
