from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field

class CourseBase(BaseModel):
    title: str = Field(..., description="课程标题")
    description: Optional[str] = Field(None, description="课程描述")
    credits: float = Field(0.0, description="课程学分")
    is_public: bool = Field(True, description="课程是否公开")

class CourseCreate(CourseBase):
    pass

class CourseUpdate(BaseModel):
    title: Optional[str] = Field(None, description="课程标题")
    description: Optional[str] = Field(None, description="课程描述")
    credits: Optional[float] = Field(None, description="课程学分")
    is_public: Optional[bool] = Field(None, description="课程是否公开")

class CourseInDBBase(CourseBase):
    id: int = Field(..., description="课程ID")
    organization_id: int = Field(..., description="所属组织ID")
    created_by: int = Field(..., description="创建者ID")
    is_active: bool = Field(True, description="课程是否激活")
    created_at: datetime = Field(..., description="创建时间")
    updated_at: datetime = Field(..., description="更新时间")

    class Config:
        from_attributes = True

class Course(CourseInDBBase):
    pass

class CourseInDB(CourseInDBBase):
    pass

class CourseWithOrganization(Course):
    organization_name: Optional[str] = Field(None, description="组织名称") 