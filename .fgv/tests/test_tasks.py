import json
import tempfile
import unittest
from pathlib import Path

from fgv_state.config import load_settings
from fgv_state.tasks import parse_tasks


class TaskTests(unittest.TestCase):
    def settings(self, root: Path):
        path = root / "subjects.json"
        path.write_text(json.dumps({
            "schema_version": 1, "semester": "2026.2", "timezone": "America/Sao_Paulo",
            "subjects": [{"id": "contabilidade-financeira", "display_name": "Contabilidade Financeira",
                          "folder": "ContabilidadeFinanceira", "path": "10 Matérias/ContabilidadeFinanceira",
                          "task_tag": "#cont", "aliases": [], "legacy_frontmatter_values": []}],
        }), encoding="utf-8")
        return load_settings(path)

    def test_parses_real_tasks_but_ignores_fenced_examples(self):
        text = """# Tasks
```
- [ ] Exemplo #cont 📅 2026-08-01
```
- [ ] Prova #cont 📅 2026-08-28 🔺
- [x] Feita #cont ✅ 2026-08-27
- [ ] Casa #casa
"""
        with tempfile.TemporaryDirectory() as tmp:
            records = parse_tasks(text, "00 Home/Tasks.md", self.settings(Path(tmp)))
        self.assertEqual([record["description"] for record in records], ["Prova", "Feita", "Casa"])
        self.assertEqual(records[0]["subject_ids"], ["contabilidade-financeira"])
        self.assertEqual(records[0]["priority"], "highest")
        self.assertEqual(records[0]["source_line"], 5)

    def test_invalid_date_is_warning_not_crash(self):
        with tempfile.TemporaryDirectory() as tmp:
            record = parse_tasks("- [ ] Prova #cont 📅 2026-02-30\n", "00 Home/Tasks.md", self.settings(Path(tmp)))[0]
        self.assertIsNone(record["due"])
        self.assertEqual(record["warnings"], ["invalid due date: 2026-02-30"])


if __name__ == "__main__":
    unittest.main()
