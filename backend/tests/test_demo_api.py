from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_demo_telemetry_returns_simulated_readings_and_risk() -> None:
    response = client.get("/api/v1/demo/telemetry?samples=6&seed=11")
    assert response.status_code == 200
    payload = response.json()
    assert payload["mode"] == "simulated"
    assert len(payload["readings"]) == 6
    assert 0 <= payload["risk"]["score"] <= 100
    assert payload["risk"]["advisory_only"] is True
    assert "Simulated" in payload["notice"]


def test_demo_telemetry_seed_is_repeatable_for_values() -> None:
    first = client.get("/api/v1/demo/telemetry?samples=5&seed=19").json()
    second = client.get("/api/v1/demo/telemetry?samples=5&seed=19").json()
    assert first["readings"] == second["readings"]
    assert first["risk"] == second["risk"]


def test_demo_telemetry_rejects_invalid_sample_count() -> None:
    response = client.get("/api/v1/demo/telemetry?samples=0")
    assert response.status_code == 422
