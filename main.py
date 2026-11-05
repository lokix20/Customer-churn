"""
Main Command-Line Interface (CLI) for the IBM Telco Churn & CLV Project.
Usage:
    python main.py --train       # Run training and evaluation pipeline
    python main.py --serve       # Launch web platform interface
    python main.py --predict     # Run sample inference
"""

import argparse
import sys
from src.config import DEFAULT_PORT
from src.model_trainer import train_and_evaluate_all
from src.inference import predictor
from src.recommendations import SAMPLE_PERSONAS
from src.server import run_server


def main():
    parser = argparse.ArgumentParser(description="IBM Telco Churn & CLV Platform CLI")
    parser.add_argument("--train", action="store_true", help="Train baseline and champion models")
    parser.add_argument("--serve", action="store_true", help="Launch interactive web server")
    parser.add_argument("--port", type=int, default=DEFAULT_PORT, help="Port to serve web app on")
    parser.add_argument("--predict", action="store_true", help="Test sample inference on demo personas")

    args = parser.parse_args()

    if args.train:
        print("[CLI] Starting Model Training & Benchmark Pipeline...")
        train_and_evaluate_all()

    elif args.predict:
        print("[CLI] Testing Inference with Sample Persona...")
        persona = SAMPLE_PERSONAS[0]
        print(f"Customer Profile: {persona['name']}")
        result = predictor.evaluate_customer(persona)
        print(f"Predicted Churn Probability: {result['churn_probability']*100:.1f}%")
        print(f"Risk Tier: {result['risk_tier']}")
        print(f"Expected Remaining Lifetime: {result['clv']['expected_remaining_months']} months")
        print(f"Remaining CLV: ${result['clv']['clv_value']:,.2f}")
        print("Recommended Actions:")
        for r in result["recommendations"]:
            print(f" - [{r['action']}]: {r['detail']} ({r['impact']})")

    elif args.serve or len(sys.argv) == 1:
        print(f"[CLI] Starting Web Application on port {args.port}...")
        run_server(port=args.port)


if __name__ == "__main__":
    main()
