from typing import Any, List
from datetime import datetime
from sqlalchemy import or_

from fastapi import APIRouter, Depends, HTTPException, status, Query
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import models
from app.api import deps
from app.schemas.log import LogListResponse

router = APIRouter()


@router.get("/", response_model=LogListResponse)
async def read_logs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    log_type: str = Query(None, description="Log Type"),
    user_id: int = Query(None, description="User ID"),
    organization_id: int = Query(None, description="Organization ID"),
    search: str = Query(None, description="Search keyword for action or details"),
    start_date: str = Query(None, description="Start Date (YYYY-MM-DD)"),
    end_date: str = Query(None, description="End Date (YYYY-MM-DD)"),
    current_user: models.user.User = Depends(deps.get_current_e_admin),
) -> Any:
    """获取系统日志（需要E-Admin权限）"""
    # 构建查询
    query = db.query(models.Log)
    
    # 应用过滤条件
    if log_type:
        query = query.filter(models.Log.log_type == log_type)
    
    if user_id:
        query = query.filter(models.Log.user_id == user_id)
    
    if organization_id:
        query = query.filter(models.Log.organization_id == organization_id)
    
    if search:
        query = query.filter(
            or_(
                models.Log.action.ilike(f"%{search}%"),
                models.Log.details.ilike(f"%{search}%")
            )
        )
    
    if start_date:
        try:
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(models.Log.created_at >= start_datetime)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="开始日期格式无效，请使用YYYY-MM-DD格式",
            )
    
    if end_date:
        try:
            end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
            # 设置为当天的结束时间
            end_datetime = end_datetime.replace(hour=23, minute=59, second=59)
            query = query.filter(models.Log.created_at <= end_datetime)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="结束日期格式无效，请使用YYYY-MM-DD格式",
            )
    
    # 统计总数（在分页前！）
    total = query.count()
    
    # 排序和分页
    query = query.order_by(models.Log.created_at.desc())
    logs = query.offset(skip).limit(limit).all()
    
    # 转换为字典列表，包含用户和组织信息
    result = []
    for log in logs:
        log_data = jsonable_encoder(log)
        
        # 添加用户信息
        if log.user_id:
            user = db.query(models.User).filter(models.User.id == log.user_id).first()
            log_data["user_email"] = user.email if user else None
        
        # 添加组织信息
        if log.organization_id:
            organization = db.query(models.Organization).filter(models.Organization.id == log.organization_id).first()
            log_data["organization_name"] = organization.name if organization else None
        
        result.append(log_data)
    
    return LogListResponse(items=result, total=total)


@router.get("/my-logs", response_model=List[dict])
async def read_my_logs(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    log_type: str = Query(None, description="日志类型"),
    start_date: str = Query(None, description="开始日期 (YYYY-MM-DD)"),
    end_date: str = Query(None, description="结束日期 (YYYY-MM-DD)"),
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """获取当前用户的日志"""
    # 构建查询
    query = db.query(models.Log).filter(models.Log.user_id == current_user.id)
    
    # 应用过滤条件
    if log_type:
        query = query.filter(models.Log.log_type == log_type)
    
    if start_date:
        try:
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(models.Log.created_at >= start_datetime)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="开始日期格式无效，请使用YYYY-MM-DD格式",
            )
    
    if end_date:
        try:
            end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
            # 设置为当天的结束时间
            end_datetime = end_datetime.replace(hour=23, minute=59, second=59)
            query = query.filter(models.Log.created_at <= end_datetime)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="结束日期格式无效，请使用YYYY-MM-DD格式",
            )
    
    # 按时间倒序排序
    query = query.order_by(models.Log.created_at.desc())
    
    # 执行查询
    logs = query.offset(skip).limit(limit).all()
    
    # 转换为字典列表
    result = [jsonable_encoder(log) for log in logs]
    
    return result


@router.get("/organization/{organization_id}", response_model=List[dict])
async def read_organization_logs(
    organization_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    log_type: str = Query(None, description="日志类型"),
    start_date: str = Query(None, description="开始日期 (YYYY-MM-DD)"),
    end_date: str = Query(None, description="结束日期 (YYYY-MM-DD)"),
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """获取组织的日志"""
    # 检查组织是否存在
    organization = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="组织不存在",
        )
    
    # 检查权限：只有组织成员、组织协调人或管理员可以查看组织的日志
    is_admin = current_user.role in [models.UserRole.E_ADMIN, models.UserRole.T_ADMIN, models.UserRole.SENIOR_E_ADMIN]
    is_member = current_user.organization_id == organization_id
    is_convener = current_user.id == organization.convener_id
    
    if not (is_admin or is_member or is_convener):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，无法查看组织的日志",
        )
    
    # 构建查询
    query = db.query(models.Log).filter(models.Log.organization_id == organization_id)
    
    # 应用过滤条件
    if log_type:
        query = query.filter(models.Log.log_type == log_type)
    
    if start_date:
        try:
            start_datetime = datetime.strptime(start_date, "%Y-%m-%d")
            query = query.filter(models.Log.created_at >= start_datetime)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="开始日期格式无效，请使用YYYY-MM-DD格式",
            )
    
    if end_date:
        try:
            end_datetime = datetime.strptime(end_date, "%Y-%m-%d")
            # 设置为当天的结束时间
            end_datetime = end_datetime.replace(hour=23, minute=59, second=59)
            query = query.filter(models.Log.created_at <= end_datetime)
        except ValueError:
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="结束日期格式无效，请使用YYYY-MM-DD格式",
            )
    
    # 按时间倒序排序
    query = query.order_by(models.Log.created_at.desc())
    
    # 执行查询
    logs = query.offset(skip).limit(limit).all()
    
    # 转换为字典列表，包含用户信息
    result = []
    for log in logs:
        log_data = jsonable_encoder(log)
        
        # 添加用户信息
        if log.user_id:
            user = db.query(models.User).filter(models.User.id == log.user_id).first()
            log_data["user_email"] = user.email if user else None
        
        result.append(log_data)
    
    return result