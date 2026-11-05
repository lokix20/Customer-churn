"""
Unit tests for CLV calculations.
"""

import unittest
from src.clv import calculate_clv, calculate_simple_clv


class TestCLV(unittest.TestCase):
    def test_calculate_clv_high_vs_low_risk(self):
        # Low risk customer (low churn prob) should have higher CLV than high risk
        low_risk = calculate_clv(monthly_charges=70.0, tenure=24, churn_prob=0.05)
        high_risk = calculate_clv(monthly_charges=70.0, tenure=2, churn_prob=0.85)

        self.assertGreater(low_risk["clv_value"], high_risk["clv_value"])
        self.assertGreater(low_risk["expected_remaining_months"], high_risk["expected_remaining_months"])

    def test_simple_clv(self):
        # 40% margin, 90% retention, 10% discount rate
        clv = calculate_simple_clv(monthly_charges=100.0, retention_rate=0.9, horizon_years=3)
        self.assertGreater(clv, 0.0)


if __name__ == "__main__":
    unittest.main()
