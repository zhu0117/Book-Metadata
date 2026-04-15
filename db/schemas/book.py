from pydantic import BaseModel, Field
from typing import List, Optional


class AuthorBase(BaseModel):
    name: str


class AuthorCreate(AuthorBase):
    pass


class Author(AuthorBase):
    id: int

    class Config:
        from_attributes = True


class BookBase(BaseModel):
    title: str
    isbn: str
    publication_year: Optional[int] = None
    cover_url: Optional[str] = None
    language_code: Optional[str] = None


class BookCreate(BookBase):
    author_ids: List[int] = []


class BookUpdate(BaseModel):
    title: Optional[str] = None
    isbn: Optional[str] = None
    publication_year: Optional[int] = None
    cover_url: Optional[str] = None
    language_code: Optional[str] = None
    author_ids: Optional[List[int]] = None


class Book(BookBase):
    id: int
    average_rating: float
    rating_count: int
    authors: List[Author] = []

    class Config:
        from_attributes = True


class RatingBase(BaseModel):
    book_id: int
    rating: float = Field(..., ge=1, le=5)


class RatingCreate(RatingBase):
    pass


class Rating(RatingBase):
    id: int
    user_id: int

    class Config:
        from_attributes = True


class BookList(BaseModel):
    items: List[Book]
    total: int
    page: int
    size: int
    pages: int


class BookRecommendation(BaseModel):
    id: int
    title: str
    isbn: str
    publication_year: Optional[int] = None
    cover_url: Optional[str] = None
    language_code: Optional[str] = None
    average_rating: float
    rating_count: int
    authors: List[Author] = []
    similar_user: str
    similarity_score: float
    rating_from_similar_user: float

    class Config:
        from_attributes = True
