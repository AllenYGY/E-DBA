from typing import Optional, Dict, Any
from datetime import datetime, timezone, timedelta

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.service import ExternalApiConfig
from app.schemas.service import ExternalApiConfigCreate, ExternalApiConfigUpdate

tz_utc_8 = timezone(timedelta(hours=8))

class CRUDExternalApiConfig(CRUDBase[ExternalApiConfig, ExternalApiConfigCreate, ExternalApiConfigUpdate]):
    def get_by_service(self, db: Session, *, service_id: int) -> Optional[ExternalApiConfig]:
        """根据服务ID获取外部API配置"""
        return db.query(ExternalApiConfig).filter(ExternalApiConfig.service_id == service_id).first()

    def create_with_service(
        self, db: Session, *, service_id: int, obj_in: Dict[str, Any]
    ) -> ExternalApiConfig:
        """为服务创建外部API配置"""
        db_obj = ExternalApiConfig(
            service_id=service_id,
            base_url=obj_in["base_url"],
            path=obj_in["path"],
            method=obj_in["method"],
            input_format=obj_in.get("input_format"),
            output_format=obj_in.get("output_format"),
            created_at=datetime.now(tz_utc_8),
            updated_at=datetime.now(tz_utc_8),
            service_type=obj_in.get("service_type")
        )
        db.add(db_obj)
        db.commit()
        db.refresh(db_obj)
        return db_obj

    def update(
        self, db: Session, *, db_obj: ExternalApiConfig, obj_in: Dict[str, Any]
    ) -> ExternalApiConfig:
        """更新外部API配置"""
        if isinstance(obj_in, dict):
            update_data = obj_in
        else:
            update_data = obj_in.dict(exclude_unset=True)
        
        # 更新时间戳
        update_data["updated_at"] = datetime.now(tz_utc_8)
        
        return super().update(db, db_obj=db_obj, obj_in=update_data)

external_api_config = CRUDExternalApiConfig(ExternalApiConfig) 