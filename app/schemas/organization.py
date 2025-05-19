from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

# 共享属性
class OrganizationBase(BaseModel):
    name: str = Field(..., description="Organization name")
    full_name: Optional[str] = Field(None, description="Organization full name")
    email_domain: Optional[str] = None
    verification_document: Optional[str] = None
    is_verified: bool = Field(False, description="Organization is verified")
    is_active: bool = Field(True, description="Organization is active")
    convener_id: Optional[int] = None

# 创建组织时的属性
class OrganizationCreate(OrganizationBase):
    email_domain: str = Field(..., description="Organization email domain")
    verification_document: Optional[bytes] = None
    is_verified: bool = Field(False, description="Organization is verified")
    is_active: bool = Field(True, description="Organization is active")

# 更新组织时的属性
class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, description="Organization name")
    full_name: Optional[str] = Field(None, description="Organization full name")
    is_verified: Optional[bool] = Field(None, description="Organization is verified")
    is_active: Optional[bool] = Field(None, description="Organization is active")

# 数据库存储的基础属性
class OrganizationInDBBase(OrganizationBase):
    id: int = Field(..., description="Organization ID")
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    created_at: datetime = Field(..., description="Created time")
    updated_at: datetime = Field(..., description="Updated time")

    class Config:
        from_attributes = True

# API 响应模型
class Organization(OrganizationInDBBase):
    pass

# 验证状态模型
class VerificationStatusBase(BaseModel):
    organization_id: int
    e_admin_id: Optional[int] = None
    senior_e_admin_id: Optional[int] = None
    e_admin_approved: Optional[bool] = False
    senior_approved: Optional[bool] = False
    e_admin_comment: Optional[str] = None
    senior_comment: Optional[str] = None

class OrganizationListResponse(BaseModel):
    items: List[Organization]
    total: int

class VerificationStatusCreate(VerificationStatusBase):
    pass

class VerificationStatusUpdate(VerificationStatusBase):
    pass

class VerificationStatusInDBBase(VerificationStatusBase):
    id: int
    submitted_at: datetime
    e_admin_reviewed_at: Optional[datetime] = None
    senior_reviewed_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class VerificationStatus(VerificationStatusInDBBase):
    pass

class OrganizationInDB(OrganizationInDBBase):
    pass 