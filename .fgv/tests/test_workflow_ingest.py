import hashlib
from datetime import date
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from fgv_workflow.date_resolution import DateEvidence, resolve_class_date
from fgv_workflow.naming import artifact_path, lesson_dir
from fgv_workflow.plaud import AnalysisError, validate_analysis
from fgv_workflow.source_store import make_transaction_id
from fgv_workflow.subjects import SubjectRegistry


ANALYSIS = {
    "schema_version": 1,
    "subject_id": "contabilidade-financeira",
    "topic": "DRE e provisões",
    "cleaned_transcript": (
        "## Competência\n\n"
        "Provisão afeta competência agora e caixa quando houver pagamento.\n"
    ),
    "summary": (
        "## Conceitos essenciais\n\n"
        "| Item | O que é |\n|---|---|\n"
        "| Provisão | Reconhecimento por competência. |\n\n"
        "## Pegadinhas\n\n- Provisão não implica saída imediata de caixa.\n"
    ),
    "topics": ["DRE", "provisões", "competência"],
    "review_questions": [
        "Quando a provisão afeta a DRE?",
        "Quando a provisão afeta o caixa?",
        "Qual é o efeito no balanço?",
        "Qual é a diferença entre competência e caixa?",
        "Como reconciliar DRE e DFC?",
    ],
    "concept_candidates": [],
    "task_mentions": [],
    "calendar_mentions": [],
}


class WorkflowIngestTests(unittest.TestCase):
    def test_subject_alias_and_naming_follow_contract(self) -> None:
        registry = SubjectRegistry.load_default()
        subject = registry.resolve("Contabilidade")
        self.assertEqual(subject.id, "contabilidade-financeira")
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            lesson = lesson_dir(root, subject, date(2026, 8, 28))
            self.assertEqual(
                lesson.relative_to(root).as_posix(),
                "10 Matérias/ContabilidadeFinanceira/Aulas/08.28",
            )
            result = artifact_path(lesson, "resumo", "DRE e provisões")
            self.assertEqual(result.name, "Resumo - DRE e provisões.md")
            self.assertNotIn("2026", result.name)

    def test_transaction_id_uses_canonical_bytes(self) -> None:
        digest = "0" * 64
        expected = hashlib.sha256(
            b"\x00".join(
                (
                    b"fgv:v1",
                    digest.encode("ascii"),
                    b"contabilidade-financeira",
                    b"2026-08-28",
                )
            )
        ).hexdigest()[:20]
        self.assertEqual(
            make_transaction_id(digest, "contabilidade-financeira", "2026-08-28"),
            expected,
        )

    def test_analysis_gate_runs_before_any_write(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "input.txt"
            source.write_text("raw", encoding="utf-8")
            invalid = dict(ANALYSIS)
            invalid["review_questions"] = ["uma"]
            with self.assertRaisesRegex(AnalysisError, "5 to 10"):
                validate_analysis(invalid)
            self.assertFalse((root / "vault").exists())

    def test_date_resolution_never_uses_mtime_alone(self) -> None:
        weak = DateEvidence("mtime", "2026-08-28", 0.4, "fixture")
        result = resolve_class_date((weak,))
        self.assertEqual(result.status, "ambiguous")
        self.assertIsNone(result.value)

        explicit = DateEvidence("explicit", "2026-08-28", 1.0, "user")
        result = resolve_class_date((weak, explicit))
        self.assertEqual(result.status, "resolved")
        self.assertEqual(result.value, "2026-08-28")


if __name__ == "__main__":
    unittest.main()
