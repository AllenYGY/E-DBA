from datetime import timedelta
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, File, Form, UploadFile, BackgroundTasks
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
import base64
import random
import string

from app import schemas, crud
from app.models import user
from app.models.log import LogType
from app.api import deps
from app.core import security
from app.core.config import settings
from app.utils import verify_email, extract_email_domain
from app.models.user import UserRole
from app.models.enums import PermissionLevel
from app.core.email import send_email
from app.core.cache import (
    set_email_code, get_email_code, can_send_code,
    record_send_code, record_attempt
)

router = APIRouter()

async def auto_register_user_by_domain(db: Session, email: str, password: str = None) -> Any:
    """
    根据邮箱域名自动注册用户
    如果邮箱域名匹配某个组织的域名，则创建新用户
    """
    domain = extract_email_domain(email)
    if not domain:
        return None
    
    # 查找匹配域名的组织
    organization = crud.organization.get_by_email_domain(db, email_domain=domain)
    if not organization:
        return None
    
    # 生成随机密码（如果未提供密码）
    if not password:
        password = ''.join(random.choices(string.ascii_letters + string.digits, k=12))
    
    # 创建新用户
    username = email.split('@')[0]  # 使用邮箱前缀作为用户名
    user_in = schemas.UserCreate(
        email=email,
        password=password,
        username=username,
        permission_level=PermissionLevel.PUBLIC_DATA.value,
        role=UserRole.DATA_USER,
        organization_id=organization.id,
        balance=1000.0
    )
    
    try:
        user = crud.user.create(db, obj_in=user_in)
        
        # 记录日志
        crud.log.create_log(
            db=db,
            user_id=user.id,
            organization_id=organization.id,
            log_type=LogType.SYSTEM,
            action="Auto register user",
            details=f"Auto registered user {user.email} for organization {organization.name} based on email domain"
        )
        
        return user
    except Exception as e:
        print(f"Error auto registering user: {str(e)}")
        return None

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
    
    如果用户不存在但邮箱域名匹配某个组织，将自动创建新用户
    """
    user = crud.user.authenticate(
        db, email=form_data.username, password=form_data.password
    )
    
    # 如果用户不存在，尝试自动注册
    if not user:
        # 先检查邮箱是否存在（不需要密码验证）
        existing_user = crud.user.get_by_email(db, email=form_data.username)
        if not existing_user:
            # 尝试自动注册
            user = await auto_register_user_by_domain(db, form_data.username, form_data.password)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Invalid email or password",
                )
        else:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Invalid email or password",
            )
    
    if not user.is_active:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User is not active",
        )
    
    # 记录登录日志
    crud.log.create_log(
        db=db,
        user_id=user.id,
        organization_id=user.organization_id,
        log_type=LogType.LOGIN,
        action="User login",
        details=f"User {user.email} logged in"
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
            detail="Only O-Convener can register new users",
        )
    
    # 检查权限级别是否有效
    if user_in.permission_level not in [level.value for level in PermissionLevel]:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid permission level",
        )
    
    # 检查邮箱是否已存在
    existing_user = crud.user.get_by_email(db, email=user_in.email)
    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="The email is already registered.",
        )
    
    # 验证邮箱格式
    if not verify_email(user_in.email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format",
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
        action="Create new user",
        details=f"O-Convener {current_user.email} created a new user {user.email}, permission level: {user.permission_level}"
    )
    return user


@router.post("/register-o-convener", response_model=schemas.User)
async def register_o_convener(
    *,
    db: Session = Depends(deps.get_db),
    username: str = Form("organizer", description="User name"),
    email: str = Form("organizer@example.com", description="User email"),
    password: str = Form("strongpassword123", description="User password"),
    name: str = Form("Example Organization", description="Organization name"),
    full_name: str = Form("This is an example organization", description="Organization full name"),
    email_domain: str = Form("example.com", description="Organization email domain"),
    verification_document: UploadFile = File(..., description="Organization verification document"),
) -> Any:
    """
    Register new o-convener (with file upload).
    """
    # check if the email is already registered
    existing_user = crud.user.get_by_email(db, email=email)
    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="The email is already registered.",
        )
    
    # check if the organization name is already registered
    organization = crud.organization.get_by_name(db, name=name)
    if organization:
        raise HTTPException(
            status_code=400,
            detail="The organization with this name already exists in the system.",
        )
    
    # process the file (e.g. store it in the database or file system)
    file_content = await verification_document.read()
    mime_type = verification_document.content_type
    base64_str = base64.b64encode(file_content).decode('utf-8')
    file_content_str = f"data:{mime_type};base64,{base64_str}"

    user_in = schemas.UserCreate(
        email=email,
        password=password,
        username=username,
        role=UserRole.O_CONVENER,
        permission_level=3,
        balance=1000.0
    )
    user = crud.user.create(db, obj_in=user_in)
    
    organization_in = schemas.OrganizationCreate(
        name=name,
        full_name=full_name,
        email_domain=email_domain,
        verification_document=file_content_str  # save as string
    )
    organization = crud.organization.create_with_convener(
        db=db,
        obj_in=organization_in,
        convener_id=user.id
    )
    
    user = crud.user.update(
        db,
        db_obj=user,
        obj_in={
            "organization_id": organization.id
        }
    )

    # create verification record
    crud.verification_status.create_verification_status(db, organization_id=organization.id)

    # create log
    crud.log.create_log(
        db=db,
        user_id=user.id,
        organization_id=organization.id,
        log_type=LogType.SYSTEM,
        action="Register O-Convener and organization",
        details=f"O-Convener {user.email} registered organization {organization.name}"
    )

    return user


@router.get("/test-token", response_model=schemas.User)
async def test_token(current_user: user.User = Depends(deps.get_current_user)) -> Any:
    """测试访问令牌, 需要登录"""
    return current_user


@router.post("/send-email-code")
async def send_email_code(
    email: str,
    background_tasks: BackgroundTasks,
    db: Session = Depends(deps.get_db)
):
    """
    发送邮箱验证码
    """
    # 检查邮箱格式
    if not verify_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    
    # 检查用户是否存在
    user = crud.user.get_by_email(db, email=email)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="User not found"
        )
    
    # 检查是否可以发送验证码
    can_send, reason = can_send_code(email)
    if not can_send:
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=reason
        )
    
    # 生成6位数字验证码
    code = ''.join(random.choices(string.digits, k=6))
    print(code)
    # 存储验证码
    set_email_code(email, code)

    
    # 记录发送时间
    record_send_code(email)
    
    # 发送邮件
    email_body = f"""
    Hello,

    Your verification code is: {code}

    This verification code will be valid for 5 minutes.
    If this is not your operation, please ignore this email.

    Best regards,
    E-DBA Team
    """
    
    background_tasks.add_task(
        send_email,
        to=email,
        subject="E-DBA Login Verification Code",
        body=email_body
    )
    
    return {"msg": "Verification code has been sent"}

@router.post("/login-email-code", response_model=schemas.Token)
async def login_email_code(
    email: str = Form(...),
    code: str = Form(...),
    db: Session = Depends(deps.get_db)
):
    """
    邮箱验证码登录
    
    如果用户不存在但邮箱域名匹配某个组织，将自动创建新用户
    """
    # 检查邮箱格式
    if not verify_email(email):
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Invalid email format"
        )
    
    # 检查用户是否存在
    user = crud.user.get_by_email(db, email=email)
    
    # 如果用户不存在，尝试自动注册
    if not user:
        # 获取并验证验证码
        stored_code = get_email_code(email)
        if not stored_code:
            record_attempt(email, False)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码已过期或不存在"
            )
        
        if stored_code != code:
            record_attempt(email, False)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码错误"
            )
        
        # 验证码正确，尝试自动注册
        user = await auto_register_user_by_domain(db, email)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found and no matching organization domain"
            )
    else:
        # 用户存在，验证验证码
        stored_code = get_email_code(email)
        if not stored_code:
            record_attempt(email, False)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码已过期或不存在"
            )
        
        if stored_code != code:
            record_attempt(email, False)
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail="验证码错误"
            )
    
    # 验证成功，记录成功尝试
    record_attempt(email, True)
    
    # 记录登录日志
    crud.log.create_log(
        db=db,
        user_id=user.id,
        organization_id=user.organization_id,
        log_type=LogType.LOGIN,
        action="User login with email code",
        details=f"User {user.email} logged in with email code"
    )
    
    # 生成token
    access_token_expires = timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    return {
        "access_token": security.create_access_token(
            user.id, expires_delta=access_token_expires
        ),
        "token_type": "bearer",
    }