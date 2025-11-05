from typing import Any, List, Optional
from datetime import date, datetime

from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from pydantic import BaseModel

from school_management_system.database.session import get_db
from school_management_system.models.payment import (
    FeeStructure, FeeItem, FeeRecord, Payment, PaymentStatus, PaymentMethod, FeeType
)

router = APIRouter()


# Pydantic schemas for FeeStructure
class FeeStructureBase(BaseModel):
    name: str
    description: Optional[str] = None
    academic_year: str
    grade_level: str
    is_active: bool = True


class FeeStructureCreate(FeeStructureBase):
    pass


class FeeStructureUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    academic_year: Optional[str] = None
    grade_level: Optional[str] = None
    is_active: Optional[bool] = None


class FeeStructureInDBBase(FeeStructureBase):
    id: int

    class Config:
        orm_mode = True


class FeeStructureResponse(FeeStructureInDBBase):
    pass


# Pydantic schemas for FeeItem
class FeeItemBase(BaseModel):
    name: str
    description: Optional[str] = None
    fee_type: FeeType
    amount: float
    due_date: Optional[date] = None
    is_mandatory: bool = True
    fee_structure_id: int


class FeeItemCreate(FeeItemBase):
    pass


class FeeItemUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    fee_type: Optional[FeeType] = None
    amount: Optional[float] = None
    due_date: Optional[date] = None
    is_mandatory: Optional[bool] = None


class FeeItemInDBBase(FeeItemBase):
    id: int

    class Config:
        orm_mode = True


class FeeItemResponse(FeeItemInDBBase):
    pass


# Pydantic schemas for FeeRecord
class FeeRecordBase(BaseModel):
    academic_year: str
    term: str
    total_amount: float
    paid_amount: float = 0.0
    balance: float
    status: PaymentStatus = PaymentStatus.PENDING
    due_date: date
    student_id: int
    fee_structure_id: int


class FeeRecordCreate(FeeRecordBase):
    pass


class FeeRecordUpdate(BaseModel):
    academic_year: Optional[str] = None
    term: Optional[str] = None
    total_amount: Optional[float] = None
    paid_amount: Optional[float] = None
    balance: Optional[float] = None
    status: Optional[PaymentStatus] = None
    due_date: Optional[date] = None


class FeeRecordInDBBase(FeeRecordBase):
    id: int

    class Config:
        orm_mode = True


class FeeRecordResponse(FeeRecordInDBBase):
    pass


# Pydantic schemas for Payment
class PaymentBase(BaseModel):
    amount: float
    payment_date: datetime = datetime.now()
    payment_method: PaymentMethod
    transaction_id: Optional[str] = None
    receipt_number: Optional[str] = None
    notes: Optional[str] = None
    fee_record_id: int


class PaymentCreate(PaymentBase):
    pass


class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    payment_date: Optional[datetime] = None
    payment_method: Optional[PaymentMethod] = None
    transaction_id: Optional[str] = None
    receipt_number: Optional[str] = None
    notes: Optional[str] = None


class PaymentInDBBase(PaymentBase):
    id: int

    class Config:
        orm_mode = True


class PaymentResponse(PaymentInDBBase):
    pass


# FeeStructure endpoints
@router.post("/fee-structures/", response_model=FeeStructureResponse)
async def create_fee_structure(
    fee_structure_in: FeeStructureCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create a new fee structure.
    """
    fee_structure = FeeStructure(**fee_structure_in.dict())
    db.add(fee_structure)
    await db.commit()
    await db.refresh(fee_structure)
    return fee_structure


@router.get("/fee-structures/{fee_structure_id}", response_model=FeeStructureResponse)
async def get_fee_structure(
    fee_structure_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a fee structure by ID.
    """
    result = await db.execute(select(FeeStructure).where(FeeStructure.id == fee_structure_id))
    fee_structure = result.scalars().first()
    if not fee_structure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fee structure not found",
        )
    return fee_structure


@router.get("/fee-structures/", response_model=List[FeeStructureResponse])
async def get_fee_structures(
    skip: int = 0,
    limit: int = 100,
    academic_year: Optional[str] = None,
    grade_level: Optional[str] = None,
    is_active: bool = True,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get all fee structures with optional filters.
    """
    query = select(FeeStructure)
    
    if academic_year:
        query = query.where(FeeStructure.academic_year == academic_year)
    
    if grade_level:
        query = query.where(FeeStructure.grade_level == grade_level)
    
    query = query.where(FeeStructure.is_active == is_active)
    query = query.offset(skip).limit(limit)
    
    result = await db.execute(query)
    fee_structures = result.scalars().all()
    return fee_structures


@router.put("/fee-structures/{fee_structure_id}", response_model=FeeStructureResponse)
async def update_fee_structure(
    fee_structure_id: int,
    fee_structure_in: FeeStructureUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update a fee structure.
    """
    result = await db.execute(select(FeeStructure).where(FeeStructure.id == fee_structure_id))
    fee_structure = result.scalars().first()
    if not fee_structure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fee structure not found",
        )
    
    # Update fee structure fields
    update_data = fee_structure_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(fee_structure, field, value)
    
    await db.commit()
    await db.refresh(fee_structure)
    return fee_structure


@router.delete("/fee-structures/{fee_structure_id}", response_model=FeeStructureResponse)
async def delete_fee_structure(
    fee_structure_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Delete a fee structure.
    """
    result = await db.execute(select(FeeStructure).where(FeeStructure.id == fee_structure_id))
    fee_structure = result.scalars().first()
    if not fee_structure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fee structure not found",
        )
    
    await db.delete(fee_structure)
    await db.commit()
    return fee_structure


# FeeItem endpoints
@router.post("/fee-items/", response_model=FeeItemResponse)
async def create_fee_item(
    fee_item_in: FeeItemCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create a new fee item.
    """
    # Check if fee structure exists
    result = await db.execute(select(FeeStructure).where(FeeStructure.id == fee_item_in.fee_structure_id))
    fee_structure = result.scalars().first()
    if not fee_structure:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fee structure not found",
        )
    
    fee_item = FeeItem(**fee_item_in.dict())
    db.add(fee_item)
    await db.commit()
    await db.refresh(fee_item)
    return fee_item


@router.get("/fee-items/{fee_item_id}", response_model=FeeItemResponse)
async def get_fee_item(
    fee_item_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a fee item by ID.
    """
    result = await db.execute(select(FeeItem).where(FeeItem.id == fee_item_id))
    fee_item = result.scalars().first()
    if not fee_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fee item not found",
        )
    return fee_item


@router.get("/fee-items/by-structure/{fee_structure_id}", response_model=List[FeeItemResponse])
async def get_fee_items_by_structure(
    fee_structure_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get all fee items for a specific fee structure.
    """
    result = await db.execute(select(FeeItem).where(FeeItem.fee_structure_id == fee_structure_id))
    fee_items = result.scalars().all()
    return fee_items


@router.put("/fee-items/{fee_item_id}", response_model=FeeItemResponse)
async def update_fee_item(
    fee_item_id: int,
    fee_item_in: FeeItemUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update a fee item.
    """
    result = await db.execute(select(FeeItem).where(FeeItem.id == fee_item_id))
    fee_item = result.scalars().first()
    if not fee_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fee item not found",
        )
    
    # Update fee item fields
    update_data = fee_item_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(fee_item, field, value)
    
    await db.commit()
    await db.refresh(fee_item)
    return fee_item


@router.delete("/fee-items/{fee_item_id}", response_model=FeeItemResponse)
async def delete_fee_item(
    fee_item_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Delete a fee item.
    """
    result = await db.execute(select(FeeItem).where(FeeItem.id == fee_item_id))
    fee_item = result.scalars().first()
    if not fee_item:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fee item not found",
        )
    
    await db.delete(fee_item)
    await db.commit()
    return fee_item


# FeeRecord endpoints
@router.post("/fee-records/", response_model=FeeRecordResponse)
async def create_fee_record(
    fee_record_in: FeeRecordCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create a new fee record.
    """
    fee_record = FeeRecord(**fee_record_in.dict())
    db.add(fee_record)
    await db.commit()
    await db.refresh(fee_record)
    return fee_record


@router.get("/fee-records/{fee_record_id}", response_model=FeeRecordResponse)
async def get_fee_record(
    fee_record_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a fee record by ID.
    """
    result = await db.execute(select(FeeRecord).where(FeeRecord.id == fee_record_id))
    fee_record = result.scalars().first()
    if not fee_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fee record not found",
        )
    return fee_record


@router.get("/fee-records/by-student/{student_id}", response_model=List[FeeRecordResponse])
async def get_fee_records_by_student(
    student_id: int,
    status: Optional[PaymentStatus] = None,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get all fee records for a specific student with optional status filter.
    """
    query = select(FeeRecord).where(FeeRecord.student_id == student_id)
    
    if status:
        query = query.where(FeeRecord.status == status)
    
    result = await db.execute(query)
    fee_records = result.scalars().all()
    return fee_records


@router.put("/fee-records/{fee_record_id}", response_model=FeeRecordResponse)
async def update_fee_record(
    fee_record_id: int,
    fee_record_in: FeeRecordUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update a fee record.
    """
    result = await db.execute(select(FeeRecord).where(FeeRecord.id == fee_record_id))
    fee_record = result.scalars().first()
    if not fee_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fee record not found",
        )
    
    # Update fee record fields
    update_data = fee_record_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(fee_record, field, value)
    
    await db.commit()
    await db.refresh(fee_record)
    return fee_record


@router.delete("/fee-records/{fee_record_id}", response_model=FeeRecordResponse)
async def delete_fee_record(
    fee_record_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Delete a fee record.
    """
    result = await db.execute(select(FeeRecord).where(FeeRecord.id == fee_record_id))
    fee_record = result.scalars().first()
    if not fee_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fee record not found",
        )
    
    await db.delete(fee_record)
    await db.commit()
    return fee_record


# Payment endpoints
@router.post("/payments/", response_model=PaymentResponse)
async def create_payment(
    payment_in: PaymentCreate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Create a new payment.
    """
    # Check if fee record exists
    result = await db.execute(select(FeeRecord).where(FeeRecord.id == payment_in.fee_record_id))
    fee_record = result.scalars().first()
    if not fee_record:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Fee record not found",
        )
    
    # Create payment
    payment = Payment(**payment_in.dict())
    db.add(payment)
    
    # Update fee record
    fee_record.paid_amount += payment_in.amount
    fee_record.balance = fee_record.total_amount - fee_record.paid_amount
    
    # Update status based on payment
    if fee_record.balance <= 0:
        fee_record.status = PaymentStatus.PAID
    elif fee_record.paid_amount > 0:
        fee_record.status = PaymentStatus.PARTIALLY_PAID
    
    await db.commit()
    await db.refresh(payment)
    return payment


@router.get("/payments/{payment_id}", response_model=PaymentResponse)
async def get_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get a payment by ID.
    """
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalars().first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )
    return payment


@router.get("/payments/by-fee-record/{fee_record_id}", response_model=List[PaymentResponse])
async def get_payments_by_fee_record(
    fee_record_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Get all payments for a specific fee record.
    """
    result = await db.execute(select(Payment).where(Payment.fee_record_id == fee_record_id))
    payments = result.scalars().all()
    return payments


@router.put("/payments/{payment_id}", response_model=PaymentResponse)
async def update_payment(
    payment_id: int,
    payment_in: PaymentUpdate,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Update a payment.
    """
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalars().first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )
    
    # Get original amount
    original_amount = payment.amount
    
    # Update payment fields
    update_data = payment_in.dict(exclude_unset=True)
    for field, value in update_data.items():
        setattr(payment, field, value)
    
    # If amount was updated, update fee record
    if "amount" in update_data and update_data["amount"] != original_amount:
        # Get fee record
        result = await db.execute(select(FeeRecord).where(FeeRecord.id == payment.fee_record_id))
        fee_record = result.scalars().first()
        
        if fee_record:
            # Update fee record
            fee_record.paid_amount = fee_record.paid_amount - original_amount + payment.amount
            fee_record.balance = fee_record.total_amount - fee_record.paid_amount
            
            # Update status based on payment
            if fee_record.balance <= 0:
                fee_record.status = PaymentStatus.PAID
            elif fee_record.paid_amount > 0:
                fee_record.status = PaymentStatus.PARTIALLY_PAID
            else:
                fee_record.status = PaymentStatus.PENDING
    
    await db.commit()
    await db.refresh(payment)
    return payment


@router.delete("/payments/{payment_id}", response_model=PaymentResponse)
async def delete_payment(
    payment_id: int,
    db: AsyncSession = Depends(get_db),
) -> Any:
    """
    Delete a payment.
    """
    result = await db.execute(select(Payment).where(Payment.id == payment_id))
    payment = result.scalars().first()
    if not payment:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Payment not found",
        )
    
    # Get fee record to update
    result = await db.execute(select(FeeRecord).where(FeeRecord.id == payment.fee_record_id))
    fee_record = result.scalars().first()
    
    if fee_record:
        # Update fee record
        fee_record.paid_amount -= payment.amount
        fee_record.balance = fee_record.total_amount - fee_record.paid_amount
        
        # Update status based on payment
        if fee_record.paid_amount <= 0:
            fee_record.status = PaymentStatus.PENDING
        else:
            fee_record.status = PaymentStatus.PARTIALLY_PAID
    
    await db.delete(payment)
    await db.commit()
    return payment
