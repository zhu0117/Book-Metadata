# Book Metadata and Recommendation API

## 项目概述

这是一个使用FastAPI框架开发的书籍元数据和推荐API，提供以下功能：

- 书籍的CRUD操作（创建、读取、更新、删除）
- 用户管理和评分系统
- 基于用户评分和作者相似度的书籍推荐
- 自动生成的API文档

## 技术栈

- **后端框架**: FastAPI
- **数据库**: SQLite (默认) / PostgreSQL
- **ORM**: SQLAlchemy
- **数据验证**: Pydantic
- **API文档**: Swagger UI, ReDoc

## 安装步骤

1. 克隆仓库

2. 安装依赖
   ```bash
   pip install -r requirements.txt
   ```

3. 导入测试数据
   ```bash
   python import_data.py
   ```

4. 启动服务器
   ```bash
   uvicorn main:app --reload
   ```

## 访问API

- API根路径: http://localhost:8000
- Swagger UI文档: http://localhost:8000/docs
- ReDoc文档: http://localhost:8000/redoc

## API端点

### 书籍相关
- `GET /api/books/` - 获取书籍列表
- `POST /api/books/` - 创建新书籍
- `GET /api/books/{book_id}` - 获取书籍详情
- `PUT /api/books/{book_id}` - 更新书籍信息
- `DELETE /api/books/{book_id}` - 删除书籍
- `GET /api/books/recommendations/{user_id}` - 获取书籍推荐

### 用户相关
- `GET /api/users/` - 获取用户列表
- `POST /api/users/` - 创建新用户
- `GET /api/users/{user_id}` - 获取用户详情
- `PUT /api/users/{user_id}` - 更新用户信息
- `DELETE /api/users/{user_id}` - 删除用户

### 评分相关
- `GET /api/ratings/` - 获取评分列表
- `POST /api/ratings/` - 创建新评分
- `GET /api/ratings/{rating_id}` - 获取评分详情
- `PUT /api/ratings/{rating_id}` - 更新评分
- `DELETE /api/ratings/{rating_id}` - 删除评分

## 测试数据

运行 `import_data.py` 脚本会自动创建以下测试数据：

- 2个测试用户: user1, user2
- 测试评分数据
- 注意：由于Google Books API的请求限制，可能无法获取书籍数据，但用户和评分数据会正常创建

## 环境变量

可以通过 `.env` 文件配置以下环境变量：

- `DATABASE_URL` - 数据库连接URL (默认: sqlite:///./books.db)

## 项目结构

```
.
├── main.py              # 主应用文件
├── import_data.py       # 数据导入脚本
├── requirements.txt     # 依赖文件
├── README.md            # 项目说明
├── API_DOCUMENTATION.md # API详细文档
├── TECHNICAL_REPORT.md   # 技术报告
├── PRESENTATION_SLIDES.md # 演示文稿
├── api/                 # API层
│   ├── endpoints/       # 路由端点
│   └── deps.py         # 依赖注入
├── core/               # 核心配置
│   ├── config.py       # 应用配置
│   ├── security.py    # JWT安全
│   └── exceptions.py   # 异常处理
└── db/                  # 数据库层
    ├── models/         # SQLAlchemy模型
    ├── schemas/        # Pydantic schemas
    ├── base.py         # 数据库基类
    ├── session.py      # 数据库会话
    └── init_db.py      # 数据库初始化
```

## 数据库表结构

### books（书籍表）

| 字段 | 类型 | 约束 | 含义 |
|------|------|------|------|
| `id` | Integer | PK, 索引 | 书籍唯一标识符 |
| `title` | String | 索引 | 书籍标题 |
| `isbn` | String | **唯一** | 国际标准书号 |
| `publication_date` | Date | - | 出版日期 |
| `publisher` | String | - | 出版社名称 |
| `description` | String | - | 书籍描述 |
| `cover_url` | String | - | 封面图片URL |
| `average_rating` | Float | 默认0.0 | 平均评分 |
| `rating_count` | Integer | 默认0 | 评分次数 |

### authors（作者表）

| 字段 | 类型 | 约束 | 含义 |
|------|------|------|------|
| `id` | Integer | PK, 索引 | 作者唯一标识符 |
| `name` | String | 索引 | 作者姓名 |
| `bio` | String | - | 作者简介 |

### book_author（书籍-作者关联表）

| 字段 | 类型 | 约束 | 含义 |
|------|------|------|------|
| `book_id` | Integer | PK, FK | 关联书籍ID |
| `author_id` | Integer | PK, FK | 关联作者ID |

### users（用户表）

| 字段 | 类型 | 约束 | 含义 |
|------|------|------|------|
| `id` | Integer | PK, 索引 | 用户唯一标识符 |
| `username` | String | **唯一**, 索引 | 用户名 |
| `email` | String | **唯一**, 索引 | 电子邮箱 |
| `password_hash` | String | - | 密码哈希值 |

### ratings（评分表）

| 字段 | 类型 | 约束 | 含义 |
|------|------|------|------|
| `id` | Integer | PK, 索引 | 评分记录ID |
| `user_id` | Integer | FK | 评分用户ID |
| `book_id` | Integer | FK | 被评书籍ID |
| `rating` | Float | - | 评分值(1.0-5.0) |

## 表关系说明

- **Book ↔ Author**: 多对多关系（一本书可有多个作者，一个作者可写多本书）
- **User → Rating**: 一对多关系（一个用户可给多本书评分）
- **Book → Rating**: 一对多关系（一本书可被多个用户评分）