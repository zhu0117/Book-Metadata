# Book Metadata API Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [API Endpoints](#api-endpoints)
4. [Data Models](#data-models)
5. [Error Handling](#error-handling)
6. [Deployment](#deployment)

## Introduction

The Book Metadata API is a RESTful API for managing book metadata, user authentication, and ratings. Built with FastAPI and SQLAlchemy.

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- SQLite (default) or PostgreSQL

### Installation

1. Clone the repository
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```
3. Import sample data:
   ```bash
   python import_data.py
   ```
4. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

### Accessing the API

- API base URL: `http://localhost:8000`
- Swagger UI: `http://localhost:8000/docs`
- ReDoc: `http://localhost:8000/redoc`

## API Endpoints

### Authentication

#### Register User
```
POST /api/auth/register
```
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "password123"
}
```

#### Login
```
POST /api/auth/login
```
Form data: `username`, `password`

Response:
```json
{
  "access_token": "eyJhbGc...",
  "token_type": "bearer"
}
```

### Books

#### Get Books List
```
GET /api/books/
```
Parameters:
- `page` (int, default: 1)
- `limit` (int, default: 10)
- `title` (string, optional): Filter by title
- `author` (string, optional): Filter by author name
- `language` (string, optional): Filter by language code
- `sort_by` (string, default: "id")
- `sort_order` (string, "asc" or "desc")

Response:
```json
{
  "items": [...],
  "total": 100,
  "page": 1,
  "size": 10,
  "pages": 10
}
```

#### Get Single Book
```
GET /api/books/{book_id}
```

#### Create Book (Requires Auth)
```
POST /api/books/
```
Header: `Authorization: Bearer <token>`
```json
{
  "title": "Book Title",
  "isbn": "978-1234567890",
  "original_title": "Original Title",
  "publication_year": 2023,
  "cover_url": "https://example.com/cover.jpg",
  "language_code": "en",
  "author_ids": [1, 2]
}
```

#### Update Book (Requires Auth)
```
PUT /api/books/{book_id}
```
Header: `Authorization: Bearer <token>`
```json
{
  "title": "Updated Title"
}
```

#### Delete Book (Requires Auth)
```
DELETE /api/books/{book_id}
```
Header: `Authorization: Bearer <token>`

### Users

#### Get Users List
```
GET /api/users/
```

#### Get Single User
```
GET /api/users/{user_id}
```

### Ratings

#### Get Ratings List
```
GET /api/ratings/
```
Parameters:
- `user_id` (int, optional)
- `book_id` (int, optional)

#### Create Rating (Requires Auth)
```
POST /api/ratings/
```
Header: `Authorization: Bearer <token>`
```json
{
  "book_id": 1,
  "rating": 4.5
}
```

### Recommendations

#### Get Popular Books
```
GET /recommendations/popular
```
Parameters:
- `limit` (int, default: 10)
- `min_rating_count` (int, default: 3)

#### Get Author-Based Recommendations
```
GET /recommendations/authors/{user_id}
```
Parameters:
- `user_id` (int, required)
- `limit` (int, default: 10)

#### Get Collaborative Filtering Recommendations
```
GET /recommendations/collaborative/{user_id}
```
Parameters:
- `user_id` (int, required)
- `limit` (int, default: 10)

#### Get Hybrid Recommendations
```
GET /recommendations/hybrid/{user_id}
```
Parameters:
- `user_id` (int, required)
- `limit` (int, default: 10)

## Data Models

### Book

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| title | String | Book title |
| isbn | String | ISBN (unique) |
| publication_year | Integer | Publication year |
| cover_url | String | Cover image URL |
| language_code | String | Language code (e.g., en, en-US) |
| average_rating | Float | Average rating |
| rating_count | Integer | Number of ratings |
| authors | List[Author] | List of authors |

### Author

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| name | String | Author name |

### User

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| username | String | Unique username |
| email | String | Unique email |
| password_hash | String | Hashed password |

### Rating

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | FK to User |
| book_id | Integer | FK to Book |
| rating | Float | Rating (1-5) |

## Error Handling

| Status Code | Description |
|-------------|-------------|
| 400 | Bad request |
| 401 | Not authenticated |
| 404 | Resource not found |
| 409 | Conflict (e.g., duplicate ISBN) |
| 500 | Internal server error |

## Deployment

### Local Development
```bash
pip install -r requirements.txt
uvicorn main:app --reload
```

### Production
```bash
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | Database connection URL | sqlite:///./books.db |
