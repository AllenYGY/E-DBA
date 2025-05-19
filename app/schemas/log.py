from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field

class LogBase(BaseModel):
    user_id: Optional[int] = Field(None, description="用户ID")
    organization_id: Optional[int] = Field(None, description="组织ID")
    log_type: str = Field(..., description="日志类型")
    action: str = Field(..., description="操作类型")
    details: Optional[str] = Field(None, description="详细信息")

class LogCreate(LogBase):
    pass

class LogInDBBase(LogBase):
    id: int = Field(..., description="日志ID")
    created_at: datetime = Field(..., description="创建时间")

    class Config:
        from_attributes = True

class Log(LogInDBBase):
    pass

class LogInDB(LogInDBBase):
    pass

class LogListResponse(BaseModel):
    items: List[Log]
    total: int 