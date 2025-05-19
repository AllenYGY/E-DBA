from typing import Any, Dict, List, Optional, Tuple
from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Session
from fastapi import HTTPException, status

from app import schemas
from app.crud.base import CRUDBase
from app.models.service import Service, ServiceType
from app.models.user import User, UserRole
from app.models.organization import Organization
from app.models.enums import PermissionLevel
from app.schemas.service import ServiceCreate, ServiceUpdate

tz_utc_8 = timezone(timedelta(hours=8))

class CRUDService(CRUDBase[Service, ServiceCreate, ServiceUpdate]):
    def get_by_organization(self, db: Session, *, organization_id: int) -> List[Service]:
        """获取组织的所有服务"""
        return db.query(Service).filter(Service.organization_id == organization_id).all()
    
    def get_by_type(
        self, db: Session, *, service_type: ServiceType
    ) -> Optional[Service]:
        """根据服务类型获取服务"""
        return db.query(Service).filter(Service.service_type == service_type).first()
    
    def get_public_services(self, db: Session) -> List[Service]:
        """获取所有公开服务"""
        return db.query(Service).filter(Service.is_public == True, Service.is_active == True).all()
    
    def check_service_exists(
        self, 
        db: Session, 
        *, 
        organization_id: int, 
        service_type: ServiceType,
        name: str
    ) -> bool:
        """检查组织中是否已存在相同类型和名称的服务"""
        return db.query(Service).filter(
            Service.organization_id == organization_id,
            Service.service_type == service_type,
            Service.name == name
        ).first() is not None

    def create_service(
        self, 
        db: Session, 
        *, 
        obj_in: ServiceCreate
    ) -> Service:
        """创建新服务"""
        # 检查服务是否已存在
        if self.check_service_exists(
            db,
            organization_id=obj_in.organization_id,
            service_type=obj_in.service_type,
            name=obj_in.name
        ):
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=f"Service with type {obj_in.service_type} and name '{obj_in.name}' already exists in this organization"
            )

        # 根据服务类型自动设置API配置
        service_data = obj_in.dict()
        # 设置默认的base_url
        # base_url = "http://172.16.160.88:8001"
        
        # 根据服务类型设置API配置
        if obj_in.service_type == ServiceType.STUDENT_VERIFICATION:
            service_data.update({
                # "base_url": base_url,
                "api_path": "/hw/student/authenticate",
                "api_method": "POST",
                "input_format": {
                    "name": "string",
                    "id": "string",
                    "photo": "file"
                },
                "output_format": {
                    "status": "string"
                }
            })
        elif obj_in.service_type == ServiceType.STUDENT_GPA:
            service_data.update({
                # "base_url": base_url,
                "api_path": "/hw/student/record",
                "api_method": "POST",
                "input_format": {
                    "name": "string",
                    "id": "string"
                },
                "output_format": {
                    "name": "string",
                    "enroll_year": "string",
                    "graduation_year": "string",
                    "gpa": "float"
                }
            })
        elif obj_in.service_type == ServiceType.PAPER_SHARING:
            service_data.update({
                # "base_url": base_url,
                "api_path": "/hw/thesis/search",
                "api_method": "POST",
                "input_format": {
                    "keywords": "string"
                },
                "output_format": {
                    "title": "string",
                    "abstract": "string"
                }
            })
        elif obj_in.service_type == ServiceType.PAPER_PDF:
            service_data.update({
                # "base_url": base_url,
                "api_path": "/hw/thesis/pdf",
                "api_method": "GET",
                "input_format": {
                    "title": "string"
                },
                "output_format": {
                    "file": "file",
                    "error": "PDF not found for given title."
                }
            })
        elif obj_in.service_type == ServiceType.BANK_AUTH:
            service_data.update({
                # "base_url": base_url,
                "api_path": "/hw/bank/authenticate",
                "api_method": "POST",
                "input_format": {
                    "bank": "string",
                    "account_name": "string",
                    "account_number": "string",
                    "password": "string"
                },
                "output_format": {
                    "status": "string"  # "success" or "fail"
                }
            })
        elif obj_in.service_type == ServiceType.BANK_TRANSFER:
            service_data.update({
                # "base_url": base_url,
                "api_path": "/hw/bank/transfer",
                "api_method": "POST",
                "input_format": {
                    "from_bank": "string",
                    "from_name": "string",
                    "from_account": "string",
                    "password": "string",
                    "to_bank": "string",
                    "to_name": "string",
                    "to_account": "string",
                    "amount": "int"
                },
                "output_format": {
                    "status": "string",  # "success" or "fail"
                    "reason": "string"   # Optional error reason
                }
            })

        service_data.update({
            "created_at": datetime.now(tz_utc_8),
            "updated_at": datetime.now(tz_utc_8)
        })
        
        service = Service(**service_data)
        db.add(service)
        db.commit()
        db.refresh(service)
        return service
    
    def update_service(
        self, 
        db: Session, 
        *, 
        service_id: int, 
        obj_in: ServiceUpdate
    ) -> Optional[Service]:
        """更新服务信息"""
        service = self.get(db, id=service_id)
        if not service:
            return None
        
        update_data = obj_in.dict(exclude_unset=True)
        update_data["updated_at"] = datetime.now(tz_utc_8)
        
        return self.update(db, db_obj=service, obj_in=update_data)

    def can_create_service(self, db: Session, *, user_id: int, organization_id: int) -> bool:
        """检查用户是否有权限创建服务"""
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        # 检查用户是否属于组织
        if user.organization_id != organization_id:
            return False
        
        # 检查用户是否有权限（O-Convener）
        is_convener = user.role == UserRole.O_CONVENER        
        return is_convener 
    
    def can_update_service(self, db: Session, *, user_id: int, service_id: int) -> bool:
        """检查用户是否有权限更新服务"""
        service = self.get(db, id=service_id)
        if not service:
            return False
        
        user = db.query(User).filter(User.id == user_id).first()
        if not user:
            return False
        
        # 检查用户是否属于服务所属组织
        if user.organization_id != service.organization_id:
            return False
        
        # 检查用户是否有权限（O-Convener 或 PermissionLevel 3）
        is_convener = user.role == UserRole.O_CONVENER
        # print(is_convener)
        has_permission_level_3 = user.permission_level == PermissionLevel.PRIVATE_DATA_PROVIDER.value
        
        return is_convener or has_permission_level_3

    def get_edba_organization(self, db: Session) -> Optional[Organization]:
        """获取 E-DBA 组织"""
        return db.query(Organization).filter(Organization.name == "E-DBA").first()

    def get_edba_public_service(
        self, 
        db: Session, 
        *, 
        service_type: ServiceType
    ) -> Optional[Service]:
        """获取 E-DBA 的公开服务"""
        edba_org = self.get_edba_organization(db)
        if not edba_org:
            return None
            
        return db.query(Service).filter(
            Service.service_type == service_type,
            Service.organization_id == edba_org.id,
            Service.is_public == True,
            Service.is_active == True
        ).first()

    def activate_service_from_edba(
        self,
        db: Session,
        *,
        service_type: ServiceType,
        organization_id: int,
        user_id: int
    ) -> Tuple[Service, str]:
        """
        从 E-DBA 激活服务到指定组织
        
        Returns:
            Tuple[Service, str]: (新创建的服务, 错误信息)
        """
        # 获取 E-DBA 组织
        edba_org = self.get_edba_organization(db)
        if not edba_org:
            return None, "E-DBA organization not found"
        
        # 获取要激活的服务
        source_service = self.get_edba_public_service(db, service_type=service_type)
        if not source_service:
            return None, f"Service type {service_type} not found or not available for activating"
        
        # 检查服务是否已存在
        if self.check_service_exists(
            db,
            organization_id=organization_id,
            service_type=service_type,
            name=source_service.name
        ):
            return None, f"Service with type {service_type} and name '{source_service.name}' already exists in your organization"

        # 创建新服务
        service_data = {
            "name": source_service.name,
            "description": source_service.description,
            "service_type": source_service.service_type,
            "is_public": False,
            "fee_per_use": source_service.fee_per_use,
            "fee_unit": source_service.fee_unit,
            "organization_id": organization_id,
            "external_api_config_id": source_service.external_api_config_id
        }

        try:
            new_service = self.create(
                db=db,
                obj_in=schemas.ServiceCreate(**service_data)
            )
            return new_service, None
        except Exception as e:
            return None, str(e)

service = CRUDService(Service)