from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class PolicyBase(BaseModel):
    title: str
    description: Optional[str] = None
    file_path: str
    is_active: bool = True

class PolicyCreate(PolicyBase):
    pass

class PolicyUpdate(PolicyBase):
    title: Optional[str] = None
    description: Optional[str] = None
    file_path: Optional[str] = None
    is_active: Optional[bool] = None

class PolicyInDBBase(PolicyBase):
    id: int
    created_by: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Policy(PolicyInDBBase):
    pass 