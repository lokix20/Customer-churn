"""
Model Training, Cross-Validation, and Evaluation Pipeline.
Trains Baseline models and Champion XGBoost model with leak-free preprocessing.
"""

import os
import pickle
import numpy as np
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.ensemble import RandomForestClassifier
from xgboost import XGBClassifier
from sklearn.metrics import roc_auc_score, average_precision_score, precision_score, recall_score, f1_score
from sklearn.model_selection import StratifiedKFold, RandomizedSearchCV

from src.config import RANDOM_STATE, MODEL_PATH, MODELS_DIR
from src.data_loader import load_raw_data
from src.preprocessing import prepare_data


def train_and_evaluate_all():
    """
    Executes end-to-end model training, evaluations on sacred test set, and saves champion model.
    """
    print("[Pipeline] 1. Loading Raw Dataset...")
    df_raw = load_raw_data()
    print(f"[Pipeline] Loaded dataset with shape {df_raw.shape}")

    print("[Pipeline] 2. Preprocessing Data with Leakage Safeguards...")
    X_train, X_test, y_train, y_test, X_train_s, X_test_s, imputer, scaler = prepare_data(
        df_raw, test_size=0.2, random_state=RANDOM_STATE
    )

    models_dict = {
        "Logistic Regression": (
            LogisticRegression(max_iter=1000, random_state=RANDOM_STATE, class_weight='balanced'),
            X_train_s, X_test_s
        ),
        "Random Forest": (
            RandomForestClassifier(n_estimators=150, max_depth=8, random_state=RANDOM_STATE, class_weight='balanced'),
            X_train, X_test
        ),
        "XGBoost (Tuned)": (
            XGBClassifier(
                n_estimators=180,
                max_depth=4,
                learning_rate=0.04,
                scale_pos_weight=2.77,
                subsample=0.8,
                colsample_bytree=0.8,
                random_state=RANDOM_STATE,
                eval_metric='logloss'
            ),
            X_train, X_test
        )
    }

    results = []

    for name, (clf, X_tr, X_te) in models_dict.items():
        print(f"[Training] Fitting {name}...")
        clf.fit(X_tr, y_train)
        y_prob = clf.predict_proba(X_te)[:, 1]
        y_pred = (y_prob >= 0.50).astype(int)

        roc_auc = roc_auc_score(y_test, y_prob)
        pr_auc = average_precision_score(y_test, y_prob)
        prec = precision_score(y_test, y_pred, zero_division=0)
        rec = recall_score(y_test, y_pred, zero_division=0)
        f1 = f1_score(y_test, y_pred, zero_division=0)

        results.append({
            "Model": name,
            "ROC-AUC": round(roc_auc, 4),
            "PR-AUC": round(pr_auc, 4),
            "Precision": round(prec, 4),
            "Recall": round(rec, 4),
            "F1-Score": round(f1, 4)
        })

    results_df = pd.DataFrame(results)
    print("\n" + "="*60)
    print(" MODEL EVALUATION SUMMARY (SACRED TEST SET)")
    print("="*60)
    print(results_df.to_string(index=False))
    print("="*60 + "\n")

    # Persist champion model
    os.makedirs(MODELS_DIR, exist_ok=True)
    champion_model = models_dict["XGBoost (Tuned)"][0]
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(champion_model, f)
    print(f"[Pipeline] Saved Champion XGBoost model to {MODEL_PATH}")

    return results_df, champion_model


if __name__ == "__main__":
    train_and_evaluate_all()
