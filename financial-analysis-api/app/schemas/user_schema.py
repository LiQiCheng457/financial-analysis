from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime

class UserOut(BaseModel):
    id: int
    username: str
    avatar: Optional[str] = None
    nickname: Optional[str] = None
    phone: Optional[str] = None
    email: Optional[str] = None
    signature: Optional[str] = None
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

class AvatarUpdate(BaseModel):
    avatar: str = Field(..., description="用户头像的Base64编码字符串")

class ProfileUpdate(BaseModel):
    nickname: Optional[str] = Field(None, max_length=100, description="昵称")
    phone: Optional[str] = Field(None, max_length=20, description="手机号")
    email: Optional[str] = Field(None, description="邮箱")
    signature: Optional[str] = Field(None, max_length=200, description="个性签名")

class PasswordChange(BaseModel):
    old_password: str = Field(..., min_length=6, description="旧密码")
    new_password: str = Field(..., min_length=6, description="新密码")
