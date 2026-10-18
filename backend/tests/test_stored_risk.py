from fastapi.testclient import TestClient


def test_stored_risk_uses_cold_room_readings(client: TestClient) -> None:
    room_response = client.post(
        "/api/v1/cold-rooms",
        json={
            "name": "Risk Test Room",
            "location": "Ado-Ekiti",
            "commodity": "Tomatoes",
            "target_min_c": 2,
            "target_max_c": 8,
        },
    )
    assert room_response.status_code == 201
    room_id = room_response.json()["id"]

    response = client.post(
        f"/api/v1/cold-rooms/{room_id}/readings",
        json={
            "timestamp": "2026-10-18T10:00:00Z",
            "temperature_c": 10,
            "humidity_pct": 70,
            "battery_pct": 15,
            "solar_power_w": 0,
            "load_power_w": 330,
        },
    )
    assert response.status_code == 201

    risk_response = client.get(f"/api/v1/cold-rooms/{room_id}/risk")
    assert risk_response.status_code == 200
    risk = risk_response.json()
    assert risk["score"] >= 65
    assert risk["level"] in {"high", "critical"}
    assert risk["advisory_only"] is True


def test_stored_risk_returns_404_for_unknown_room(client: TestClient) -> None:
    response = client.get("/api/v1/cold-rooms/99999/risk")
    assert response.status_code == 404
