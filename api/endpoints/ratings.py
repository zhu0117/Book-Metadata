from fastapi import APIRouter, Depends, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from db.session import get_db
from db.models import Book, User, Rating
from db.schemas import Rating as RatingSchema, RatingCreate
from core.exceptions import create_not_found_exception, create_conflict_exception
from api.deps import get_current_active_user

router = APIRouter(prefix="/api/ratings", tags=["ratings"])


def update_book_rating_stats(db: Session, book_id: int):
    """更新书籍的平均评分和评分数量"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        return

    ratings = db.query(Rating).filter(Rating.book_id == book_id).all()
    if ratings:
        total = sum(r.rating for r in ratings)
        book.average_rating = round(total / len(ratings), 2)
        book.rating_count = len(ratings)
    else:
        book.average_rating = 0.0
        book.rating_count = 0
    db.commit()


@router.post("/", response_model=RatingSchema)
async def create_rating(
    rating: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """创建新评分"""
    book = db.query(Book).filter(Book.id == rating.book_id).first()
    if not book:
        raise create_not_found_exception("Book")

    existing = db.query(Rating).filter(
        Rating.user_id == current_user.id,
        Rating.book_id == rating.book_id
    ).first()
    if existing:
        raise create_conflict_exception("You have already rated this book")

    db_rating = Rating(
        user_id=current_user.id,
        book_id=rating.book_id,
        rating=rating.rating
    )
    db.add(db_rating)
    db.commit()
    db.refresh(db_rating)

    update_book_rating_stats(db, rating.book_id)

    return db_rating


@router.get("/", response_model=List[RatingSchema])
async def get_ratings(
    user_id: Optional[int] = None,
    book_id: Optional[int] = None,
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """获取评分列表，可按用户ID或书籍ID筛选"""
    query = db.query(Rating)

    if user_id:
        query = query.filter(Rating.user_id == user_id)
    if book_id:
        query = query.filter(Rating.book_id == book_id)

    return query.offset(skip).limit(limit).all()


@router.get("/{rating_id}", response_model=RatingSchema)
async def get_rating(rating_id: int, db: Session = Depends(get_db)):
    """获取单个评分"""
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not db_rating:
        raise create_not_found_exception("Rating")
    return db_rating


@router.put("/{rating_id}", response_model=RatingSchema)
async def update_rating(
    rating_id: int,
    rating: RatingCreate,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """更新评分"""
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not db_rating:
        raise create_not_found_exception("Rating")

    if db_rating.user_id != current_user.id:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="You can only update your own ratings")

    if rating.book_id != db_rating.book_id:
        raise HTTPException(status_code=400, detail="Cannot change the book of a rating")

    old_book_id = db_rating.book_id
    db_rating.rating = rating.rating
    db.commit()
    db.refresh(db_rating)

    update_book_rating_stats(db, old_book_id)

    return db_rating


@router.delete("/{rating_id}")
async def delete_rating(
    rating_id: int,
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_active_user)
):
    """删除评分"""
    db_rating = db.query(Rating).filter(Rating.id == rating_id).first()
    if not db_rating:
        raise create_not_found_exception("Rating")

    if db_rating.user_id != current_user.id:
        from fastapi import HTTPException
        raise HTTPException(status_code=403, detail="You can only delete your own ratings")

    book_id = db_rating.book_id
    db.delete(db_rating)
    db.commit()

    update_book_rating_stats(db, book_id)

    return {"message": "Rating deleted successfully"}
