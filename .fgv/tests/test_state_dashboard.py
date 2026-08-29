import hashlib
import tempfile
import unittest
from pathlib import Path

from test_catalog import CatalogTests
from fgv_state.catalog import build_catalog, serialize_catalog
from fgv_state.config import load_settings
from fgv_state.dashboard import render_dashboard


class DashboardTests(unittest.TestCase):
    def test_filters_future_classes_and_archived_learning_from_active_sections(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = CatalogTests().make_vault(Path(tmp))
            settings = load_settings(vault / ".fgv/config/subjects.json")
            build = build_catalog(vault, settings, "2026-08-28")
            catalog = serialize_catalog(build, settings)
            output = render_dashboard(build.records, settings, "2026-08-28", build.build_fingerprint,
                                      "sha256:" + hashlib.sha256(catalog).hexdigest())
        self.assertIn("# Painel", output)
        self.assertIn("Prova", output)
        self.assertIn("08.27", output)
        self.assertIn("### Aulas de hoje, processamento pendente", output)
        today_section = output.split("### Aulas de hoje, processamento pendente", 1)[1].split("### Aulas sem transcrito", 1)[0]
        historical_missing = output.split("### Aulas sem transcrito", 1)[1].split("### Aulas com material e sem resumo", 1)[0]
        historical_material = output.split("### Aulas com material e sem resumo", 1)[1].split(
            "## Revisões vencidas", 1
        )[0]
        self.assertIn("08.28", today_section)
        self.assertIn("sem transcrito; com material e sem resumo", today_section)
        self.assertIn("`Contabilidade Financeira 08.28`", today_section)
        self.assertNotIn("Material/Resumo - Leitura", today_section)
        self.assertNotIn("08.28", historical_missing)
        self.assertNotIn("08.29", output)
        self.assertIn("Contabilidade Financeira 08.25", historical_material)
        self.assertIn("Contabilidade Financeira 08.24", historical_material)
        self.assertNotIn("Material/Leitura", historical_material)
        self.assertIn("Aprendizagem ativa", output)
        self.assertIn("Aprendizagem arquivada", output)
        self.assertNotIn("- [ ]", output)

    def test_only_direct_lesson_notes_count_as_summary_or_transcript(self):
        with tempfile.TemporaryDirectory() as tmp:
            vault = CatalogTests().make_vault(Path(tmp))
            material = vault / "10 Matérias/ContabilidadeFinanceira/Aulas/08.27/Material"
            material.mkdir(parents=True, exist_ok=True)
            (material / "Transcrito - Leitura.md").write_text("# Apoio\n", encoding="utf-8")
            settings = load_settings(vault / ".fgv/config/subjects.json")
            build = build_catalog(vault, settings, "2026-08-28")
            catalog = serialize_catalog(build, settings)
            output = render_dashboard(
                build.records,
                settings,
                "2026-08-28",
                build.build_fingerprint,
                "sha256:" + hashlib.sha256(catalog).hexdigest(),
            )

        historical_missing = output.split("### Aulas sem transcrito", 1)[1].split(
            "### Aulas com material e sem resumo", 1
        )[0]
        self.assertIn("Contabilidade Financeira 08.27", historical_missing)
        self.assertNotIn("Material/Transcrito - Leitura", historical_missing)


if __name__ == "__main__":
    unittest.main()
