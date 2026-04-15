# Book Metadata and Recommendation API

## 项目概述

这是一个使用FastAPI框架开发的书籍元数据管理API，提供以下功能：

- 书籍的CRUD操作（创建、读取、更新、删除）
- 用户管理和认证系统
- 用户评分功能
- 书籍推荐系统（热门推荐、作者推荐、协同过滤）
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

### 推荐相关
- `GET /recommendations/popular` - 获取热门书籍推荐
- `GET /recommendations/authors/{user_id}` - 基于作者推荐
- `GET /recommendations/collaborative/{user_id}` - 协同过滤推荐
- `GET /recommendations/hybrid/{user_id}` - 混合推荐

## 测试数据

运行 `import_data.py` 脚本会自动创建示例数据，包括测试用户和书籍信息。

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
| `publication_year` | Integer | - | 出版年份 |
| `cover_url` | String | - | 封面图片URL |
| `language_code` | String | - | 语言代码 (如 en, en-US) |
| `average_rating` | Float | 默认0.0 | 平均评分 |
| `rating_count` | Integer | 默认0 | 评分次数 |

### authors（作者表）

| 字段 | 类型 | 约束 | 含义 |
|------|------|------|------|
| `id` | Integer | PK, 索引 | 作者唯一标识符 |
| `name` | String | 索引 | 作者姓名 |

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

## 数据来源

本项目使用 [GoodBooks-10K](https://github.com/zygmuntz/goodbooks-10k) 数据集，包含 10,000 本最受欢迎书籍的元数据、评分和标签信息。

运行以下命令导入数据：
```bash
python import_data.py        # 导入用户
python import_books_from_csv.py  # 导入书籍
python generate_test_ratings.py  # 生成测试评分数据
```