from sqlalchemy import Column, Integer, String, Float, ForeignKey, Date, Table
from sqlalchemy.orm import relationship
from database import Base

# 书籍和作者的多对多关系表
book_author = Table('book_author', Base.metadata,
    Column('book_id', Integer, ForeignKey('books.id'), primary_key=True),
    Column('author_id', Integer, ForeignKey('authors.id'), primary_key=True)
)

class Book(Base):
    __tablename__ = "books"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    isbn = Column(String, unique=True, index=True)
    publication_date = Column(Date)
    publisher = Column(String)
    description = Column(String)
    cover_url = Column(String)
    average_rating = Column(Float, default=0.0)
    rating_count = Column(Integer, default=0)

    # 关系
    authors = relationship("Author", secondary=book_author, back_populates="books")
    ratings = relationship("Rating", back_populates="book")

class Author(Base):
    __tablename__ = "authors"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    bio = Column(String)

    # 关系
    books = relationship("Book", secondary=book_author, back_populates="authors")

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    password_hash = Column(String)

    # 关系
    ratings = relationship("Rating", back_populates="user")

class Rating(Base):
    __tablename__ = "ratings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    book_id = Column(Integer, ForeignKey("books.id"))
    rating = Column(Float)

    # 关系
    user = relationship("User", back_populates="ratings")
    book = relationship("Book", back_populates="ratings")