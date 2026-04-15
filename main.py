from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from core.config import settings
from db.init_db import init_db
from api.endpoints import auth, books, ratings, recommendations

# 初始化数据库
init_db()

# 创建FastAPI应用
app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    description="API for managing book metadata and providing book recommendations",
    debug=settings.DEBUG
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(auth.router)
app.include_router(books.router)
app.include_router(ratings.router)
app.include_router(recommendations.router)


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
