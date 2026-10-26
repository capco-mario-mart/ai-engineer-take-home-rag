"""Minimal HTTP wrapper for the exercise; no external packages required."""

import json
from http.server import BaseHTTPRequestHandler, HTTPServer
from pathlib import Path
from typing import Any, Dict, List

from rag_assessment.core import answer_question
from rag_assessment.demo_model import generate


DATA_PATH = Path(__file__).resolve().parent.parent / "data" / "knowledge.json"


def load_documents() -> List[Dict[str, Any]]:
    with DATA_PATH.open(encoding="utf-8") as handle:
        return json.load(handle)


class Handler(BaseHTTPRequestHandler):
    def do_POST(self) -> None:
        if self.path != "/answer":
            self.send_error(404)
            return
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if length < 1 or length > 16_384:
                raise ValueError("invalid request size")
            payload = json.loads(self.rfile.read(length))
            if not isinstance(payload, dict):
                raise ValueError("expected a JSON object")
            question = payload.get("question")
            role = payload.get("role")
            if not isinstance(question, str) or not question.strip() or role not in ("general", "operations"):
                raise ValueError("question and valid role are required")
            result = answer_question(question, role, load_documents(), generate)
        except (ValueError, json.JSONDecodeError) as exc:
            self._send_json(400, {"error": str(exc)})
            return
        self._send_json(200, result)

    def _send_json(self, status: int, payload: Dict[str, Any]) -> None:
        body = json.dumps(payload).encode("utf-8")
        self.send_response(status)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)


if __name__ == "__main__":
    print("Serving on http://localhost:8000")
    HTTPServer(("127.0.0.1", 8000), Handler).serve_forever()
