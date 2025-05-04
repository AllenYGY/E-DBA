from datetime import datetime
from typing import Optional, Dict, Any
from pydantic import BaseModel

class SystemConfigBase(BaseModel):
    key: str
    value: Dict[str, Any]
    description: Optional[str] = None
    is_active: bool = True

class SystemConfigUpdate(BaseModel):
    value: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class SystemConfigInDBBase(SystemConfigBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class SystemConfig(SystemConfigInDBBase):
    pass 