from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ColdRoom, TelemetryRecord
from app.schemas import TelemetryReading, TelemetryRecordRead

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
) -> TelemetryRecord:
    room = db.get(ColdRoom, cold_room_id)
    if room is None:
        raise HTTPException(status_code=404, detail="Cold room not found")
    record = TelemetryRecord(cold_room_id=cold_room_id, **payload.model_dump())
    db.add(record)
    db.commit()
    db.refresh(record)
    return record


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
