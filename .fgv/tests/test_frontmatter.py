import unittest

from fgv_state.frontmatter import parse_markdown_metadata


class FrontmatterTests(unittest.TestCase):
    def test_normalizes_metadata_and_derives_class_date(self):
        text = """---
materia: ContabilidadeFinanceira
materias: [ProdutosFinanceiros, ContabilidadeFinanceira]
tema: DRE, provisões e arrendamentos
tags: [resumo, prova]
status: completo
dominio: 1
proxima_revisao: 2026-08-29
---
# Revisão final PP1
"""
        metadata = parse_markdown_metadata(
            text, "10 Matérias/ContabilidadeFinanceira/Aulas/08.27/Resumo - DRE.md", "2026.2"
        )
        self.assertEqual(metadata.subjects_raw, ("ContabilidadeFinanceira", "ProdutosFinanceiros"))
        self.assertEqual(metadata.date, "2026-08-27")
        self.assertEqual(metadata.date_source, "path")
        self.assertEqual(metadata.note_type, "resumo")
        self.assertEqual(metadata.mastery, 1)
        self.assertEqual(metadata.review_due, "2026-08-29")

    def test_invalid_frontmatter_is_partial_and_warns(self):
        metadata = parse_markdown_metadata(
            "---\ntags: [resumo\ndata: ontem\ndominio: 8\n---\n# Nota\n",
            "10 Matérias/Psicologia/Nota.md",
            "2026.2",
        )
        self.assertEqual(metadata.title, "Nota")
        self.assertIsNone(metadata.date)
        self.assertIsNone(metadata.mastery)
        self.assertGreaterEqual(len(metadata.warnings), 2)

    def test_block_lists_and_concept_type(self):
        metadata = parse_markdown_metadata(
            "---\nmaterias:\n  - MatemáticaAplicada\ntags:\n  - cálculo\n---\n# Assíntota\n",
            "20 Conhecimento/Conceitos/Assíntota.md",
            "2026.2",
        )
        self.assertEqual(metadata.subjects_raw, ("MatemáticaAplicada",))
        self.assertEqual(metadata.note_type, "conceito")

    def test_ambiguous_yaml_constructs_are_ignored_with_warnings(self):
        metadata = parse_markdown_metadata(
            """---
tags: [primeira]
tags: [segunda]
tema: valor # comentário ambíguo
aliases: &nomes [A, B]
status: *estado
descricao: >-
  texto dobrado
title: "Hash # literal"
---
# Fallback
""",
            "10 Matérias/Psicologia/Nota.md",
            "2026.2",
        )
        self.assertEqual(metadata.tags, ("primeira",))
        self.assertIsNone(metadata.topic)
        self.assertEqual(metadata.aliases, ())
        self.assertIsNone(metadata.status)
        self.assertEqual(metadata.title, "Hash # literal")
        warnings = "\n".join(metadata.warnings)
        self.assertIn("duplicate frontmatter key: tags", warnings)
        self.assertIn("inline comment", warnings)
        self.assertIn("anchor or alias", warnings)
        self.assertIn("block scalar", warnings)


if __name__ == "__main__":
    unittest.main()
