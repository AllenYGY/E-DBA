import sys
from pathlib import Path

sys.path.append(str(Path(__file__).parent.parent.parent))

from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from app.core.config import settings


def test_db_connection():
    try:
        engine = create_engine(settings.SQLALCHEMY_DATABASE_URI)
        SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
        session = SessionLocal()
        
        # 执行一个简单的查询来测试连接
        result = session.execute(text("SELECT 1"))
        print("✅ 数据库连接成功！")
        print(f"数据库URI: {settings.SQLALCHEMY_DATABASE_URI}")
        print(f"测试查询结果: {result.scalar()}")
        
        session.close()
        
    except Exception as e:
        print("❌ 数据库连接失败！")
        print(f"错误信息: {str(e)}")

if __name__ == "__main__":
    test_db_connection() 