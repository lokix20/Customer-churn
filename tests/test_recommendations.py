"""
Unit tests for recommendations and risk tiers.
"""

import unittest
from src.recommendations import get_risk_tier, get_recommendations, SAMPLE_PERSONAS


class TestRecommendations(unittest.TestCase):
    def test_risk_tiers(self):
        self.assertEqual(get_risk_tier(0.65), "HIGH")
        self.assertEqual(get_risk_tier(0.35), "MEDIUM")
        self.assertEqual(get_risk_tier(0.10), "LOW")

    def test_recommendation_generation(self):
        cust = {
            "Contract": "Month-to-month",
            "TechSupport": "No",
            "OnlineSecurity": "No",
            "PaymentMethod": "Electronic check",
            "tenure": 2
        }
        recs = get_recommendations(cust, churn_prob=0.75)
        self.assertGreaterEqual(len(recs), 3)
        actions = [r["action"] for r in recs]
        self.assertIn("Contract Upgrade Incentive", actions)
        self.assertIn("Complimentary Tech Support Add-on", actions)

    def test_personas_exist(self):
        self.assertGreaterEqual(len(SAMPLE_PERSONAS), 3)


if __name__ == "__main__":
    unittest.main()
