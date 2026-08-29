from dataclasses import asdict
import unittest

from fgv_workflow.calendar import build_calendar_intent
from fgv_workflow.concepts import ConceptCandidate, should_promote
from fgv_workflow.tasks import TaskMention, make_task_id, validate_task_fields


class WorkflowActionTests(unittest.TestCase):
    def test_concepts_require_explicit_promotion_gate(self) -> None:
        incidental = ConceptCandidate("Termo", False, False, 1, False, False)
        assessed = ConceptCandidate("Provisão", False, True, 1, False, False)
        recurring = ConceptCandidate("DRE", False, False, 2, False, False)
        self.assertFalse(should_promote(incidental))
        self.assertTrue(should_promote(assessed))
        self.assertTrue(should_promote(recurring))

    def test_task_identity_is_deterministic_and_fields_are_strict(self) -> None:
        mention = TaskMention(
            "Prova parcial de Contabilidade",
            "2026-09-04",
            "#cont",
            "🔺",
        )
        validate_task_fields(mention)
        self.assertEqual(
            make_task_id(mention.description, mention.due, mention.tag),
            make_task_id(mention.description, mention.due, mention.tag),
        )
        with self.assertRaises(ValueError):
            validate_task_fields(
                TaskMention("linha 1\nlinha 2", "2026-09-04", "#cont", "")
            )
        with self.assertRaises(ValueError):
            validate_task_fields(TaskMention("Leitura", "próxima aula", "#cont", ""))

    def test_calendar_intent_is_deterministic_pending_and_confirmable(self) -> None:
        first = build_calendar_intent(
            transaction_id="tx-1",
            action="reschedule",
            calendar_alias="classes",
            payload={"event_id": "event-1", "start": "2026-09-05T11:00:00-03:00"},
        )
        second = build_calendar_intent(
            transaction_id="tx-1",
            action="reschedule",
            calendar_alias="classes",
            payload={"event_id": "event-1", "start": "2026-09-05T11:00:00-03:00"},
        )
        self.assertEqual(asdict(first), asdict(second))
        self.assertTrue(first.requires_confirmation)
        self.assertEqual(first.status, "pending")


if __name__ == "__main__":
    unittest.main()
