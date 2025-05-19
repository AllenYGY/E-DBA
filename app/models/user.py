from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum, DateTime, Text, Float
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta

from app.db.session import Base
from app.models.enums import UserRole, PermissionLevel

tz_utc_8 = timezone(timedelta(hours=8))

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String(255), unique=True, index=True, nullable=False)
    username = Column(String(255), index=True)
    hashed_password = Column(String(255), nullable=False)
    role = Column(Enum(UserRole), default=UserRole.DATA_USER)
    permission_level = Column(Integer, default=PermissionLevel.PUBLIC_DATA.value)
    is_active = Column(Boolean, default=True)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)

    created_at = Column(DateTime, default=lambda: datetime.now(tz_utc_8))
    updated_at = Column(DateTime, default=lambda: datetime.now(tz_utc_8), onupdate=lambda: datetime.now(tz_utc_8))
    
    # 关系
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    organization = relationship("Organization", foreign_keys=[organization_id])
    
    # 用户余额（单位：RMB）
    balance = Column(Float, default=1000.0)
    
    # 用户问题和帮助请求
    questions = relationship("Question", back_populates="user")
    
    # 日志记录
    logs = relationship("Log", back_populates="user")
    
    # 转账记录
    transfers = relationship("Transfer", back_populates="from_user")
    

class Question(Base):
    __tablename__ = "questions"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    title = Column(String(255))
    description = Column(Text)
    email = Column(String(255))  # 提问者邮箱
    role = Column(String(50))    # 提问者角色
    is_resolved = Column(Boolean, default=False)
    is_starred = Column(Boolean, default=False)  # T-Admin回复后显示星标
    submitted_at = Column(DateTime, default=lambda: datetime.now(tz_utc_8))  # 提交时间
    responded_at = Column(DateTime, nullable=True)  # 首次回复时间
    created_at = Column(DateTime, default=lambda: datetime.now(tz_utc_8))
    updated_at = Column(DateTime, default=lambda: datetime.now(tz_utc_8), onupdate=lambda: datetime.now(tz_utc_8))
    
    # 关系
    user = relationship("User", back_populates="questions")
    responses = relationship("QuestionResponse", back_populates="question")


class QuestionResponse(Base):
    __tablename__ = "question_responses"
    
    id = Column(Integer, primary_key=True, index=True)
    question_id = Column(Integer, ForeignKey("questions.id"))
    responder_id = Column(Integer, ForeignKey("users.id"))  # 通常是T-Admin
    content = Column(Text)
    created_at = Column(DateTime, default=lambda: datetime.now(tz_utc_8))
    updated_at = Column(DateTime, default=lambda: datetime.now(tz_utc_8), onupdate=lambda: datetime.now(tz_utc_8))
    
    # 关系
    question = relationship("Question", back_populates="responses")
    responder = relationship("User")