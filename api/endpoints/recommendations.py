from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List

from db.session import get_db
from recommendation import RecommendationEngine
from db.schemas import Book as BookSchema, BookRecommendation

router = APIRouter(prefix="/recommendations", tags=["recommendations"])


def get_recommendation_engine(db: Session = Depends(get_db)) -> RecommendationEngine:
    return RecommendationEngine(db)


@router.get("/popular", response_model=List[BookSchema])
def get_popular_books(
    limit: int = 10,
    min_rating_count: int = 3,
    engine: RecommendationEngine = Depends(get_recommendation_engine)
):
    """获取热门书籍推荐"""
    books = engine.get_popular_books(limit=limit, min_rating_count=min_rating_count)
    return books


@router.get("/authors/{user_id}", response_model=List[BookSchema])
def get_author_recommendations(
    user_id: int,
    limit: int = 10,
    engine: RecommendationEngine = Depends(get_recommendation_engine)
):
    """基于用户喜欢的作者推荐书籍"""
    books = engine.get_books_by_popular_authors(user_id=user_id, limit=limit)
    return books


@router.get("/collaborative/{user_id}", response_model=List[BookRecommendation])
def get_collaborative_recommendations(
    user_id: int,
    limit: int = 10,
    engine: RecommendationEngine = Depends(get_recommendation_engine)
):
    """基于用户的协同过滤推荐"""
    recommendations = engine.get_user_based_recommendations(user_id=user_id, limit=limit)
    if not recommendations:
        return []
    return recommendations


@router.get("/hybrid/{user_id}", response_model=List[BookSchema])
def get_hybrid_recommendations(
    user_id: int,
    limit: int = 10,
    engine: RecommendationEngine = Depends(get_recommendation_engine)
):
    """混合推荐：结合热门推荐和作者推荐"""
    author_books = engine.get_books_by_popular_authors(user_id=user_id, limit=limit)
    popular_books = engine.get_popular_books(limit=limit, min_rating_count=3)

    seen_ids = set()
    unique_books = []
    for book in author_books:
        if book.id not in seen_ids:
            seen_ids.add(book.id)
            unique_books.append(book)

    for book in popular_books:
        if book.id not in seen_ids:
            seen_ids.add(book.id)
            unique_books.append(book)
        if len(unique_books) >= limit:
            break

    return unique_books[:limit]