import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from app.database import Base, get_db
from app.main import app

test_engine = create_engine(
    "sqlite://",
    connect_args={"check_same_thread": False},
    poolclass=StaticPool,
)
TestingSessionLocal = sessionmaker(bind=test_engine, autoflush=False, autocommit=False)


@pytest.fixture()
def client():
    Base.metadata.create_all(bind=test_engine)

    def override_get_db():
        db = TestingSessionLocal()
        try:
            yield db
        finally:
            db.close()

    app.dependency_overrides[get_db] = override_get_db
    with TestClient(app) as test_client:
        yield test_client
    app.dependency_overrides.clear()
    Base.metadata.drop_all(bind=test_engine)


def test_create_and_list_cold_rooms(client: TestClient) -> None:
    payload = {
        "name": "Ado Produce Store",
        "location": "Ado-Ekiti, Ekiti State",
        "commodity": "Tomatoes",
        "target_min_c": 3,
        "target_max_c": 8,
    }
    created = client.post("/api/v1/cold-rooms", json=payload)
    assert created.status_code == 201
    assert created.json()["name"] == payload["name"]
    assert created.json()["commodity"] == "Tomatoes"

    listed = client.get("/api/v1/cold-rooms")
    assert listed.status_code == 200
    assert len(listed.json()) == 1
    assert listed.json()[0]["location"] == payload["location"]


def test_create_cold_room_rejects_reversed_temperature_bounds(client: TestClient) -> None:
    response = client.post(
        "/api/v1/cold-rooms",
        json={
            "name": "Bad bounds room",
            "location": "Lagos",
            "commodity": "Produce",
            "target_min_c": 9,
            "target_max_c": 4,
        },
    )
    assert response.status_code == 422
