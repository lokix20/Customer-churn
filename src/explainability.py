"""
Explainability & Feature Importance Utilities.
"""

from typing import Dict, List, Any
import numpy as np
import pandas as pd


def get_feature_importance_ranking(model, feature_names: List[str]) -> List[Dict[str, Any]]:
    """
    Extracts sorted feature importance dictionary from a fitted tree model.
    """
    if hasattr(model, "feature_importances_"):
        importances = model.feature_importances_
        sorted_indices = np.argsort(importances)[::-1]
        ranking = []
        for idx in sorted_indices:
            ranking.append({
                "feature": feature_names[idx],
                "importance": float(round(importances[idx], 4))
            })
        return ranking
    return []


def explain_prediction_heuristic(data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Generates rule-based factor contributions for quick interpretability.
    """
    factors = []
    
    # Positive risk drivers (increase churn)
    if data.get("Contract") == "Month-to-month":
        factors.append({"factor": "Month-to-month Contract", "direction": "RISK", "weight": "+35%"})
    if data.get("InternetService") == "Fiber optic":
        factors.append({"factor": "Fiber Optic Line (High bill sensitivity)", "direction": "RISK", "weight": "+15%"})
    if data.get("PaymentMethod") == "Electronic check":
        factors.append({"factor": "Electronic Check (Manual Payment)", "direction": "RISK", "weight": "+10%"})
    if float(data.get("tenure", 12)) <= 6:
        factors.append({"factor": "Early Tenure (< 6 months)", "direction": "RISK", "weight": "+15%"})
        
    # Protective drivers (decrease churn)
    if data.get("Contract") in ["One year", "Two year"]:
        factors.append({"factor": f"{data.get('Contract')} Term Commitment", "direction": "PROTECTIVE", "weight": "-40%"})
    if data.get("TechSupport") == "Yes":
        factors.append({"factor": "Active Tech Support Add-on", "direction": "PROTECTIVE", "weight": "-15%"})
    if data.get("OnlineSecurity") == "Yes":
        factors.append({"factor": "Subscribed Online Security", "direction": "PROTECTIVE", "weight": "-12%"})
    if float(data.get("tenure", 12)) >= 36:
        factors.append({"factor": "High Tenure (> 3 years loyalty)", "direction": "PROTECTIVE", "weight": "-25%"})

    return factors
