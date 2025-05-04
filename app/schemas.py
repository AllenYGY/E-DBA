from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, validator

from app.models.user import UserRole, PermissionLevel


# Token相关模型
class Token(BaseModel):
    access_token: str
    token_type: str


class TokenPayload(BaseModel):
    sub: Optional[int] = None


# 通用消息响应
class Msg(BaseModel):
    msg: str


# 用户相关模型
class UserBase(BaseModel):
    email: EmailStr
    username: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[UserRole] = UserRole.DATA_USER
    permission_level: Optional[int] = PermissionLevel.PUBLIC_DATA.value


class UserCreate(UserBase):
    password: str

    @validator('password')
    def password_min_length(cls, v):
        if len(v) < 8:
            raise ValueError('密码长度必须至少为8个字符')
        return v


class UserUpdate(UserBase):
    password: Optional[str] = None
    organization_id: Optional[int] = None
    paper_download_quota: Optional[float] = None


class UserInDBBase(UserBase):
    id: int
    organization_id: Optional[int] = None
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class User(UserInDBBase):
    paper_download_quota: float


class UserInDB(UserInDBBase):
    hashed_password: str


# 组织相关模型
class OrganizationBase(BaseModel):
    name: str
    description: Optional[str] = None
    email_domain: Optional[str] = None


class OrganizationCreate(OrganizationBase):
    verification_document: Optional[str] = None


class OrganizationUpdate(OrganizationBase):
    is_verified: Optional[bool] = None
    is_active: Optional[bool] = None
    convener_id: Optional[int] = None


class OrganizationInDBBase(OrganizationBase):
    id: int
    convener_id: int
    is_verified: bool
    is_active: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class Organization(OrganizationInDBBase):
    pass


# 验证状态相关模型
class VerificationStatusBase(BaseModel):
    organization_id: int
    e_admin_approved: Optional[bool] = False
    senior_approved: Optional[bool] = False
    e_admin_comment: Optional[str] = None
    senior_comment: Optional[str] = None


class VerificationStatusCreate(VerificationStatusBase):
    pass


class VerificationStatusUpdate(BaseModel):
    e_admin_id: Optional[int] = None
    senior_e_admin_id: Optional[int] = None
    e_admin_approved: Optional[bool] = None
    senior_approved: Optional[bool] = None
    e_admin_comment: Optional[str] = None
    senior_comment: Optional[str] = None
    e_admin_reviewed_at: Optional[datetime] = None
    senior_reviewed_at: Optional[datetime] = None


class VerificationStatusInDBBase(VerificationStatusBase):
    id: int
    e_admin_id: Optional[int] = None
    senior_e_admin_id: Optional[int] = None
    submitted_at: datetime
    e_admin_reviewed_at: Optional[datetime] = None
    senior_reviewed_at: Optional[datetime] = None

    class Config:
        orm_mode = True


class VerificationStatus(VerificationStatusInDBBase):
    pass


# 帮助请求相关模型
class HelpRequestBase(BaseModel):
    title: str
    content: str


class HelpRequestCreate(HelpRequestBase):
    pass


class HelpRequestUpdate(BaseModel):
    is_resolved: Optional[bool] = None
    is_starred: Optional[bool] = None


class HelpRequestInDBBase(HelpRequestBase):
    id: int
    user_id: int
    is_resolved: bool
    is_starred: bool
    created_at: datetime
    updated_at: datetime

    class Config:
        orm_mode = True


class HelpRequest(HelpRequestInDBBase):
    pass


# 帮助响应相关模型
class HelpResponseBase(BaseModel):
    content: str


class HelpResponseCreate(HelpResponseBase):
    help_request_id: int


class HelpResponseInDBBase(HelpResponseBase):
    id: int
    help_request_id: int
    responder_id: int
    created_at: datetime

    class Config:
        orm_mode = True


class HelpResponse(HelpResponseInDBBase):
    pass