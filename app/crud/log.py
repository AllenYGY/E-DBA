from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session
from datetime import datetime

from app.crud.base import CRUDBase
from app.models.log import Log, LogType
from datetime import timezone, timedelta

tz_utc_8 = timezone(timedelta(hours=8))

class CRUDLog(CRUDBase[Log, Dict[str, Any], Dict[str, Any]]):
    def create_log(
        self, 
        db: Session, 
        *, 
        user_id: Optional[int] = None,
        organization_id: Optional[int] = None,
        log_type: LogType,
        action: str,
        details: Optional[str] = None,
        ip_address: Optional[str] = None,
        user_agent: Optional[str] = None
    ) -> Log:
        """创建日志记录"""
        log_data = {
            "user_id": user_id,
            "organization_id": organization_id,
            "log_type": log_type,
            "action": action,
            "details": details,
            "ip_address": ip_address,
            "user_agent": user_agent,
            "created_at": datetime.now(tz_utc_8)
        }
        
        log = Log(**log_data)
        db.add(log)
        db.commit()
        db.refresh(log)
        return log
    
    def get_logs_by_user(
        self, 
        db: Session, 
        *, 
        user_id: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Log]:
        """获取用户的日志记录"""
        return db.query(Log).filter(Log.user_id == user_id).order_by(Log.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_logs_by_organization(
        self, 
        db: Session, 
        *, 
        organization_id: int,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Log]:
        """获取组织的日志记录"""
        return db.query(Log).filter(Log.organization_id == organization_id).order_by(Log.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_logs_by_type(
        self, 
        db: Session, 
        *, 
        log_type: LogType,
        skip: int = 0, 
        limit: int = 100
    ) -> List[Log]:
        """获取指定类型的日志记录"""
        return db.query(Log).filter(Log.log_type == log_type).order_by(Log.created_at.desc()).offset(skip).limit(limit).all()


log = CRUDLog(Log)