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


def test_stored_risk_uses_room_specific_temperature_range(client: TestClient) -> None:
    room_response = client.post(
        "/api/v1/cold-rooms",
        json={
            "name": "Warm Produce Trial",
            "location": "Ado-Ekiti",
            "commodity": "Example commodity",
            "target_min_c": 10,
            "target_max_c": 15,
        },
    )
    assert room_response.status_code == 201
    room_id = room_response.json()["id"]

    posted = client.post(
        f"/api/v1/cold-rooms/{room_id}/readings",
        json={
            "timestamp": "2026-10-18T10:00:00Z",
            "temperature_c": 8,
            "humidity_pct": 70,
            "battery_pct": 80,
            "solar_power_w": 400,
            "load_power_w": 300,
        },
    )
    assert posted.status_code == 201

    risk = client.get(f"/api/v1/cold-rooms/{room_id}/risk").json()
    assert risk["score"] == 25
    assert any("configured minimum (10°C)" in factor for factor in risk["factors"])
