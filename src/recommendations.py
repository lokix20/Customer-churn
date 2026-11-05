"""
Retention Strategies, Recommendation Engine & Sample Personas.
"""

from typing import Dict, List, Any


def get_risk_tier(churn_prob: float) -> str:
    """Classifies risk level into HIGH, MEDIUM, or LOW."""
    if churn_prob >= 0.50:
        return "HIGH"
    elif churn_prob >= 0.25:
        return "MEDIUM"
    return "LOW"


def get_recommendations(data: Dict[str, Any], churn_prob: float) -> List[Dict[str, str]]:
    """
    Generates actionable, data-driven retention recommendations based on customer attributes.
    """
    recs = []
    contract = data.get("Contract", "Month-to-month")
    tech = data.get("TechSupport", "No")
    security = data.get("OnlineSecurity", "No")
    pay = data.get("PaymentMethod", "Electronic check")
    internet = data.get("InternetService", "DSL")
    tenure = float(data.get("tenure", 12))
    
    if contract == "Month-to-month":
        recs.append({
            "action": "Contract Upgrade Incentive",
            "detail": "Offer a 15% discount or streaming bundle upgrade to transition from Month-to-Month to a 1-Year or 2-Year Contract.",
            "impact": "Reduces churn hazard rate by up to 94%"
        })
    if tech != "Yes" and internet != "No":
        recs.append({
            "action": "Complimentary Tech Support Add-on",
            "detail": "Provide 3 months of complimentary 24/7 dedicated Technical Support onboarding.",
            "impact": "Lowers churn probability by ~15%"
        })
    if security != "Yes" and internet != "No":
        recs.append({
            "action": "Online Security & Privacy Shield",
            "detail": "Enable identity and device security suite to increase ecosystem lock-in.",
            "impact": "Increases customer retention significantly"
        })
    if pay == "Electronic check":
        recs.append({
            "action": "Auto-Pay Direct Discount",
            "detail": "Prompt customer with a $5/month bill credit for switching to Automatic Bank Transfer or Credit Card Auto-Pay.",
            "impact": "Lowers involuntary and frictional churn"
        })
    if tenure < 6:
        recs.append({
            "action": "VIP Onboarding & Check-in",
            "detail": "Customer is in the critical first-6-months danger window. Schedule a proactive customer success check-in call.",
            "impact": "Builds early loyalty and trust"
        })
        
    if not recs:
        recs.append({
            "action": "Loyalty & Referral Rewards",
            "detail": "Customer is at low risk. Offer loyalty tier benefits and family referral discounts.",
            "impact": "Maximizes lifetime value"
        })
    return recs


SAMPLE_PERSONAS = [
    {
        "name": "High-Risk New Customer (Fiber Optic, Month-to-Month)",
        "tenure": 2,
        "MonthlyCharges": 95.5,
        "TotalCharges": 191.0,
        "gender": "Female",
        "SeniorCitizen": "0",
        "Partner": "No",
        "Dependents": "No",
        "PhoneService": "Yes",
        "MultipleLines": "No",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "No",
        "OnlineBackup": "No",
        "DeviceProtection": "No",
        "TechSupport": "No",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Month-to-month",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Electronic check"
    },
    {
        "name": "Medium-Risk Family Plan (DSL, 1-Year)",
        "tenure": 18,
        "MonthlyCharges": 58.0,
        "TotalCharges": 1044.0,
        "gender": "Male",
        "SeniorCitizen": "0",
        "Partner": "Yes",
        "Dependents": "Yes",
        "PhoneService": "Yes",
        "MultipleLines": "Yes",
        "InternetService": "DSL",
        "OnlineSecurity": "Yes",
        "OnlineBackup": "No",
        "DeviceProtection": "Yes",
        "TechSupport": "No",
        "StreamingTV": "No",
        "StreamingMovies": "No",
        "Contract": "One year",
        "PaperlessBilling": "No",
        "PaymentMethod": "Mailed check"
    },
    {
        "name": "Low-Risk Loyal Subscriber (2-Year, Full Security)",
        "tenure": 60,
        "MonthlyCharges": 85.0,
        "TotalCharges": 5100.0,
        "gender": "Female",
        "SeniorCitizen": "0",
        "Partner": "Yes",
        "Dependents": "No",
        "PhoneService": "Yes",
        "MultipleLines": "Yes",
        "InternetService": "Fiber optic",
        "OnlineSecurity": "Yes",
        "OnlineBackup": "Yes",
        "DeviceProtection": "Yes",
        "TechSupport": "Yes",
        "StreamingTV": "Yes",
        "StreamingMovies": "Yes",
        "Contract": "Two year",
        "PaperlessBilling": "Yes",
        "PaymentMethod": "Credit card (automatic)"
    }
]
