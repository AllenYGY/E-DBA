from typing import Any, Dict, List, Optional, Union
from pydantic import AnyHttpUrl, validator
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    API_V1_STR: str = "/api/v1"
    SECRET_KEY: str
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 11520
    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    @validator("BACKEND_CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    PROJECT_NAME: str 
    MYSQL_SERVER: str 
    MYSQL_PORT: int 
    MYSQL_USER: str
    MYSQL_PASSWORD: str 
    MYSQL_DB: str 
    SQLALCHEMY_DATABASE_URI: Optional[str] = None
    
    E_ADMIN_EMAIL: str 
    E_ADMIN_NAME: str
    E_ADMIN_PASSWORD: str

    SENIOR_E_ADMIN_EMAIL: str
    SENIOR_E_NAME: str    
    SENIOR_E_ADMIN_PASSWORD: str

    T_ADMIN_EMAIL: str
    T_ADMIN_NAME: str
    T_ADMIN_PASSWORD: str

    # External Service Configuration
    EXTERNAL_SERVICE_BASE_URL: str

    # Student Verification Service
    STUDENT_VERIFICATION_PATH: str
    STUDENT_VERIFICATION_METHOD: str
    STUDENT_VERIFICATION_NAME: str
    STUDENT_VERIFICATION_DESCRIPTION: str

    # Student GPA Service
    STUDENT_GPA_PATH: str
    STUDENT_GPA_METHOD: str
    STUDENT_GPA_NAME: str
    STUDENT_GPA_DESCRIPTION: str

    # Paper Sharing Service
    PAPER_SHARING_PATH: str
    PAPER_SHARING_METHOD: str
    PAPER_SHARING_NAME: str
    PAPER_SHARING_DESCRIPTION: str

    # Paper PDF Service
    PAPER_PDF_PATH: str
    PAPER_PDF_METHOD: str
    PAPER_PDF_NAME: str
    PAPER_PDF_DESCRIPTION: str

    # Bank Authentication Service
    BANK_AUTH_PATH: str
    BANK_AUTH_METHOD: str
    BANK_AUTH_NAME: str
    BANK_AUTH_DESCRIPTION: str

    # Bank Transfer Service
    BANK_TRANSFER_PATH: str
    BANK_TRANSFER_METHOD: str
    BANK_TRANSFER_NAME: str
    BANK_TRANSFER_DESCRIPTION: str

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def assemble_db_connection(cls, v: Optional[str], values: Dict[str, Any]) -> Any:
        if isinstance(v, str):
            return v
        return f"mysql+mysqlconnector://{values.get('MYSQL_USER')}:{values.get('MYSQL_PASSWORD')}@{values.get('MYSQL_SERVER')}:{values.get('MYSQL_PORT')}/{values.get('MYSQL_DB')}"

    class Config:
        from_attributes = True
        case_sensitive = True
        env_file = ".env"
    
settings = Settings()

# 当直接运行此文件时，打印配置信息
if __name__ == "__main__":
    print("当前配置信息：")
    print(f"项目名称: {settings.PROJECT_NAME}")
    print(f"API版本: {settings.API_V1_STR}")
    print(f"数据库URI: {settings.SQLALCHEMY_DATABASE_URI}")
    print(f"CORS origins: {settings.BACKEND_CORS_ORIGINS}")
    print(f"Token过期时间: {settings.ACCESS_TOKEN_EXPIRE_MINUTES} 分钟")
    print(f"外部服务基础URL: {settings.EXTERNAL_SERVICE_BASE_URL}")
    print(f"学生验证服务路径: {settings.STUDENT_VERIFICATION_PATH}")
    print(f"学生GPA服务路径: {settings.STUDENT_GPA_PATH}")
    print(f"论文共享服务路径: {settings.PAPER_SHARING_PATH}")
    print(f"论文PDF服务路径: {settings.PAPER_PDF_PATH}")
    print(f"银行认证服务路径: {settings.BANK_AUTH_PATH}")
    print(f"银行转账服务路径: {settings.BANK_TRANSFER_PATH}")
    print(f"管理员邮箱: {settings.E_ADMIN_EMAIL}")
    print(f"管理员名称: {settings.E_ADMIN_NAME}")
    print(f"管理员密码: {settings.E_ADMIN_PASSWORD}")
    print(f"高级管理员邮箱: {settings.SENIOR_E_ADMIN_EMAIL}")
    print(f"高级管理员名称: {settings.SENIOR_E_NAME}")
    print(f"高级管理员密码: {settings.SENIOR_E_ADMIN_PASSWORD}")
    print(f"学生验证服务名称: {settings.STUDENT_VERIFICATION_NAME}")
    print(f"学生验证服务描述: {settings.STUDENT_VERIFICATION_DESCRIPTION}")
    print(f"学生GPA服务名称: {settings.STUDENT_GPA_NAME}")
    print(f"学生GPA服务描述: {settings.STUDENT_GPA_DESCRIPTION}")
    print(f"论文共享服务名称: {settings.PAPER_SHARING_NAME}")
    print(f"论文共享服务描述: {settings.PAPER_SHARING_DESCRIPTION}")
    print(f"论文PDF服务名称: {settings.PAPER_PDF_NAME}")
    
    
