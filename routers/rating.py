from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from database import get_db
from models import Rating, Book, User
from schemas import Rating as RatingSchema, RatingCreate

router = APIRouter()

@router.post("/", response_model=RatingSchema)
async def create_rating(rating: RatingCreate, db: Session = Depends(get_db)):
    # 检查用户是否存在
    db_user = db.query(User).filter(User.id == rating.user_id).first()
    if not db_user:
        raise HTTPException(status_code=404, detail="User not found")
    
    # 检查书籍是否存在
    db_book = db.query(Book).filter(Book.id == rating.book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # 检查用户是否已经为该书籍评分
    existing_rating = db.query(Rating).filter(
        Rating.user_id == rating.user_id,
        Rating.book_id == rating.book_id
    ).first()
    if existing_rating:
        raise HTTPException(status_code=400, detail="User has already rated this book")
    
    # 创建新评分
    db_rating = Rating(
        user_id=rating.user_id,
        book_id=rating.book_id,
        rating=rating.rating
    )
    
    db.add(db_rating)
    
    # 更新书籍的平均评分
    book_ratings = db.query(Rating).filter(Rating.book_id == rating.book_id).all()
    total_rating = sum(r.rating for r in book_ratings) + rating.rating
    rating_count = len(book_ratings) + 1
    db_book.average_rating = total_rating / rating_count
    db_book.rating_count = rating_count
    
    db.commit()
    db.refresh(db_rating)
    return db_rating

@router.get("/", response_model=List[RatingSchema])
async def get_ratings(
    skip: int = 0,
    limit: int = 100,
    user_id: int = None,
    book_id: int = None,
    db: Session = Depends(get_db)
):
    query = db.query(Rating)
    
    if user_id:
        query = query.filter(Rating.user_id == user_id)
    
    if book_id:
        query = query.filter(Rating.book_id == book_id)
    
    ratings = query.offset(skip).limit(limit).all()
    return ratings

@router.get("/{rating_id}", response_model=RatingSchema)
async def get_rating(rating_id: int, db: Session = Depends(get_db)):
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not db_rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    return db_rating

@router.put("/{rating_id}", response_model=RatingSchema)
async def update_rating(rating_id: int, rating: RatingCreate, db: Session = Depends(get_db)):
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not db_rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    # 检查书籍是否存在
    db_book = db.query(Book).filter(Book.id == rating.book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # 保存旧评分
    old_rating = db_rating.rating
    
    # 更新评分
    db_rating.rating = rating.rating
    
    # 更新书籍的平均评分
    book_ratings = db.query(Rating).filter(Rating.book_id == rating.book_id).all()
    total_rating = sum(r.rating for r in book_ratings) - old_rating + rating.rating
    rating_count = len(book_ratings)
    db_book.average_rating = total_rating / rating_count
    
    db.commit()
    db.refresh(db_rating)
    return db_rating

@router.delete("/{rating_id}")
async def delete_rating(rating_id: int, db: Session = Depends(get_db)):
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not db_rating:
        raise HTTPException(status_code=404, detail="Rating not found")
    
    # 保存书籍ID和评分值，用于后续更新平均评分
    book_id = db_rating.book_id
    deleted_rating = db_rating.rating
    
    db.delete(db_rating)
    
    # 更新书籍的平均评分
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if db_book:
        book_ratings = db.query(Rating).filter(Rating.book_id == book_id).all()
        if book_ratings:
            total_rating = sum(r.rating for r in book_ratings)
            rating_count = len(book_ratings)
            db_book.average_rating = total_rating / rating_count
            db_book.rating_count = rating_count
        else:
            db_book.average_rating = 0.0
            db_book.rating_count = 0
    
    db.commit()
    return {"message": "Rating deleted successfully"}