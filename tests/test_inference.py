"""
Unit tests for model inference and feature building.
"""

import unittest
import pandas as pd
from src.inference import predictor, ChurnPredictor
from src.config import FEATURE_NAMES


class TestInference(unittest.TestCase):
    def setUp(self):
        self.sample_customer = {
            "tenure": 3,
            "MonthlyCharges": 80.0,
            "TotalCharges": 240.0,
            "Contract": "Month-to-month",
            "InternetService": "Fiber optic",
            "TechSupport": "No",
            "PaymentMethod": "Electronic check"
        }

    def test_feature_vector_builder(self):
        vec = ChurnPredictor.build_feature_vector(self.sample_customer)
        self.assertIsInstance(vec, pd.DataFrame)
        self.assertEqual(list(vec.columns), FEATURE_NAMES)
        self.assertEqual(len(vec), 1)
        self.assertEqual(vec["tenure"].iloc[0], 3.0)
        self.assertEqual(vec["MonthlyCharges"].iloc[0], 80.0)

    def test_predict_churn_evaluation(self):
        result = predictor.evaluate_customer(self.sample_customer)
        self.assertIn("churn_probability", result)
        self.assertIn("risk_tier", result)
        self.assertIn("clv", result)
        self.assertIn("recommendations", result)

        self.assertGreaterEqual(result["churn_probability"], 0.0)
        self.assertLessEqual(result["churn_probability"], 1.0)
        self.assertIn(result["risk_tier"], ["HIGH", "MEDIUM", "LOW"])


if __name__ == "__main__":
    unittest.main()
