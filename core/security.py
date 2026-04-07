from datetime import datetime, timedelta
from typing import Optional, Union
from jose import JWTError, jwt
from core.config import settings
import hashlib


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None) -> str:
    """创建访问令牌"""
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """验证密码"""
    # 使用简单的哈希方法进行验证
    return get_password_hash(plain_password) == hashed_password


def get_password_hash(password: str) -> str:
    """获取密码哈希值"""
    # 使用SHA-256进行密码哈希
    return hashlib.sha256((password + settings.SECRET_KEY).encode()).hexdigest()


def decode_token(token: str) -> Optional[dict]:
    """解码令牌"""
    try:
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        return payload
    except JWTError:
        return None
