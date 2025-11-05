from typing import List, Optional
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, Table, Text, Float
from sqlalchemy.orm import relationship

from school_management_system.database.base import Base

# Association table for many-to-many relationship between students and subjects
student_subject = Table(
    "student_subject",
    Base.metadata,
    Column("student_id", Integer, ForeignKey("students.id"), primary_key=True),
    Column("subject_id", Integer, ForeignKey("subjects.id"), primary_key=True),
)


class Student(Base):
    """
    Student model for managing student information.
    """
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, index=True)
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    enrollment_date = Column(Date, nullable=False)
    grade_level = Column(String, nullable=False)
    student_id = Column(String, unique=True, index=True, nullable=False)
    address = Column(String, nullable=True)
    phone_number = Column(String, nullable=True)
    email = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Foreign keys
    parent_id = Column(Integer, ForeignKey("parent_profiles.id"), nullable=True)
    
    # Relationships
    parent = relationship("ParentProfile", back_populates="students")
    subjects = relationship("Subject", secondary=student_subject, back_populates="students")
    attendance_records = relationship("Attendance", back_populates="student")
    exam_results = relationship("ExamResult", back_populates="student")
    fee_records = relationship("FeeRecord", back_populates="student")
    admission = relationship("Admission", back_populates="student", uselist=False)


class Attendance(Base):
    """
    Attendance model for tracking student attendance.
    """
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    status = Column(String, nullable=False)  # Present, Absent, Late, Excused
    remarks = Column(String, nullable=True)
    
    # Foreign keys
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=True)
    
    # Relationships
    student = relationship("Student", back_populates="attendance_records")
    subject = relationship("Subject", back_populates="attendance_records")


# ExamResult is now defined in exam.py


class StudentProgress(Base):
    """
    StudentProgress model for tracking student progress over time.
    """
    __tablename__ = "student_progress"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(Date, nullable=False)
    category = Column(String, nullable=False)  # Academic, Behavioral, Social, etc.
    notes = Column(Text, nullable=False)
    action_items = Column(Text, nullable=True)
    
    # Foreign keys
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teacher_profiles.id"), nullable=False)
    
    # Relationships
    student = relationship("Student")
    teacher = relationship("TeacherProfile")
