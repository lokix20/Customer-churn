"""
IBM Telco Customer Churn & CLV Machine Learning Package.
"""

from src.config import RANDOM_STATE, FEATURE_NAMES, MODEL_PATH, RAW_DATA_PATH
from src.data_loader import download_dataset, load_raw_data
from src.preprocessing import prepare_data
from src.inference import predictor, ChurnPredictor
from src.clv import calculate_clv, calculate_simple_clv
from src.recommendations import get_recommendations, get_risk_tier, SAMPLE_PERSONAS

__all__ = [
    "RANDOM_STATE",
    "FEATURE_NAMES",
    "MODEL_PATH",
    "RAW_DATA_PATH",
    "download_dataset",
    "load_raw_data",
    "prepare_data",
    "predictor",
    "ChurnPredictor",
    "calculate_clv",
    "calculate_simple_clv",
    "get_recommendations",
    "get_risk_tier",
    "SAMPLE_PERSONAS",
]
