from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel
from app.schemas.organization import Organization
from enum import Enum

class VerificationStatusEnum(str, Enum):
    PENDING = 'PENDING'
    APPROVAL = 'APPROVAL'
    REJECTION = 'REJECTION'

class TAdminVerificationUpdate(BaseModel):
    approved: VerificationStatusEnum
    comment: Optional[str] = None

class VerificationStatusBase(BaseModel):
    organization_id: int
    e_admin_id: Optional[int] = None
    senior_e_admin_id: Optional[int] = None
    e_admin_approved: VerificationStatusEnum
    senior_approved: VerificationStatusEnum = VerificationStatusEnum.PENDING
    e_admin_comment: Optional[str] = None
    senior_comment: Optional[str] = None
    submitted_at: datetime
    e_admin_reviewed_at: Optional[datetime] = None
    senior_reviewed_at: Optional[datetime] = None

class VerificationStatus(VerificationStatusBase):
    id: int
    organization: Optional[Organization] = None

    class Config:
        from_attributes = True

class VerificationStatusCreate(VerificationStatusBase):
    pass

class EAdminVerificationStatusUpdate(BaseModel):
    e_admin_approved: VerificationStatusEnum
    e_admin_comment: Optional[str] = None

    class Config:
        from_attributes = True

class SeniorEAdminVerificationStatusUpdate(BaseModel):
    senior_approved: VerificationStatusEnum
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

class VerificationStatusListResponse(BaseModel):
    items: List[VerificationStatus]
    total: int 