from typing import Any, List, Optional
from datetime import date

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from school_management_system.database.session import get_db
from school_management_system.models.exam import Exam, ExamType, ExamResult

router = APIRouter()


# Pydantic schemas for Exam
class ExamBase(BaseModel):
    name: str
    description: Optional[str] = None
    exam_type: ExamType
    date: date
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    total_marks: float
    passing_marks: float
    grade_level: str
    academic_year: str
    term: str
    instructions: Optional[str] = None


class ExamCreate(ExamBase):
    pass


class ExamUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    exam_type: Optional[ExamType] = None
    date: Optional[date] = None
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    total_marks: Optional[float] = None
    passing_marks: Optional[float] = None
    grade_level: Optional[str] = None
    academic_year: Optional[str] = None
    term: Optional[str] = None
    instructions: Optional[str] = None


class ExamInDBBase(ExamBase):
    id: int

    class Config:
        from_attributes = True


class ExamResponse(ExamInDBBase):
    pass


# Pydantic schemas for ExamResult
class ExamResultBase(BaseModel):
    score: float
    grade: Optional[str] = None
    remarks: Optional[str] = None
    student_id: int
    exam_id: int
    subject_id: int


class ExamResultCreate(ExamResultBase):
    pass


class ExamResultUpdate(BaseModel):
    score: Optional[float] = None
    grade: Optional[str] = None
    remarks: Optional[str] = None


class ExamResultInDBBase(ExamResultBase):
    id: int

    class Config:
        from_attributes = True


class ExamResultResponse(ExamResultInDBBase):
    pass


# Exam endpoints
@router.post("/", response_model=ExamResponse)
async def create_exam(
    exam_in: ExamCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create a new exam.
    """
    exam = Exam(**exam_in.dict())
    db.add(exam)
    await db.commit()
    await db.refresh(exam)
    return exam


@router.get("/{exam_id}", response_model=ExamResponse)
async def get_exam(
    exam_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get an exam by ID.
    """
    result = await db.execute(select(Exam).where(Exam.id == exam_id))
    exam = result.scalars().first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found",
        )
    return exam


@router.get("/", response_model=List[ExamResponse])
async def get_exams(
    skip: int = 0,
    limit: int = 100,
    exam_type: Optional[ExamType] = None,
    grade_level: Optional[str] = None,
    academic_year: Optional[str] = None,
    term: Optional[str] = None,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get all exams with optional filters.
    """
    query = select(Exam)
    
    if exam_type:
        query = query.where(Exam.exam_type == exam_type)
    
    if grade_level:
        query = query.where(Exam.grade_level == grade_level)
    
    if academic_year:
        query = query.where(Exam.academic_year == academic_year)
    
    if term:
        query = query.where(Exam.term == term)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    exams = result.scalars().all()
    return exams


@router.put("/{exam_id}", response_model=ExamResponse)
async def update_exam(
    exam_id: int,
    exam_in: ExamUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update an exam.
    """
    result = await db.execute(select(Exam).where(Exam.id == exam_id))
    exam = result.scalars().first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found",
        )
    
    # Update exam fields
    update_data = exam_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(exam, field, value)
    
    await db.commit()
    await db.refresh(exam)
    return exam


@router.delete("/{exam_id}", response_model=ExamResponse)
async def delete_exam(
    exam_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Delete an exam.
    """
    result = await db.execute(select(Exam).where(Exam.id == exam_id))
    exam = result.scalars().first()
    if not exam:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found",
        )
    
    await db.delete(exam)
    await db.commit()
    return exam


# ExamResult endpoints
@router.post("/results/", response_model=ExamResultResponse)
async def create_exam_result(
    result_in: ExamResultCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create a new exam result.
    """
    # Check if exam exists
    exam_result = await db.execute(select(Exam).where(Exam.id == result_in.exam_id))
    if not exam_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam not found",
        )
    
    # Check if result already exists for this student, exam, and subject
    query = select(ExamResult).where(
        ExamResult.student_id == result_in.student_id,
        ExamResult.exam_id == result_in.exam_id,
        ExamResult.subject_id == result_in.subject_id
    )
    existing_result = await db.execute(query)
    if existing_result.scalars().first():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Result already exists for this student, exam, and subject",
        )
    
    result = ExamResult(**result_in.dict())
    db.add(result)
    await db.commit()
    await db.refresh(result)
    return result


@router.get("/results/{result_id}", response_model=ExamResultResponse)
async def get_exam_result(
    result_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get an exam result by ID.
    """
    result = await db.execute(select(ExamResult).where(ExamResult.id == result_id))
    exam_result = result.scalars().first()
    if not exam_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam result not found",
        )
    return exam_result


@router.get("/results/by-exam/{exam_id}", response_model=List[ExamResultResponse])
async def get_results_by_exam(
    exam_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get all results for a specific exam.
    """
    result = await db.execute(select(ExamResult).where(ExamResult.exam_id == exam_id))
    exam_results = result.scalars().all()
    return exam_results


@router.get("/results/by-student/{student_id}", response_model=List[ExamResultResponse])
async def get_results_by_student(
    student_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get all results for a specific student.
    """
    result = await db.execute(select(ExamResult).where(ExamResult.student_id == student_id))
    exam_results = result.scalars().all()
    return exam_results


@router.put("/results/{result_id}", response_model=ExamResultResponse)
async def update_exam_result(
    result_id: int,
    result_in: ExamResultUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update an exam result.
    """
    result = await db.execute(select(ExamResult).where(ExamResult.id == result_id))
    exam_result = result.scalars().first()
    if not exam_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam result not found",
        )
    
    # Update exam result fields
    update_data = result_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(exam_result, field, value)
    
    await db.commit()
    await db.refresh(exam_result)
    return exam_result


@router.delete("/results/{result_id}", response_model=ExamResultResponse)
async def delete_exam_result(
    result_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Delete an exam result.
    """
    result = await db.execute(select(ExamResult).where(ExamResult.id == result_id))
    exam_result = result.scalars().first()
    if not exam_result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Exam result not found",
        )
    
    await db.delete(exam_result)
    await db.commit()
    return exam_result
