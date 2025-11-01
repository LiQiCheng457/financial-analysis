from sqlalchemy.orm import Session
from typing import Optional
from app.schemas.auth import UserCreate, UserLogin
from app.models.user import User
from fastapi import HTTPException, status  # type: ignore[reportMissingImports]
from passlib.context import CryptContext  # type: ignore[reportMissingImports]
import jwt
from datetime import datetime, timedelta
from dotenv import load_dotenv
import os

load_dotenv()

# 密码哈希
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES"))

class AuthService:

    @staticmethod
    def get_user_by_username(db: Session, username: str):
        return db.query(User).filter(User.username == username).first()

    @staticmethod
    def verify_password(plain_password, hashed_password):
        return pwd_context.verify(plain_password, hashed_password)

    @staticmethod
    def get_password_hash(password):
        return pwd_context.hash(password)

    @staticmethod
    def create_user(db: Session, user: UserCreate):
        # 支持可选 role 参数（默认 'user'）
        hashed_password = AuthService.get_password_hash(user.password)
        role = getattr(user, 'role', 'user')
        db_user = User(username=user.username, hashed_password=hashed_password, role=role)
        # 可选字段
        if getattr(user, 'nickname', None):
            db_user.nickname = user.nickname
        if getattr(user, 'email', None):
            db_user.email = user.email
        if getattr(user, 'phone', None):
            db_user.phone = user.phone
        if getattr(user, 'signature', None):
            db_user.signature = user.signature
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

    @staticmethod
    def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
        return encoded_jwt

    @staticmethod
    def login_for_access_token(db: Session, user_in: UserLogin):
        user = AuthService.get_user_by_username(db, username=user_in.username)
        if not user or not AuthService.verify_password(user_in.password, user.hashed_password):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",
                headers={"WWW-Authenticate": "Bearer"},
            )
        access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
        access_token = AuthService.create_access_token(
            data={"sub": user.username}, expires_delta=access_token_expires
        )
        # 返回 token 的同时带上用户信息（包含 role）以便前端快速识别
        user_data = {
            "id": user.id,
            "username": user.username,
            "role": getattr(user, 'role', 'user'),
            "avatar": getattr(user, 'avatar', None),
            "nickname": getattr(user, 'nickname', None),
            "email": getattr(user, 'email', None),
        }
        return {"access_token": access_token, "token_type": "bearer", "user": user_data}

    @staticmethod
    def update_user_password(db: Session, username: str, new_password: str):
        user = AuthService.get_user_by_username(db, username=username)
        if not user:
            return None
        user.hashed_password = AuthService.get_password_hash(new_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user


from fastapi import Depends  # type: ignore[reportMissingImports]
from fastapi.security import OAuth2PasswordBearer  # type: ignore[reportMissingImports]
from app.core.database import get_db

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

async def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except jwt.PyJWTError:
        raise credentials_exception
    
    user = AuthService.get_user_by_username(db, username=username)
    if user is None:
        raise credentials_exception
    return user


def admin_required(current_user: User = Depends(get_current_user)):
    """FastAPI dependency to ensure the current user is an admin."""
    if getattr(current_user, 'role', None) != 'admin':
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="管理员权限不足")
    return current_user
