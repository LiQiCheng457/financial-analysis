from sqlalchemy import Column, Integer, String, Text, DateTime
from datetime import datetime
from app.core.database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True, nullable=False)
    hashed_password = Column(String(255), nullable=False)
    avatar = Column(Text, nullable=True)  # Base64存储
    nickname = Column(String(100), nullable=True)  # 昵称
    phone = Column(String(20), nullable=True)  # 手机号
    email = Column(String(100), nullable=True)  # 邮箱
    signature = Column(String(200), nullable=True)  # 个性签名
    created_at = Column(DateTime, default=datetime.now)  # 注册时间
