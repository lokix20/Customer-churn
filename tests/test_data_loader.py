"""
Unit tests for data_loader module.
"""

import unittest
import os
import pandas as pd
from src.data_loader import load_raw_data, DEFAULT_DATA_PATH


class TestDataLoader(unittest.TestCase):
    def test_load_raw_data(self):
        df = load_raw_data()
        self.assertIsInstance(df, pd.DataFrame)
        self.assertGreater(len(df), 1000)
        self.assertIn("Churn", df.columns)
        self.assertIn("MonthlyCharges", df.columns)
        self.assertIn("tenure", df.columns)


if __name__ == "__main__":
    unittest.main()
