from typing import Optional, Dict, Any
from pydantic import BaseModel
from datetime import datetime

from app.models.service import ServiceType

class ExternalApiConfigBase(BaseModel):
    """外部 API 配置基础模型"""
    base_url: str
    path: str
    method: str = "POST"
    input_format: Optional[Dict[str, Any]] = None
    output_format: Optional[Dict[str, Any]] = None

class ExternalApiConfigCreate(ExternalApiConfigBase):
    """创建外部 API 配置"""
    service_type: ServiceType

class ExternalApiConfigUpdate(ExternalApiConfigBase):
    """更新外部 API 配置"""
    base_url: Optional[str] = None
    path: Optional[str] = None
    method: Optional[str] = None

class ExternalApiConfig(ExternalApiConfigBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ServiceBase(BaseModel):
    """服务基础模型"""
    name: str
    description: Optional[str] = None
    organization_id: int
    service_type: ServiceType
    is_active: bool = True
    is_public: bool = False
    fee_per_use: float = 0.0
    fee_unit: str = "RMB"
    
    # 通用API配置
    base_url: Optional[str] = None
    api_path: Optional[str] = None
    api_method: Optional[str] = None
    input_format: Optional[Dict[str, Any]] = None
    output_format: Optional[Dict[str, Any]] = None

class ServiceCreate(ServiceBase):
    """创建服务"""
    pass

class ServiceUpdate(BaseModel):
    """更新服务"""
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None
    is_public: Optional[bool] = None
    fee_per_use: Optional[float] = None
    fee_unit: Optional[str] = None
    base_url: Optional[str] = None
    api_path: Optional[str] = None
    api_method: Optional[str] = None
    input_format: Optional[Dict[str, Any]] = None
    output_format: Optional[Dict[str, Any]] = None

class ServiceInDBBase(ServiceBase):
    """数据库中的服务模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Service(ServiceInDBBase):
    """服务模型"""
    pass

class ServiceConfigBase(BaseModel):
    """服务配置基础模型"""
    service_id: int
    config_key: str
    config_value: Dict[str, Any]
    description: Optional[str] = None
    is_active: bool = True

class ServiceConfigCreate(ServiceConfigBase):
    """创建服务配置"""
    pass

class ServiceConfigUpdate(BaseModel):
    """更新服务配置"""
    config_value: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ServiceConfigInDBBase(ServiceConfigBase):
    """数据库中的服务配置模型"""
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ServiceConfig(ServiceConfigInDBBase):
    """服务配置模型"""
    pass

class ServiceUsageBase(BaseModel):
    """服务使用记录基础模型"""
    service_id: int
    user_id: int
    usage_details: str
    fee_charged: float

class ServiceUsageCreate(ServiceUsageBase):
    """创建服务使用记录"""
    pass

class ServiceUsage(ServiceUsageBase):
    """服务使用记录模型"""
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 