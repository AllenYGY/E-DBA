from fastapi import APIRouter, Depends, Query, HTTPException, status
from sqlalchemy.orm import Session
from typing import Any, List
from fastapi.encoders import jsonable_encoder
from app.core.config import settings
from app.api.api_v1.endpoints import (
    users, auth, organizations, services, thesis, bank,
    courses, transfer, student_verification, logs,
    policies, system_config, verification
)
from app.api import deps
from app.models.service import ServiceType
from app.crud.service import service as service_crud
from app import models, schemas

api_router = APIRouter()

# 认证相关路由
api_router.include_router(auth.router, prefix="/auth", tags=["Auth"])

# 用户相关路由
api_router.include_router(users.router, prefix="/users", tags=["Users"])

# 组织相关路由
api_router.include_router(organizations.router,
                          prefix="/organizations", tags=["Organizations"])

# 服务相关路由
api_router.include_router(
    services.router, prefix="/services", tags=["Services"])

# 验证相关路由
api_router.include_router(
    verification.router, prefix="/verification", tags=["Verification"])

# 课程相关路由
api_router.include_router(courses.router, prefix="/courses", tags=["Courses"])

# 转账相关路由
api_router.include_router(
    transfer.router, prefix="/transfer", tags=["Transfer"])

# 日志相关路由
api_router.include_router(logs.router, prefix="/logs", tags=["Logs"])

# 政策相关路由
api_router.include_router(
    policies.router, prefix="/policies", tags=["Policies"])

# 系统配置相关路由
api_router.include_router(system_config.router,
                          prefix="/system", tags=["System"])

# 动态加载外部服务路由
def get_service_router(service_type: ServiceType, db: Session = Depends(deps.get_db)):
    service = service_crud.get_by_type(db, service_type=service_type)
    if service and service.external_api_config:
        return service.external_api_config.route_prefix
    return None


# 学生验证相关路由
api_router.include_router(
    student_verification.router,
    prefix="/hw/student",  # 默认前缀，如果数据库中没有配置
    tags=["Student"]
)

# 论文相关路由
api_router.include_router(
    thesis.router,
    prefix="/hw/thesis",  # 使用外部API的路由前缀
    tags=["Thesis"]
)

# 银行相关路由
api_router.include_router(
    bank.router,
    prefix="/hw/bank",  # 使用外部API的路由前缀
    tags=["Bank"]
)
