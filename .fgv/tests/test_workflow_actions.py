import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from fgv_workflow.calendar import build_calendar_intent, queue_intent
from fgv_workflow.concepts import ConceptCandidate, apply_concept_candidates
from fgv_workflow.tasks import TaskMention, append_tasks


class WorkflowActionTests(unittest.TestCase):
    def test_concepts_require_gate_and_queue_is_idempotent(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            root = Path(temporary_directory)
            concepts = root / "20 Conhecimento" / "Conceitos"
            queue = root / "30 Sistema" / "Estado" / "concept-candidates.jsonl"
            candidates = (
                ConceptCandidate("Termo incidental", False, False, 1, False, False),
                ConceptCandidate("Provisão", True, False, 1, False, False),
            )
            first = apply_concept_candidates(
                candidates,
                concepts_dir=concepts,
                queue_path=queue,
                subject_id="contabilidade-financeira",
                transaction_id="tx-1",
            )
            second = apply_concept_candidates(
                candidates,
                concepts_dir=concepts,
                queue_path=queue,
                subject_id="contabilidade-financeira",
                transaction_id="tx-1",
            )
            self.assertEqual([item.action for item in first], ["queue", "create"])
            self.assertEqual([item.action for item in second], ["queue", "link_existing"])
            self.assertEqual(len(queue.read_text(encoding="utf-8").splitlines()), 1)
            note = concepts / "Provisão.md"
            original = note.read_text(encoding="utf-8")
            apply_concept_candidates(
                (ConceptCandidate("Provisão", True, True, 5, True, True),),
                concepts_dir=concepts,
                queue_path=queue,
                subject_id="contabilidade-financeira",
                transaction_id="tx-2",
            )
            self.assertEqual(note.read_text(encoding="utf-8"), original)

    def test_tasks_require_concrete_date_and_deduplicate(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "00 Home" / "Tasks.md"
            mention = TaskMention(
                "Prova parcial de Contabilidade",
                "2026-09-04",
                "#cont",
                "🔺",
            )
            self.assertEqual(append_tasks(path, (mention, mention), "tx-1"), 1)
            self.assertEqual(append_tasks(path, (mention,), "tx-2"), 0)
            text = path.read_text(encoding="utf-8")
            self.assertEqual(text.count("Prova parcial"), 1)
            with self.assertRaises(ValueError):
                append_tasks(
                    path,
                    (TaskMention("Leitura", "próxima aula", "#cont", ""),),
                    "tx-3",
                )

    def test_task_deduplicates_equivalent_existing_line_without_marker(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            path = Path(temporary_directory) / "00 Home" / "Tasks.md"
            path.parent.mkdir(parents=True)
            path.write_text(
                "# Tasks\n\n"
                "- [ ] Prova parcial de Contabilidade #cont 📅 2026-09-04 🔺\n",
                encoding="utf-8",
            )
            mention = TaskMention(
                "Prova parcial de Contabilidade",
                "2026-09-04",
                "#cont",
                "🔺",
            )
            self.assertEqual(append_tasks(path, (mention,), "tx-1"), 0)
            self.assertEqual(
                path.read_text(encoding="utf-8").count("Prova parcial"),
                1,
            )

    def test_calendar_is_intent_only_confirmable_and_idempotent(self) -> None:
        with TemporaryDirectory() as temporary_directory:
            queue = Path(temporary_directory) / "calendar-intents.jsonl"
            intent = build_calendar_intent(
                transaction_id="tx-1",
                action="reschedule",
                calendar_alias="classes",
                payload={"event_id": "event-1", "start": "2026-09-05T11:00:00-03:00"},
            )
            self.assertTrue(intent.requires_confirmation)
            self.assertEqual(intent.status, "pending")
            self.assertTrue(queue_intent(queue, intent))
            self.assertFalse(queue_intent(queue, intent))
            row = json.loads(queue.read_text(encoding="utf-8"))
            self.assertEqual(row["action_id"], intent.action_id)
            self.assertNotIn("applied_at", row)


if __name__ == "__main__":
    unittest.main()
