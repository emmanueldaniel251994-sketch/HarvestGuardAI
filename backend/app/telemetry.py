from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ColdRoom, TelemetryRecord
from app.risk import assess_risk
from app.schemas import RiskAssessment, TelemetryBatchCreate, TelemetryReading, TelemetryRecordRead
from app.security import require_device_api_key
from app.simulator import generate_readings

router = APIRouter(prefix="/api/v1/cold-rooms", tags=["telemetry"])


@router.post(
    "/{cold_room_id}/readings",
    response_model=TelemetryRecordRead,
    status_code=status.HTTP_201_CREATED,
)
def ingest_reading(
    cold_room_id: int,
    payload: TelemetryReading,
    db: Session = Depends(get_db),
    _: None = Depends(require_device_api_key),
) -> TelemetryRecord:
    room = db.get(ColdRoom, cold_room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Cold room not found")
    record = TelemetryRecord(cold_room_id=cold_room_id, **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


@router.post(
    "/{cold_room_id}/readings/bulk",
    response_model=list[TelemetryRecordRead],
    status_code=status.HTTP_201_CREATED,
)
def ingest_readings_bulk(
    cold_room_id: int,
    payload: TelemetryBatchCreate,
    db: Session = Depends(get_db),
    _: None = Depends(require_device_api_key),
) -> list[TelemetryRecord]:
    """Persist a bounded batch in one transaction for authenticated devices."""
    if db.get(ColdRoom, cold_room_id) is None:
        raise HTTPException(status_code=404, detail="Cold room not found")
    records = [
        TelemetryRecord(cold_room_id=cold_room_id, **reading.model_dump())
        for reading in payload.readings
    ]
    db.add_all(records)
    db.commit()
    for record in records:
        db.refresh(record)
    return records


@router.post(
    "/{cold_room_id}/readings/demo",
    response_model=list[TelemetryRecordRead],
    status_code=status.HTTP_201_CREATED,
)
def save_demo_readings(
    cold_room_id: int,
    samples: int = Query(default=24, ge=1, le=168),
    seed: int = Query(default=42, ge=0, le=2_147_483_647),
    db: Session = Depends(get_db),
) -> list[TelemetryRecord]:
    """Generate and persist clearly synthetic demo readings; never accepts sensor data."""
    if db.get(ColdRoom, cold_room_id) is None:
        raise HTTPException(status_code=404, detail="Cold room not found")
    readings = generate_readings(samples=samples, seed=seed)
    records = [
        TelemetryRecord(cold_room_id=cold_room_id, **reading.model_dump())
        for reading in readings
    ]
    db.add_all(records)
    db.commit()
    for record in records:
        db.refresh(record)
    return records


@router.get("/{cold_room_id}/readings", response_model=list[TelemetryRecordRead])
def list_readings(
    cold_room_id: int,
    limit: int = Query(default=100, ge=1, le=500),
    db: Session = Depends(get_db),
) -> list[TelemetryRecord]:
    if db.get(ColdRoom, cold_room_id) is None:
        raise HTTPException(status_code=404, detail="Cold room not found")
    query = (
        select(TelemetryRecord)
        .where(TelemetryRecord.cold_room_id == cold_room_id)
        .order_by(TelemetryRecord.timestamp.desc(), TelemetryRecord.id.desc())
        .limit(limit)
    )
    return list(db.scalars(query).all())


@router.get("/{cold_room_id}/risk", response_model=RiskAssessment)
def assess_stored_room_risk(
    cold_room_id: int,
    limit: int = Query(default=24, ge=1, le=168),
    db: Session = Depends(get_db),
) -> RiskAssessment:
    """Return advisory threshold-based risk from the latest stored readings."""
    room = db.get(ColdRoom, cold_room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Cold room not found")
    query = (
        select(TelemetryRecord)
        .where(TelemetryRecord.cold_room_id == cold_room_id)
        .order_by(TelemetryRecord.timestamp.desc(), TelemetryRecord.id.desc())
        .limit(limit)
    )
    newest_first = list(db.scalars(query).all())
    readings = [
        TelemetryReading.model_validate(record, from_attributes=True)
        for record in reversed(newest_first)
    ]
    return assess_risk(
        readings,
        target_min_c=room.target_min_c,
        target_max_c=room.target_max_c,
    )
