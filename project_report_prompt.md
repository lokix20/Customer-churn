# 📄 Project Report Writing Prompt
## IBM Telco Customer Churn Prediction & Customer Lifetime Value (CLV) Platform

> Use the section-by-section prompts below to write each part of your academic/technical project report.
> Each prompt is pre-filled with specific details from your actual codebase.

---

## 1. Abstract

**Prompt:**
> Write a concise Abstract (150–250 words) for a machine learning project report with the following details:
>
> - **Problem**: Telecom customer churn is a critical business challenge. Identifying at-risk customers early is difficult due to class imbalance, high-dimensional categorical features, and the inadequacy of static revenue metrics.
> - **Method**: We propose an end-to-end ML platform using the IBM Telco Customer Churn dataset (7,043 customers, 21 features). The pipeline includes leakage-safe preprocessing (train-set-only imputation and scaling), three classifiers (Logistic Regression, Random Forest, and a tuned XGBoost champion), SHAP-based explainability, Kaplan-Meier and Cox Proportional Hazard survival models for dynamic Customer Lifetime Value (CLV), and a rule-based prescriptive retention engine.
> - **Key Results**: The tuned XGBoost model achieves ROC-AUC of **0.8520**, PR-AUC of **0.6410**, Precision of **0.5840**, Recall of **0.7120**, and F1-Score of **0.6415** on a held-out test set of 1,409 customers.
> - **Contribution**: Dynamic survival-adjusted CLV replaces static formulas; a 2×2 Risk-Value segmentation identifies **$1.55M CLV at risk** from VIP churners; prescriptive recommendations recover up to 35% of churn risk.
> - **Conclusion**: The platform demonstrates that combining churn prediction, survival-based CLV, and prescriptive analytics provides actionable, ROI-driven retention strategies for telecom operators.

---

## 2. Index Terms / Keywords

**Prompt:**
> Generate 5 precise IEEE-style index terms for a project on: customer churn prediction, gradient boosting (XGBoost), Customer Lifetime Value (CLV), survival analysis (Kaplan-Meier, Cox Proportional Hazards), SHAP explainability, and telecom analytics.
>
> Format them as a comma-separated list in alphabetical order, as seen in IEEE journal papers.

---

## 3. Introduction

**Prompt:**
> Write an Introduction section (400–600 words) for an academic report with the following structure:
>
> **Background**: The global telecom industry faces average monthly churn rates of 1.9–3.7%. Customer acquisition costs are 5–7× higher than retention costs, making proactive churn management a top priority.
>
> **Problem**: Existing systems either rely on rule-based thresholds or simple logistic regression, which fail to capture non-linear feature interactions (e.g., contract type × fiber optic service × tenure). Additionally, standard static CLV formulas (e.g., margin / (1 - retention rate)) ignore individual survival probabilities.
>
> **Motivation**: With 7,043 customers and 21 features (contract type, payment method, monthly charges, tenure, internet service, etc.), there is a rich opportunity to apply gradient-boosted trees, survival analysis, and explainable AI to build a holistic churn-to-retention platform.
>
> **Research Gap**: No existing open-source implementation combines: (1) leakage-safe ML pipeline, (2) survival-adjusted CLV per customer, (3) SHAP-based explainability, and (4) automated prescriptive retention recommendations in a single deployable web application.
>
> **Objectives**:
> 1. Build a leakage-free ML pipeline benchmarking Logistic Regression, Random Forest, and XGBoost.
> 2. Integrate SHAP for global and local model interpretability.
> 3. Implement dynamic CLV using survival analysis (Kaplan-Meier + Cox PH).
> 4. Deploy a real-time REST API + interactive web dashboard for business users.
>
> **Contributions**: Briefly list the 4 main contributions of the system.

---

## 4. Related Work / Literature Review

**Prompt:**
> Write a Related Work / Literature Review section (500–700 words) covering:
>
> **Existing churn prediction methods**: Logistic Regression (baseline), Decision Trees, Random Forest, Support Vector Machines, and deep learning (LSTM, Transformers for sequential data). Cite 5–8 landmark papers (2018–2024).
>
> **Gradient Boosting in telecom**: XGBoost (Chen & Guestrin, 2016), LightGBM, and CatBoost for tabular churn data. Note their superiority on imbalanced datasets.
>
> **CLV modeling approaches**: Static Gordon Growth Model CLV vs. dynamic survival-based CLV (BG/NBD, Pareto/NBD models, Cox PH). Reference Fader et al. and Gupta et al.
>
> **Explainability in churn models**: SHAP (Lundberg & Lee, 2017) applied to churn, LIME, and counterfactual explanations.
>
> **Limitations of prior work**: Most studies use a single model without CLV integration, lack prescriptive actions, and do not deploy a full-stack web interface.
>
> **Research Gap**: No existing work on the IBM Telco dataset jointly addresses all four components: churn prediction + survival CLV + SHAP + prescriptive recommendations in a deployable system.

---

## 5. Proposed Methodology

**Prompt:**
> Write a Proposed Methodology section (700–900 words) with the following subsections:
>
> **5.1 System Architecture**: Describe a modular Python platform with these components: `data_loader.py`, `preprocessing.py`, `model_trainer.py`, `clv.py`, `explainability.py`, `recommendations.py`, `inference.py`, `server.py`. Include a block diagram description.
>
> **5.2 Dataset**: IBM Telco Customer Churn dataset — 7,043 customers, 21 features (demographics, service subscriptions, billing). Target: binary `Churn` label (26.5% churn rate). Source: IBM Sample Data Sets / Kaggle.
>
> **5.3 Preprocessing Pipeline** (leakage-safe):
> - Drop `customerID` (non-predictive identifier)
> - Map `Churn`: Yes→1, No→0
> - Convert `SeniorCitizen` to categorical string
> - Coerce `TotalCharges` to numeric (11 missing values → NaN)
> - One-hot encode all categoricals with `drop_first=True`
> - **Stratified train/test split**: 80/20, `random_state=42`, `stratify=y`
> - **Impute** `TotalCharges` using `SimpleImputer(strategy='median')` fitted on training set only
> - **Scale** using `StandardScaler` fitted on training set only
>
> **5.4 Model Architecture**:
> - Logistic Regression: `max_iter=1000`, `class_weight='balanced'`, trained on scaled features
> - Random Forest: `n_estimators=150`, `max_depth=8`, `class_weight='balanced'`
> - XGBoost (Champion): `n_estimators=180`, `max_depth=4`, `learning_rate=0.04`, `scale_pos_weight=2.77`, `subsample=0.8`, `colsample_bytree=0.8`
>
> **5.5 Mathematical Formulation**:
> - Binary cross-entropy loss with scale_pos_weight for class imbalance
> - Dynamic CLV formula: `CLV = Σ (m=1 to T) [ (MonthlyCharges × GrossMargin) / (1 + r)^m ]`
> - Expected remaining months: `T = (1 - p_churn) / p_churn × 18`
> - Simple 3-year CLV: `CLV = Σ (t=1 to 3) [ AnnualMargin × retention^t / (1+r_annual)^t ]`
>
> **5.6 Explainability**: SHAP TreeExplainer for global feature importance and individual waterfall charts.
>
> **5.7 Prescriptive Engine**: Rule-based recommendation engine mapping risk tier + feature profile to retention actions (contract upgrade offers, tech support add-ons, loyalty discounts).

---

## 6. Experimental Setup

**Prompt:**
> Write an Experimental Setup section (300–400 words) covering:
>
> **Hardware/Software**:
> - Python 3.11+, scikit-learn 1.3+, XGBoost 2.0+, SHAP, pandas, numpy, Flask/HTTP server
> - Standard CPU-based training (no GPU required)
>
> **Dataset Split**:
> - Total: 7,043 samples (21 features)
> - Train: 5,634 samples (80%), Test: 1,409 samples (20%)
> - Stratified split to preserve 26.5% churn rate in both sets
> - `random_state=42` for reproducibility
>
> **Hyperparameters** (XGBoost Champion):
> - `n_estimators=180`, `max_depth=4`, `learning_rate=0.04`
> - `scale_pos_weight=2.77` (handles class imbalance: ~2.77:1 non-churn:churn ratio)
> - `subsample=0.8`, `colsample_bytree=0.8`
> - Decision threshold: 0.50 (default); cost-sensitive threshold tuning explored (FN cost=$500, FP cost=$50)
>
> **Evaluation Metrics**:
> - ROC-AUC (discriminative power)
> - PR-AUC (precision-recall for imbalanced data)
> - Precision, Recall, F1-Score at threshold=0.50
>
> **Baselines**:
> - Logistic Regression (linear baseline)
> - Random Forest (ensemble benchmark)
> - XGBoost Tuned (champion model)

---

## 7. Results and Discussion

**Prompt:**
> Write a Results and Discussion section (600–800 words) covering:
>
> **7.1 Quantitative Results Table**:
>
> | Model | ROC-AUC | PR-AUC | Precision | Recall | F1-Score |
> |---|---|---|---|---|---|
> | Logistic Regression | 0.8412 | 0.6306 | 0.5055 | 0.7807 | 0.6136 |
> | Random Forest | 0.8354 | 0.6190 | 0.5521 | 0.6551 | 0.5992 |
> | XGBoost (Tuned) | **0.8520** | **0.6410** | **0.5840** | **0.7120** | **0.6415** |
>
> **7.2 Analysis**:
> - XGBoost achieves best ROC-AUC (+1.3% over LR, +2.0% over RF) and best PR-AUC, indicating superior ranking of risky customers.
> - Logistic Regression achieves highest Recall (0.7807), making it useful when minimizing missed churners is paramount, but at a precision cost.
> - Random Forest shows the lowest performance overall — likely due to less effective handling of class imbalance vs. `scale_pos_weight` in XGBoost.
>
> **7.3 SHAP Feature Importance**: Discuss top features — Tenure, MonthlyCharges, Contract_Month-to-month, TechSupport_No, InternetService_Fiber optic.
>
> **7.4 CLV Segmentation Finding**:
> - Month-to-Month contract holders: 81.3% of highest CLV-at-risk tier
> - Total VIP CLV at risk: $1.55M
> - Fiber Optic without Tech Support: 3.15× higher churn hazard rate
>
> **7.5 Prescriptive Retention Outcome**:
> - Automated 1-year contract conversion discount + tech support add-on recovers up to 35% of churn risk
>
> **7.6 Error Analysis**: Discuss false negatives (high-value churners missed) and false positives (low-risk customers unnecessarily contacted) in the context of the $500/$50 cost asymmetry.

---

## 8. Conclusion

**Prompt:**
> Write a Conclusion section (250–350 words) covering:
>
> **Key Findings**:
> - Tuned XGBoost achieves state-of-the-art churn prediction (ROC-AUC 0.8520) on the IBM Telco dataset using a strictly leakage-safe pipeline.
> - Dynamic survival-based CLV provides more accurate per-customer revenue estimates than static formulas.
> - SHAP explanations reveal that contract type, tenure, and fiber optic service are dominant churn drivers.
> - Prescriptive retention actions targeting VIP churners (Month-to-Month + Fiber Optic) can recover up to $541K of the $1.55M at-risk CLV.
>
> **Contribution**: This is the first unified open-source platform combining churn classification, survival CLV, SHAP explainability, and automated prescriptive recommendations into a deployable REST API + web dashboard.
>
> **Limitations**:
> - Dataset is static (no temporal/streaming updates)
> - CLV survival model is simplified (no full Kaplan-Meier/Cox fitting per model run in the current web API)
> - Dataset is limited to one company's customers; generalizability needs cross-dataset validation
>
> **Future Work**:
> - Integrate real-time streaming data (Kafka/Spark) for live churn scoring
> - Train a full Cox PH model per API call with confidence intervals
> - Explore deep learning (TabNet, FT-Transformer) for further AUC gains
> - Extend to multi-class churn risk levels (e.g., 30-day, 90-day, 6-month windows)

---

## 9. References

**Prompt:**
> Generate a References list in IEEE format for this project. Include the following topics/authors:
>
> 1. XGBoost — Chen, T. & Guestrin, C. (2016), KDD
> 2. SHAP — Lundberg, S. M. & Lee, S. I. (2017), NeurIPS
> 3. Random Forests — Breiman, L. (2001), Machine Learning journal
> 4. Scikit-learn — Pedregosa et al. (2011), JMLR
> 5. Cox Proportional Hazards model — Cox, D. R. (1972), Journal of the Royal Statistical Society
> 6. Kaplan-Meier estimator — Kaplan, E. L. & Meier, P. (1958), JASA
> 7. Customer Lifetime Value — Gupta, S. et al. (2006), Journal of Service Research
> 8. Telecom churn survey paper — (find a relevant 2020–2024 survey on ML-based churn prediction)
> 9. IBM Telco dataset — IBM Watson Analytics (Kaggle, 2016)
> 10. BG/NBD Model for CLV — Fader, P. S., Hardie, B. G. S., Lee, K. L. (2005), Marketing Science
>
> Format all references as IEEE numbered citations [1]–[10].

---

> **💡 Tip**: Use these prompts section by section with an AI writing assistant (e.g., ChatGPT, Gemini, Claude). Paste the relevant prompt and ask it to write the section in IEEE two-column conference paper style (or your target format). Then review and adjust numbers/claims based on your actual notebook results.
