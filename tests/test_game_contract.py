"""Checks the written contract and evaluation data, never simulated model outputs.

Behavioral safety, playability, and reasoning quality need recorded assistant
transcripts and human review, as described in docs/evaluation.md.
"""

import json
import unittest

from scripts import validate


class GameContractTests(unittest.TestCase):
    def test_all_four_modes_have_one_canonical_definition(self):
        self.assertEqual(validate.validate_modes(validate.ROOT), [])

    def test_evaluation_corpus_is_well_formed_and_diverse(self):
        self.assertEqual(validate.validate_fixtures(validate.ROOT), [])

    def test_default_response_contract_remains_present(self):
        # Presence is a documentation regression check, not proof of obedience.
        text = validate.read_text(validate.ROOT / validate.SKILL_PATH / "SKILL.md")
        for label in ("Your Objective", "The Loophole", "The AI's Interpretation",
                      "The Catastrophe", "Failure Mechanism", "Plausibility", "The Fix", "Your Turn"):
            with self.subTest(label=label):
                self.assertIn(f"**{label}:**", text)

    def test_multi_turn_cases_have_reviewable_outcomes(self):
        data = json.loads(validate.read_text(validate.ROOT / "tests/fixtures/objectives.json"))
        iterative = [case for case in data["cases"] if len(case["turns"]) > 1]
        self.assertGreaterEqual(len(iterative), 3)
        for case in iterative:
            with self.subTest(case=case["id"]):
                self.assertGreaterEqual(len(case["expected"]), 2)
                self.assertGreaterEqual(len(case["forbidden"]), 1)
                self.assertGreater(len(set(case["turns"])), 1)


if __name__ == "__main__":
    unittest.main()
