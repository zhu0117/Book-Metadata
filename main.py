from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from routers import book, user, rating
from database import engine, Base

# 创建数据库表
Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Book Metadata and Recommendation API",
    description="API for managing book metadata and providing book recommendations",
    version="1.0.0"
)

# 配置CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 在生产环境中应该设置具体的域名
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# 注册路由
app.include_router(book.router, prefix="/api/books", tags=["books"])
app.include_router(user.router, prefix="/api/users", tags=["users"])
app.include_router(rating.router, prefix="/api/ratings", tags=["ratings"])

@app.get("/")
async def root():
    return {"message": "Welcome to Book Metadata and Recommendation API"}