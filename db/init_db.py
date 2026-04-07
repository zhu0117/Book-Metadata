from db.base import Base
from db.session import engine
from db.models import book, user  # 导入所有模型


def init_db():
    """初始化数据库，创建所有表结构"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    print("Database initialized successfully!")


if __name__ == "__main__":
    init_db()
