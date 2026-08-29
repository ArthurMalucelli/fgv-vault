from __future__ import annotations

import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[2]


class NavigationShellTests(unittest.TestCase):
    def test_visible_roots_are_closed_and_sort_home_first(self) -> None:
        visible = sorted(
            path.name for path in ROOT.iterdir() if not path.name.startswith(".")
        )
        self.assertEqual(
            visible,
            ["00 Home", "10 Matérias", "20 Conhecimento", "30 Sistema", "90 Arquivo"],
        )

    def test_every_active_subject_has_one_shell(self) -> None:
        registry = json.loads((ROOT / ".fgv/config/subjects.json").read_text())
        subjects = registry["subjects"]
        self.assertEqual(len(subjects), 7)
        for subject in subjects:
            shell = ROOT / subject["path"] / "Disciplina.md"
            text = shell.read_text()
            self.assertIn(f"materias: [{subject['id']}]", text)
            self.assertIn(f"# {subject['display_name']}", text)
            self.assertIn("[[00 Home/Tasks|Tasks]]", text)

    def test_home_navigation_shells_exist(self) -> None:
        revisions = (ROOT / "00 Home/Revisões.md").read_text()
        inbox = (ROOT / "00 Home/Inbox/README.md").read_text()
        self.assertIn("# Revisões", revisions)
        self.assertIn("fonte canônica", inbox)


if __name__ == "__main__":
    unittest.main()
