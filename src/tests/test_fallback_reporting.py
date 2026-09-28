"""Focused contract for evaluation-scoped fallback reporting."""

import unittest

import numpy as np

from timebench.evaluation.fallback import summarize_fallbacks


class FallbackReportingTests(unittest.TestCase):
    def test_counts_and_reasons_use_only_evaluated_rows(self):
        summary = summarize_fallbacks(
            np.array([True, True, True, False]),
            np.array([True, False, True, True]),
            {0: "nonfinite", 1: "insufficient_history", 2: "nonfinite"},
        )

        self.assertEqual(summary["fallback_count"], 2)
        self.assertEqual(summary["evaluated_rows"], 3)
        self.assertEqual(summary["all_fallback_rows"], 3)
        self.assertEqual(summary["fallback_reasons"], {"nonfinite": 2})

    def test_every_evaluated_fallback_requires_a_reason(self):
        with self.assertRaisesRegex(ValueError, "have no reason"):
            summarize_fallbacks(
                np.array([True, True]),
                np.array([True, False]),
                {1: "outside_evaluation"},
            )


if __name__ == "__main__":
    unittest.main()
