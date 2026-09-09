from pathlib import Path

from fastapi.testclient import TestClient

from app.main import app
from app.services.retrieval import Retriever


def setup_module() -> None:
    app.state.retriever = Retriever(
        Path("data/documents"),
        Path("data/vector_store/index.json"),
    )


def test_health() -> None:
    with TestClient(app) as client:
        response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "ok"}


def test_query_returns_grounded_source() -> None:
    with TestClient(app) as client:
        response = client.post(
            "/query",
            json={"question": "Why should expensive resources load during application lifespan?"},
        )
    assert response.status_code == 200
    payload = response.json()
    assert payload["retrieval"]["grounded"] is True
    assert payload["sources"]
    assert "lifespan" in payload["answer"].lower()


def test_query_rejects_short_input() -> None:
    with TestClient(app) as client:
        response = client.post("/query", json={"question": "x"})
    assert response.status_code == 422