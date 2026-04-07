from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional, Dict
from database import get_db
from models import Book, Author, Rating
from schemas import Book as BookSchema, BookCreate, BookUpdate, Recommendation
from recommendation import RecommendationEngine
from ai_analyzer import AIBookAnalyzer

router = APIRouter()

# 创建AI分析器实例
ai_analyzer = AIBookAnalyzer()

@router.post("/", response_model=BookSchema)
async def create_book(book: BookCreate, db: Session = Depends(get_db)):
    # 检查ISBN是否已存在
    db_book = db.query(Book).filter(Book.isbn == book.isbn).first()
    if db_book:
        raise HTTPException(status_code=400, detail="Book with this ISBN already exists")
    
    # 创建新书籍
    db_book = Book(
        title=book.title,
        isbn=book.isbn,
        publication_date=book.publication_date,
        publisher=book.publisher,
        description=book.description,
        cover_url=book.cover_url
    )
    
    # 添加作者
    for author_id in book.author_ids:
        author = db.query(Author).filter(Author.id == author_id).first()
        if author:
            db_book.authors.append(author)
    
    db.add(db_book)
    db.commit()
    db.refresh(db_book)
    return db_book

@router.get("/", response_model=List[BookSchema])
async def get_books(
    skip: int = 0,
    limit: int = 100,
    title: Optional[str] = None,
    author: Optional[str] = None,
    db: Session = Depends(get_db)
):
    query = db.query(Book)
    
    if title:
        query = query.filter(Book.title.ilike(f"%{title}%"))
    
    if author:
        query = query.join(Book.authors).filter(Author.name.ilike(f"%{author}%"))
    
    books = query.offset(skip).limit(limit).all()
    return books

@router.get("/{book_id}", response_model=BookSchema)
async def get_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    return db_book

@router.put("/{book_id}", response_model=BookSchema)
async def update_book(book_id: int, book: BookUpdate, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # 更新基本信息
    update_data = book.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        if field != "author_ids":
            setattr(db_book, field, value)
    
    # 更新作者
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
async def delete_book(book_id: int, db: Session = Depends(get_db)):
    db_book = db.query(Book).filter(Book.id == book_id).first()
    if not db_book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    db.delete(db_book)
    db.commit()
    return {"message": "Book deleted successfully"}

@router.get("/recommendations/{user_id}", response_model=List[Recommendation])
async def get_recommendations(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    # 获取用户已评分的书籍
    user_ratings = db.query(Rating).filter(Rating.user_id == user_id).all()
    if not user_ratings:
        # 如果用户没有评分，返回评分最高的书籍
        top_books = db.query(Book).order_by(Book.average_rating.desc()).limit(limit).all()
        return [Recommendation(book=book, score=book.average_rating) for book in top_books]
    
    # 基于用户评分的简单推荐算法
    # 1. 获取用户喜欢的书籍（评分>=4）
    liked_book_ids = [r.book_id for r in user_ratings if r.rating >= 4]
    
    # 2. 获取这些书籍的所有作者
    liked_authors = set()
    for book_id in liked_book_ids:
        book = db.query(Book).filter(Book.id == book_id).first()
        if book:
            for author in book.authors:
                liked_authors.add(author.id)
    
    # 3. 推荐这些作者的其他书籍
    recommended_books = db.query(Book).join(Book.authors).filter(
        Author.id.in_(liked_authors),
        ~Book.id.in_([r.book_id for r in user_ratings])
    ).distinct().limit(limit).all()
    
    if not recommended_books:
        # 如果没有推荐，返回评分最高的书籍
        top_books = db.query(Book).order_by(Book.average_rating.desc()).limit(limit).all()
        return [Recommendation(book=book, score=book.average_rating) for book in top_books]
    
    return [Recommendation(book=book, score=book.average_rating) for book in recommended_books]

@router.get("/recommendations/content/{book_id}", response_model=List[Recommendation])
async def get_content_based_recommendations(book_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """基于内容的推荐"""
    engine = RecommendationEngine(db)
    recommendations = engine.get_content_based_recommendations(book_id, limit)
    return [Recommendation(book=book, score=score) for book, score in recommendations]

@router.get("/recommendations/collaborative/{user_id}", response_model=List[Recommendation])
async def get_collaborative_recommendations(user_id: int, limit: int = 10, db: Session = Depends(get_db)):
    """基于协同过滤的推荐"""
    engine = RecommendationEngine(db)
    recommendations = engine.get_collaborative_filtering_recommendations(user_id, limit)
    return [Recommendation(book=book, score=score) for book, score in recommendations]

@router.get("/recommendations/hybrid/{user_id}", response_model=List[Recommendation])
async def get_hybrid_recommendations(user_id: int, book_id: Optional[int] = None, limit: int = 10, db: Session = Depends(get_db)):
    """混合推荐，结合内容和协同过滤"""
    engine = RecommendationEngine(db)
    recommendations = engine.get_hybrid_recommendations(user_id, book_id, limit)
    return [Recommendation(book=book, score=score) for book, score in recommendations]

@router.get("/analyze/{book_id}", response_model=Dict)
async def analyze_book(book_id: int, db: Session = Depends(get_db)):
    """使用AI分析书籍内容"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # 使用AI分析器分析书籍内容
    analysis = ai_analyzer.analyze_book_content(book.title, book.description)
    return analysis

@router.get("/review/{book_id}")
async def generate_book_review(book_id: int, db: Session = Depends(get_db)):
    """生成书籍评论"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # 生成书籍评论
    review = ai_analyzer.generate_book_review(book.title, book.description, book.average_rating)
    return {"review": review}

@router.get("/concepts/{book_id}")
async def extract_key_concepts(book_id: int, db: Session = Depends(get_db)):
    """提取书籍关键概念"""
    book = db.query(Book).filter(Book.id == book_id).first()
    if not book:
        raise HTTPException(status_code=404, detail="Book not found")
    
    # 提取关键概念
    concepts = ai_analyzer.extract_key_concepts(book.description)
    return {"concepts": concepts}