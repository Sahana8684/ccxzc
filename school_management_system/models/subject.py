from typing import List, Optional
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Text, Table
from sqlalchemy.orm import relationship

from school_management_system.database.base import Base


class Subject(Base):
    """
    Subject model for managing academic subjects.
    """
    __tablename__ = "subjects"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    code = Column(String, unique=True, index=True, nullable=False)
    description = Column(Text, nullable=True)
    grade_level = Column(String, nullable=False)
    credits = Column(Integer, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Foreign keys
    teacher_id = Column(Integer, ForeignKey("teacher_profiles.id"), nullable=True)
    
    # Relationships
    teacher = relationship("TeacherProfile", back_populates="subjects")
    students = relationship("Student", secondary="student_subject", back_populates="subjects")
    timetable_slots = relationship("TimetableSlot", back_populates="subject")
    attendance_records = relationship("Attendance", back_populates="subject")
    exam_results = relationship("ExamResult", back_populates="subject")
    syllabus_items = relationship("SyllabusItem", back_populates="subject")


class SyllabusItem(Base):
    """
    SyllabusItem model for managing subject syllabus.
    """
    __tablename__ = "syllabus_items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    order = Column(Integer, nullable=False)
    duration_in_hours = Column(Integer, nullable=True)
    learning_objectives = Column(Text, nullable=True)
    resources = Column(Text, nullable=True)
    
    # Foreign keys
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    parent_id = Column(Integer, ForeignKey("syllabus_items.id"), nullable=True)
    
    # Relationships
    subject = relationship("Subject", back_populates="syllabus_items")
    parent = relationship("SyllabusItem", remote_side=[id], backref="children")


class SubjectResource(Base):
    """
    SubjectResource model for managing resources associated with subjects.
    """
    __tablename__ = "subject_resources"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    resource_type = Column(String, nullable=False)  # Book, Website, Video, Document, etc.
    url = Column(String, nullable=True)
    file_path = Column(String, nullable=True)
    description = Column(Text, nullable=True)
    is_required = Column(Boolean, default=False)
    
    # Foreign keys
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    
    # Relationships
    subject = relationship("Subject")


class SubjectAssignment(Base):
    """
    SubjectAssignment model for managing assignments for subjects.
    """
    __tablename__ = "subject_assignments"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    due_date = Column(String, nullable=False)
    total_marks = Column(Integer, nullable=False)
    
    # Foreign keys
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    
    # Relationships
    subject = relationship("Subject")
    submissions = relationship("AssignmentSubmission", back_populates="assignment")


class AssignmentSubmission(Base):
    """
    AssignmentSubmission model for tracking student assignment submissions.
    """
    __tablename__ = "assignment_submissions"

    id = Column(Integer, primary_key=True, index=True)
    submission_date = Column(String, nullable=False)
    file_path = Column(String, nullable=True)
    comments = Column(Text, nullable=True)
    marks_obtained = Column(Integer, nullable=True)
    is_graded = Column(Boolean, default=False)
    
    # Foreign keys
    assignment_id = Column(Integer, ForeignKey("subject_assignments.id"), nullable=False)
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Relationships
    assignment = relationship("SubjectAssignment", back_populates="submissions")
    student = relationship("Student")
