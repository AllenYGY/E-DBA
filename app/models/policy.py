from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Boolean
from sqlalchemy.dialects.mysql import LONGTEXT
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta

from app.db.session import Base

tz_utc_8 = timezone(timedelta(hours=8))


class Policy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    file_content = Column(LONGTEXT, nullable=False)  # 直接存储文件内容
    is_active = Column(Boolean, default=True)
    created_by = Column(Integer, ForeignKey("users.id"))  # E-Admin创建
    created_at = Column(DateTime, default=lambda: datetime.now(tz_utc_8))
    updated_at = Column(DateTime,
                        default=lambda: datetime.now(tz_utc_8),
                        onupdate=lambda: datetime.now(tz_utc_8))
    is_deleted = Column(Boolean, default=False)

    # 关系
    admin = relationship("User")
