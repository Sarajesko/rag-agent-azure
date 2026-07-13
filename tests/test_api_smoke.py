import sys
from pathlib import Path
from unittest.mock import MagicMock, patch

from fastapi.testclient import TestClient

sys.path.append(str(Path(__file__).resolve().parents[1]))

from api import app


def test_root_status_code() -> None:
    client = TestClient(app)
    response = client.get("/")
    assert response.status_code == 200


def test_root_contains_routes() -> None:
    client = TestClient(app)
    response = client.get("/")
    payload = response.json()
    assert "routes" in payload
    assert "/health" in payload["routes"]
    assert "/ask" in payload["routes"]


def test_health_reports_database_error_without_connection() -> None:
    client = TestClient(app)
    with patch("api.get_connection", side_effect=RuntimeError("sin conexion")):
        response = client.get("/health")
    assert response.status_code == 200
    payload = response.json()
    assert payload["status"] == "error"
    assert payload["database"] == "not connected"


def test_ask_returns_sources_with_mocked_agent() -> None:
    client = TestClient(app)
    mocked_response = {
        "question": "Que es RAG?",
        "answer": "Respuesta demo",
        "sources": [{"title": "Que es RAG", "source": "guia", "score": 0.91}],
    }
    with patch("api.ask_agent", return_value=mocked_response):
        response = client.post("/ask", json={"question": "Que es RAG?"})
    assert response.status_code == 200
    assert response.json()["sources"]
