from typing import Optional
from datetime import datetime, timezone,timedelta
from pydantic import BaseModel, EmailStr, Field

from app.models.enums import UserRole, PermissionLevel

tz_utc_8 = timezone(timedelta(hours=8))

# Login request schema
class LoginRequest(BaseModel):
    """Login request model"""
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "yourpassword"
            }
        }

# 银行账户信息模型
class BankAccountInfo(BaseModel):
    bank: str = Field(..., description="Bank name")
    account_name: str = Field(..., description="Bank account name")
    account_number: str = Field(..., description="Bank account number")
    password: str = Field(..., description="Bank account password")

# O-Convener registration request
class OConvenerRegisterRequest(BaseModel):
    """O-Convener registration request model"""
    # User information
    email: EmailStr = Field(..., description="User email")
    password: str = Field(..., description="User password")
    username: str = Field(..., description="User name")
    permission_level: int = 3
    
    # Organization information
    name: str = Field(..., description="Organization name")
    description: Optional[str] = Field(None, description="Organization description")
    email_domain: str = Field(..., description="Organization email domain")
    verification_document: str = Field(..., description="Organization verification document Base64 encoded string")


    class Config:
        json_schema_extra = {
            "example": {
                "email": "organizer@example.com",
                "password": "strongpassword123",
                "username": "organizer",
                "name": "Example Organization",
                "description": "This is an example organization",
                "email_domain": "example.com",
                "verification_document": "pdf base64 encoded string",
            }
        }

# Shared properties
class UserBase(BaseModel):
    """User base information, all fields are optional"""    
    email: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = True
    role: Optional[UserRole] = None
    permission_level: Optional[int] = None
    organization_id: Optional[int] = None
    balance: Optional[float] = None

# Properties to receive via API on creation
class UserCreate(UserBase):
    """User create model, only include required fields and optional fields when creating a user"""
    # Required fields
    email: str
    password: str
    username: str
    role: UserRole = Field(
        default=UserRole.DATA_USER,
        description="User role, optional, default is DATA_USER"
    )
    permission_level: int = PermissionLevel.PUBLIC_DATA.value
    balance: float = Field(
        default=1000.0,
        description="User initial balance (unit: RMB)"
    )
    # Optional fields, with default values
    organization_id: Optional[int] = Field(
        default=None, # E-DBA 组织ID
        description="Organization ID, optional, default is None"
    )
    is_active: bool = Field(
        default=True,
        description="Whether the user is active, optional, default is True"
    )

    class Config:
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "password": "strongpassword123",
                "username": "example_user",
                "permission_level": 1,
                "balance": 1000.0,
                "role": "DATA_USER"
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

# Question 相关 schema
class QuestionBase(BaseModel):
    title: str
    description: str

class QuestionCreate(QuestionBase):
    pass

class Question(QuestionBase):
    id: int
    user_id: int
    is_resolved: bool
    is_starred: bool
    submitted_at: datetime = Field(default_factory=lambda: datetime.now(tz_utc_8))
    responded_at: Optional[datetime] = None
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True

class QuestionResponseBase(BaseModel):
    content: str

class QuestionResponseCreate(QuestionResponseBase):
    pass

class QuestionResponse(QuestionResponseBase):
    id: int
    question_id: int
    responder_id: int
    created_at: datetime
    updated_at: datetime
    class Config:
        from_attributes = True 