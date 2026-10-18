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


def test_bulk_ingest_persists_multiple_readings(client: TestClient) -> None:
    room_response = client.post(
        "/api/v1/cold-rooms",
        json={
            "name": "Bulk Test Room",
            "location": "Ado-Ekiti",
            "commodity": "Peppers",
            "target_min_c": 2,
            "target_max_c": 8,
        },
    )
    assert room_response.status_code == 201
    room_id = room_response.json()["id"]
    readings = [
        {
            "timestamp": f"2026-10-18T{hour:02d}:00:00Z",
            "temperature_c": 4.0 + hour / 10,
            "humidity_pct": 66,
            "battery_pct": 80,
            "solar_power_w": 300,
            "load_power_w": 320,
        }
        for hour in range(3)
    ]

    posted = client.post(
        f"/api/v1/cold-rooms/{room_id}/readings/bulk",
        json={"readings": readings},
    )
    assert posted.status_code == 201
    assert len(posted.json()) == 3
    history = client.get(f"/api/v1/cold-rooms/{room_id}/readings")
    assert history.status_code == 200
    assert len(history.json()) == 3


def test_device_ingestion_requires_configured_api_key(client: TestClient, monkeypatch) -> None:
    from app.config import settings

    monkeypatch.setattr(settings, "device_api_key", "test-device-secret")
    room_response = client.post(
        "/api/v1/cold-rooms",
        json={
            "name": "Protected Room",
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

    missing_key = client.post(f"/api/v1/cold-rooms/{room_id}/readings", json=reading)
    assert missing_key.status_code == 401
    wrong_key = client.post(
        f"/api/v1/cold-rooms/{room_id}/readings",
        json=reading,
        headers={"X-Device-API-Key": "wrong"},
    )
    assert wrong_key.status_code == 401
    valid_key = client.post(
        f"/api/v1/cold-rooms/{room_id}/readings",
        json=reading,
        headers={"X-Device-API-Key": "test-device-secret"},
    )
    assert valid_key.status_code == 201


def test_device_ingestion_fails_closed_in_production_without_key(
    client: TestClient, monkeypatch
) -> None:
    from app.config import settings

    monkeypatch.setattr(settings, "app_env", "production")
    monkeypatch.setattr(settings, "device_api_key", "")
    response = client.post(
        "/api/v1/cold-rooms/1/readings",
        json={
            "timestamp": "2026-10-18T10:00:00Z",
            "temperature_c": 4.5,
            "humidity_pct": 68,
            "battery_pct": 77,
            "solar_power_w": 410,
            "load_power_w": 320,
        },
    )
    assert response.status_code == 503


def test_demo_endpoint_persists_synthetic_readings(client: TestClient) -> None:
    room_response = client.post(
        "/api/v1/cold-rooms",
        json={
            "name": "Demo Only Room",
            "location": "Ado-Ekiti",
            "commodity": "Tomatoes",
            "target_min_c": 3,
            "target_max_c": 8,
        },
    )
    assert room_response.status_code == 201
    room_id = room_response.json()["id"]

    response = client.post(
        f"/api/v1/cold-rooms/{room_id}/readings/demo?samples=5&seed=42"
    )
    assert response.status_code == 201
    records = response.json()
    assert len(records) == 5
    assert all(record["cold_room_id"] == room_id for record in records)
    history = client.get(f"/api/v1/cold-rooms/{room_id}/readings")
    assert history.status_code == 200
    assert len(history.json()) == 5
