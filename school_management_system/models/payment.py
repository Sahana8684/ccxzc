from typing import List, Optional
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Date, DateTime, Enum, Text, Float, Table
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
import enum

from school_management_system.database.base import Base


class PaymentStatus(enum.Enum):
    """
    Enum for payment status.
    """
    PENDING = "pending"
    PAID = "paid"
    PARTIALLY_PAID = "partially_paid"
    OVERDUE = "overdue"
    CANCELLED = "cancelled"
    REFUNDED = "refunded"


class PaymentMethod(enum.Enum):
    """
    Enum for payment methods.
    """
    CASH = "cash"
    CREDIT_CARD = "credit_card"
    DEBIT_CARD = "debit_card"
    BANK_TRANSFER = "bank_transfer"
    CHECK = "check"
    ONLINE_PAYMENT = "online_payment"
    OTHER = "other"


class FeeType(enum.Enum):
    """
    Enum for fee types.
    """
    TUITION = "tuition"
    ADMISSION = "admission"
    EXAMINATION = "examination"
    TRANSPORTATION = "transportation"
    LIBRARY = "library"
    LABORATORY = "laboratory"
    SPORTS = "sports"
    TECHNOLOGY = "technology"
    UNIFORM = "uniform"
    BOOKS = "books"
    LATE_FEE = "late_fee"
    OTHER = "other"


class FeeStructure(Base):
    """
    FeeStructure model for managing fee structures.
    """
    __tablename__ = "fee_structures"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    academic_year = Column(String, nullable=False)
    grade_level = Column(String, nullable=False)
    is_active = Column(Boolean, default=True)
    
    # Relationships
    fee_items = relationship("FeeItem", back_populates="fee_structure")


class FeeItem(Base):
    """
    FeeItem model for managing individual fee items in a fee structure.
    """
    __tablename__ = "fee_items"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    fee_type = Column(Enum(FeeType), nullable=False)
    amount = Column(Float, nullable=False)
    due_date = Column(Date, nullable=True)
    is_mandatory = Column(Boolean, default=True)
    
    # Foreign keys
    fee_structure_id = Column(Integer, ForeignKey("fee_structures.id"), nullable=False)
    
    # Relationships
    fee_structure = relationship("FeeStructure", back_populates="fee_items")


class FeeRecord(Base):
    """
    FeeRecord model for managing student fee records.
    """
    __tablename__ = "fee_records"

    id = Column(Integer, primary_key=True, index=True)
    academic_year = Column(String, nullable=False)
    term = Column(String, nullable=False)
    total_amount = Column(Float, nullable=False)
    paid_amount = Column(Float, default=0.0)
    balance = Column(Float, nullable=False)
    status = Column(Enum(PaymentStatus), nullable=False, default=PaymentStatus.PENDING)
    due_date = Column(Date, nullable=False)
    
    # Foreign keys
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    fee_structure_id = Column(Integer, ForeignKey("fee_structures.id"), nullable=False)
    
    # Relationships
    student = relationship("Student", back_populates="fee_records")
    fee_structure = relationship("FeeStructure")
    payments = relationship("Payment", back_populates="fee_record")


class Payment(Base):
    """
    Payment model for managing payments.
    """
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    payment_date = Column(DateTime, nullable=False, default=func.now())
    payment_method = Column(Enum(PaymentMethod), nullable=False)
    transaction_id = Column(String, nullable=True)
    receipt_number = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    
    # Foreign keys
    fee_record_id = Column(Integer, ForeignKey("fee_records.id"), nullable=False)
    
    # Relationships
    fee_record = relationship("FeeRecord", back_populates="payments")


class Discount(Base):
    """
    Discount model for managing fee discounts.
    """
    __tablename__ = "discounts"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    discount_type = Column(String, nullable=False)  # Percentage, Fixed Amount
    discount_value = Column(Float, nullable=False)
    start_date = Column(Date, nullable=True)
    end_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Foreign keys
    fee_structure_id = Column(Integer, ForeignKey("fee_structures.id"), nullable=True)
    
    # Relationships
    fee_structure = relationship("FeeStructure")


class FinancialAid(Base):
    """
    FinancialAid model for managing financial aid for students.
    """
    __tablename__ = "financial_aid"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    description = Column(Text, nullable=True)
    aid_type = Column(String, nullable=False)  # Scholarship, Grant, Loan
    amount = Column(Float, nullable=False)
    start_date = Column(Date, nullable=False)
    end_date = Column(Date, nullable=True)
    is_active = Column(Boolean, default=True)
    
    # Foreign keys
    student_id = Column(Integer, ForeignKey("students.id"), nullable=False)
    
    # Relationships
    student = relationship("Student")
