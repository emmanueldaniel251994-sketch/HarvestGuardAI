from datetime import datetime
from typing import Literal

from pydantic import BaseModel, Field


class TelemetryReading(BaseModel):
    timestamp: datetime
    temperature_c: float = Field(ge=-30, le=60)
    humidity_pct: float = Field(ge=0, le=100)
    battery_pct: float = Field(ge=0, le=100)
    solar_power_w: float = Field(ge=0, le=100_000)
    load_power_w: float = Field(ge=0, le=100_000)


class RiskAssessment(BaseModel):
    score: int = Field(ge=0, le=100)
    level: Literal["low", "moderate", "high", "critical"]
    factors: list[str]
    advisory_only: bool = True


class TelemetryResponse(BaseModel):
    mode: Literal["simulated"] = "simulated"
    readings: list[TelemetryReading]
    risk: RiskAssessment
    notice: str = "Simulated data only; not a live sensor feed."


class ColdRoomCreate(BaseModel):
    name: str = Field(min_length=2, max_length=120)
    location: str = Field(min_length=2, max_length=200)
    commodity: str = Field(min_length=2, max_length=100)
    target_min_c: float = Field(default=2.0, ge=-30, le=30)
    target_max_c: float = Field(default=8.0, ge=-20, le=40)
    notes: str | None = Field(default=None, max_length=2000)
    active: bool = True


class ColdRoomRead(ColdRoomCreate):
    id: int
    created_at: datetime

    model_config = {"from_attributes": True}


class TelemetryRecordRead(TelemetryReading):
    id: int
    cold_room_id: int

    model_config = {"from_attributes": True}
