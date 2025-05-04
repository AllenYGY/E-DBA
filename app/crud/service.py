from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from datetime import datetime

from app.crud.base import CRUDBase
from app.models.service import Service, ServiceType, StudentVerificationConfig, DataVaultConfig, ExternalApiConfig, ThesisSharingConfig
from app.schemas.service import ServiceCreate, ServiceUpdate, ExternalApiConfigCreate


class CRUDService(CRUDBase[Service, ServiceCreate, ServiceUpdate]):
    def get_by_organization(self, db: Session, *, organization_id: int) -> List[Service]:
        """获取组织的所有服务"""
        return db.query(Service).filter(Service.organization_id == organization_id).all()
    
    def get_by_type(
        self, db: Session, *, service_type: ServiceType
    ) -> Optional[Service]:
        return db.query(Service).filter(Service.service_type == service_type).first()
    
    def get_public_services(self, db: Session) -> List[Service]:
        """获取所有公开服务"""
        return db.query(Service).filter(Service.is_public == True, Service.is_active == True).all()
    
    def create_service(self, db: Session, *, organization_id: int, service_type: ServiceType, name: str, 
                      description: Optional[str] = None, api_endpoint: Optional[str] = None, 
                      api_key: Optional[str] = None, is_public: bool = False, 
                      fee_per_use: float = 0.0) -> Service:
        """创建新服务"""
        service_data = {
            "organization_id": organization_id,
            "service_type": service_type,
            "name": name,
            "description": description,
            "api_endpoint": api_endpoint,
            "api_key": api_key,
            "is_active": True,
            "is_public": is_public,
            "fee_per_use": fee_per_use,
            "fee_unit": "RMB",  # 默认使用人民币
            "created_at": datetime.utcnow(),
            "updated_at": datetime.utcnow()
        }
        
        service = Service(**service_data)
        db.add(service)
        db.commit()
        db.refresh(service)
        return service
    
    def update_service(self, db: Session, *, service_id: int, obj_in: Dict[str, Any]) -> Optional[Service]:
        """更新服务信息"""
        service = self.get(db, id=service_id)
        if not service:
            return None
        
        obj_in["updated_at"] = datetime.utcnow()
        return self.update(db, db_obj=service, obj_in=obj_in)

    def create_api_config(
        self, db: Session, *, service_id: int, obj_in: ExternalApiConfigCreate
    ) -> ExternalApiConfig:
        db_obj = ExternalApiConfig(
            service_id=service_id,
            base_url=obj_in.base_url,
            path=obj_in.path,
            method=obj_in.method,
            input_format=obj_in.input_format,
            output_format=obj_in.output_format,
            api_key=obj_in.api_key
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


class CRUDStudentVerificationConfig(CRUDBase[StudentVerificationConfig, Dict[str, Any], Dict[str, Any]]):
    def get_by_service(self, db: Session, *, service_id: int) -> Optional[StudentVerificationConfig]:
        """获取服务的学生验证配置"""
        return db.query(StudentVerificationConfig).filter(StudentVerificationConfig.service_id == service_id).first()
    
    def create_config(self, db: Session, *, service_id: int, verification_method: str = "basic", 
                     database_connection: Optional[str] = None, api_credentials: Optional[str] = None) -> StudentVerificationConfig:
        """创建学生验证配置"""
        config_data = {
            "service_id": service_id,
            "verification_method": verification_method,
            "database_connection": database_connection,
            "api_credentials": api_credentials
        }
        
        config = StudentVerificationConfig(**config_data)
        db.add(config)
        db.commit()
        db.refresh(config)
        return config
    
    def update_config(self, db: Session, *, config_id: int, obj_in: Dict[str, Any]) -> Optional[StudentVerificationConfig]:
        """更新学生验证配置"""
        config = self.get(db, id=config_id)
        if not config:
            return None
        
        return self.update(db, db_obj=config, obj_in=obj_in)


class CRUDThesisSharingConfig(CRUDBase[ThesisSharingConfig, Dict[str, Any], Dict[str, Any]]):
    def get_by_service(self, db: Session, *, service_id: int) -> Optional[ThesisSharingConfig]:
        """获取服务的论文共享配置"""
        return db.query(ThesisSharingConfig).filter(ThesisSharingConfig.service_id == service_id).first()
    
    def create_config(self, db: Session, *, service_id: int, allow_preview: bool = True, 
                     allow_download: bool = True, download_fee: float = 0.0, 
                     repository_connection: Optional[str] = None) -> ThesisSharingConfig:
        """创建论文共享配置"""
        config_data = {
            "service_id": service_id,
            "allow_preview": allow_preview,
            "allow_download": allow_download,
            "download_fee": download_fee,
            "repository_connection": repository_connection
        }
        
        config = ThesisSharingConfig(**config_data)
        db.add(config)
        db.commit()
        db.refresh(config)
        return config
    
    def update_config(self, db: Session, *, config_id: int, obj_in: Dict[str, Any]) -> Optional[ThesisSharingConfig]:
        """更新论文共享配置"""
        config = self.get(db, id=config_id)
        if not config:
            return None
        
        return self.update(db, db_obj=config, obj_in=obj_in)


class CRUDDataVaultConfig(CRUDBase[DataVaultConfig, Dict[str, Any], Dict[str, Any]]):
    def get_by_service(self, db: Session, *, service_id: int) -> Optional[DataVaultConfig]:
        """获取服务的数据保险库配置"""
        return db.query(DataVaultConfig).filter(DataVaultConfig.service_id == service_id).first()
    
    def create_config(self, db: Session, *, service_id: int, storage_quota: float = 1.0, 
                     encryption_level: str = "standard", backup_frequency: str = "daily") -> DataVaultConfig:
        """创建数据保险库配置"""
        config_data = {
            "service_id": service_id,
            "storage_quota": storage_quota,
            "encryption_level": encryption_level,
            "backup_frequency": backup_frequency
        }
        
        config = DataVaultConfig(**config_data)
        db.add(config)
        db.commit()
        db.refresh(config)
        return config
    
    def update_config(self, db: Session, *, config_id: int, obj_in: Dict[str, Any]) -> Optional[DataVaultConfig]:
        """更新数据保险库配置"""
        config = self.get(db, id=config_id)
        if not config:
            return None
        
        return self.update(db, db_obj=config, obj_in=obj_in)


service = CRUDService(Service)
student_verification_config = CRUDStudentVerificationConfig(StudentVerificationConfig)
paper_sharing_config = CRUDThesisSharingConfig(ThesisSharingConfig)
data_vault_config = CRUDDataVaultConfig(DataVaultConfig)