"""
Customer Lifetime Value (CLV) Calculation Module.
Provides functions for simple discounted CLV and survival-adjusted CLV.
"""

from typing import Dict, Any
from src.config import MONTHLY_DISCOUNT_RATE, GROSS_MARGIN


def calculate_clv(
    monthly_charges: float,
    tenure: float,
    churn_prob: float,
    discount_rate: float = MONTHLY_DISCOUNT_RATE,
    gross_margin: float = GROSS_MARGIN
) -> Dict[str, Any]:
    """
    Computes expected remaining lifetime and dynamic discounted CLV.

    Args:
        monthly_charges: Monthly billing amount in USD.
        tenure: Customer tenure in months.
        churn_prob: Predicted churn probability (between 0.0 and 1.0).
        discount_rate: Monthly financial discount rate.
        gross_margin: Gross profit margin percentage.

    Returns:
        Dict containing expected remaining months, CLV value, and annualized value.
    """
    safe_prob = min(max(float(churn_prob), 0.01), 0.99)
    
    # Expected remaining months based on hazard/churn probability
    # Higher churn probability reduces expected remaining lifetime
    expected_remaining_months = max(1.0, round((1.0 - safe_prob) / safe_prob * 18.0, 1))
    
    # Net Present Value (NPV) of remaining margin stream
    clv_val = 0.0
    for m in range(1, int(expected_remaining_months) + 1):
        clv_val += (monthly_charges * gross_margin) / ((1 + discount_rate) ** m)
        
    # Total revenue stream undiscounted and discounted
    undiscounted_revenue = monthly_charges * expected_remaining_months
    
    return {
        "expected_remaining_months": expected_remaining_months,
        "clv_value": round(clv_val, 2),
        "undiscounted_revenue": round(undiscounted_revenue, 2),
        "annualized_value": round(monthly_charges * 12, 2)
    }


def calculate_simple_clv(
    monthly_charges: float,
    retention_rate: float,
    discount_rate_annual: float = 0.10,
    gross_margin: float = GROSS_MARGIN,
    horizon_years: int = 3
) -> float:
    """
    Computes static 3-year discounted CLV formula:
    CLV = sum_{t=1}^horizon [ Margin * (Retention_rate ^ t) / (1 + r)^t ]
    """
    clv = 0.0
    annual_revenue = monthly_charges * 12
    annual_margin = annual_revenue * gross_margin
    
    for t in range(1, horizon_years + 1):
        clv += annual_margin * (retention_rate ** t) / ((1 + discount_rate_annual) ** t)
        
    return round(clv, 2)
