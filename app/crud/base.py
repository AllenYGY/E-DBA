from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union
from datetime import datetime, timezone, timedelta

from fastapi.encoders import jsonable_encoder
from pydantic import BaseModel, Field
from sqlalchemy.orm import Session

from app.db.session import Base

ModelType = TypeVar("ModelType", bound=Base)  # type: ignore
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
        通过ID获取对象（不包括已删除的对象）
        """
        return db.query(self.model).filter(
            self.model.id == id,
            self.model.is_deleted == False
            
        ).first()

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
        print(f"Updating object of type {type(db_obj)}")
        print(f"Update data: {obj_in}")
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        print(f"Processed update data: {update_data}")
        for field, value in update_data.items():
            print(f"Setting {field} = {value}")
            setattr(db_obj, field, value)
        try:
            db.add(db_obj)
            print("Added to session")
            db.commit()
            print("Committed")
            db.refresh(db_obj)
            print("Refreshed")
            return db_obj
        except Exception as e:
            print(f"Error in update: {str(e)}")
            print(f"Error type: {type(e)}")
            import traceback
            print(f"Traceback: {traceback.format_exc()}")
            db.rollback()
            raise

    def remove(self, db: Session, *, id: int) -> Optional[ModelType]:
        """
        软删除对象
        """
        obj = db.query(self.model).get(id)
        if obj:
            if hasattr(obj, 'is_deleted'):
                obj.is_deleted = True
                if hasattr(obj, 'deleted_at'):
                    obj.deleted_at = datetime.now(timezone(timedelta(hours=8)))
                db.add(obj)
                db.commit()
                db.refresh(obj)
            else:
                # 如果模型没有软删除字段，则执行物理删除
                db.delete(obj)
                db.commit()
        return obj