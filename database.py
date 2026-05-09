import os
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Base

# 加载 .env 文件中的环境变量
load_dotenv()

# 从 .env 文件读取数据库连接字符串
DATABASE_URL = os.getenv("DATABASE_URL")

# 创建数据库连接引擎
engine = create_engine(DATABASE_URL)

# 创建 Session 工厂
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建所有表（如果不存在才创建）
Base.metadata.create_all(bind=engine)