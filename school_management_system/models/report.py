from typing import List, Optional
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, DateTime, Enum, Text, Float, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from school_management_system.database.base import Base


class ReportType(enum.Enum):
    """
    Enum for report types.
    """
    ATTENDANCE = "attendance"
    ACADEMIC = "academic"
    FINANCIAL = "financial"
    BEHAVIORAL = "behavioral"
    ADMINISTRATIVE = "administrative"
    CUSTOM = "custom"


class Report(Base):
    """
    Report model for managing system reports.
    """
    __tablename__ = "reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    report_type = Column(Enum(ReportType), nullable=False)
    created_at = Column(DateTime, nullable=False, default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    parameters = Column(Text, nullable=True)  # JSON string of parameters
    file_path = Column(String, nullable=True)
    is_scheduled = Column(Boolean, default=False)
    schedule_frequency = Column(String, nullable=True)  # Daily, Weekly, Monthly, etc.
    last_run = Column(DateTime, nullable=True)
    next_run = Column(DateTime, nullable=True)
    
    # Relationships
    creator = relationship("User")


class AttendanceReport(Base):
    """
    AttendanceReport model for managing attendance reports.
    """
    __tablename__ = "attendance_reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    grade_level = Column(String, nullable=True)
    section = Column(String, nullable=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String, nullable=True)
    
    # Relationships
    creator = relationship("User")
    subject = relationship("Subject")


class AcademicReport(Base):
    """
    AcademicReport model for managing academic reports.
    """
    __tablename__ = "academic_reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    academic_year = Column(String, nullable=False)
    term = Column(String, nullable=True)
    grade_level = Column(String, nullable=True)
    section = Column(String, nullable=True)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String, nullable=True)
    
    # Relationships
    creator = relationship("User")
    subject = relationship("Subject")
    exam = relationship("Exam")


class FinancialReport(Base):
    """
    FinancialReport model for managing financial reports.
    """
    __tablename__ = "financial_reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=False)
    report_category = Column(String, nullable=False)  # Income, Expense, Outstanding, etc.
    grade_level = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String, nullable=True)
    
    # Relationships
    creator = relationship("User")


class StudentProgressReport(Base):
    """
    StudentProgressReport model for managing student progress reports.
    """
    __tablename__ = "student_progress_reports"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    academic_year = Column(String, nullable=False)
    term = Column(String, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    created_by = Column(Integer, ForeignKey("users.id"), nullable=False)
    file_path = Column(String, nullable=True)
    
    # Foreign keys
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Relationships
    creator = relationship("User")
    student = relationship("Student")


class NotificationTemplate(Base):
    """
    NotificationTemplate model for managing notification templates.
    """
    __tablename__ = "notification_templates"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    notification_type = Column(String, nullable=False)  # Email, SMS, In-app, etc.
    is_active = Column(Boolean, default=True)
    
    # Relationships
    notifications = relationship("Notification", back_populates="template")


class Notification(Base):
    """
    Notification model for managing notifications.
    """
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    subject = Column(String, nullable=False)
    body = Column(Text, nullable=False)
    notification_type = Column(String, nullable=False)  # Email, SMS, In-app, etc.
    status = Column(String, nullable=False)  # Pending, Sent, Failed, etc.
    sent_at = Column(DateTime, nullable=True)
    created_at = Column(DateTime, nullable=False, default=func.now())
    
    # Foreign keys
    template_id = Column(Integer, ForeignKey("notification_templates.id"), nullable=True)
    recipient_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # Relationships
    template = relationship("NotificationTemplate", back_populates="notifications")
    recipient = relationship("User")
