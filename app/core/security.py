from datetime import datetime, timedelta, timezone
from typing import Any, Union, Optional

from jose import jwt
from passlib.context import CryptContext

from app.core.config import settings

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

tz_utc_8 = timezone(timedelta(hours=8))

now = datetime.now(tz_utc_8)


def create_access_token(
    subject: Union[str, Any], expires_delta: Optional[timedelta] = None
) -> str:
    """创建JWT访问令牌"""
    if expires_delta:
        expire = datetime.now(tz_utc_8) + expires_delta
    else:
        expire = datetime.now(tz_utc_8) + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {
        "exp": int(expire.timestamp()),  # 过期时间
        "sub": str(subject),             # 用户ID
    }
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    """获取密码哈希值"""
    return pwd_context.hash(password)