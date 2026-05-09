"""
数据库模型：定义数据库里的表结构
类似前端：数据库表结构设计（不是传输数据的格式）
"""
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import DeclarativeBase


# 基类：所有数据库表都要继承它（类似前端的抽象基类）
class Base(DeclarativeBase):
    pass


# User 类 = 数据库里的 users 表
class User(Base):
    __tablename__ = 'users'

    # Column = 定义数据库字段，每个 Column 对应表的一列
    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)  # 存加密后的密码，不能明文
    name = Column(String)
    age = Column(Integer)


# Post 类 = 数据库里的 posts 表
class Post(Base):
    __tablename__ = "posts"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    content = Column(String, nullable=False)
    author = Column(String)  # 作者，暂时存用户名
    user_id = Column(Integer , ForeignKey("users.id") , nullable =False )
