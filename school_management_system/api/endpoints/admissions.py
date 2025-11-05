from typing import Any, List, Optional
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, EmailStr

from school_management_system.database.session import get_db
from school_management_system.models.admission import Admission, AdmissionStatus

router = APIRouter()


# Pydantic schemas
class AdmissionBase(BaseModel):
    application_date: date
    status: AdmissionStatus = AdmissionStatus.PENDING
    desired_grade_level: str
    previous_school: Optional[str] = None
    previous_grade_level: Optional[str] = None
    notes: Optional[str] = None
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    address: str
    phone_number: str
    email: Optional[str] = None
    parent_name: str
    parent_phone: str
    parent_email: Optional[str] = None
    parent_address: Optional[str] = None
    relationship_to_applicant: str
    student_id: Optional[int] = None


class AdmissionCreate(AdmissionBase):
    pass


class AdmissionUpdate(BaseModel):
    application_date: Optional[date] = None
    status: Optional[AdmissionStatus] = None
    desired_grade_level: Optional[str] = None
    previous_school: Optional[str] = None
    previous_grade_level: Optional[str] = None
    notes: Optional[str] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[str] = None
    parent_name: Optional[str] = None
    parent_phone: Optional[str] = None
    parent_email: Optional[str] = None
    parent_address: Optional[str] = None
    relationship_to_applicant: Optional[str] = None
    student_id: Optional[int] = None


class AdmissionInDBBase(AdmissionBase):
    id: int

    class Config:
        orm_mode = True


class AdmissionResponse(AdmissionInDBBase):
    pass


@router.post("/", response_model=AdmissionResponse)
async def create_admission(
    admission_in: AdmissionCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create a new admission application.
    """
    admission = Admission(**admission_in.dict())
    db.add(admission)
    await db.commit()
    await db.refresh(admission)
    return admission


@router.get("/{admission_id}", response_model=AdmissionResponse)
async def get_admission(
    admission_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get an admission application by ID.
    """
    result = await db.execute(select(Admission).where(Admission.id == admission_id))
    admission = result.scalars().first()
    if not admission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admission application not found",
        )
    return admission


@router.get("/", response_model=List[AdmissionResponse])
async def get_admissions(
    skip: int = 0,
    limit: int = 100,
    status: Optional[AdmissionStatus] = None,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get all admission applications with optional status filter.
    """
    query = select(Admission)
    if status:
        query = query.where(Admission.status == status)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    admissions = result.scalars().all()
    return admissions


@router.put("/{admission_id}", response_model=AdmissionResponse)
async def update_admission(
    admission_id: int,
    admission_in: AdmissionUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update an admission application.
    """
    result = await db.execute(select(Admission).where(Admission.id == admission_id))
    admission = result.scalars().first()
    if not admission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admission application not found",
        )
    
    # Update admission fields
    update_data = admission_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(admission, field, value)
    
    await db.commit()
    await db.refresh(admission)
    return admission


@router.delete("/{admission_id}", response_model=AdmissionResponse)
async def delete_admission(
    admission_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Delete an admission application.
    """
    result = await db.execute(select(Admission).where(Admission.id == admission_id))
    admission = result.scalars().first()
    if not admission:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Admission application not found",
        )
    
    await db.delete(admission)
    await db.commit()
    return admission


@router.get("/by-status/{status}", response_model=List[AdmissionResponse])
async def get_admissions_by_status(
    status: AdmissionStatus,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get admission applications by status.
    """
    result = await db.execute(select(Admission).where(Admission.status == status))
    admissions = result.scalars().all()
    return admissions
