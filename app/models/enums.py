import enum

class UserRole(str, enum.Enum):
    T_ADMIN = "T_ADMIN"  # 技术管理员
    E_ADMIN = "E_ADMIN"  # 管理员
    SENIOR_E_ADMIN = "SENIOR_E_ADMIN"  # 高级管理员
    O_CONVENER = "O_CONVENER"  # 组织协调人
    DATA_USER = "DATA_USER"  # 数据用户

class PermissionLevel(int, enum.Enum):
    PUBLIC_DATA = 1  # 公开数据访问（课程信息）
    PRIVATE_DATA_CONSUMER = 2  # 私有数据消费（论文下载、身份验证）
    PRIVATE_DATA_PROVIDER = 3  # 私有数据提供（配置服务接口） 