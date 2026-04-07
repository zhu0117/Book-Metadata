from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date


# 作者相关模型
class AuthorBase(BaseModel):
    """作者基础模型"""
    name: str
    bio: Optional[str] = None


class AuthorCreate(AuthorBase):
    """创建作者模型"""
    pass


class Author(AuthorBase):
    """作者响应模型"""
    id: int

    class Config:
        from_attributes = True


# 书籍相关模型
class BookBase(BaseModel):
    """书籍基础模型"""
    title: str
    isbn: str
    publication_date: Optional[date] = None
    publisher: Optional[str] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None


class BookCreate(BookBase):
    """创建书籍模型"""
    author_ids: List[int] = []


class BookUpdate(BaseModel):
    """更新书籍模型"""
    title: Optional[str] = None
    isbn: Optional[str] = None
    publication_date: Optional[date] = None
    publisher: Optional[str] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None
    author_ids: Optional[List[int]] = None


class Book(BookBase):
    """书籍响应模型"""
    id: int
    average_rating: float
    rating_count: int
    authors: List[Author] = []

    class Config:
        from_attributes = True


# 评分相关模型
class RatingBase(BaseModel):
    """评分基础模型"""
    book_id: int
    rating: float = Field(..., ge=1, le=5)


class RatingCreate(RatingBase):
    """创建评分模型"""
    pass


class Rating(RatingBase):
    """评分响应模型"""
    id: int
    user_id: int

    class Config:
        from_attributes = True


# 推荐相关模型
class Recommendation(BaseModel):
    """推荐响应模型"""
    book: Book
    score: float


# 分页相关模型
class BookList(BaseModel):
    """书籍列表响应模型"""
    items: List[Book]
    total: int
    page: int
    size: int
    pages: int
