from typing import Any, List, Optional
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel, EmailStr

from school_management_system.database.session import get_db
from school_management_system.models.student import Student

router = APIRouter()


# Pydantic schemas
class StudentBase(BaseModel):
    first_name: str
    last_name: str
    date_of_birth: date
    gender: str
    enrollment_date: date
    grade_level: str
    student_id: str
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: bool = True
    parent_id: Optional[int] = None


class StudentCreate(StudentBase):
    pass


class StudentUpdate(BaseModel):
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    date_of_birth: Optional[date] = None
    gender: Optional[str] = None
    enrollment_date: Optional[date] = None
    grade_level: Optional[str] = None
    student_id: Optional[str] = None
    address: Optional[str] = None
    phone_number: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = None
    parent_id: Optional[int] = None


class StudentInDBBase(StudentBase):
    id: int

    class Config:
        orm_mode = True


class StudentResponse(StudentInDBBase):
    pass


@router.post("/", response_model=StudentResponse)
async def create_student(
    student_in: StudentCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create a new student.
    """
    # Check if student with this student_id already exists
    result = await db.execute(select(Student).where(Student.student_id == student_in.student_id))
    student = result.scalars().first()
    if student:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="A student with this student ID already exists.",
        )
    
    # Create new student
    student = Student(**student_in.dict())
    db.add(student)
    await db.commit()
    await db.refresh(student)
    return student


@router.get("/{student_id}", response_model=StudentResponse)
async def get_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a student by ID.
    """
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    return student


@router.get("/", response_model=List[StudentResponse])
async def get_students(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get all students.
    """
    result = await db.execute(select(Student).offset(skip).limit(limit))
    students = result.scalars().all()
    return students


@router.put("/{student_id}", response_model=StudentResponse)
async def update_student(
    student_id: int,
    student_in: StudentUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update a student.
    """
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    
    # Update student fields
    update_data = student_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(student, field, value)
    
    await db.commit()
    await db.refresh(student)
    return student


@router.delete("/{student_id}", response_model=StudentResponse)
async def delete_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Delete a student.
    """
    result = await db.execute(select(Student).where(Student.id == student_id))
    student = result.scalars().first()
    if not student:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Student not found",
        )
    
    await db.delete(student)
    await db.commit()
    return student


@router.get("/by-grade/{grade_level}", response_model=List[StudentResponse])
async def get_students_by_grade(
    grade_level: str,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get students by grade level.
    """
    result = await db.execute(select(Student).where(Student.grade_level == grade_level))
    students = result.scalars().all()
    return students


@router.get("/by-parent/{parent_id}", response_model=List[StudentResponse])
async def get_students_by_parent(
    parent_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get students by parent ID.
    """
    result = await db.execute(select(Student).where(Student.parent_id == parent_id))
    students = result.scalars().all()
    return students
