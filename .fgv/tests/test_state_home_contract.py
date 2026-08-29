import unittest
from pathlib import Path


ROOT = Path(__file__).resolve().parents[2]


class HomeContractTests(unittest.TestCase):
    def test_home_is_human_owned_shell_with_generated_embed(self):
        home = (ROOT / "00 Home/Home.md").read_text(encoding="utf-8")
        self.assertIn("tipo: dashboard", home)
        self.assertIn("contract_version: 1", home)
        self.assertIn("[[00 Home/Tasks|Tasks]]", home)
        self.assertIn("![[30 Sistema/Estado/dashboard-snapshot#Painel]]", home)
        self.assertNotIn("GENERATED FILE", home)

    def test_state_readme_declares_ownership_and_fallback(self):
        readme = (ROOT / "30 Sistema/Estado/README.md").read_text(encoding="utf-8")
        self.assertIn("único escritor", readme)
        self.assertIn("fonte canônica", readme)
        self.assertIn("filesystem", readme)
        self.assertIn("fallback", readme)


if __name__ == "__main__":
    unittest.main()
