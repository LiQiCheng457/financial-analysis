from pydantic import BaseModel, Field
from typing import Optional

class UserOut(BaseModel):
    username: str
    avatar: Optional[str] = None

    class Config:
        from_attributes = True

class AvatarUpdate(BaseModel):
    avatar: str = Field(..., description="用户头像的Base64编码字符串")
