"""
Customer Churn & CLV Intelligence Platform
Application Server Entry Point
"""

import sys
# pyrefly: ignore [missing-import]
from src.config import DEFAULT_PORT
# pyrefly: ignore [missing-import]
from src.server import run_server

if __name__ == "__main__":
    port = int(sys.argv[1]) if len(sys.argv) > 1 else DEFAULT_PORT
    run_server(port=port)
