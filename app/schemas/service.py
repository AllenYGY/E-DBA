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
    name: str
    description: Optional[str] = None
    organization_id: int
    is_active: bool = True
    is_public: bool = False  

class ServiceCreate(ServiceBase):
    service_type: ServiceType
    external_api_config_id: int
    


class ServiceUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ServiceInDBBase(ServiceBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class Service(ServiceInDBBase):
    pass

class ServiceConfigBase(BaseModel):
    service_id: int
    config_key: str
    config_value: Dict[str, Any]
    description: Optional[str] = None
    is_active: bool = True

class ServiceConfigCreate(ServiceConfigBase):
    pass

class ServiceConfigUpdate(BaseModel):
    config_value: Optional[Dict[str, Any]] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None

class ServiceConfigInDBBase(ServiceConfigBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True

class ServiceConfig(ServiceConfigInDBBase):
    pass

class ServiceUsageBase(BaseModel):
    service_id: int
    user_id: int
    usage_details: str
    fee_charged: float

class ServiceUsageCreate(ServiceUsageBase):
    pass

class ServiceUsage(ServiceUsageBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True 