from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class TAdminVerificationUpdate(BaseModel):
    approved: bool
    comment: Optional[str] = None

class VerificationStatusBase(BaseModel):
    organization_id: int
    e_admin_id: Optional[int] = None
    senior_e_admin_id: Optional[int] = None
    e_admin_approved: bool = False
    senior_approved: bool = False
    e_admin_comment: Optional[str] = None
    senior_comment: Optional[str] = None
    submitted_at: datetime
    e_admin_reviewed_at: Optional[datetime] = None
    senior_reviewed_at: Optional[datetime] = None

class VerificationStatus(VerificationStatusBase):
    id: int

    class Config:
        from_attributes = True

class VerificationStatusCreate(VerificationStatusBase):
    pass

class EAdminVerificationStatusUpdate(BaseModel):
    e_admin_approved: bool
    e_admin_comment: Optional[str] = None

    class Config:
        from_attributes = True

class SeniorEAdminVerificationStatusUpdate(BaseModel):
    senior_approved: bool
    senior_comment: Optional[str] = None

    class Config:
        from_attributes = True

class VerificationStatusInDBBase(VerificationStatusBase):
    id: int
    e_admin_id: Optional[int] = None
    senior_e_admin_id: Optional[int] = None
    submitted_at: datetime
    e_admin_reviewed_at: Optional[datetime] = None
    senior_reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True 