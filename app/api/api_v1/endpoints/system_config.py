from typing import Any, Dict

from fastapi import APIRouter, Body, Depends
from sqlalchemy.orm import Session

from app import models, crud
from app.api import deps
from app.core.config import settings

router = APIRouter()


@router.get("/get_system_config", response_model=Dict[str, Any])
async def get_system_config(
    db: Session = Depends(deps.get_db),
    current_user: models.user.User= Depends(deps.get_current_active_user), 
) -> Any:
    """获取系统配置"""
    # 检查权限：只有管理员可以查看完整的系统配置
    print("get_system_config called")
    
    is_admin = current_user.role in [models.UserRole.E_ADMIN, models.UserRole.T_ADMIN, models.UserRole.SENIOR_E_ADMIN]
    
    print(current_user)
    
    # 这里假设系统配置存储在数据库中的某个表中

    # 实际应用中可能需要创建一个专门的系统配置表
    
    # 模拟系统配置数据
    config = {
        "system": {
            "name": settings.PROJECT_NAME,
            "version": "1.0.0",
            "maintenance_mode": False,
            "registration_open": True,
        },
        "security": {
            "password_expiry_days": 90,
            "max_login_attempts": 5,
            "session_timeout_minutes": 30,
        },
        "payment": {
            "default_quota": 100,
            "quota_unit_price": 1.0,
        }
    }
    
    # 非管理员只能查看部分配置
    if not is_admin:
        # 移除敏感配置
        if "security" in config:
            del config["security"]
    
    return config


@router.put("/update_system_config", response_model=Dict[str, Any])
async def update_system_config(
    *,
    db: Session = Depends(deps.get_db),
    config_in: Dict[str, Any] = Body(...),
    current_user: models.user.User= Depends(deps.get_current_senior_e_admin),
) -> Any:
    """更新系统配置（需要Senior-E-Admin权限）"""

    # 这里假设系统配置存储在数据库中的某个表中

    # 实际应用中需要实现配置的更新逻辑
    
    # 模拟更新系统配置
    updated_config = config_in
    
    # 记录配置更新日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        log_type=models.LogType.ADMIN_ACTION,
        action="更新系统配置",
        details=f"管理员 {current_user.email} 更新了系统配置"
    )
    
    return updated_config


@router.post("/maintenance-mode", response_model=Dict[str, Any])
async def toggle_maintenance_mode(
    *,
    db: Session = Depends(deps.get_db),
    enable: bool = Body(...),
    current_user: models.user.User= Depends(deps.get_current_senior_e_admin),
) -> Any:
    """切换系统维护模式（需要Senior-E-Admin权限）"""

    # 这里假设系统配置存储在数据库中的某个表中

    # 实际应用中需要实现维护模式的切换逻辑
    
    # 模拟切换维护模式
    maintenance_mode = enable
    
    # 记录维护模式切换日志
    action = "启用" if enable else "禁用"
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        log_type=models.LogType.ADMIN_ACTION,
        action=f"{action}系统维护模式",
        details=f"管理员 {current_user.email} {action}了系统维护模式"
    )
    
    return {
        "maintenance_mode": maintenance_mode,
        "message": f"系统维护模式已{action}"
    }