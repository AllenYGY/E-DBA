from typing import Any, List

from fastapi import APIRouter, Body, Depends, HTTPException, status
from fastapi.encoders import jsonable_encoder
from sqlalchemy.orm import Session

from app import schemas, crud
from app.api import deps
from app.core.config import settings
from app.models.user import UserRole
from app.models import User
from app.models.log import LogType

router = APIRouter()

ROLE_LEVEL = {
    "T_ADMIN": 3,
    "SENIOR_E_ADMIN": 2,
    "E_ADMIN": 1,
    "O_CONVENER": 0,
    "DATA_USER": 0,
}

def can_create(creator_role, target_role):
    if creator_role == "T_ADMIN":
        return True
    if creator_role == "SENIOR_E_ADMIN":
        return target_role in ["E_ADMIN", "O_CONVENER", "DATA_USER"]
    if creator_role == "E_ADMIN":
        return target_role in ["O_CONVENER", "DATA_USER"]
    return False

@router.get("/", response_model=List[schemas.User])
async def read_users(
    db: Session = Depends(deps.get_db),
    skip: int = 0,
    limit: int = 100,
    current_user: User = Depends(deps.get_current_e_admin),
) -> Any:
    """获取用户列表（需要E-Admin权限）"""
    users = crud.user.get_multi(db, skip=skip, limit=limit)
    return users


# @router.post("/", response_model=schemas.User)
# async def create_user(
#     *,
#     db: Session = Depends(deps.get_db),
#     user_in: schemas.UserCreate,
#     current_user: User = Depends(deps.get_current_e_admin),
# ) -> Any:
#     """创建新用户（需要E-Admin权限）"""
#     user = crud.user.get_by_email(db, email=user_in.email)
#     if user:
#         raise HTTPException(
#             status_code=status.HTTP_400_BAD_REQUEST,
#             detail="该邮箱已被注册",
#         )
#     target_role = user_in.role if isinstance(user_in.role, str) else user_in.role.value
#     creator_role = current_user.role if isinstance(current_user.role, str) else current_user.role.value
#     if not can_create(creator_role, target_role):
#         raise HTTPException(
#             status_code=status.HTTP_403_FORBIDDEN,
#             detail=f"{creator_role} 无权创建 {target_role} 用户",
#         )
#     user = crud.user.create(db, obj_in=user_in)
    
#     # 记录用户创建日志
#     crud.log.create_log(
#         db=db,
#         user_id=current_user.id,
#         log_type=LogType.SYSTEM,
#         action="创建用户",
#         details=f"管理员 {current_user.email} 创建了用户 {user.email}"
#     )
#     return user


@router.get("/me", response_model=schemas.User)
async def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """获取当前登录用户信息"""
    return current_user


@router.put("/me", response_model=schemas.User)
async def update_user_me(
    *,
    db: Session = Depends(deps.get_db),
    password: str = Body(None),
    username: str = Body(None),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    """更新当前登录用户信息"""
    current_user_data = jsonable_encoder(current_user)
    user_in = schemas.UserUpdate(**current_user_data)
    
    print(user_in.password,user_in.username)
    if password is not None:
        user_in.password = password
    if username is not None:
        user_in.username = username
    user = crud.user.update(db, db_obj=current_user, obj_in=user_in)
    
    # 记录用户更新日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        log_type=LogType.SYSTEM,
        action="更新个人信息",
        details=f"用户 {user.email} 更新了个人信息"
    )
    
    return user


@router.get("/{user_id}", response_model=schemas.User)
async def read_user_by_id(
    user_id: int,
    current_user: User = Depends(deps.get_current_active_user),
    db: Session = Depends(deps.get_db),
) -> Any:
    """根据ID获取用户信息"""
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在"
        )
    if user == current_user:
        return user
    if current_user.role not in [UserRole.E_ADMIN, UserRole.T_ADMIN, UserRole.SENIOR_E_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，无法访问其他用户信息",
        )
    
    # 记录查看用户信息的日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        log_type=LogType.SYSTEM,
        action="查看用户信息",
        details=f"管理员 {current_user.email} 查看了用户 {user.email} 的信息"
    )
    
    return user

@router.put("/{user_id}", response_model=schemas.User)
async def update_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    user_in: schemas.UserUpdate,
    current_user: User = Depends(deps.get_current_e_admin),
) -> Any:
    """更新用户信息（需要E-Admin权限）"""
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在, 无法更新",
        )
    user = crud.user.update(db, db_obj=user, obj_in=user_in)
    
    # 记录用户更新日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        log_type=LogType.SYSTEM,
        action="更新用户信息",
        details=f"管理员 {current_user.email} 更新了用户 {user.email} 的信息"
    )
    
    return user


@router.delete("/{user_id}", response_model=schemas.User)
async def delete_user(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    current_user: User = Depends(deps.get_current_t_admin),
) -> Any:
    """删除用户（需要T-Admin权限）"""
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在，无法删除",
        )
    if user.id == current_user.id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="不能删除自己的账户",
        )
    user = crud.user.remove(db, id=user_id)
    
    # 记录用户删除日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        log_type=LogType.SYSTEM,
        action="删除用户",
        details=f"管理员 {current_user.email} 删除了用户 {user.email}"
    )
    
    return user


@router.post("/add-quota/{user_id}", response_model=schemas.User)
async def add_paper_download_quota(
    *,
    db: Session = Depends(deps.get_db),
    user_id: int,
    amount: float = Body(..., embed=True),
    current_user: User = Depends(deps.get_current_e_admin),
) -> Any:
    """为用户增加论文下载配额（需要E-Admin权限）"""
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    if amount <= 0:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="增加的配额必须大于0",
        )
    
    # 更新用户配额
    new_quota = user.balance + amount
    user = crud.user.update(db, db_obj=user, obj_in={"balance": new_quota})
    
    # 记录配额增加日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        log_type=LogType.SYSTEM,
        action="增加下载配额",
        details=f"管理员 {current_user.email} 为用户 {user.email} 增加了 {amount} 元下载配额"
    )
    
    return user

@router.post("/{user_id}/add_balance", response_model=dict)
async def add_balance(
    user_id: int,
    *,
    db: Session = Depends(deps.get_db),
    amount: float = Body(...),
    current_user: User = Depends(deps.get_current_e_admin),
) -> Any:
    """增加用户余额（需要E-Admin权限）"""
    user = crud.user.get(db, id=user_id)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="用户不存在",
        )
    
    # 增加用户余额
    new_balance = user.balance + amount
    user = crud.user.update(db, db_obj=user, obj_in={"balance": new_balance})
    
    # 记录日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        log_type=LogType.PAYMENT,
        action="增加用户余额",
        details=f"管理员 {current_user.email} 为用户 {user.email} 增加了 {amount} 元余额，当前余额：{user.balance} 元"
    )
    
    return {
        "message": "增加用户余额成功",
        "user_id": user.id,
        "amount": amount,
        "current_balance": user.balance
    }