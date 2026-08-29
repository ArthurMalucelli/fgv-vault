import hashlib
import json
from datetime import date, datetime, timezone
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from fgv_workflow.date_resolution import DateEvidence, resolve_class_date
from fgv_workflow.naming import artifact_path, lesson_dir
from fgv_workflow.plaud import AnalysisError, process_plaud
from fgv_workflow.source_store import make_transaction_id
from fgv_workflow.subjects import SubjectRegistry


ANALYSIS = {
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

    def test_process_preserves_raw_and_is_idempotent(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "downloads" / "Plaud export.txt"
            source.parent.mkdir()
            raw = b"Speaker 1: DRE e provisoes.\r\n\x00fim\n"
            source.write_bytes(raw)
            vault = root / "vault"
            timestamp = datetime(2026, 8, 28, 18, 30, tzinfo=timezone.utc)

            first = process_plaud(
                vault_root=vault,
                source=source,
                class_date=date(2026, 8, 28),
                analysis=ANALYSIS,
                processor="test",
                ingested_at=timestamp,
            )
            second = process_plaud(
                vault_root=vault,
                source=source,
                class_date=date(2026, 8, 28),
                analysis=ANALYSIS,
                processor="test",
                ingested_at=timestamp,
            )

            self.assertTrue(first.created)
            self.assertFalse(second.created)
            self.assertEqual(source.read_bytes(), raw)
            self.assertEqual(first.raw_path.read_bytes(), raw)
            self.assertEqual(first.transaction_id, second.transaction_id)
            self.assertEqual(
                {path.name for path in first.artifacts},
                {
                    "Transcrito - DRE e provisões.md",
                    "Resumo - DRE e provisões.md",
                },
            )
            lesson = first.raw_path.parents[1]
            self.assertEqual(len(tuple(lesson.glob("Transcrito - *.md"))), 1)
            self.assertEqual(len(tuple(lesson.glob("Resumo - *.md"))), 1)
            manifest = json.loads(first.manifest_path.read_text(encoding="utf-8"))
            self.assertEqual(len(manifest["sources"]), 1)
            for artifact in first.artifacts:
                text = artifact.read_text(encoding="utf-8")
                self.assertIn("materias: [contabilidade-financeira]", text)
                self.assertIn("semestre: 2026.2", text)
                self.assertIn("data: 2026-08-28", text)
                self.assertIn("tema: DRE e provisões", text)
                self.assertIn("status: completo", text)
                self.assertIn("contract_version: 1", text)
                self.assertIn(f"transaction_id: {first.transaction_id}", text)
                self.assertIn("source_sha256: ", text)

    def test_analysis_gate_runs_before_any_write(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            source = root / "input.txt"
            source.write_text("raw", encoding="utf-8")
            invalid = dict(ANALYSIS)
            invalid["review_questions"] = ["uma"]
            with self.assertRaisesRegex(AnalysisError, "5 to 10"):
                process_plaud(
                    vault_root=root / "vault",
                    source=source,
                    class_date=date(2026, 8, 28),
                    analysis=invalid,
                    processor="test",
                    ingested_at=datetime(2026, 8, 28, tzinfo=timezone.utc),
                )
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
