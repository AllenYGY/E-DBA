from sqlalchemy import Boolean, Column, Integer, String, ForeignKey, Enum, DateTime, Text, Float, JSON
from sqlalchemy.orm import relationship
from datetime import datetime, timezone, timedelta
import enum

from app.db.session import Base

tz_utc_8 = timezone(timedelta(hours=8))
SERVICE_ID_FOREIGN_KEY = "services.id"

class ServiceType(str, enum.Enum):
    COURSE_SHARING = "course_sharing"  # 课程信息共享（免费）
    STUDENT_VERIFICATION = "student_verification"  # 学生身份验证
    PAPER_SHARING = "paper_sharing"  # 论文共享
    STUDENT_GPA = "student_gpa"  # 学生GPA记录
    DATA_VAULT = "data_vault"  # 数据保险库（可选功能）
    PAPER_PDF = "paper_pdf"  # 论文PDF获取
    BANK_AUTH = "bank_auth"  # 银行账户认证
    BANK_TRANSFER = "bank_transfer"  # 银行转账


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
    
    # API 配置
    external_api_config_id = Column(Integer, ForeignKey("external_api_configs.id"), unique=True, nullable=True)
    
    # 关系
    organization = relationship("Organization", back_populates="services")
    external_api_config = relationship("ExternalApiConfig", back_populates="service", uselist=False)
    
    # 服务特定配置
    student_verification_config = relationship("StudentVerificationConfig", back_populates="service", uselist=False)
    thesis_sharing_config = relationship("ThesisSharingConfig", back_populates="service", uselist=False)
    data_vault_config = relationship("DataVaultConfig", back_populates="service", uselist=False)


class StudentVerificationConfig(Base):
    __tablename__ = "student_verification_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey(SERVICE_ID_FOREIGN_KEY), unique=True)
    database_connection = Column(String(255), nullable=False)  # 数据库连接信息
    verification_api = Column(String(255), nullable=True)  # 验证API地址
    verification_rules = Column(Text, nullable=True)  # 验证规则
    is_private_only = Column(Boolean, default=True)  # 是否仅限私有数据消费者访问
    
    # 关系
    service = relationship("Service", back_populates="student_verification_config")


class ThesisSharingConfig(Base):
    __tablename__ = "thesis_sharing_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey(SERVICE_ID_FOREIGN_KEY), unique=True)
    database_connection = Column(String(255), nullable=False)  # 论文库连接信息
    allow_preview = Column(Boolean, default=True)  # 是否允许预览
    allow_download = Column(Boolean, default=True)  # 是否允许下载
    download_fee = Column(Float, default=0.0)  # 下载费用
    is_public = Column(Boolean, default=False)  # 是否对所有组织开放
    
    # 关系
    service = relationship("Service", back_populates="thesis_sharing_config")


class DataVaultConfig(Base):
    __tablename__ = "data_vault_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    service_id = Column(Integer, ForeignKey(SERVICE_ID_FOREIGN_KEY), unique=True)
    storage_quota = Column(Float, default=1.0)  # 存储配额（GB）
    encryption_level = Column(String(50), default="standard")  # standard, advanced, military
    backup_frequency = Column(String(50), default="daily")  # daily, weekly, monthly
    
    # 关系
    service = relationship("Service", back_populates="data_vault_config")


class ExternalApiConfig(Base):
    __tablename__ = "external_api_configs"
    
    id = Column(Integer, primary_key=True, index=True)
    base_url = Column(String(255), nullable=False)  # API基础URL
    path = Column(String(255), nullable=False)  # API路径
    method = Column(String(10), nullable=False)  # HTTP方法（GET/POST）
    input_format = Column(JSON, nullable=True)  # 输入格式定义
    output_format = Column(JSON, nullable=True)  # 输出格式定义
    service_type = Column(String(255))  # 确保有这一行
    created_at = Column(DateTime, default=lambda: datetime.now(tz_utc_8))
    updated_at = Column(DateTime, default=lambda: datetime.now(tz_utc_8), onupdate=lambda: datetime.now(tz_utc_8))
    
    # 关系
    service = relationship("Service", back_populates="external_api_config", uselist=False)