from sqlalchemy import Boolean, Column, Integer, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta

from app.db.session import Base

tz_utc_8 = timezone(timedelta(hours=8))

class VerificationStatus(Base):
    __tablename__ = "verification_status"
    
    id = Column(Integer, primary_key=True, index=True)
    user_id = "users.id"
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    e_admin_id = Column(Integer, ForeignKey(user_id), nullable=True)  # 初审管理员
    senior_e_admin_id = Column(Integer, ForeignKey(user_id), nullable=True)  # 终审管理员
    e_admin_approved = Column(Boolean, default=False)  # E-Admin初审结果
    senior_approved = Column(Boolean, default=False)  # Senior E-Admin终审结果
    e_admin_comment = Column(Text, nullable=True)
    senior_comment = Column(Text, nullable=True)
    submitted_at = Column(DateTime(timezone=True), default=lambda: datetime.now(tz_utc_8))
    e_admin_reviewed_at = Column(DateTime(timezone=True), nullable=True)
    senior_reviewed_at = Column(DateTime(timezone=True), nullable=True)
    
    # 关系
    organization = relationship("Organization", back_populates="verification_status")
    e_admin = relationship("User", foreign_keys=[e_admin_id])
    senior_e_admin = relationship("User", foreign_keys=[senior_e_admin_id]) 