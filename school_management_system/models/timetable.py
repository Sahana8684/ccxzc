from typing import List, Optional
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Time, Enum, Text, Table
from sqlalchemy.orm import relationship
import enum

from school_management_system.database.base import Base


class DayOfWeek(enum.Enum):
    """
    Enum for days of the week.
    """
    MONDAY = "monday"
    TUESDAY = "tuesday"
    WEDNESDAY = "wednesday"
    THURSDAY = "thursday"
    FRIDAY = "friday"
    SATURDAY = "saturday"
    SUNDAY = "sunday"


class Timetable(Base):
    """
    Timetable model for managing school timetables.
    """
    __tablename__ = "timetables"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    academic_year = Column(String, nullable=False)
    term = Column(String, nullable=False)
    grade_level = Column(String, nullable=False)
    section = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    slots = relationship("TimetableSlot", back_populates="timetable")


class TimetableSlot(Base):
    """
    TimetableSlot model for managing individual slots in a timetable.
    """
    __tablename__ = "timetable_slots"

    id = Column(Integer, primary_key=True, index=True)
    day = Column(Enum(DayOfWeek), nullable=False)
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    room_number = Column(String, nullable=True)
    
    # Foreign keys
    timetable_id = Column(Integer, ForeignKey("timetables.id"), nullable=False)
    subject_id = Column(Integer, ForeignKey("subjects.id"), nullable=False)
    teacher_id = Column(Integer, ForeignKey("teacher_profiles.id"), nullable=True)
    
    # Relationships
    timetable = relationship("Timetable", back_populates="slots")
    subject = relationship("Subject", back_populates="timetable_slots")
    teacher = relationship("TeacherProfile")


class ClassRoom(Base):
    """
    ClassRoom model for managing physical classrooms.
    """
    __tablename__ = "classrooms"

    id = Column(Integer, primary_key=True, index=True)
    room_number = Column(String, unique=True, index=True, nullable=False)
    name = Column(String, nullable=True)
    capacity = Column(Integer, nullable=False)
    building = Column(String, nullable=True)
    floor = Column(Integer, nullable=True)
    has_projector = Column(Boolean, default=False)
    has_whiteboard = Column(Boolean, default=True)
    has_computers = Column(Boolean, default=False)
    notes = Column(Text, nullable=True)


class AcademicCalendar(Base):
    """
    AcademicCalendar model for managing school calendar events.
    """
    __tablename__ = "academic_calendar"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    event_type = Column(String, nullable=False)  # Holiday, Exam, Activity, etc.
    is_holiday = Column(Boolean, default=False)
    academic_year = Column(String, nullable=False)
    term = Column(String, nullable=True)
    applies_to_grades = Column(String, nullable=True)  # Comma-separated list of grades
    notes = Column(Text, nullable=True)


class SchoolTerm(Base):
    """
    SchoolTerm model for managing academic terms.
    """
    __tablename__ = "school_terms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    academic_year = Column(String, nullable=False)
    start_date = Column(String, nullable=False)
    end_date = Column(String, nullable=False)
    is_current = Column(Boolean, default=False)
    description = Column(Text, nullable=True)
