from sqlalchemy import Column, Integer, String, Boolean, JSON, DateTime
from datetime import datetime, timezone, timedelta

from app.db.session import Base

tz_utc_8 = timezone(timedelta(hours=8))

class SystemConfig(Base):
    __tablename__ = "system_config"

    id = Column(Integer, primary_key=True, index=True)
    key = Column(String(255), unique=True, index=True, nullable=False)  # 配置键名
    value = Column(JSON, nullable=True)  # 配置值（JSON格式）
    description = Column(String(255), nullable=True)  # 配置描述
    is_public = Column(Boolean, default=True)  # 是否公开（非公开配置只有管理员可见）
    updated_by = Column(Integer, nullable=True)  # 最后更新人ID
    updated_at = Column(DateTime, default=lambda: datetime.now(tz_utc_8), onupdate=lambda: datetime.now(tz_utc_8))  # 最后更新时间