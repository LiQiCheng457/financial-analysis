from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.database import get_db
from app.services.auth_service import get_current_user
from app.models.user import User
from app.schemas.user_schema import UserOut, AvatarUpdate

router = APIRouter()

@router.get("/me", response_model=UserOut)
async def read_users_me(current_user: User = Depends(get_current_user)):
    return current_user

@router.put("/me/avatar", response_model=UserOut)
async def update_avatar(
    avatar_data: AvatarUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    current_user.avatar = avatar_data.avatar
    db.add(current_user)
    db.commit()
    db.refresh(current_user)
    return current_user
