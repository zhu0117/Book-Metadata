from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from db.session import get_db
from db.models import Book, Author, User
from db.schemas import Book as BookSchema, BookCreate, BookUpdate, BookList
from core.exceptions import create_not_found_exception, create_conflict_exception
from api.deps import get_current_active_user

router = APIRouter(prefix="/api/books", tags=["books"])


@router.post("/", response_model=BookSchema)
async def create_book(
    book: BookCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建新书籍"""
    db_book = db.query(Book).filter(Book.isbn == book.isbn).first()
    if db_book:
        raise create_conflict_exception("Book with this ISBN")

    db_book = Book(
        title=book.title,
        isbn=book.isbn,
        publication_date=book.publication_date,
        publisher=book.publisher,
        description=book.description,
        cover_url=book.cover_url
    )

    for author_id in book.author_ids:
        author = db.query(Author).filter(Author.id == author_id).first()
        if author:
            db_book.authors.append(author)

    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book


@router.get("/", response_model=BookList)
async def get_books(
    skip: int = 0,
    limit: int = 10,
    page: int = 1,
    title: Optional[str] = None,
    author: Optional[str] = None,
    publisher: Optional[str] = None,
    sort_by: Optional[str] = "id",
    sort_order: Optional[str] = "asc",
    db: Session = Depends(get_db)
):
    """获取书籍列表，支持分页、搜索和排序"""
    query = db.query(Book)

    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))

    if author:
        query = query.join(Book.authors).filter(Author.name.ilike(f"%{author}%"))

    if publisher:
        query = query.filter(Book.publisher.ilike(f"%{publisher}%"))

    sort_column = getattr(Book, sort_by, Book.id)
    if sort_order == "desc":
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column.asc())

    total = query.count()
    offset = (page - 1) * limit
    books = query.offset(offset).limit(limit).all()
    pages = (total + limit - 1) // limit

    return BookList(
        items=books,
        total=total,
        page=page,
        size=limit,
        pages=pages
    )


@router.get("/{book_id}", response_model=BookSchema)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    """获取书籍详情"""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise create_not_found_exception("Book")
    return db_book


@router.put("/{book_id}", response_model=BookSchema)
async def update_book(
    book_id: int,
    book: BookUpdate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新书籍信息"""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise create_not_found_exception("Book")

    if book.isbn and book.isbn != db_book.isbn:
        existing_book = db.query(Book).filter(Book.isbn == book.isbn).first()
        if existing_book:
            raise create_conflict_exception("Book with this ISBN")

    update_data = book.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field != "author_ids":
            setattr(db_book, field, value)

    if "author_ids" in update_data:
        db_book.authors = []
        for author_id in book.author_ids:
            author = db.query(Author).filter(Author.id == author_id).first()
            if author:
                db_book.authors.append(author)

    db.commit()
    db.refresh(db_book)
    return db_book


@router.delete("/{book_id}")
async def delete_book(
    book_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除书籍"""
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise create_not_found_exception("Book")

    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}
