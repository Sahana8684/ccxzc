from typing import Any, List, Optional
from datetime import time

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from school_management_system.database.session import get_db
from school_management_system.models.timetable import Timetable, TimetableSlot, DayOfWeek

router = APIRouter()


# Pydantic schemas for Timetable
class TimetableBase(BaseModel):
    name: str
    description: Optional[str] = None
    academic_year: str
    term: str
    grade_level: str
    section: Optional[str] = None
    is_active: bool = True


class TimetableCreate(TimetableBase):
    pass


class TimetableUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    academic_year: Optional[str] = None
    term: Optional[str] = None
    grade_level: Optional[str] = None
    section: Optional[str] = None
    is_active: Optional[bool] = None


class TimetableInDBBase(TimetableBase):
    id: int

    class Config:
        orm_mode = True


class TimetableResponse(TimetableInDBBase):
    pass


# Pydantic schemas for TimetableSlot
class TimetableSlotBase(BaseModel):
    day: DayOfWeek
    start_time: time
    end_time: time
    room_number: Optional[str] = None
    timetable_id: int
    subject_id: int
    teacher_id: Optional[int] = None


class TimetableSlotCreate(TimetableSlotBase):
    pass


class TimetableSlotUpdate(BaseModel):
    day: Optional[DayOfWeek] = None
    start_time: Optional[time] = None
    end_time: Optional[time] = None
    room_number: Optional[str] = None
    subject_id: Optional[int] = None
    teacher_id: Optional[int] = None


class TimetableSlotInDBBase(TimetableSlotBase):
    id: int

    class Config:
        orm_mode = True


class TimetableSlotResponse(TimetableSlotInDBBase):
    pass


# Timetable endpoints
@router.post("/", response_model=TimetableResponse)
async def create_timetable(
    timetable_in: TimetableCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create a new timetable.
    """
    timetable = Timetable(**timetable_in.dict())
    db.add(timetable)
    await db.commit()
    await db.refresh(timetable)
    return timetable


@router.get("/{timetable_id}", response_model=TimetableResponse)
async def get_timetable(
    timetable_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a timetable by ID.
    """
    result = await db.execute(select(Timetable).where(Timetable.id == timetable_id))
    timetable = result.scalars().first()
    if not timetable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable not found",
        )
    return timetable


@router.get("/", response_model=List[TimetableResponse])
async def get_timetables(
    skip: int = 0,
    limit: int = 100,
    academic_year: Optional[str] = None,
    grade_level: Optional[str] = None,
    is_active: bool = True,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get all timetables with optional filters.
    """
    query = select(Timetable)
    
    if academic_year:
        query = query.where(Timetable.academic_year == academic_year)
    
    if grade_level:
        query = query.where(Timetable.grade_level == grade_level)
    
    query = query.where(Timetable.is_active == is_active)
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    timetables = result.scalars().all()
    return timetables


@router.put("/{timetable_id}", response_model=TimetableResponse)
async def update_timetable(
    timetable_id: int,
    timetable_in: TimetableUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update a timetable.
    """
    result = await db.execute(select(Timetable).where(Timetable.id == timetable_id))
    timetable = result.scalars().first()
    if not timetable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable not found",
        )
    
    # Update timetable fields
    update_data = timetable_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(timetable, field, value)
    
    await db.commit()
    await db.refresh(timetable)
    return timetable


@router.delete("/{timetable_id}", response_model=TimetableResponse)
async def delete_timetable(
    timetable_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Delete a timetable.
    """
    result = await db.execute(select(Timetable).where(Timetable.id == timetable_id))
    timetable = result.scalars().first()
    if not timetable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable not found",
        )
    
    await db.delete(timetable)
    await db.commit()
    return timetable


# TimetableSlot endpoints
@router.post("/slots/", response_model=TimetableSlotResponse)
async def create_timetable_slot(
    slot_in: TimetableSlotCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create a new timetable slot.
    """
    # Check if timetable exists
    result = await db.execute(select(Timetable).where(Timetable.id == slot_in.timetable_id))
    timetable = result.scalars().first()
    if not timetable:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable not found",
        )
    
    # Check for time conflicts
    query = select(TimetableSlot).where(
        TimetableSlot.timetable_id == slot_in.timetable_id,
        TimetableSlot.day == slot_in.day,
        TimetableSlot.start_time < slot_in.end_time,
        TimetableSlot.end_time > slot_in.start_time
    )
    result = await db.execute(query)
    conflicts = result.scalars().all()
    
    if conflicts:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Time slot conflicts with existing slots",
        )
    
    slot = TimetableSlot(**slot_in.dict())
    db.add(slot)
    await db.commit()
    await db.refresh(slot)
    return slot


@router.get("/slots/{slot_id}", response_model=TimetableSlotResponse)
async def get_timetable_slot(
    slot_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a timetable slot by ID.
    """
    result = await db.execute(select(TimetableSlot).where(TimetableSlot.id == slot_id))
    slot = result.scalars().first()
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable slot not found",
        )
    return slot


@router.get("/slots/by-timetable/{timetable_id}", response_model=List[TimetableSlotResponse])
async def get_timetable_slots(
    timetable_id: int,
    day: Optional[DayOfWeek] = None,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get all slots for a specific timetable with optional day filter.
    """
    query = select(TimetableSlot).where(TimetableSlot.timetable_id == timetable_id)
    
    if day:
        query = query.where(TimetableSlot.day == day)
    
    query = query.order_by(TimetableSlot.day, TimetableSlot.start_time)
    result = await db.execute(query)
    slots = result.scalars().all()
    return slots


@router.put("/slots/{slot_id}", response_model=TimetableSlotResponse)
async def update_timetable_slot(
    slot_id: int,
    slot_in: TimetableSlotUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update a timetable slot.
    """
    result = await db.execute(select(TimetableSlot).where(TimetableSlot.id == slot_id))
    slot = result.scalars().first()
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable slot not found",
        )
    
    # Check for time conflicts if time is being updated
    if slot_in.day or slot_in.start_time or slot_in.end_time:
        day = slot_in.day or slot.day
        start_time = slot_in.start_time or slot.start_time
        end_time = slot_in.end_time or slot.end_time
        
        query = select(TimetableSlot).where(
            TimetableSlot.id != slot_id,
            TimetableSlot.timetable_id == slot.timetable_id,
            TimetableSlot.day == day,
            TimetableSlot.start_time < end_time,
            TimetableSlot.end_time > start_time
        )
        result = await db.execute(query)
        conflicts = result.scalars().all()
        
        if conflicts:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="Time slot conflicts with existing slots",
            )
    
    # Update slot fields
    update_data = slot_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(slot, field, value)
    
    await db.commit()
    await db.refresh(slot)
    return slot


@router.delete("/slots/{slot_id}", response_model=TimetableSlotResponse)
async def delete_timetable_slot(
    slot_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Delete a timetable slot.
    """
    result = await db.execute(select(TimetableSlot).where(TimetableSlot.id == slot_id))
    slot = result.scalars().first()
    if not slot:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Timetable slot not found",
        )
    
    await db.delete(slot)
    await db.commit()
    return slot
