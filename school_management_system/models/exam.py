from typing import List, Optional
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, DateTime, Enum, Text, Float, Table
from sqlalchemy.orm import relationship
import enum

from school_management_system.database.base import Base


class ExamType(enum.Enum):
    """
    Enum for exam types.
    """
    QUIZ = "quiz"
    TEST = "test"
    MIDTERM = "midterm"
    FINAL = "final"
    ASSIGNMENT = "assignment"
    PROJECT = "project"
    PRACTICAL = "practical"
    OTHER = "other"


class Exam(Base):
    """
    Exam model for managing exams.
    """
    __tablename__ = "exams"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    exam_type = Column(Enum(ExamType), nullable=False)
    date = Column(Date, nullable=False)
    start_time = Column(String, nullable=True)
    end_time = Column(String, nullable=True)
    total_marks = Column(Float, nullable=False)
    passing_marks = Column(Float, nullable=False)
    grade_level = Column(String, nullable=False)
    academic_year = Column(String, nullable=False)
    term = Column(String, nullable=False)
    instructions = Column(Text, nullable=True)
    
    # Relationships
    results = relationship("ExamResult", back_populates="exam")
    questions = relationship("ExamQuestion", back_populates="exam")


class ExamQuestion(Base):
    """
    ExamQuestion model for managing questions in an exam.
    """
    __tablename__ = "exam_questions"

    id = Column(Integer, primary_key=True, index=True)
    question_text = Column(Text, nullable=False)
    question_type = Column(String, nullable=False)  # MCQ, Short Answer, Long Answer, etc.
    marks = Column(Float, nullable=False)
    order = Column(Integer, nullable=False)
    
    # Foreign keys
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    
    # Relationships
    exam = relationship("Exam", back_populates="questions")
    options = relationship("QuestionOption", back_populates="question")


class QuestionOption(Base):
    """
    QuestionOption model for managing options for MCQ questions.
    """
    __tablename__ = "question_options"

    id = Column(Integer, primary_key=True, index=True)
    option_text = Column(Text, nullable=False)
    is_correct = Column(Boolean, default=False)
    order = Column(Integer, nullable=False)
    
    # Foreign keys
    question_id = Column(Integer, ForeignKey("exam_questions.id"), nullable=False)
    
    # Relationships
    question = relationship("ExamQuestion", back_populates="options")


class GradingScale(Base):
    """
    GradingScale model for managing grading scales.
    """
    __tablename__ = "grading_scales"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    academic_year = Column(String, nullable=False)
    
    # Relationships
    grades = relationship("Grade", back_populates="scale")


class Grade(Base):
    """
    Grade model for managing grades in a grading scale.
    """
    __tablename__ = "grades"

    id = Column(Integer, primary_key=True, index=True)
    letter = Column(String, nullable=False)
    min_percentage = Column(Float, nullable=False)
    max_percentage = Column(Float, nullable=False)
    description = Column(String, nullable=True)
    gpa_point = Column(Float, nullable=True)
    
    # Foreign keys
    scale_id = Column(Integer, ForeignKey("grading_scales.id"), nullable=False)
    
    # Relationships
    scale = relationship("GradingScale", back_populates="grades")


class ReportCard(Base):
    """
    ReportCard model for managing student report cards.
    """
    __tablename__ = "report_cards"

    id = Column(Integer, primary_key=True, index=True)
    academic_year = Column(String, nullable=False)
    term = Column(String, nullable=False)
    issue_date = Column(Date, nullable=False)
    comments = Column(Text, nullable=True)
    teacher_remarks = Column(Text, nullable=True)
    principal_remarks = Column(Text, nullable=True)
    attendance_percentage = Column(Float, nullable=True)
    
    # Foreign keys
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Relationships
    student = relationship("Student")
    subject_results = relationship("ReportCardSubject", back_populates="report_card")


class ReportCardSubject(Base):
    """
    ReportCardSubject model for managing subject results in a report card.
    """
    __tablename__ = "report_card_subjects"

    id = Column(Integer, primary_key=True, index=True)
    marks_obtained = Column(Float, nullable=False)
    total_marks = Column(Float, nullable=False)
    percentage = Column(Float, nullable=False)
    grade = Column(String, nullable=True)
    teacher_remarks = Column(String, nullable=True)
    
    # Foreign keys
    report_card_id = Column(Integer, ForeignKey("report_cards.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    
    # Relationships
    report_card = relationship("ReportCard", back_populates="subject_results")
    subject = relationship("Subject")


class ExamResult(Base):
    """
    ExamResult model for managing exam results.
    """
    __tablename__ = "exam_results"

    id = Column(Integer, primary_key=True, index=True)
    score = Column(Float, nullable=False)
    grade = Column(String, nullable=True)
    remarks = Column(Text, nullable=True)
    
    # Foreign keys
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    exam_id = Column(Integer, ForeignKey("exams.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    
    # Relationships
    exam = relationship("Exam", back_populates="results")
    student = relationship("Student")
    subject = relationship("Subject")
