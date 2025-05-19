from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum, DateTime, Text, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
import enum

from app.db.session import Base

tz_utc_8 = timezone(timedelta(hours=8))
SERVICE_ID_FOREIGN_KEY = "services.id"

class ServiceType(str, enum.Enum):
    COURSE_SHARING = "course_sharing"  # Course Sharing 
    STUDENT_VERIFICATION = "student_verification"  # Student Verification
    PAPER_SHARING = "paper_sharing"  # Paper Sharing
    STUDENT_GPA = "student_gpa"  # Student GPA Record
    DATA_VAULT = "data_vault"  # Data Vault (Optional Feature)
    PAPER_PDF = "paper_pdf"  # Paper PDF Retrieval
    BANK_AUTH = "bank_auth"  # Bank Account Authentication
    BANK_TRANSFER = "bank_transfer"     # Bank Transfer
    CUSTOM_SERVICE = "custom_service"  # Custom Service

class Service(Base):
    __tablename__ = "services"

    id = Column(Integer, primary_key=True, index=True)
    organization_id = Column(Integer, ForeignKey("organizations.id"))
    service_type = Column(
        Enum(ServiceType, values_callable=lambda obj: [e.value for e in obj]),
        nullable=False
    )
    name = Column(String(255), nullable=False)
    description = Column(Text, nullable=True)
    is_active = Column(Boolean, default=True)
    is_public = Column(Boolean, default=False)  # 是否为公开服务
    created_at = Column(DateTime, default=lambda: datetime.now(tz_utc_8))
    updated_at = Column(DateTime, default=lambda: datetime.now(tz_utc_8), onupdate=lambda: datetime.now(tz_utc_8))
    
    # 服务费用设置
    fee_per_use = Column(Float, default=0.0)  # 每次使用的费用
    fee_unit = Column(String(50), default="RMB")  # 费用单位
    
    # 通用API配置
    base_url = Column(String(255), nullable=True)  # API基础URL
    api_path = Column(String(255), nullable=True)  # API路径
    api_method = Column(String(10), nullable=True)  # HTTP方法（GET/POST）
    input_format = Column(JSON, nullable=True)  # 输入格式定义
    output_format = Column(JSON, nullable=True)  # 输出格式定义
    
    
    # 关系
    organization = relationship("Organization", back_populates="services")

