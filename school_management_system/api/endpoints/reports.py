from typing import Any, List, Optional
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from school_management_system.database.session import get_db
from school_management_system.models.report import Report, ReportType

router = APIRouter()


# Pydantic schemas
class ReportBase(BaseModel):
    title: str
    description: Optional[str] = None
    report_type: ReportType
    parameters: Optional[str] = None
    file_path: Optional[str] = None
    is_scheduled: bool = False
    schedule_frequency: Optional[str] = None
    next_run: Optional[datetime] = None


class ReportCreate(ReportBase):
    created_by: int


class ReportUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    report_type: Optional[ReportType] = None
    parameters: Optional[str] = None
    file_path: Optional[str] = None
    is_scheduled: Optional[bool] = None
    schedule_frequency: Optional[str] = None
    last_run: Optional[datetime] = None
    next_run: Optional[datetime] = None


class ReportInDBBase(ReportBase):
    id: int
    created_at: datetime
    created_by: int
    last_run: Optional[datetime] = None

    class Config:
        orm_mode = True


class ReportResponse(ReportInDBBase):
    pass


@router.post("/", response_model=ReportResponse)
async def create_report(
    report_in: ReportCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create a new report.
    """
    report = Report(**report_in.dict())
    db.add(report)
    await db.commit()
    await db.refresh(report)
    return report


@router.get("/{report_id}", response_model=ReportResponse)
async def get_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a report by ID.
    """
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalars().first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )
    return report


@router.get("/", response_model=List[ReportResponse])
async def get_reports(
    skip: int = 0,
    limit: int = 100,
    report_type: Optional[ReportType] = None,
    is_scheduled: Optional[bool] = None,
    created_by: Optional[int] = None,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get all reports with optional filters.
    """
    query = select(Report)
    
    if report_type:
        query = query.where(Report.report_type == report_type)
    
    if is_scheduled is not None:
        query = query.where(Report.is_scheduled == is_scheduled)
    
    if created_by:
        query = query.where(Report.created_by == created_by)
    
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    reports = result.scalars().all()
    return reports


@router.put("/{report_id}", response_model=ReportResponse)
async def update_report(
    report_id: int,
    report_in: ReportUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update a report.
    """
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalars().first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )
    
    # Update report fields
    update_data = report_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(report, field, value)
    
    await db.commit()
    await db.refresh(report)
    return report


@router.delete("/{report_id}", response_model=ReportResponse)
async def delete_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Delete a report.
    """
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalars().first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )
    
    await db.delete(report)
    await db.commit()
    return report


@router.post("/{report_id}/run", response_model=ReportResponse)
async def run_report(
    report_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Run a report manually.
    """
    result = await db.execute(select(Report).where(Report.id == report_id))
    report = result.scalars().first()
    if not report:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Report not found",
        )
    
    # In a real application, this would trigger the report generation process
    # For now, we'll just update the last_run timestamp
    report.last_run = datetime.now()
    
    # If the report is scheduled, update the next_run timestamp based on frequency
    if report.is_scheduled and report.schedule_frequency:
        # This is a simplified example - in a real app, you'd calculate the next run time
        # based on the frequency (daily, weekly, monthly, etc.)
        if report.schedule_frequency == "daily":
            report.next_run = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            report.next_run = report.next_run.replace(day=report.next_run.day + 1)
        elif report.schedule_frequency == "weekly":
            report.next_run = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            report.next_run = report.next_run.replace(day=report.next_run.day + 7)
        elif report.schedule_frequency == "monthly":
            report.next_run = datetime.now().replace(hour=0, minute=0, second=0, microsecond=0)
            month = report.next_run.month + 1
            year = report.next_run.year
            if month > 12:
                month = 1
                year += 1
            report.next_run = report.next_run.replace(year=year, month=month, day=1)
    
    await db.commit()
    await db.refresh(report)
    return report


@router.get("/by-type/{report_type}", response_model=List[ReportResponse])
async def get_reports_by_type(
    report_type: ReportType,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get reports by type.
    """
    result = await db.execute(select(Report).where(Report.report_type == report_type))
    reports = result.scalars().all()
    return reports


@router.get("/scheduled", response_model=List[ReportResponse])
async def get_scheduled_reports(
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get all scheduled reports.
    """
    result = await db.execute(select(Report).where(Report.is_scheduled == True))
    reports = result.scalars().all()
    return reports


@router.get("/due", response_model=List[ReportResponse])
async def get_due_reports(
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get all reports that are due to run (next_run <= current time).
    """
    now = datetime.now()
    result = await db.execute(
        select(Report).where(
            Report.is_scheduled == True,
            Report.next_run <= now
        )
    )
    reports = result.scalars().all()
    return reports


@router.get("/by-user/{user_id}", response_model=List[ReportResponse])
async def get_reports_by_user(
    user_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get all reports created by a specific user.
    """
    result = await db.execute(select(Report).where(Report.created_by == user_id))
    reports = result.scalars().all()
    return reports
