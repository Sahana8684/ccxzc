from typing import List, Optional
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, Enum, Text, DateTime
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from school_management_system.database.base import Base


class AdmissionStatus(enum.Enum):
    """
    Enum for admission status.
    """
    PENDING = "pending"
    REVIEWING = "reviewing"
    APPROVED = "approved"
    REJECTED = "rejected"
    WAITLISTED = "waitlisted"
    ENROLLED = "enrolled"
    WITHDRAWN = "withdrawn"


class Admission(Base):
    """
    Admission model for managing student admissions.
    """
    __tablename__ = "admissions"

    id = Column(Integer, primary_key=True, index=True)
    application_date = Column(Date, nullable=False, default=func.current_date())
    status = Column(Enum(AdmissionStatus), nullable=False, default=AdmissionStatus.PENDING)
    desired_grade_level = Column(String, nullable=False)
    previous_school = Column(String, nullable=True)
    previous_grade_level = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Applicant information
    first_name = Column(String, nullable=False)
    last_name = Column(String, nullable=False)
    date_of_birth = Column(Date, nullable=False)
    gender = Column(String, nullable=False)
    address = Column(String, nullable=False)
    phone_number = Column(String, nullable=False)
    email = Column(String, nullable=True)
    
    # Parent/Guardian information
    parent_name = Column(String, nullable=False)
    parent_phone = Column(String, nullable=False)
    parent_email = Column(String, nullable=True)
    parent_address = Column(String, nullable=True)
    relationship_to_applicant = Column(String, nullable=False)
    
    # Foreign keys
    student_id = Column(Integer, ForeignKey("students.id"), nullable=True)
    
    # Relationships
    student = relationship("Student", back_populates="admission")
    documents = relationship("AdmissionDocument", back_populates="admission")
    interviews = relationship("AdmissionInterview", back_populates="admission")
    communications = relationship("AdmissionCommunication", back_populates="admission")


class AdmissionDocument(Base):
    """
    AdmissionDocument model for tracking documents submitted during admission.
    """
    __tablename__ = "admission_documents"

    id = Column(Integer, primary_key=True, index=True)
    document_type = Column(String, nullable=False)  # Birth Certificate, Previous School Records, etc.
    document_path = Column(String, nullable=False)  # Path to the stored document
    upload_date = Column(Date, nullable=False, default=func.current_date())
    is_verified = Column(Boolean, default=False)
    verification_date = Column(Date, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Foreign keys
    admission_id = Column(Integer, ForeignKey("admissions.id"), nullable=False)
    
    # Relationships
    admission = relationship("Admission", back_populates="documents")


class AdmissionInterview(Base):
    """
    AdmissionInterview model for tracking interviews conducted during admission.
    """
    __tablename__ = "admission_interviews"

    id = Column(Integer, primary_key=True, index=True)
    interview_date = Column(DateTime, nullable=False)
    interviewer_name = Column(String, nullable=False)
    interview_type = Column(String, nullable=False)  # Academic, Behavioral, Parent, etc.
    notes = Column(Text, nullable=True)
    outcome = Column(String, nullable=True)
    
    # Foreign keys
    admission_id = Column(Integer, ForeignKey("admissions.id"), nullable=False)
    
    # Relationships
    admission = relationship("Admission", back_populates="interviews")


class AdmissionCommunication(Base):
    """
    AdmissionCommunication model for tracking communications during admission.
    """
    __tablename__ = "admission_communications"

    id = Column(Integer, primary_key=True, index=True)
    date = Column(DateTime, nullable=False, default=func.now())
    communication_type = Column(String, nullable=False)  # Email, Phone, In-person, etc.
    subject = Column(String, nullable=False)
    content = Column(Text, nullable=False)
    sender = Column(String, nullable=False)
    recipient = Column(String, nullable=False)
    
    # Foreign keys
    admission_id = Column(Integer, ForeignKey("admissions.id"), nullable=False)
    
    # Relationships
    admission = relationship("Admission", back_populates="communications")
