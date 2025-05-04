from typing import Any, Dict, List, Optional, Union

from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.models.system_config import SystemConfig


class CRUDSystemConfig(CRUDBase[SystemConfig, Dict[str, Any], Dict[str, Any]]):
    def get_by_key(self, db: Session, *, key: str) -> Optional[SystemConfig]:
        """根据键名获取配置"""
        return db.query(SystemConfig).filter(SystemConfig.key == key).first()
    
    def get_public_configs(self, db: Session) -> List[SystemConfig]:
        """获取所有公开配置"""
        return db.query(SystemConfig).filter(SystemConfig.is_public == True).all()
    
    def get_all_configs(self, db: Session) -> List[SystemConfig]:
        """获取所有配置（包括非公开配置）"""
        return db.query(SystemConfig).all()
    
    def upsert(self, db: Session, *, key: str, value: Any, description: Optional[str] = None, 
               is_public: bool = True, updated_by: Optional[int] = None) -> SystemConfig:
        """更新或插入配置"""
        config = self.get_by_key(db, key=key)
        if config:
            # 更新现有配置
            update_data = {"value": value}
            if description is not None:
                update_data["description"] = description
            if is_public is not None:
                update_data["is_public"] = is_public
            if updated_by is not None:
                update_data["updated_by"] = updated_by
            
            return self.update(db, db_obj=config, obj_in=update_data)
        else:
            # 创建新配置
            config_data = {
                "key": key,
                "value": value,
                "description": description,
                "is_public": is_public,
                "updated_by": updated_by
            }
            return self.create(db, obj_in=config_data)


system_config = CRUDSystemConfig(SystemConfig)