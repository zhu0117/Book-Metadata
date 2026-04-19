from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from db.init_db import init_db
from api.endpoints import auth, books, ratings, recommendations

init_db()

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API for managing book metadata and providing book recommendations",
    debug=settings.DEBUG
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth.router)
app.include_router(books.router)
app.include_router(ratings.router)
app.include_router(recommendations.router)


@app.on_event("startup")
async def startup_event():
    from import_books_from_csv import import_books_from_csv
    from db.session import SessionLocal
    from db.models.book import Book
    import os

    db = SessionLocal()
    try:
        existing_count = db.query(Book).count()
        if existing_count == 0:
            csv_path = os.path.join(os.path.dirname(__file__), "data", "books.csv")
            if os.path.exists(csv_path):
                imported, skipped = import_books_from_csv(csv_path, limit=200)
                print(f"Auto-imported {imported} books on startup")
        else:
            print(f"Database already has {existing_count} books, skipping import")
    finally:
        db.close()


@app.get("/")
async def root():
    """根路径"""
    return {
        "message": "Welcome to Book Metadata and Recommendation API",
        "version": settings.APP_VERSION,
        "docs": "/docs"
    }


@app.get("/health")
async def health_check():
    """健康检查"""
    return {"status": "healthy"}