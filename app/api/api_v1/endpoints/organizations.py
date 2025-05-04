from typing import Any, List
import os

from fastapi import APIRouter, Depends, HTTPException, status, UploadFile, File
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.api import deps
from app.core.config import settings
from datetime import datetime
from app.api.api_v1.endpoints.bank import bank_auth

router = APIRouter()


@router.get("/", response_model=List[schemas.Organization])
async def read_organizations(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_e_admin),
) -> Any:
    """获取组织列表（需要E-Admin权限）"""
    organizations = db.query(models.Organization).offset(skip).limit(limit).all()
    return organizations


class OrganizationCreateWithBank(schemas.OrganizationCreate):
    account_name: str
    account_number: str
    bank: str
    password: str


# @router.post("/register", response_model=schemas.Organization)
# async def create_organization(
#     *,
#     db: Session = Depends(deps.get_db),
#     organization_in: schemas.OrganizationCreate,
#     current_user: models.user.User = Depends(deps.get_current_active_user),
# ) -> Any:
#     """创建新组织（需要O-Convener权限）"""
#     # 检查当前用户是否已经是组织协调人
#     if current_user.role == models.UserRole.O_CONVENER:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="您已经是组织协调人，无法再次创建组织",
#         )
    
#     # 创建组织
#     organization = crud.organization.create_with_convener(
#         db=db,
#         obj_in=organization_in,
#         convener_id=current_user.id
#     )
    
#     # 更新用户的角色为O-Convener
#     crud.user.update(db, db_obj=current_user, obj_in={"role": models.UserRole.O_CONVENER})
    
#     # 更新用户的组织ID
#     crud.user.update(db, db_obj=current_user, obj_in={"organization_id": organization.id})

#     # 关键：刷新 user 对象，获取最新 organization_id
#     db.refresh(current_user)
    
#     # 记录组织创建日志
#     crud.log.create_log(
#         db=db,
#         user_id=current_user.id,
#         organization_id=organization.id,
#         log_type=models.LogType.ORGANIZATION,
#         action="创建组织",
#         details=f"用户 {current_user.email} 创建了组织 {organization.name}"
#     )
    
#     return organization


@router.get("/my-organization", response_model=schemas.Organization)
async def read_my_organization(
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """获取当前用户所属组织信息"""
    if not current_user.organization_id:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="您不属于任何组织",
        )
    organization = db.query(models.Organization).filter(models.Organization.id == current_user.organization_id).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="组织不存在，无法获得组织信息",
        )
    return organization


@router.get("/{organization_id}", response_model=schemas.Organization)
async def read_organization(
    organization_id: int,
    db: Session = Depends(deps.get_db),
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """根据ID获取组织信息"""
    organization = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="组织不存在 ",
        )
    
    # 检查权限：只有组织成员、组织协调人或管理员可以查看组织信息
    if current_user.organization_id != organization_id and current_user.role not in [
        models.UserRole.E_ADMIN, models.UserRole.T_ADMIN, models.UserRole.SENIOR_E_ADMIN
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，无法查看其他组织信息",
        )
    
    return organization


@router.put("/{organization_id}", response_model=schemas.Organization)
async def update_organization(
    *,
    db: Session = Depends(deps.get_db),
    organization_id: int,
    organization_in: schemas.OrganizationUpdate,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """更新组织信息"""
    organization = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="组织不存在 ",
        )
    
    # 检查权限：只有组织协调人或管理员可以更新组织信息
    is_admin = current_user.role in [models.UserRole.E_ADMIN, models.UserRole.T_ADMIN, models.UserRole.SENIOR_E_ADMIN]
    is_convener = current_user.id == organization.convener_id
    
    if not (is_admin or is_convener):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，只有组织协调人或管理员可以更新组织信息",
        )
    
    # 管理员可以更新所有字段，协调人只能更新基本信息
    if not is_admin:
        # 移除协调人无权更新的字段
        if hasattr(organization_in, "is_verified"):
            delattr(organization_in, "is_verified")
        if hasattr(organization_in, "is_active"):
            delattr(organization_in, "is_active")
        if hasattr(organization_in, "convener_id"):
            delattr(organization_in, "convener_id")
    
    organization = crud.organization.update(db, db_obj=organization, obj_in=organization_in)
    
    # 记录组织更新日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=organization.id,
        log_type=models.LogType.ORGANIZATION,
        action="更新组织信息",
        details=f"用户 {current_user.email} 更新了组织 {organization.name} 的信息"
    )
    
    return organization


@router.post("/{organization_id}/upload-verification", response_model=schemas.Organization)
async def upload_verification_document(
    *,
    db: Session = Depends(deps.get_db),
    organization_id: int,
    file: UploadFile = File(...),
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """上传组织验证文件"""
    organization = crud.organization.get(db, id=organization_id)
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="组织不存在",
        )
    
    # 检查权限：只有组织协调人或管理员可以上传验证文件
    if current_user.id != organization.convener_id and current_user.role not in [
        models.UserRole.E_ADMIN, models.UserRole.SENIOR_E_ADMIN, models.UserRole.T_ADMIN
    ]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，无法上传验证文件",
        )
    
    # 检查文件类型
    if not file.filename.endswith(".pdf"):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="只支持PDF格式的文件",
        )
    
    # 生成文件存储路径
    file_path = f"uploads/verification/{organization_id}_{file.filename}"
    
    # 自动创建目录
    os.makedirs(os.path.dirname(file_path), exist_ok=True)

    try:
        with open(file_path, "wb") as f:
            content = await file.read()
            f.write(content)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"文件保存失败: {str(e)}",
        )
    
    # 更新组织验证文件路径
    organization = crud.organization.update(
        db,
        db_obj=organization,
        obj_in={"verification_document": file_path}
    )
    
    # 创建或更新验证状态记录
    verification_status = crud.verification_status.get_by_organization(db, organization_id=organization_id)
    if not verification_status:
        verification_status = crud.verification_status.create_verification_status(db, organization_id=organization_id)
    
    # 记录文件上传日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=organization.id,
        log_type=models.LogType.ORGANIZATION,
        action="上传验证文件",
        details=f"用户 {current_user.email} 为组织 {organization.name} 上传了验证文件"
    )
    
    return organization


@router.get("/{organization_id}/members", response_model=List[schemas.User])
async def read_organization_members(
    organization_id: int,
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: models.user.User = Depends(deps.get_current_active_user),
) -> Any:
    """获取组织成员列表"""
    organization = db.query(models.Organization).filter(models.Organization.id == organization_id).first()
    if not organization:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="组织不存在",
        )
    
    # 检查权限：只有组织成员、组织协调人或管理员可以查看组织成员
    is_admin = current_user.role in [models.UserRole.E_ADMIN, models.UserRole.T_ADMIN, models.UserRole.SENIOR_E_ADMIN]
    is_member = current_user.organization_id == organization_id
    is_convener = current_user.id == organization.convener_id
    
    if not (is_admin or is_member or is_convener):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，无法查看组织成员",
        )
    
    members = db.query(models.User).filter(models.User.organization_id == organization_id).offset(skip).limit(limit).all()
    return members