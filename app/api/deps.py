from typing import Generator

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt
from pydantic import ValidationError
from sqlalchemy.orm import Session

from app import models, schemas, crud
from app.core.config import settings
from app.db.session import SessionLocal
from app.models.enums import UserRole

# OAuth2密码流的令牌URL
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    scheme_name="OAuth2密码模式",
    description="使用邮箱和密码登录获取访问令牌",
    auto_error=True
)


def get_db() -> Generator:
    """获取数据库会话"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.user.User:
    """获取当前用户"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="无法验证凭据",
        )
    user = crud.user.get(db, id=int(token_data.sub))
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="用户未激活")
    return user


def get_current_active_user(
    current_user: models.user.User = Depends(get_current_user),
) -> models.user.User:
    """获取当前激活的用户"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="用户未激活")
    return current_user


def get_current_t_admin(
    current_user: models.user.User = Depends(get_current_user),
) -> models.user.User:
    """获取当前技术管理员（T-Admin）"""
    if current_user.role != UserRole.T_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要技术管理员权限",
        )
    return current_user


def get_current_e_admin(
    current_user: models.user.User = Depends(get_current_user),
) -> models.user.User:
    """获取当前管理管理员（E-Admin）"""
    if current_user.role not in [UserRole.E_ADMIN, UserRole.SENIOR_E_ADMIN, UserRole.T_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要管理管理员权限",
        )
    return current_user


def get_current_senior_e_admin(
    current_user: models.user.User = Depends(get_current_user),
) -> models.user.User:
    """获取当前高级管理管理员（Senior E-Admin）"""
    if current_user.role != UserRole.SENIOR_E_ADMIN and current_user.role != UserRole.T_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要高级管理管理员权限",
        )
    return current_user


def get_current_o_convener(
    current_user: models.user.User = Depends(get_current_user),
) -> models.user.User:
    """获取当前组织协调人（O-Convener）"""
    if current_user.role != UserRole.O_CONVENER and current_user.role != UserRole.T_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="权限不足，需要组织协调人权限",
        )
    return current_user
