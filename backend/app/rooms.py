from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database import get_db
from app.models import ColdRoom
from app.schemas import ColdRoomCreate, ColdRoomRead

router = APIRouter(prefix="/api/v1/cold-rooms", tags=["cold rooms"])


@router.get("", response_model=list[ColdRoomRead])
def list_cold_rooms(db: Session = Depends(get_db)) -> list[ColdRoom]:
    return list(db.scalars(select(ColdRoom).order_by(ColdRoom.id)).all())


@router.post("", response_model=ColdRoomRead, status_code=status.HTTP_201_CREATED)
def create_cold_room(payload: ColdRoomCreate, db: Session = Depends(get_db)) -> ColdRoom:
    if payload.target_min_c >= payload.target_max_c:
        raise HTTPException(
            status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
            detail="target_min_c must be less than target_max_c",
        )
    room = ColdRoom(**payload.model_dump())
    db.add(room)
    db.commit()
    db.refresh(room)
    return room
