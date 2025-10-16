from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import get_current_user, AuthService
from app.models.user import User
from app.schemas.user_schema import UserOut, AvatarUpdate, ProfileUpdate, PasswordChange

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    """获取当前用户信息"""
    return current_user

@router.put("/me/avatar", response_model=UserOut)
async def update_avatar(
    avatar_data: AvatarUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新用户头像"""
    current_user.avatar = avatar_data.avatar
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.put("/me/profile", response_model=UserOut)
async def update_profile(
    profile_data: ProfileUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """更新用户资料"""
    # 只更新提供的字段
    if profile_data.nickname is not None:
        current_user.nickname = profile_data.nickname
    if profile_data.phone is not None:
        current_user.phone = profile_data.phone
    if profile_data.email is not None:
        current_user.email = profile_data.email
    if profile_data.signature is not None:
        current_user.signature = profile_data.signature
    
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user

@router.post("/me/password")
async def change_password(
    password_data: PasswordChange,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    """修改密码"""
    # 验证旧密码
    if not AuthService.verify_password(password_data.old_password, current_user.hashed_password):
        raise HTTPException(status_code=400, detail="旧密码不正确")
    
    # 更新密码
    current_user.hashed_password = AuthService.get_password_hash(password_data.new_password)
    db.add(current_user)
    db.commit()
    
    return {"message": "密码修改成功"}
