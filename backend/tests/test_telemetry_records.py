from fastapi.testclient import TestClient


def test_ingest_and_list_telemetry_records(client: TestClient) -> None:
    room_response = client.post(
        "/api/v1/cold-rooms",
        json={
            "name": "Telemetry Test Room",
            "location": "Ado-Ekiti",
            "commodity": "Tomatoes",
            "target_min_c": 3,
            "target_max_c": 8,
        },
    )
    assert room_response.status_code == 201
    room_id = room_response.json()["id"]

    reading = {
        "timestamp": "2026-10-18T10:00:00Z",
        "temperature_c": 4.5,
        "humidity_pct": 68,
        "battery_pct": 77,
        "solar_power_w": 410,
        "load_power_w": 320,
    }
    posted = client.post(f"/api/v1/cold-rooms/{room_id}/readings", json=reading)
    assert posted.status_code == 201
    assert posted.json()["cold_room_id"] == room_id
    assert posted.json()["temperature_c"] == 4.5

    history = client.get(f"/api/v1/cold-rooms/{room_id}/readings")
    assert history.status_code == 200
    assert len(history.json()) == 1
    assert history.json()[0]["battery_pct"] == 77


def test_ingest_rejects_unknown_cold_room(client: TestClient) -> None:
    response = client.post(
        "/api/v1/cold-rooms/99999/readings",
        json={
            "timestamp": "2026-10-18T10:00:00Z",
            "temperature_c": 4.5,
            "humidity_pct": 68,
            "battery_pct": 77,
            "solar_power_w": 410,
            "load_power_w": 320,
        },
    )
    assert response.status_code == 404
