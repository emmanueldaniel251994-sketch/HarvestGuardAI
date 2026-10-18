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
