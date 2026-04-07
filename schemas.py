from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import date

# 作者相关模型
class AuthorBase(BaseModel):
    name: str
    bio: Optional[str] = None

class AuthorCreate(AuthorBase):
    pass

class Author(AuthorBase):
    id: int
    books: List['Book'] = []

    class Config:
        from_attributes = True

# 书籍相关模型
class BookBase(BaseModel):
    title: str
    isbn: str
    publication_date: Optional[date] = None
    publisher: Optional[str] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None

class BookCreate(BookBase):
    author_ids: List[int] = []

class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    publication_date: Optional[date] = None
    publisher: Optional[str] = None
    description: Optional[str] = None
    cover_url: Optional[str] = None
    author_ids: Optional[List[int]] = None

class Book(BookBase):
    id: int
    average_rating: float
    rating_count: int
    authors: List[Author] = []

    class Config:
        from_attributes = True

# 用户相关模型
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int

    class Config:
        from_attributes = True

# 评分相关模型
class RatingBase(BaseModel):
    book_id: int
    rating: float = Field(..., ge=1, le=5)

class RatingCreate(RatingBase):
    user_id: int

class Rating(RatingBase):
    id: int
    user: User
    book: Book

    class Config:
        from_attributes = True

# 推荐相关模型
class Recommendation(BaseModel):
    book: Book
    score: float

# 解析循环引用
Author.model_rebuild()
Book.model_rebuild()