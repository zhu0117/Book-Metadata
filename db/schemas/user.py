from pydantic import BaseModel, EmailStr
from typing import Optional


# 用户基础模型
class UserBase(BaseModel):
    """用户基础模型"""
    username: str
    email: EmailStr


# 用户创建模型
class UserCreate(UserBase):
    """创建用户模型"""
    password: str


# 用户响应模型
class User(UserBase):
    """用户响应模型"""
    id: int

    class Config:
        from_attributes = True


# 登录请求模型
class UserLogin(BaseModel):
    """登录请求模型"""
    username: str
    password: str


# 令牌响应模型
class Token(BaseModel):
    """令牌响应模型"""
    access_token: str
    token_type: str = "bearer"


# 令牌数据模型
class TokenData(BaseModel):
    """令牌数据模型"""
    username: Optional[str] = None
