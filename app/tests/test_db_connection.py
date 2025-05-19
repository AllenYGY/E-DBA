import sys
from pathlib import Path
import os

sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings

print("os.environ['MYSQL_PASSWORD']:", os.environ.get('MYSQL_PASSWORD'))

def test_db_connection():
    try:
        # 打印配置信息
        print("当前数据库配置：")
        print(f"MYSQL_SERVER: {settings.MYSQL_SERVER}")
        print(f"MYSQL_PORT: {settings.MYSQL_PORT}")
        print(f"MYSQL_USER: {settings.MYSQL_USER}")
        print(f"MYSQL_PASSWORD: {'*' * len(settings.MYSQL_PASSWORD) if settings.MYSQL_PASSWORD else 'None'}")
        print(f"MYSQL_DB: {settings.MYSQL_DB}")
        print(f"SQLALCHEMY_DATABASE_URI: {settings.SQLALCHEMY_DATABASE_URI}")
        
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        # 执行一个简单的查询来测试连接
        result = session.execute(text("SELECT 1"))
        print("\n✅ 数据库连接成功！")
        print(f"测试查询结果: {result.scalar()}")
        
        session.close()
        
    except Exception as e:
        print("\n❌ 数据库连接失败！")
        print(f"错误信息: {str(e)}")

if __name__ == "__main__":
    test_db_connection() 