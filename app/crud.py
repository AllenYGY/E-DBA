from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.db.session import Base

ModelType = TypeVar("ModelType", bound=Base)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseModel)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseModel)


class CRUDBase(Generic[ModelType, CreateSchemaType, UpdateSchemaType]):
    def __init__(self, model: Type[ModelType]):
        """
        CRUD对象与SQLAlchemy模型类一起使用
        :param model: SQLAlchemy模型类
        """
        self.model = model

    def get(self, db: Session, id: Any) -> Optional[ModelType]:
        """
        通过ID获取对象
        """
        return db.query(self.model).filter(self.model.id == id).first()

    def get_multi(
        self, db: Session, *, skip: int = 0, limit: int = 100
    ) -> List[ModelType]:
        """
        获取多个对象
        """
        return db.query(self.model).offset(skip).limit(limit).all()

    def create(self, db: Session, *, obj_in: CreateSchemaType) -> ModelType:
        """
        创建对象
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = self.model(**obj_in_data)  # type: ignore
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self,
        db: Session,
        *,
        db_obj: ModelType,
        obj_in: Union[UpdateSchemaType, Dict[str, Any]]
    ) -> ModelType:
        """
        更新对象
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def remove(self, db: Session, *, id: int) -> ModelType:
        """
        删除对象
        """
        obj = db.query(self.model).get(id)
        db.delete(obj)
        db.commit()
        return obj


# 导入具体的CRUD实现
from app.models.user import User, HelpRequest, HelpResponse
from app.models.organization import Organization, PaymentAccount
from app.models.verification import VerificationStatus
from app.models.log import Log, LogType
from app.schemas import UserCreate, UserUpdate
from app.core.security import get_password_hash, verify_password


class CRUDUser(CRUDBase[User, UserCreate, UserUpdate]):
    def get_by_email(self, db: Session, *, email: str) -> Optional[User]:
        """
        通过邮箱获取用户
        """
        return db.query(User).filter(User.email == email).first()

    def create(self, db: Session, *, obj_in: UserCreate) -> User:
        """
        创建新用户
        """
        db_obj = User(
            email=obj_in.email,
            hashed_password=get_password_hash(obj_in.password),
            username=obj_in.username,
            role=obj_in.role,
            permission_level=obj_in.permission_level,
            is_active=obj_in.is_active,
            paper_download_quota=0.0,
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def authenticate(self, db: Session, *, email: str, password: str) -> Optional[User]:
        """
        验证用户
        """
        user = self.get_by_email(db, email=email)
        if not user:
            return None
        if not verify_password(password, user.hashed_password):
            return None
        return user


class CRUDOrganization(CRUDBase[Organization, Any, Any]):
    def create_with_convener(self, db: Session, *, obj_in: Any, convener_id: int) -> Organization:
        """
        创建组织并关联协调人
        """
        obj_in_data = jsonable_encoder(obj_in)
        db_obj = Organization(**obj_in_data, convener_id=convener_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def create_verification_status(self, db: Session, *, organization_id: int) -> VerificationStatus:
        """
        创建组织验证状态记录
        """
        db_obj = VerificationStatus(organization_id=organization_id)
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update_verification_status(
        self,
        db: Session,
        *,
        db_obj: VerificationStatus,
        obj_in: Union[Dict[str, Any], Any]
    ) -> VerificationStatus:
        """
        更新组织验证状态
        """
        obj_data = jsonable_encoder(db_obj)
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        for field in obj_data:
            if field in update_data:
                setattr(db_obj, field, update_data[field])
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def get_by_convener(self, db: Session, *, convener_id: int) -> Optional[Organization]:
        """
        通过协调人ID获取组织
        """
        return db.query(Organization).filter(Organization.convener_id == convener_id).first()


class CRUDLog:
    def create_log(self, db: Session, *, user_id: int, log_type: LogType, action: str, details: str, organization_id: Optional[int] = None) -> Log:
        """
        创建日志记录
        """
        db_obj = Log(
            user_id=user_id,
            organization_id=organization_id,
            log_type=log_type,
            action=action,
            details=details
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj


# 实例化CRUD对象
user = CRUDUser(User)
organization = CRUDOrganization(Organization)
log = CRUDLog()