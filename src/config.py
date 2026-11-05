"""
Centralized Configuration for IBM Telco Churn & CLV Platform.
"""

import os
from pathlib import Path

# Paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
MODELS_DIR = BASE_DIR / "models"
TEMPLATES_DIR = BASE_DIR / "templates"
STATIC_DIR = BASE_DIR / "static"

DATA_URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
RAW_DATA_PATH = DATA_DIR / "Telco-Customer-Churn.csv"
MODEL_PATH = MODELS_DIR / "xgb_churn.pkl"

# Project Constants
RANDOM_STATE = 42
TEST_SIZE = 0.20
DISCOUNT_RATE_ANNUAL = 0.10
MONTHLY_DISCOUNT_RATE = 0.01
GROSS_MARGIN = 0.40

# Business Cost Matrix ($)
COST_FALSE_NEGATIVE = 500.0  # Cost of lost customer (unidentified churner)
COST_FALSE_POSITIVE = 50.0   # Cost of unnecessary retention incentive

# Default Web Server Config
DEFAULT_PORT = 5000
HOST = "0.0.0.0"

# Schema: Model Feature Columns
FEATURE_NAMES = [
    'tenure', 'MonthlyCharges', 'TotalCharges', 'gender_Male', 'SeniorCitizen_1',
    'Partner_Yes', 'Dependents_Yes', 'PhoneService_Yes',
    'MultipleLines_No phone service', 'MultipleLines_Yes',
    'InternetService_Fiber optic', 'InternetService_No',
    'OnlineSecurity_No internet service', 'OnlineSecurity_Yes',
    'OnlineBackup_No internet service', 'OnlineBackup_Yes',
    'DeviceProtection_No internet service', 'DeviceProtection_Yes',
    'TechSupport_No internet service', 'TechSupport_Yes',
    'StreamingTV_No internet service', 'StreamingTV_Yes',
    'StreamingMovies_No internet service', 'StreamingMovies_Yes',
    'Contract_One year', 'Contract_Two year', 'PaperlessBilling_Yes',
    'PaymentMethod_Credit card (automatic)', 'PaymentMethod_Electronic check',
    'PaymentMethod_Mailed check'
]
