from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta  

from app.db.session import Base
tz_utc_8 = timezone(timedelta(hours=8))

class Organization(Base):
    __tablename__ = "organizations"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(255), index=True, nullable=False)
    full_name = Column(Text, nullable=True)
    email_domain = Column(String(255), nullable=True)  # 用于通配符邮箱验证（如 *@domain）
    verification_document = Column(LONGTEXT)  
    is_verified = Column(Boolean, default=False, nullable=False)
    is_active = Column(Boolean, default=True, nullable=False)
    is_deleted = Column(Boolean, default=False)
    deleted_at = Column(DateTime, nullable=True)
    # create time at utc-8
    created_at = Column(DateTime, default=lambda: datetime.now(tz_utc_8), nullable=False)
    updated_at = Column(DateTime, default=lambda: datetime.now(tz_utc_8), onupdate=lambda: datetime.now(tz_utc_8), nullable=False)
    
    # 关系
    convener_id = Column(Integer, ForeignKey("users.id"), nullable=False)
    
    # 组织提供的服务
    services = relationship("Service", back_populates="organization")
    
    # 组织的课程
    courses = relationship("Course", back_populates="organization")
    
    # 组织的日志
    logs = relationship("Log", back_populates="organization")
    
    # 验证状态
    verification_status = relationship("VerificationStatus", back_populates="organization", uselist=False)
    
    # 转账记录
    transfers = relationship("Transfer", back_populates="organization")