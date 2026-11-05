"""
Real-time & Batch Model Inference Module.
Handles loading model artifacts, constructing feature vectors, predicting churn, and assembling response payloads.
"""

import os
import pickle
from typing import Dict, Any, Optional
import pandas as pd
from src.config import MODEL_PATH, FEATURE_NAMES
from src.clv import calculate_clv
from src.recommendations import get_recommendations, get_risk_tier
from src.explainability import explain_prediction_heuristic



class ChurnPredictor:
    def __init__(self, model_path: Optional[str] = None):
        self.model_path = model_path or MODEL_PATH
        self.model = None
        self._load_model()

    def _load_model(self):
        """Loads trained XGBoost model from disk if available."""
        if os.path.exists(self.model_path):
            try:
                with open(self.model_path, "rb") as f:
                    self.model = pickle.load(f)
                print(f"[ChurnPredictor] Successfully loaded model from {self.model_path}")
            except Exception as e:
                print(f"[ChurnPredictor] Warning: Failed to load model artifact: {e}")
        else:
            print(f"[ChurnPredictor] Notice: Model artifact not found at {self.model_path}. Using fallback heuristic.")

    @staticmethod
    def build_feature_vector(data: Dict[str, Any]) -> pd.DataFrame:
        """
        Constructs a 1-row DataFrame strictly matching the model feature columns.
        """
        row = {col: 0.0 for col in FEATURE_NAMES}
        
        # Numerical features
        tenure = float(data.get("tenure", 12))
        monthly = float(data.get("MonthlyCharges", 70.0))
        total = float(data.get("TotalCharges", tenure * monthly))
        if total <= 0:
            total = tenure * monthly
            
        row["tenure"] = tenure
        row["MonthlyCharges"] = monthly
        row["TotalCharges"] = total
        
        # Categoricals
        if data.get("gender") == "Male":
            row["gender_Male"] = 1.0
        if str(data.get("SeniorCitizen", "0")) in ["1", "Yes", "true", "True"]:
            row["SeniorCitizen_1"] = 1.0
        if data.get("Partner") == "Yes":
            row["Partner_Yes"] = 1.0
        if data.get("Dependents") == "Yes":
            row["Dependents_Yes"] = 1.0
        if data.get("PhoneService") == "Yes":
            row["PhoneService_Yes"] = 1.0
            
        mul_lines = data.get("MultipleLines", "No")
        if mul_lines == "No phone service":
            row["MultipleLines_No phone service"] = 1.0
        elif mul_lines == "Yes":
            row["MultipleLines_Yes"] = 1.0
            
        internet = data.get("InternetService", "Fiber optic")
        if internet == "Fiber optic":
            row["InternetService_Fiber optic"] = 1.0
        elif internet == "No":
            row["InternetService_No"] = 1.0
            
        def set_service(key: str, prefix: str):
            val = data.get(key, "No")
            if internet == "No" or val == "No internet service":
                row[f"{prefix}_No internet service"] = 1.0
            elif val == "Yes":
                row[f"{prefix}_Yes"] = 1.0
                
        set_service("OnlineSecurity", "OnlineSecurity")
        set_service("OnlineBackup", "OnlineBackup")
        set_service("DeviceProtection", "DeviceProtection")
        set_service("TechSupport", "TechSupport")
        set_service("StreamingTV", "StreamingTV")
        set_service("StreamingMovies", "StreamingMovies")
        
        contract = data.get("Contract", "Month-to-month")
        if contract == "One year":
            row["Contract_One year"] = 1.0
        elif contract == "Two year":
            row["Contract_Two year"] = 1.0
            
        if data.get("PaperlessBilling") == "Yes":
            row["PaperlessBilling_Yes"] = 1.0
            
        pay_method = data.get("PaymentMethod", "Electronic check")
        if pay_method == "Credit card (automatic)":
            row["PaymentMethod_Credit card (automatic)"] = 1.0
        elif pay_method == "Electronic check":
            row["PaymentMethod_Electronic check"] = 1.0
        elif pay_method == "Mailed check":
            row["PaymentMethod_Mailed check"] = 1.0
            
        return pd.DataFrame([row], columns=FEATURE_NAMES)

    def predict_churn_probability(self, data: Dict[str, Any]) -> float:
        """
        Computes the probability of churn (0.0 to 1.0).
        Uses the trained model if available, else applies domain heuristic baseline.
        """
        if self.model is not None:
            X_df = self.build_feature_vector(data)
            prob = float(self.model.predict_proba(X_df)[0, 1])
            return prob
        
        # Domain fallback heuristic
        score = 0.25
        if data.get("Contract") == "Month-to-month": score += 0.35
        if data.get("InternetService") == "Fiber optic": score += 0.15
        if data.get("TechSupport") == "No": score += 0.10
        if float(data.get("tenure", 12)) < 6: score += 0.15
        if data.get("PaymentMethod") == "Electronic check": score += 0.10
        return float(min(max(score, 0.02), 0.95))

    def evaluate_customer(self, data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Full evaluation: churn probability, risk tier, CLV estimate, and retention recommendations.
        """
        prob = self.predict_churn_probability(data)
        tier = get_risk_tier(prob)
        monthly_charges = float(data.get("MonthlyCharges", 70.0))
        tenure = float(data.get("tenure", 12.0))
        
        clv_info = calculate_clv(monthly_charges=monthly_charges, tenure=tenure, churn_prob=prob)
        recommendations = get_recommendations(data, prob)
        explanation = explain_prediction_heuristic(data)
        
        return {
            "churn_probability": round(prob, 4),
            "risk_tier": tier,
            "clv": clv_info,
            "recommendations": recommendations,
            "explanation": explanation
        }



# Singleton instance
predictor = ChurnPredictor()
