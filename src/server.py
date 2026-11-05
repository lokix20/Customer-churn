"""
HTTP Server and REST API router for the Churn Intelligence Platform.
"""

import http.server
import socketserver
import json
import os
import urllib.parse
from typing import Tuple

from src.config import DEFAULT_PORT, TEMPLATES_DIR, STATIC_DIR
from src.inference import predictor
from src.recommendations import SAMPLE_PERSONAS


class ChurnPlatformHandler(http.server.BaseHTTPRequestHandler):
    def log_message(self, format, *args):
        pass  # Quiet logger for clean terminal output

    def do_GET(self):
        parsed_url = urllib.parse.urlparse(self.path)
        url_path = parsed_url.path

        # 1. Root & Index page
        if url_path in ["/", "/index.html"]:
            index_path = TEMPLATES_DIR / "index.html"
            if index_path.exists():
                with open(index_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self._send_response(200, "text/html; charset=utf-8", content.encode("utf-8"))
            else:
                self.send_error(404, "Index template not found")

        # 2. Static CSS files
        elif url_path.startswith("/static/css/"):
            filename = os.path.basename(url_path)
            css_path = STATIC_DIR / "css" / filename
            if css_path.exists():
                with open(css_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self._send_response(200, "text/css; charset=utf-8", content.encode("utf-8"))
            else:
                self.send_error(404, f"CSS file {filename} not found")

        # 3. Static JS files
        elif url_path.startswith("/static/js/"):
            filename = os.path.basename(url_path)
            js_path = STATIC_DIR / "js" / filename
            if js_path.exists():
                with open(js_path, "r", encoding="utf-8") as f:
                    content = f.read()
                self._send_response(200, "application/javascript; charset=utf-8", content.encode("utf-8"))
            else:
                self.send_error(404, f"JS file {filename} not found")

        # 4. API: Platform Stats & Personas
        elif url_path == "/api/stats":
            resp = {
                "total_records": 7043,
                "churn_rate": 0.2654,
                "contract_churn": {
                    "Month-to-month": 0.427,
                    "One year": 0.113,
                    "Two year": 0.028
                },
                "personas": SAMPLE_PERSONAS
            }
            self._send_json(200, resp)

        # 5. Health Check
        elif url_path == "/api/health":
            self._send_json(200, {"status": "healthy", "model_loaded": predictor.model is not None})

        else:
            self.send_error(404, "Not Found")

    def do_POST(self):
        parsed_url = urllib.parse.urlparse(self.path)
        url_path = parsed_url.path

        if url_path == "/api/predict":
            length = int(self.headers.get("Content-Length", 0))
            body = self.rfile.read(length)
            try:
                data = json.loads(body.decode("utf-8"))
                evaluation = predictor.evaluate_customer(data)
                self._send_json(200, evaluation)
            except Exception as e:
                self._send_json(500, {"error": str(e)})
        else:
            self.send_error(404, "Not Found")

    def _send_response(self, code: int, content_type: str, content: bytes):
        self.send_response(code)
        self.send_header("Content-Type", content_type)
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def _send_json(self, code: int, data: dict):
        payload = json.dumps(data).encode("utf-8")
        self._send_response(code, "application/json", payload)


def run_server(port: int = DEFAULT_PORT):
    server_address = ("", port)
    with socketserver.TCPServer(server_address, ChurnPlatformHandler) as httpd:
        print("\n" + "="*60)
        print("  Customer Churn & CLV Platform Server Active!")
        print(f"  Access in browser: http://localhost:{port}")
        print("="*60 + "\n")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down server.")


if __name__ == "__main__":
    run_server()
