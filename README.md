# IBM Telco Customer Churn Prediction & Lifetime Value (CLV) Platform

[![Python](https://img.shields.io/badge/Python-3.11+-blue.svg)](https://www.python.org/)
[![XGBoost](https://img.shields.io/badge/XGBoost-2.0+-green.svg)](https://xgboost.readthedocs.io/)
[![Scikit-Learn](https://img.shields.io/badge/Scikit--Learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![License](https://img.shields.io/badge/License-MIT-purple.svg)](LICENSE)

---

## 📌 Executive Summary & Architecture

This repository contains an enterprise-grade Machine Learning and Survival Analysis platform designed to predict customer churn, estimate dynamic Customer Lifetime Value (CLV), and prescribe high-ROI retention interventions for the **IBM Telco Customer Churn** dataset (7,043 customers).

### Repository Structure

```
mlpa/
├── data/
│   └── Telco-Customer-Churn.csv       # Raw IBM Telco dataset (7,043 rows x 21 cols)
├── models/
│   └── xgb_churn.pkl                  # Serialized Champion XGBoost Classifier artifact
├── notebooks/                         # Research & Exploratory Data Analysis Modules
│   ├── 01_data_loading.ipynb          # Raw ingestion & missing value inspection
│   ├── 02_eda.ipynb                   # 9 EDA charts & strategic insights
│   ├── 03_preprocessing.ipynb         # Leakage-safe train-test split & transformations
│   ├── 04_churn_models.ipynb          # Baseline models (LogReg, RF, XGBoost)
│   ├── 05_tuning.ipynb                # 5-fold Stratified CV & cost threshold tuning
│   ├── 06_explainability.ipynb        # SHAP global & individual waterfall explanations
│   ├── 07_clv_simple.ipynb            # Discounted cash flow 3-year static CLV
│   ├── 08_clv_survival.ipynb          # Kaplan-Meier & Cox Proportional Hazards modeling
│   └── 09_segmentation.ipynb          # 2x2 Risk-Value matrix ($1.55M VIP CLV at risk)
├── src/                               # Modular Core Engine & Logic
│   ├── __init__.py                    # Clean public package interface
│   ├── config.py                      # Centralized configuration & schema definitions
│   ├── data_loader.py                 # Automated dataset downloader & loader
│   ├── preprocessing.py               # Leakage-safe preprocessing pipeline
│   ├── model_trainer.py               # End-to-end model training & evaluation runner
│   ├── inference.py                   # Feature vector assembly & real-time inference
│   ├── clv.py                         # Dynamic Survival CLV & Discounted Net Present Value
│   ├── recommendations.py             # Prescriptive retention action engine & personas
│   ├── explainability.py              # Interpretability helpers & feature rankings
│   └── server.py                      # REST API router & Web Server
├── static/                            # Frontend Web Assets
│   ├── css/
│   │   └── styles.css                 # Glassmorphic dark theme CSS design system
│   └── js/
│       └── app.js                     # Interactive dashboard logic & Chart.js visualizations
├── templates/
│   └── index.html                     # Semantic HTML5 frontend
├── tests/                             # Automated Unit & Integration Tests
│   ├── __init__.py
│   ├── test_data_loader.py
│   ├── test_preprocessing.py
│   ├── test_inference.py
│   ├── test_clv.py
│   └── test_recommendations.py
├── app.py                             # Lightweight web server launcher
├── main.py                            # Unified CLI entrypoint
├── pyproject.toml                     # Modern Python project configuration
├── requirements.txt                   # Dependency specifications
└── README.md                          # Project documentation
```

---

## 🛡️ Core ML Principles & Leakage Protection

1. **Sacred Test Set**: The test set (20% stratified split, `random_state=42`) is strictly held out. Imputers and scalers are fitted exclusively on `X_train`.
2. **Asymmetric Business Cost Optimization**: Evaluates decision boundaries against a **$500 False Negative** (unidentified churner loss) vs **$50 False Positive** (unnecessary retention discount) ratio.
3. **Dynamic Survival CLV**: Replaces memoryless static formulas with time-to-event Kaplan-Meier and Cox Proportional Hazard modeling.

---

## 🚀 Quickstart & Usage

### 1. Installation

```bash
# Clone or navigate to the repository
cd mlpa

# Create and activate virtual environment
python -m venv .venv
.\.venv\Scripts\activate       # Windows PowerShell / CMD
# source .venv/bin/activate    # Linux / macOS

# Install dependencies
pip install -r requirements.txt
```

### 2. Run the Web Application

Launch the real-time AI risk evaluation and review dashboard:

```bash
python app.py
```
*Or via CLI with custom port:*
```bash
python main.py --serve --port 5000
```
Then open your browser at **`http://localhost:5000`**.

### 3. Model Training & Evaluation

To re-train all models and serialize the champion XGBoost artifact:

```bash
python main.py --train
```

### 4. Sample CLI Inference

To run a fast test evaluation on demo customer personas:

```bash
python main.py --predict
```

### 5. Running Automated Unit Tests

```bash
python -m unittest discover tests
```

---

## 📊 Model Performance Summary (Test Set: N=1,409)

| Model | ROC-AUC | PR-AUC | Precision | Recall | F1-Score | Status |
| :--- | :---: | :---: | :---: | :---: | :---: | :--- |
| **Logistic Regression** | 0.8412 | 0.6306 | 0.5055 | **0.7807** | 0.6136 | Baseline |
| **Random Forest** | 0.8354 | 0.6190 | 0.5521 | 0.6551 | 0.5992 | Benchmark |
| **Tuned XGBoost** | **0.8520** | **0.6410** | **0.5840** | **0.7120** | **0.6415** | 🏆 **Champion** |

---

## 👥 Strategic Retention Findings

- **Month-to-Month Contracts**: Account for **81.3%** of customers in the highest CLV-at-risk tier ($1.55M).
- **Fiber Optic Lines without Tech Support**: Show a **3.15x increase in churn hazard rate**.
- **Recommended Playbook**: Automated conversion discounts to 1-year contracts and complimentary tech support add-ons recover up to **35%** of churn risk.
