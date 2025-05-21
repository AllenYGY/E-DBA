from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from app.crud.base import CRUDBase
from app.models.organization import Organization

tz_utc_8 = timezone(timedelta(hours=8))

class CRUDOrganization(CRUDBase[Organization, Dict[str, Any], Dict[str, Any]]):
    def get_by_name(self, db: Session, *, name: str) -> Optional[Organization]:
        """Get organization by name"""
        return db.query(Organization).filter(Organization.name == name).first()
    
    def get_by_email_domain(self, db: Session, *, email_domain: str) -> List[Organization]:
        """Get organization by email domain"""
        return db.query(Organization).filter(Organization.email_domain == email_domain).all()
    
    def get_active_organizations(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Organization]:
        """Get all active organizations"""
        return db.query(Organization).filter(Organization.is_active == True).offset(skip).limit(limit).all()
    
    def get_verified_organizations(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[Organization]:
        """Get all verified organizations"""
        return db.query(Organization).filter(Organization.is_verified == True).offset(skip).limit(limit).all()
    
    def create_with_convener(self, db: Session, *, obj_in: Dict[str, Any], convener_id: int) -> Organization:
        """Create organization and associate convener"""
        # If input is Pydantic model, convert to dictionary
        if hasattr(obj_in, "dict"):
            obj_in_data = obj_in.dict()
        else:
            obj_in_data = obj_in
            
        db_obj = Organization(
            name=obj_in_data.get("name"),
            full_name=obj_in_data.get("full_name"),
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
    
    def create_organization(self, db: Session, *, name: str, full_name: Optional[str] = None, 
                           email_domain: Optional[str] = None, convener_id: int) -> Organization:
        """Create new organization"""
        organization_data = {
            "name": name,
            "full_name": full_name,
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
        """
        Update organization information
        """
        organization = self.get(db, id=organization_id)
        if not organization:
            return None
        
        obj_in["updated_at"] = datetime.now(tz_utc_8)
        return self.update(db, db_obj=organization, obj_in=obj_in)
    
    def verify_organization(self, db: Session, *, organization_id: int, verification_document: str) -> Optional[Organization]:
        """Submit organization verification document"""
        organization = self.get(db, id=organization_id)
        if not organization:
            return None
        
        update_data = {
            "verification_document": verification_document,
            "updated_at": datetime.now(tz_utc_8)
        }
        
        return self.update(db, db_obj=organization, obj_in=update_data)
    
    def approve_organization(self, db: Session, *, organization_id: int) -> Optional[Organization]:
        """Approve organization verification"""
        organization = self.get(db, id=organization_id)
        if not organization:
            return None
        
        update_data = {
            "is_verified": True,
            "updated_at": datetime.now(tz_utc_8)
        }
        
        return self.update(db, db_obj=organization, obj_in=update_data)

    def get_by_email_domain(self, db: Session, email_domain: str) -> Optional[Organization]:
        """
        通过邮箱域名查找组织
        
        Args:
            db: 数据库会话
            email_domain: 邮箱域名
            
        Returns:
            Optional[models.Organization]: 找到的组织对象，如果未找到则返回 None
        """
        return db.query(Organization).filter(
            Organization.email_domain == email_domain.lower(),
            Organization.is_active == True
        ).first()

organization = CRUDOrganization(Organization)