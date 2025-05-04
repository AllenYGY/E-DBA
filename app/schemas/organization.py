from typing import Optional, List
from datetime import datetime
from pydantic import BaseModel, Field

# 共享属性
class OrganizationBase(BaseModel):
    name: str = Field(..., description="组织名称")
    description: Optional[str] = Field(None, description="组织描述")
    email_domain: Optional[str] = None
    verification_document: Optional[str] = None
    is_verified: bool = Field(False, description="组织是否已验证")
    is_active: bool = Field(True, description="组织是否激活")
    convener_id: Optional[int] = None

# 创建组织时的属性
class OrganizationCreate(OrganizationBase):
    email_domain: str = Field(..., description="组织邮箱域名")
    verification_document: str = Field(..., description="组织验证文档的Base64编码字符串")
    is_verified: bool = Field(False, description="组织是否已验证")
    is_active: bool = Field(True, description="组织是否激活")

# 更新组织时的属性
class OrganizationUpdate(BaseModel):
    name: Optional[str] = Field(None, description="组织名称")
    description: Optional[str] = Field(None, description="组织描述")
    is_verified: Optional[bool] = Field(None, description="组织是否已验证")
    is_active: Optional[bool] = Field(None, description="组织是否激活")

# 数据库存储的基础属性
class OrganizationInDBBase(OrganizationBase):
    id: int = Field(..., description="组织ID")
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

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