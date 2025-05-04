from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session

from app import schemas, crud
from app.models import user
from app.models.log import LogType
from app.api import deps
from app.core import security
from app.core.config import settings
from app.utils import verify_email
from app.models.user import UserRole
from app.models.enums import PermissionLevel
from app.api.api_v1.endpoints.bank import bank_auth
from app.models.payment import PaymentType

router = APIRouter()


@router.post("/login", response_model=schemas.Token)
async def login_access_token(
    db: Session = Depends(deps.get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    """
    获取访问令牌，用于用户登录

    使用OAuth2密码流进行身份验证:
    - **username**: 用户邮箱
    - **password**: 用户密码
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="邮箱或密码不正确",
        )
    elif not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="用户未激活",
        )
    
    # 记录登录日志
    crud.log.create_log(
        db=db,
        user_id=user.id,
        organization_id=user.organization_id,
        log_type=LogType.LOGIN,
        action="用户登录",
        details=f"用户 {user.email} 登录系统"
    )
    
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }


@router.post("/register", response_model=schemas.User)
async def register_user(
    *,
    db: Session = Depends(deps.get_db),
    user_in: schemas.UserCreate,
    current_user: user.User = Depends(deps.get_current_active_user),
) -> Any:
    """
    注册新用户（需要O-Convener权限）
    """
    # 只允许 O-Convener
    if current_user.role != UserRole.O_CONVENER:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="只有组织协调人(O-Convener)可以注册新用户",
        )
    
    # 检查权限级别是否有效
    if user_in.permission_level not in [level.value for level in PermissionLevel]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="无效的权限级别",
        )
    
    # 检查邮箱是否已存在
    existing_user = crud.user.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="该邮箱已被注册",
        )
    
    # 验证邮箱格式
    if not verify_email(user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="邮箱格式不正确",
        )
    
    # 创建新的 UserCreate 对象，包含所需的所有字段
    new_user = schemas.UserCreate(
        email=user_in.email,
        password=user_in.password,
        username=user_in.username,
        permission_level=user_in.permission_level,
        role=UserRole.DATA_USER,
        organization_id=current_user.organization_id,
        balance=user_in.balance
    )
    
    # 创建用户
    user = crud.user.create(db, obj_in=new_user)
    
    # 记录日志
    crud.log.create_log(
        db=db,
        user_id=current_user.id,
        organization_id=current_user.organization_id,
        log_type=LogType.SYSTEM,
        action="注册新用户",
        details=f"组织协调人 {current_user.email} 注册了新用户 {user.email}，权限级别：{user.permission_level}"
    )
    return user


@router.post("/register-o-convener", response_model=schemas.User)
async def register_o_convener(
    *,
    db: Session = Depends(deps.get_db),
    register_data: schemas.OConvenerRegisterRequest,
) -> Any:
    """
    Register new o-convener.
    """
    # 检查邮箱是否已存在
    existing_user = crud.user.get_by_email(db, email=register_data.email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="The email is already registered.",
        )
    
    # 检查组织名称是否已存在
    organization = crud.organization.get_by_name(db, name=register_data.name)
    if organization:
        raise HTTPException(
            status_code=400,
            detail="The organization with this name already exists in the system.",
        )
    
    # 验证银行账户信息
    bank_auth_result = await bank_auth(register_data.bank_account, db)
    if not bank_auth_result["success"]:
        raise HTTPException(
            status_code=400,
            detail=bank_auth_result["message"],
        )
    
    print("Successfully authenticated bank account")
    
    # 创建用户
    user_in = schemas.UserCreate(
        email=register_data.email,
        password=register_data.password,
        username=register_data.username,
        role=UserRole.O_CONVENER,
        permission_level=register_data.permission_level,
        balance=10000.0
    )
    user = crud.user.create(db, obj_in=user_in)
    
    # 创建组织
    organization_in = schemas.OrganizationCreate(
        name=register_data.name,
        description=register_data.description,
        email_domain=register_data.email_domain,
        verification_document=register_data.verification_document
    )
    organization = crud.organization.create_with_convener(
        db=db,
        obj_in=organization_in,
        convener_id=user.id
    )
    
    # 更新用户的组织ID
    user = crud.user.update(
        db,
        db_obj=user,
        obj_in={
            "organization_id": organization.id
        }
    )

    # # 创建初始支付账户
    # payment = crud.payment.create_payment(
    #     db,
    #     organization_id=organization.id,
    #     payment_type=PaymentType.TRANSFER,
    #     account_name=register_data.bank_account.account_name,
    #     account_number=register_data.bank_account.account_number,
    #     password=register_data.bank_account.password,
    #     bank=register_data.bank_account.bank
    # )

    # # 记录日志
    # crud.log.create_log(
    #     db=db,
    #     user_id=user.id,
    #     organization_id=organization.id,
    #     log_type=LogType.SYSTEM,
    #     action="创建初始支付账户",
    #     details=f"组织协调人 {user.email} 创建了初始支付账户 {payment.id}"
    # )

    return user



@router.get("/test-token", response_model=schemas.User)
async def test_token(current_user: user.User = Depends(deps.get_current_user)) -> Any:
    """测试访问令牌, 需要登录"""
    return current_user