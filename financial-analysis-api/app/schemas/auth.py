from pydantic import BaseModel, Field

class UserBase(BaseModel):
    username: str = Field(..., min_length=3, max_length=50, description="用户名")

class UserCreate(UserBase):
    password: str = Field(..., min_length=6, description="密码")

class UserLogin(UserBase):
    password: str = Field(..., description="密码")

class Token(BaseModel):
    access_token: str
    token_type: str
