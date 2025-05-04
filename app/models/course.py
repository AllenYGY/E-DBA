from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta

from app.db.session import Base

tz_utc_8 = timezone(timedelta(hours=8))


class Course(Base):
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False, index=True)
    description = Column(Text, nullable=True)
    credits = Column(Float, default=0.0)  
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=True)  # 是否公开可见
    created_by = Column(Integer, ForeignKey("users.id"))  # 课程创建者
    created_at = Column(DateTime, default=lambda:   datetime.now(tz_utc_8))
    updated_at = Column(DateTime, default=datetime.now(tz_utc_8), onupdate=datetime.now(tz_utc_8))
    is_deleted = Column(Boolean, default=False)
    # 关系
    organization = relationship("Organization", back_populates="courses")
    schedules = relationship("CourseSchedule", back_populates="course")
    creator = relationship("User", foreign_keys=[created_by])  # 创建者关系


class CourseSchedule(Base):
    __tablename__ = "course_schedules"
    
    id = Column(Integer, primary_key=True, index=True)
    course_id = Column(Integer, ForeignKey("courses.id"))
    day_of_week = Column(Integer)  # 1-7 表示周一至周日
    start_time = Column(String(10))  # 格式：HH:MM
    end_time = Column(String(10))  # 格式：HH:MM
    location = Column(String(255))
    is_active = Column(Boolean, default=True)
    
    # 关系
    course = relationship("Course", back_populates="schedules")