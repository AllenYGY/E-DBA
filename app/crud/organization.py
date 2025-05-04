from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from app.crud.base import CRUDBase
from app.models.organization import Organization
from app.models.payment import Payment

tz_utc_8 = timezone(timedelta(hours=8))

class CRUDOrganization(CRUDBase[Organization, Dict[str, Any], Dict[str, Any]]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Organization]:
        """通过名称获取组织"""
        return db.query(Organization).filter(Organization.name == name).first()
    
    def get_by_email_domain(self, db: Session, *, email_domain: str) -> List[Organization]:
        """通过邮箱域名获取组织"""
        return db.query(Organization).filter(Organization.email_domain == email_domain).all()
    
    def get_active_organizations(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Organization]:
        """获取所有活跃组织"""
        return db.query(Organization).filter(Organization.is_active == True).offset(skip).limit(limit).all()
    
    def get_verified_organizations(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Organization]:
        """获取所有已验证组织"""
        return db.query(Organization).filter(Organization.is_verified == True).offset(skip).limit(limit).all()
    
    def create_with_convener(self, db: Session, *, obj_in: Dict[str, Any], convener_id: int) -> Organization:
        """创建组织并关联协调人"""
        # 如果输入是 Pydantic 模型，转换为字典
        if hasattr(obj_in, "dict"):
            obj_in_data = obj_in.dict()
        else:
            obj_in_data = obj_in
            
        db_obj = Organization(
            name=obj_in_data.get("name"),
            description=obj_in_data.get("description"),
            email_domain=obj_in_data.get("email_domain"),
            verification_document=obj_in_data.get("verification_document"),
            is_verified=False,
            is_active=True,
            convener_id=convener_id,
            created_at=datetime.now(tz_utc_8),
            updated_at=datetime.now(tz_utc_8)
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def create_organization(self, db: Session, *, name: str, description: Optional[str] = None, 
                           email_domain: Optional[str] = None, convener_id: int) -> Organization:
        """创建新组织"""
        organization_data = {
            "name": name,
            "description": description,
            "email_domain": email_domain,
            "convener_id": convener_id,
            "is_verified": False,
            "is_active": True,
            "created_at": datetime.now(tz_utc_8),
            "updated_at": datetime.now(tz_utc_8)
        }
        
        organization = Organization(**organization_data)
        db.add(organization)
        db.commit()
        db.refresh(organization)
        return organization
    
    def update_organization(self, db: Session, *, organization_id: int, obj_in: Dict[str, Any]) -> Optional[Organization]:
        """更新组织信息"""
        organization = self.get(db, id=organization_id)
        if not organization:
            return None
        
        obj_in["updated_at"] = datetime.now(tz_utc_8)
        return self.update(db, db_obj=organization, obj_in=obj_in)
    
    def verify_organization(self, db: Session, *, organization_id: int, verification_document: str) -> Optional[Organization]:
        """提交组织验证文件"""
        organization = self.get(db, id=organization_id)
        if not organization:
            return None
        
        update_data = {
            "verification_document": verification_document,
            "updated_at": datetime.now(tz_utc_8)
        }
        
        return self.update(db, db_obj=organization, obj_in=update_data)
    
    def approve_organization(self, db: Session, *, organization_id: int) -> Optional[Organization]:
        """批准组织验证"""
        organization = self.get(db, id=organization_id)
        if not organization:
            return None
        
        update_data = {
            "is_verified": True,
            "updated_at": datetime.now(tz_utc_8)
        }
        
        return self.update(db, db_obj=organization, obj_in=update_data)


organization = CRUDOrganization(Organization)