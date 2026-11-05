"""
Data loader module for IBM Telco Customer Churn dataset.
"""

import os
import urllib.request
import pandas as pd

DATA_URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"
DEFAULT_DATA_PATH = os.path.join("data", "Telco-Customer-Churn.csv")

def download_dataset(url: str = DATA_URL, target_path: str = DEFAULT_DATA_PATH) -> str:
    """
    Downloads the dataset from the URL if it does not already exist locally.
    """
    os.makedirs(os.path.dirname(target_path), exist_ok=True)
    if not os.path.exists(target_path):
        print(f"Downloading dataset from {url}...")
        urllib.request.urlretrieve(url, target_path)
        print(f"Dataset saved to {target_path}")
    else:
        print(f"Dataset already exists at {target_path}")
    return target_path

def load_raw_data(data_path: str = DEFAULT_DATA_PATH) -> pd.DataFrame:
    """
    Loads raw CSV dataset into a Pandas DataFrame.
    """
    data_path = download_dataset(target_path=data_path)
    return pd.read_csv(data_path)

if __name__ == "__main__":
    df = load_raw_data()
    print(f"Loaded DataFrame with shape: {df.shape}")
