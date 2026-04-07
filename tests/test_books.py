import pytest
from fastapi.testclient import TestClient
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from db.base import Base
from db.session import get_db
from main import app

# 创建测试数据库引擎
SQLALCHEMY_DATABASE_URL = "sqlite:///./test_books.db"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# 创建测试会话工厂
TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


# 覆盖依赖项，使用测试数据库
def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


app.dependency_overrides[get_db] = override_get_db


# 创建测试客户端
client = TestClient(app)


@pytest.fixture(scope="function")
def setup_database():
    """设置测试数据库"""
    # 创建所有表
    Base.metadata.create_all(bind=engine)
    yield
    # 测试结束后删除所有表
    Base.metadata.drop_all(bind=engine)


@pytest.fixture
def test_user(setup_database):
    """创建测试用户"""
    # 注册用户
    response = client.post(
        "/api/auth/register",
        json={
            "username": "testuser",
            "email": "test@example.com",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    
    # 登录获取令牌
    response = client.post(
        "/api/auth/login",
        data={
            "username": "testuser",
            "password": "testpassword"
        }
    )
    assert response.status_code == 200
    token = response.json()["access_token"]
    
    return {"username": "testuser", "token": token}


@pytest.fixture
def test_book(test_user, setup_database):
    """创建测试书籍"""
    response = client.post(
        "/api/books/",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        json={
            "title": "Test Book",
            "isbn": "9781234567890",
            "publication_date": "2023-01-01",
            "publisher": "Test Publisher",
            "description": "Test book description",
            "cover_url": "https://example.com/cover.jpg",
            "author_ids": []
        }
    )
    assert response.status_code == 200
    return response.json()


def test_root():
    """测试根路径"""
    response = client.get("/")
    assert response.status_code == 200
    assert "message" in response.json()


def test_health_check():
    """测试健康检查"""
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json()["status"] == "healthy"


def test_register_user(setup_database):
    """测试用户注册"""
    response = client.post(
        "/api/auth/register",
        json={
            "username": "newuser",
            "email": "new@example.com",
            "password": "newpassword"
        }
    )
    assert response.status_code == 200
    assert "username" in response.json()
    assert response.json()["username"] == "newuser"


def test_login_user(setup_database):
    """测试用户登录"""
    # 先注册用户
    client.post(
        "/api/auth/register",
        json={
            "username": "loginuser",
            "email": "login@example.com",
            "password": "loginpassword"
        }
    )
    
    # 登录
    response = client.post(
        "/api/auth/login",
        data={
            "username": "loginuser",
            "password": "loginpassword"
        }
    )
    assert response.status_code == 200
    assert "access_token" in response.json()


def test_create_book(test_user):
    """测试创建书籍"""
    response = client.post(
        "/api/books/",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        json={
            "title": "New Test Book",
            "isbn": "9780987654321",
            "publication_date": "2023-02-01",
            "publisher": "New Publisher",
            "description": "New test book description",
            "cover_url": "https://example.com/newcover.jpg",
            "author_ids": []
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "New Test Book"
    assert response.json()["isbn"] == "9780987654321"


def test_get_books(setup_database):
    """测试获取书籍列表"""
    response = client.get("/api/books/")
    assert response.status_code == 200
    assert "items" in response.json()
    assert "total" in response.json()


def test_get_book(test_book):
    """测试获取书籍详情"""
    book_id = test_book["id"]
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == 200
    assert response.json()["id"] == book_id
    assert response.json()["title"] == "Test Book"


def test_update_book(test_user, test_book):
    """测试更新书籍"""
    book_id = test_book["id"]
    response = client.put(
        f"/api/books/{book_id}",
        headers={"Authorization": f"Bearer {test_user['token']}"},
        json={
            "title": "Updated Test Book",
            "description": "Updated test book description"
        }
    )
    assert response.status_code == 200
    assert response.json()["title"] == "Updated Test Book"
    assert response.json()["description"] == "Updated test book description"


def test_delete_book(test_user, test_book):
    """测试删除书籍"""
    book_id = test_book["id"]
    response = client.delete(
        f"/api/books/{book_id}",
        headers={"Authorization": f"Bearer {test_user['token']}"}
    )
    assert response.status_code == 200
    assert response.json()["message"] == "Book deleted successfully"
    
    # 验证书籍已删除
    response = client.get(f"/api/books/{book_id}")
    assert response.status_code == 404


def test_get_recommendations(setup_database):
    """测试获取推荐"""
    response = client.get("/api/books/recommendations/1")
    assert response.status_code == 200
    assert isinstance(response.json(), list)
