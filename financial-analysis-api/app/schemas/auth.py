from pydantic import BaseModel, Field
from typing import Optional

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="用户名")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="密码")
    role: str = Field('user', description="角色，可选: admin 或 user")
    nickname: Optional[str] = Field(None, description="昵称")
    email: Optional[str] = Field(None, description="邮箱")
    phone: Optional[str] = Field(None, description="手机号")
    signature: Optional[str] = Field(None, description="个性签名")

class UserLogin(UserBase):
    password: str = Field(..., description="密码")

class Token(BaseModel):
    access_token: str
    token_type: str
