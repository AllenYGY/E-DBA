from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, Text, Enum
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
import enum

from app.db.session import Base

tz_utc_8 = timezone(timedelta(hours=8))

class LogType(str, enum.Enum):
    LOGIN = "login"  # 用户登录
    LOGOUT = "logout"  # 用户退出
    SERVICE_ACCESS = "service_access"  # 服务访问
    PAYMENT = "payment"  # 支付活动
    ADMIN_ACTION = "admin_action"  # 管理员操作
    ORGANIZATION = "organization"  # 组织相关操作
    SYSTEM = "system"  # 系统操作
    COURSE = "course"  # 课程相关操作


class Log(Base):
    __tablename__ = "logs"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"), nullable=True)
    log_type = Column(Enum(LogType), nullable=False)
    action = Column(String(255), nullable=False)  # 具体操作
    details = Column(Text, nullable=True)  # 详细信息
    ip_address = Column(String(50), nullable=True)  # 操作IP地址
    user_agent = Column(String(255), nullable=True)  # 用户代理
    created_at = Column(DateTime, default=datetime.now(tz_utc_8))
    
    # 关系
    user = relationship("User", back_populates="logs")
    organization = relationship("Organization", back_populates="logs")