from typing import Any, Dict, List, Optional

from sqlalchemy.orm import Session
from datetime import datetime, timezone, timedelta

from app.crud.base import CRUDBase
from app.models.user import User, HelpRequest, HelpResponse, UserRole
from app.core.security import get_password_hash, verify_password
from app.schemas.user import UserCreate, UserUpdate


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """验证用户凭据"""
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user

    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """通过邮箱获取用户"""
        return db.query(User).filter(User.email == email).first()
    
    def get_by_username(self, db: Session, *, username: str) -> Optional[User]:
        """通过用户名获取用户"""
        return db.query(User).filter(User.username == username).first()
    
    def get_active_users(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[User]:
        """获取所有活跃用户"""
        return db.query(User).filter(User.is_active).offset(skip).limit(limit).all()
    
    def get_users_by_role(self, db: Session, *, role: UserRole, skip: int = 0, limit: int = 100) -> List[User]:
        """获取指定角色的用户"""
        return db.query(User).filter(User.role == role).offset(skip).limit(limit).all()
    
    def get_users_by_organization(self, db: Session, *, organization_id: int, skip: int = 0, limit: int = 100) -> List[User]:
        """获取指定组织的用户"""
        return db.query(User).filter(User.organization_id == organization_id).offset(skip).limit(limit).all()
    
    def get_first_e_admin(self, db: Session) -> Optional[User]:
        """获取第一个 E-admin 用户"""
        user = db.query(User).filter(User.role == UserRole.E_ADMIN).first()
        print(f"Found E-admin: {user.id if user else None}")
        return user
    
    def get_first_senior_e_admin(self, db: Session) -> Optional[User]:
        """获取第一个 Senior E-admin 用户"""
        user = db.query(User).filter(User.role == UserRole.SENIOR_E_ADMIN).first()
        print(f"Found Senior E-admin: {user.id if user else None}")
        return user
    
    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """创建新用户"""
        db_obj = User(
            email=obj_in.email,
            username=obj_in.username,
            hashed_password=get_password_hash(obj_in.password),
            role=obj_in.role,
            permission_level=obj_in.permission_level,
            organization_id=obj_in.organization_id,
            balance=obj_in.balance,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj
    
    def update_user(self, db: Session, *, user_id: int, obj_in: Dict[str, Any]) -> Optional[User]:
        """更新用户信息"""
        user = self.get(db, id=user_id)
        if not user:
            return None
        
        obj_in["updated_at"] = datetime.now(timezone(timedelta(hours=8)))
        return self.update(db, db_obj=user, obj_in=obj_in)
    
    def update_password(self, db: Session, *, user_id: int, hashed_password: str) -> Optional[User]:
        """更新用户密码"""
        user = self.get(db, id=user_id)
        if not user:
            return None
        
        update_data = {
            "hashed_password": hashed_password,
            "updated_at": datetime.now(timezone(timedelta(hours=8)))
        }
        
        return self.update(db, db_obj=user, obj_in=update_data)
    
    def update_quota(self, db: Session, *, user_id: int, quota_amount: float) -> Optional[User]:
        """更新用户论文下载配额"""
        user = self.get(db, id=user_id)
        if not user:
            return None
        
        user.paper_download_quota += quota_amount
        user.updated_at = datetime.now(timezone(timedelta(hours=8)))
        
        db.add(user)
        db.commit()
        db.refresh(user)
        return user

    def add_balance(self, db: Session, *, user: User, amount: float) -> User:
        """增加用户余额"""
        user.balance += amount
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


class CRUDHelpRequest(CRUDBase[HelpRequest, Dict[str, Any], Dict[str, Any]]):
    def get_by_user(self, db: Session, *, user_id: int, skip: int = 0, limit: int = 100) -> List[HelpRequest]:
        """获取用户的帮助请求"""
        return db.query(HelpRequest).filter(HelpRequest.user_id == user_id).order_by(HelpRequest.created_at.desc()).offset(skip).limit(limit).all()
    
    def get_unresolved(self, db: Session, *, skip: int = 0, limit: int = 100) -> List[HelpRequest]:
        """获取未解决的帮助请求"""
        return db.query(HelpRequest).filter(not HelpRequest.is_resolved ).order_by(HelpRequest.created_at.desc()).offset(skip).limit(limit).all()
    
    def create_help_request(self, db: Session, *, user_id: int, title: str, content: str) -> HelpRequest:
        """创建帮助请求"""
        help_request_data = {
            "user_id": user_id,
            "title": title,
            "content": content,
            "is_resolved": False,
            "is_starred": False,
            "created_at": datetime.now(timezone(timedelta(hours=8))),
            "updated_at": datetime.now(timezone(timedelta(hours=8)))
        }
        
        help_request = HelpRequest(**help_request_data)
        db.add(help_request)
        db.commit()
        db.refresh(help_request)
        return help_request
    
    def mark_as_resolved(self, db: Session, *, request_id: int) -> Optional[HelpRequest]:
        """标记帮助请求为已解决"""
        help_request = self.get(db, id=request_id)
        if not help_request:
            return None
        
        help_request.is_resolved = True
        help_request.updated_at = datetime.now(timezone(timedelta(hours=8)))
        
        db.add(help_request)
        db.commit()
        db.refresh(help_request)
        return help_request
    
    def mark_as_starred(self, db: Session, *, request_id: int) -> Optional[HelpRequest]:
        """标记帮助请求为星标"""
        help_request = self.get(db, id=request_id)
        if not help_request:
            return None
        
        help_request.is_starred = True
        help_request.updated_at = datetime.now(timezone(timedelta(hours=8)))
        
        db.add(help_request)
        db.commit()
        db.refresh(help_request)
        return help_request


class CRUDHelpResponse(CRUDBase[HelpResponse, Dict[str, Any], Dict[str, Any]]):
    def get_by_request(self, db: Session, *, request_id: int) -> List[HelpResponse]:
        """获取帮助请求的所有回复"""
        return db.query(HelpResponse).filter(HelpResponse.help_request_id == request_id).order_by(HelpResponse.created_at.asc()).all()
    
    def create_response(self, db: Session, *, request_id: int, responder_id: int, content: str) -> HelpResponse:
        """创建帮助回复"""
        response_data = {
            "help_request_id": request_id,
            "responder_id": responder_id,
            "content": content,
            "created_at": datetime.now(timezone(timedelta(hours=8)))
        }
        
        response = HelpResponse(**response_data)
        db.add(response)
        db.commit()
        db.refresh(response)
        return response


user = CRUDUser(User)
help_request = CRUDHelpRequest(HelpRequest)
help_response = CRUDHelpResponse(HelpResponse)