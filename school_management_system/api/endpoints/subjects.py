from typing import Any, List, Optional

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from school_management_system.database.session import get_db
from school_management_system.models.subject import Subject

router = APIRouter()


# Pydantic schemas
class SubjectBase(BaseModel):
    name: str
    code: str
    description: Optional[str] = None
    grade_level: str
    credits: Optional[int] = None
    is_active: bool = True
    teacher_id: Optional[int] = None


class SubjectCreate(SubjectBase):
    pass


class SubjectUpdate(BaseModel):
    name: Optional[str] = None
    code: Optional[str] = None
    description: Optional[str] = None
    grade_level: Optional[str] = None
    credits: Optional[int] = None
    is_active: Optional[bool] = None
    teacher_id: Optional[int] = None


class SubjectInDBBase(SubjectBase):
    id: int

    class Config:
        orm_mode = True


class SubjectResponse(SubjectInDBBase):
    pass


@router.post("/", response_model=SubjectResponse)
async def create_subject(
    subject_in: SubjectCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create a new subject.
    """
    # Check if subject with this code already exists
    result = await db.execute(select(Subject).where(Subject.code == subject_in.code))
    existing_subject = result.scalars().first()
    if existing_subject:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A subject with this code already exists.",
        )
    
    subject = Subject(**subject_in.dict())
    db.add(subject)
    await db.commit()
    await db.refresh(subject)
    return subject


@router.get("/{subject_id}", response_model=SubjectResponse)
async def get_subject(
    subject_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a subject by ID.
    """
    result = await db.execute(select(Subject).where(Subject.id == subject_id))
    subject = result.scalars().first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )
    return subject


@router.get("/", response_model=List[SubjectResponse])
async def get_subjects(
    skip: int = 0,
    limit: int = 100,
    grade_level: Optional[str] = None,
    is_active: bool = True,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get all subjects with optional filters.
    """
    query = select(Subject)
    
    if grade_level:
        query = query.where(Subject.grade_level == grade_level)
    
    query = query.where(Subject.is_active == is_active)
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    subjects = result.scalars().all()
    return subjects


@router.put("/{subject_id}", response_model=SubjectResponse)
async def update_subject(
    subject_id: int,
    subject_in: SubjectUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update a subject.
    """
    result = await db.execute(select(Subject).where(Subject.id == subject_id))
    subject = result.scalars().first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )
    
    # Check if code is being updated and if it already exists
    if subject_in.code and subject_in.code != subject.code:
        result = await db.execute(select(Subject).where(Subject.code == subject_in.code))
        existing_subject = result.scalars().first()
        if existing_subject:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="A subject with this code already exists.",
            )
    
    # Update subject fields
    update_data = subject_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(subject, field, value)
    
    await db.commit()
    await db.refresh(subject)
    return subject


@router.delete("/{subject_id}", response_model=SubjectResponse)
async def delete_subject(
    subject_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Delete a subject.
    """
    result = await db.execute(select(Subject).where(Subject.id == subject_id))
    subject = result.scalars().first()
    if not subject:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Subject not found",
        )
    
    await db.delete(subject)
    await db.commit()
    return subject


@router.get("/by-teacher/{teacher_id}", response_model=List[SubjectResponse])
async def get_subjects_by_teacher(
    teacher_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get subjects taught by a specific teacher.
    """
    result = await db.execute(select(Subject).where(Subject.teacher_id == teacher_id))
    subjects = result.scalars().all()
    return subjects


@router.get("/by-grade/{grade_level}", response_model=List[SubjectResponse])
async def get_subjects_by_grade(
    grade_level: str,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get subjects for a specific grade level.
    """
    result = await db.execute(select(Subject).where(Subject.grade_level == grade_level))
    subjects = result.scalars().all()
    return subjects
