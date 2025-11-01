from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException  # type: ignore[reportMissingImports]
from sqlalchemy.orm import Session
from sqlalchemy import or_
from app.core.database import get_db
from app.services.auth_service import admin_required, AuthService
from app.models.user import User
from app.schemas.user_schema import UserOut, UserListOut
from app.schemas.auth import UserCreate

router = APIRouter()


@router.get("/", response_model=UserListOut)
def list_users(skip: int = 0, limit: int = 50, q: Optional[str] = None, db: Session = Depends(get_db), _=Depends(admin_required)):
    """管理员：列出用户（分页），支持关键字搜索（username/email/nickname），返回 { items: [...], total: N }"""
    query = db.query(User)
    if q:
        # 简单模糊匹配 username/email/nickname
        like_q = f"%{q}%"
        query = query.filter(or_(User.username.ilike(like_q), User.email.ilike(like_q), User.nickname.ilike(like_q)))
    total = query.count()
    items = query.offset(skip).limit(limit).all()
    return {"items": items, "total": total}


@router.post("/", response_model=UserOut)
def create_user(user_in: UserCreate, db: Session = Depends(get_db), _=Depends(admin_required)):
    """管理员：创建用户（可指定 role 字段在 user_in 中）"""
    existing = AuthService.get_user_by_username(db, username=user_in.username)
    if existing:
        raise HTTPException(status_code=400, detail="用户名已存在")
    created = AuthService.create_user(db=db, user=user_in)
    return created


@router.get("/{user_id}", response_model=UserOut)
def get_user(user_id: int, db: Session = Depends(get_db), _=Depends(admin_required)):
    """管理员：获取单个用户详情"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    return user


@router.put("/{user_id}", response_model=UserOut)
def update_user(user_id: int, payload: dict, db: Session = Depends(get_db), _=Depends(admin_required)):
    """管理员：更新用户信息（可修改 role、nickname 等）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    # 仅允许更新安全字段
    for k in ["role", "nickname", "phone", "email", "signature"]:
        if k in payload:
            setattr(user, k, payload[k])
    db.add(user)
    db.commit()
    db.refresh(user)
    return user


@router.patch("/{user_id}/password")
def admin_reset_password(user_id: int, payload: dict, db: Session = Depends(get_db), _=Depends(admin_required)):
    """管理员：重置用户密码，payload: {"new_password": "..."} """
    new_password = payload.get("new_password")
    if not new_password or len(new_password) < 6:
        raise HTTPException(status_code=400, detail="新密码长度至少6位")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user.hashed_password = AuthService.get_password_hash(new_password)
    db.add(user)
    db.commit()
    return {"message": "密码已重置"}


@router.delete("/{user_id}")
def delete_user(user_id: int, db: Session = Depends(get_db), _=Depends(admin_required)):
    """管理员：删除用户（注意：请谨慎操作）"""
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    db.delete(user)
    db.commit()
    return {"message": "用户已删除"}
