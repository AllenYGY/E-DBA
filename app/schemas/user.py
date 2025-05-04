from typing import Optional
from datetime import datetime
from pydantic import BaseModel, EmailStr, Field

from app.models.enums import UserRole, PermissionLevel

# Login request schema
class LoginRequest(BaseModel):
    """登录请求模型"""
    email: EmailStr = Field(..., description="用户邮箱")
    password: str = Field(..., description="用户密码")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "yourpassword"
            }
        }

# 银行账户信息模型
class BankAccountInfo(BaseModel):
    bank: str = Field(..., description="银行名称")
    account_name: str = Field(..., description="银行账户名称")
    account_number: str = Field(..., description="银行账户号码")
    password: str = Field(..., description="银行账户密码")

# O-Convener registration request
class OConvenerRegisterRequest(BaseModel):
    """组织协调人注册请求模型"""
    # 用户信息
    email: EmailStr = Field(..., description="用户邮箱")
    password: str = Field(..., description="用户密码")
    username: Optional[str] = Field(None, description="用户名，可选")
    permission_level: int = 3
    
    # 组织信息
    name: str = Field(..., description="组织名称")
    description: Optional[str] = Field(None, description="组织描述")
    email_domain: str = Field(..., description="组织邮箱域名")
    verification_document: str = Field(..., description="组织验证文档的Base64编码字符串")
    
    # 银行账户信息
    bank_account: BankAccountInfo = Field(..., description="银行账户信息")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "organizer@example.com",
                "password": "strongpassword123",
                "username": "org_admin",
                "permission_level": 1,
                "name": "Example Organization",
                "description": "This is an example organization",
                "email_domain": "example.com",
                "verification_document": "dummy_base64_string_for_test",
                "bank_account": {
                    "bank": "中国银行",
                    "account_name": "张三",
                    "account_number": "6222021234567890123",
                    "password": "bankpassword123"
                }
            }
        }

# Shared properties
class UserBase(BaseModel):
    """用户基础信息，所有字段都是可选的"""
    email: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[UserRole] = None
    permission_level: Optional[int] = None
    organization_id: Optional[int] = None
    balance: Optional[float] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    """用户创建模型，只包含创建用户时必需的字段和可选字段"""
    # 必填字段
    email: str
    password: str
    username: str
    role: UserRole = UserRole.DATA_USER
    permission_level: int = PermissionLevel.PUBLIC_DATA.value
    balance: float = Field(
        default=1000.0,
        description="用户初始余额（单位：RMB）"
    )
    # 可选字段，带默认值
    organization_id: Optional[int] = Field(
        None,
        description="组织ID，可选，默认由系统设置"
    )
    is_active: bool = Field(
        default=True,
        description="是否激活，可选，默认为True"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123",
                "username": "example_user",
                "permission_level": 1,
                "balance": 1000.0
            }
        }

# Properties to receive via API on update
class UserUpdate(UserBase):
    password: Optional[str] = None

# Properties shared by models stored in DB
class UserInDBBase(UserBase):
    id: int
    email: EmailStr
    is_deleted: bool = False
    deleted_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    balance: float

    class Config:
        from_attributes = True

# Additional properties to return via API
class User(UserInDBBase):
    pass

# Additional properties stored in DB
class UserInDB(UserInDBBase):
    hashed_password: str 