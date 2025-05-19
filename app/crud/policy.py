from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from app.crud.base import CRUDBase
from app.models.policy import Policy

tz_utc_8 = timezone(timedelta(hours=8))

class CRUDPolicy(CRUDBase[Policy, Dict[str, Any], Dict[str, Any]]):
    def get_active_policies(
        self, 
        db: Session, 
        *, 
        skip: int = 0, 
        limit: int = 100
    ) -> List[Policy]:
        """获取所有活跃的政策"""
        return db.query(Policy).filter(Policy.is_active == True).order_by(Policy.created_at.desc()).offset(skip).limit(limit).all()
    
    def create_policy(
        self, 
        db: Session, 
        *, 
        title: str,
        description: Optional[str] = None,
        file_content: str,
        created_by: int
    ) -> Policy:
        """创建新政策"""
        policy_data = {
            "title": title,
            "description": description,
            "file_content": file_content,
            "created_by": created_by,
            "is_active": True,
            "created_at": datetime.now(tz_utc_8),
            "updated_at": datetime.now(tz_utc_8)
        }
        
        policy = Policy(**policy_data)
        db.add(policy)
        db.commit()
        db.refresh(policy)
        return policy
    
    def update_policy(
        self, 
        db: Session, 
        *, 
        policy_id: int,
        title: Optional[str] = None,
        description: Optional[str] = None,
        file_content: Optional[str] = None,
        is_active: Optional[bool] = None
    ) -> Optional[Policy]:
        """更新政策信息"""
        policy = self.get(db, id=policy_id)
        if not policy:
            return None
        
        update_data = {}
        if title is not None:
            update_data["title"] = title
        if description is not None:
            update_data["description"] = description
        if file_content is not None:
            update_data["file_content"] = file_content
        if is_active is not None:
            update_data["is_active"] = is_active
        
        update_data["updated_at"] = datetime.now(tz_utc_8)
        
        return self.update(db, db_obj=policy, obj_in=update_data)


policy = CRUDPolicy(Policy)