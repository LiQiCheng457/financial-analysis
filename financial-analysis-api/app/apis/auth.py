from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.schemas.auth import UserCreate, UserLogin
from app.services.auth_service import AuthService
from app.core.database import get_db

router = APIRouter()

@router.post("/register", summary="用户注册")
def register(user: UserCreate, db: Session = Depends(get_db)):
    db_user = AuthService.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="用户名已被注册")
    AuthService.create_user(db=db, user=user)
    return {"message": "用户注册成功"}

@router.post("/login", summary="用户登录")
def login(user: UserLogin, db: Session = Depends(get_db)):
    return AuthService.login_for_access_token(db=db, user_in=user)
