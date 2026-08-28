import importlib
import json
from pathlib import Path, PurePosixPath
import unicodedata
import unittest


ROOT = Path(__file__).resolve().parents[2]
FGV = ROOT / ".fgv"

EXPECTED_SUBJECT_PATHS = {
    "contabilidade-financeira": "10 Matérias/ContabilidadeFinanceira",
    "direito-empresarial": "10 Matérias/DireitoEmpresarial",
    "estatistica-2": "10 Matérias/Estatistica2",
    "estudos-organizacionais": "10 Matérias/EstudosOrganizacionais",
    "matematica-aplicada": "10 Matérias/MatemáticaAplicada",
    "psicologia": "10 Matérias/Psicologia",
    "tecnologia-dados-negocios": "10 Matérias/TecnologiaDadosNegocios",
}


def accent_insensitive(value: str) -> str:
    decomposed = unicodedata.normalize("NFKD", value.strip().casefold())
    return "".join(character for character in decomposed if not unicodedata.combining(character))


class WorkflowContractTests(unittest.TestCase):
    def load_json(self, relative_path: str) -> dict:
        raw = (FGV / relative_path).read_text(encoding="utf-8")
        payload = json.loads(raw)
        self.assertIsInstance(payload, dict)
        return payload

    def test_contract_version_file_and_python_export_match(self) -> None:
        self.assertEqual((FGV / "VERSION").read_text(encoding="utf-8"), "1\n")
        module = importlib.import_module("fgv_workflow")
        self.assertEqual(module.CONTRACT_VERSION, 1)

    def test_core_declares_every_normative_invariant(self) -> None:
        text = (FGV / "CORE.md").read_text(encoding="utf-8")
        required_text = (
            "único contrato de máquina editável",
            "raw Plaud é imutável",
            "origem externa nunca é apagada",
            "transaction_id é determinístico",
            "Matéria ou data ambígua interrompe qualquer escrita",
            "reexecução da mesma transação é no-op",
            "outra transaction_id",
            "CalendarIntent entra primeiro em uma fila",
            "cancelamento ou reagendamento exige confirmação explícita",
            "critério explícito de promoção",
            "Codex e Claude nunca executam Git de rede",
            "Obsidian Git é o único owner de Git no Mac",
            "fgv-sync é o único owner de Git no VPS",
            "catálogo e o snapshot do dashboard têm um único writer",
            "Todos os paths são NFC",
            "Aulas/MM.DD",
            "Transcrito - <tema>.md",
            "Resumo - <tema>.md",
            "Revisao - <tema>.md",
            "ano permanece no YAML e nos IDs",
            "instalação live",
            "merge em main",
        )
        for invariant in required_text:
            with self.subTest(invariant=invariant):
                self.assertIn(invariant, text)
        self.assertNotIn("\N{EM DASH}", text)

    def test_subject_registry_has_exact_current_subjects_and_paths(self) -> None:
        payload = self.load_json("config/subjects.json")
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(payload["semester"], "2026.2")
        self.assertEqual(payload["timezone"], "America/Sao_Paulo")

        subjects = payload["subjects"]
        self.assertIsInstance(subjects, list)
        self.assertEqual(len(subjects), 7)
        by_id = {subject["id"]: subject for subject in subjects}
        self.assertEqual(set(by_id), set(EXPECTED_SUBJECT_PATHS))

        for subject_id, expected_path in EXPECTED_SUBJECT_PATHS.items():
            subject = by_id[subject_id]
            with self.subTest(subject=subject_id):
                self.assertTrue(
                    {
                        "id",
                        "display_name",
                        "folder",
                        "path",
                        "task_tag",
                        "aliases",
                        "legacy_frontmatter_values",
                    }.issubset(subject)
                )
                self.assertIsInstance(subject["display_name"], str)
                self.assertTrue(subject["display_name"])
                self.assertEqual(subject["path"], expected_path)
                self.assertEqual(PurePosixPath(expected_path).name, subject["folder"])
                self.assertTrue(subject["task_tag"].startswith("#"))
                self.assertIn(subject["folder"], subject["aliases"])
                self.assertTrue(subject["legacy_frontmatter_values"])
                self.assertTrue(
                    all(isinstance(value, str) and value for value in subject["aliases"])
                )
                self.assertTrue(
                    all(
                        isinstance(value, str) and value
                        for value in subject["legacy_frontmatter_values"]
                    )
                )

    def test_subject_paths_are_unique_relative_and_nfc(self) -> None:
        subjects = self.load_json("config/subjects.json")["subjects"]
        paths = [subject["path"] for subject in subjects]
        self.assertEqual(len(paths), len(set(paths)))
        for path in paths:
            with self.subTest(path=path):
                parsed = PurePosixPath(path)
                self.assertFalse(parsed.is_absolute())
                self.assertNotIn("..", parsed.parts)
                self.assertEqual(path, unicodedata.normalize("NFC", path))

    def test_aliases_are_unique_after_accent_insensitive_normalization(self) -> None:
        subjects = self.load_json("config/subjects.json")["subjects"]
        aliases = [alias for subject in subjects for alias in subject["aliases"]]
        normalized = [accent_insensitive(alias) for alias in aliases]
        self.assertTrue(all(normalized))
        self.assertEqual(len(normalized), len(set(normalized)))

    def test_sync_ownership_enforces_host_boundaries(self) -> None:
        payload = self.load_json("config/sync-ownership.json")
        self.assertEqual(payload["schema_version"], 1)
        self.assertEqual(set(payload["roles"]), {"mac-agent", "hermes-sync"})

        mac = payload["roles"]["mac-agent"]
        self.assertEqual(mac["git_owner"], "obsidian-git")
        self.assertEqual(set(mac["allowed"]), {"read", "status", "sync_pending"})
        self.assertTrue(
            {"fetch", "pull", "merge", "rebase", "commit", "push"}.issubset(
                mac["denied"]
            )
        )

        hermes = payload["roles"]["hermes-sync"]
        self.assertEqual(hermes["git_owner"], "fgv-sync")
        self.assertEqual(
            set(hermes["allowed"]),
            {"status", "fetch", "merge-ff-only", "commit-scoped", "push"},
        )
        self.assertEqual(hermes["retry_push_rejection"], 1)
        self.assertIs(hermes["force_push"], False)

        self.assertEqual(
            payload["single_writer"],
            {
                "catalog": ".fgv/scripts/generate_state.py",
                "dashboard": ".fgv/scripts/generate_state.py",
            },
        )

    def test_no_second_editable_core_exists(self) -> None:
        self.assertFalse((ROOT / "30 Sistema" / "Skills" / "fgv-core").exists())


if __name__ == "__main__":
    unittest.main()
