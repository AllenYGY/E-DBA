from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PolicyBase(BaseModel):
    title: str
    description: Optional[str] = None
    file_content: str
    is_active: bool = True

class PolicyCreate(PolicyBase):
    pass

class PolicyUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    file_content: Optional[str] = None
    is_active: Optional[bool] = None

class PolicyInDBBase(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    is_active: bool
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Policy(PolicyInDBBase):
    pass 