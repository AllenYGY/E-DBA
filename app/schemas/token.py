from typing import Optional
from pydantic import BaseModel, Field

class Token(BaseModel):
    access_token: str = Field(..., description="访问令牌")
    token_type: str = Field(..., description="令牌类型，固定为 'bearer'")

    class Config:
        json_schema_extra = {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer"
            }
        }

class TokenPayload(BaseModel):
    sub: Optional[str] = None  # subject (user id)
    exp: Optional[int] = None  # expiration time

    class Config:
        json_schema_extra = {
            "example": {
                "sub": "1",
                "exp": 1735689600,
                "iat": 1735686000,
                "type": "access"
            }
        } 