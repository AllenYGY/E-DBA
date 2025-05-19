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

# OAuth2 password mode token URL
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login",
    scheme_name="OAuth2 password mode",
    description="Use email and password to login and get access token",
    auto_error=True
)


def get_db() -> Generator:
    """Get database session"""
    try:
        db = SessionLocal()
        yield db
    finally:
        db.close()


def get_current_user(
    db: Session = Depends(get_db), token: str = Depends(oauth2_scheme)
) -> models.user.User:
    """Get current user"""
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=["HS256"]
        )
        token_data = schemas.TokenPayload(**payload)
    except (jwt.JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Cannot verify credentials",
        )
    user = crud.user.get(db, id=int(token_data.sub))
    if not user:
        raise HTTPException(status_code=404, detail="User does not exist")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="User is not active")
    return user


def get_current_active_user(
    current_user: models.user.User = Depends(get_current_user),
) -> models.user.User:
    """Get current active user"""
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="User is not active")
    return current_user


def get_current_t_admin(
    current_user: models.user.User = Depends(get_current_user),
) -> models.user.User:
    """Get current T-Admin"""
    if current_user.role != UserRole.T_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied, need T-Admin permission",
        )
    return current_user


def get_current_e_admin(
    current_user: models.user.User = Depends(get_current_user),
) -> models.user.User:
    """Get current E-Admin"""
    if current_user.role not in [UserRole.E_ADMIN, UserRole.SENIOR_E_ADMIN, UserRole.T_ADMIN]:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied, need E-Admin permission",
        )
    return current_user


def get_current_senior_e_admin(
    current_user: models.user.User = Depends(get_current_user),
) -> models.user.User:
    """Get current Senior E-Admin"""
    if current_user.role != UserRole.SENIOR_E_ADMIN and current_user.role != UserRole.T_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied, need Senior E-Admin permission",
        )
    return current_user


def get_current_o_convener(
    current_user: models.user.User = Depends(get_current_user),
) -> models.user.User:
    """Get current O-Convener"""
    if current_user.role != UserRole.O_CONVENER and current_user.role != UserRole.T_ADMIN and current_user.role != UserRole.E_ADMIN:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Permission denied, need O-Convener permission",
        )
    return current_user
