"""
Data Preprocessing module for IBM Telco Customer Churn Prediction.
Provides prepare_data() function with data leakage safeguards.
"""

import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import StandardScaler

def prepare_data(df: pd.DataFrame, test_size: float = 0.2, random_state: int = 42):
    """
    Preprocesses raw Telco Customer Churn DataFrame:
    1. Drops customerID.
    2. Maps Churn target (Yes -> 1, No -> 0).
    3. Converts SeniorCitizen to string/categorical.
    4. Coerces TotalCharges to numeric.
    5. One-hot encodes categorical features with drop_first=True.
    6. Splits into train/test BEFORE imputation/scaling (stratified).
    7. Imputes missing TotalCharges using training set median ONLY.
    8. Scales features using StandardScaler fitted on training set ONLY.

    Returns:
        X_train, X_test, y_train, y_test, X_train_scaled, X_test_scaled, imputer, scaler
    """
    # Make a copy to avoid mutating original df
    data = df.copy()
    
    # 1. Drop customerID if present
    if 'customerID' in data.columns:
        data = data.drop(columns=['customerID'])
        
    # 2. Map target: Churn Yes -> 1, No -> 0
    data['Churn'] = data['Churn'].map({'Yes': 1, 'No': 0})
    y = data['Churn']
    X = data.drop(columns=['Churn'])
    
    # 3. Convert SeniorCitizen to string/categorical before encoding
    if 'SeniorCitizen' in X.columns:
        X['SeniorCitizen'] = X['SeniorCitizen'].astype(str)
        
    # 4. Coerce TotalCharges to numeric (errors -> NaN)
    if 'TotalCharges' in X.columns:
        X['TotalCharges'] = pd.to_numeric(X['TotalCharges'], errors='coerce')
        
    # 5. One-hot encode all categorical columns with drop_first=True
    X_encoded = pd.get_dummies(X, drop_first=True)
    
    # 6. Split into train/test BEFORE any scaling or imputation
    X_train, X_test, y_train, y_test = train_test_split(
        X_encoded, y, test_size=test_size, random_state=random_state, stratify=y
    )
    
    # 7. Fit SimpleImputer(strategy='median') on X_train ONLY
    imputer = SimpleImputer(strategy='median')
    X_train_imp = X_train.copy()
    X_test_imp = X_test.copy()
    
    X_train_imp[['TotalCharges']] = imputer.fit_transform(X_train[['TotalCharges']])
    X_test_imp[['TotalCharges']] = imputer.transform(X_test[['TotalCharges']])
    
    # 8. Fit StandardScaler on X_train ONLY
    scaler = StandardScaler()
    X_train_scaled_arr = scaler.fit_transform(X_train_imp)
    X_test_scaled_arr = scaler.transform(X_test_imp)
    
    X_train_scaled = pd.DataFrame(X_train_scaled_arr, columns=X_train_imp.columns, index=X_train_imp.index)
    X_test_scaled = pd.DataFrame(X_test_scaled_arr, columns=X_test_imp.columns, index=X_test_imp.index)
    
    return X_train_imp, X_test_imp, y_train, y_test, X_train_scaled, X_test_scaled, imputer, scaler

if __name__ == "__main__":
    import os
    raw_path = os.path.join("data", "Telco-Customer-Churn.csv")
    if os.path.exists(raw_path):
        df_raw = pd.read_csv(raw_path)
        X_tr, X_te, y_tr, y_te, X_tr_s, X_te_s, imp, scl = prepare_data(df_raw)
        print(f"X_train shape: {X_tr.shape}, X_test shape: {X_te.shape}")
        print(f"Train churn rate: {y_tr.mean()*100:.2f}%")
        print(f"Test churn rate: {y_te.mean()*100:.2f}%")
        print(f"Median TotalCharges computed on train: ${imp.statistics_[0]:.2f}")
