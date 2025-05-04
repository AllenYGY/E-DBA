from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class BankAccountInfo(BaseModel):
    account_name: str
    account_number: str
    bank: str
    password: str

class PaymentBase(BaseModel):
    amount: float
    currency: str = "RMB"
    organization_id: int
    service_id: Optional[int] = None
    status: str = "pending"
    payment_method: str

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    amount: Optional[float] = None
    currency: Optional[str] = None
    status: Optional[str] = None
    payment_method: Optional[str] = None

class PaymentInDBBase(PaymentBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Payment(PaymentInDBBase):
    pass 