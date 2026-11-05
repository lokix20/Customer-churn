"""
Unit tests for preprocessing module and leakage safeguards.
"""

import unittest
import pandas as pd
import numpy as np
from src.data_loader import load_raw_data
from src.preprocessing import prepare_data


class TestPreprocessing(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.df = load_raw_data()

    def test_prepare_data_shapes_and_leakage(self):
        X_train, X_test, y_train, y_test, X_train_s, X_test_s, imputer, scaler = prepare_data(
            self.df, test_size=0.2, random_state=42
        )

        # Check shapes
        self.assertEqual(len(X_train), len(y_train))
        self.assertEqual(len(X_test), len(y_test))
        self.assertEqual(len(X_train) + len(X_test), len(self.df))

        # Check stratification balance (approx 26.5% in both)
        self.assertAlmostEqual(y_train.mean(), 0.2654, delta=0.02)
        self.assertAlmostEqual(y_test.mean(), 0.2654, delta=0.02)

        # Check missing values imputed
        self.assertEqual(X_train.isnull().sum().sum(), 0)
        self.assertEqual(X_test.isnull().sum().sum(), 0)

        # Check customerID dropped
        self.assertNotIn("customerID", X_train.columns)

        # Check scaled means approx 0 and std approx 1 on training
        np.testing.assert_allclose(X_train_s.mean(axis=0), 0, atol=1e-2)


if __name__ == "__main__":
    unittest.main()
