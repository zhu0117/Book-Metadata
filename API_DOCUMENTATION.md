# Book Metadata and Recommendation API Documentation

## Table of Contents

1. [Introduction](#introduction)
2. [Getting Started](#getting-started)
3. [API Endpoints](#api-endpoints)
   - [Books](#books)
   - [Users](#users)
   - [Ratings](#ratings)
4. [Data Models](#data-models)
5. [Recommendation System](#recommendation-system)
6. [AI Analysis Features](#ai-analysis-features)
7. [Error Handling](#error-handling)
8. [Examples](#examples)
9. [Deployment](#deployment)

## Introduction

The Book Metadata and Recommendation API is a comprehensive system designed to manage book metadata, user ratings, and provide intelligent book recommendations. It leverages modern technologies including FastAPI, SQLAlchemy, and machine learning to deliver a high-quality user experience.

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
3. Import test data:
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

### Books

#### `GET /api/books/`

Retrieve a list of books with optional filtering.

**Parameters:**
- `skip` (int, optional): Number of books to skip (default: 0)
- `limit` (int, optional): Maximum number of books to return (default: 100)
- `title` (string, optional): Filter books by title (case-insensitive)
- `author` (string, optional): Filter books by author name (case-insensitive)

**Response:**
```json
[
  {
    "id": 1,
    "title": "Python Programming",
    "isbn": "9781234567890",
    "publication_date": "2023-01-01",
    "publisher": "Tech Press",
    "description": "A comprehensive guide to Python programming",
    "cover_url": "https://example.com/cover.jpg",
    "average_rating": 4.5,
    "rating_count": 100,
    "authors": [
      {
        "id": 1,
        "name": "John Doe",
        "bio": "Python expert and author"
      }
    ]
  }
]
```

#### `POST /api/books/`

Create a new book.

**Request Body:**
```json
{
  "title": "New Book",
  "isbn": "9780987654321",
  "publication_date": "2023-01-01",
  "publisher": "Publisher Inc.",
  "description": "Book description",
  "cover_url": "https://example.com/cover.jpg",
  "author_ids": [1, 2]
}
```

**Response:**
```json
{
  "id": 2,
  "title": "New Book",
  "isbn": "9780987654321",
  "publication_date": "2023-01-01",
  "publisher": "Publisher Inc.",
  "description": "Book description",
  "cover_url": "https://example.com/cover.jpg",
  "average_rating": 0.0,
  "rating_count": 0,
  "authors": [
    {
      "id": 1,
      "name": "John Doe",
      "bio": "Python expert and author"
    }
  ]
}
```

#### `GET /api/books/{book_id}`

Retrieve a single book by ID.

**Parameters:**
- `book_id` (int, required): ID of the book to retrieve

**Response:**
```json
{
  "id": 1,
  "title": "Python Programming",
  "isbn": "9781234567890",
  "publication_date": "2023-01-01",
  "publisher": "Tech Press",
  "description": "A comprehensive guide to Python programming",
  "cover_url": "https://example.com/cover.jpg",
  "average_rating": 4.5,
  "rating_count": 100,
  "authors": [
    {
      "id": 1,
      "name": "John Doe",
      "bio": "Python expert and author"
    }
  ]
}
```

#### `PUT /api/books/{book_id}`

Update a book by ID.

**Parameters:**
- `book_id` (int, required): ID of the book to update

**Request Body:**
```json
{
  "title": "Updated Book Title",
  "description": "Updated description"
}
```

**Response:**
```json
{
  "id": 1,
  "title": "Updated Book Title",
  "isbn": "9781234567890",
  "publication_date": "2023-01-01",
  "publisher": "Tech Press",
  "description": "Updated description",
  "cover_url": "https://example.com/cover.jpg",
  "average_rating": 4.5,
  "rating_count": 100,
  "authors": [
    {
      "id": 1,
      "name": "John Doe",
      "bio": "Python expert and author"
    }
  ]
}
```

#### `DELETE /api/books/{book_id}`

Delete a book by ID.

**Parameters:**
- `book_id` (int, required): ID of the book to delete

**Response:**
```json
{
  "message": "Book deleted successfully"
}
```

#### `GET /api/books/recommendations/{user_id}`

Get book recommendations for a user.

**Parameters:**
- `user_id` (int, required): ID of the user
- `limit` (int, optional): Maximum number of recommendations (default: 10)

**Response:**
```json
[
  {
    "book": {
      "id": 2,
      "title": "Data Science Basics",
      "isbn": "9781122334455",
      "publication_date": "2023-02-01",
      "publisher": "Data Press",
      "description": "Introduction to data science",
      "cover_url": "https://example.com/cover2.jpg",
      "average_rating": 4.2,
      "rating_count": 50,
      "authors": [
        {
          "id": 2,
          "name": "Jane Smith",
          "bio": "Data scientist and author"
        }
      ]
    },
    "score": 4.2
  }
]
```

#### `GET /api/books/recommendations/content/{book_id}`

Get content-based recommendations for a book.

**Parameters:**
- `book_id` (int, required): ID of the book
- `limit` (int, optional): Maximum number of recommendations (default: 10)

**Response:**
```json
[
  {
    "book": {
      "id": 3,
      "title": "Advanced Python",
      "isbn": "9785566778899",
      "publication_date": "2023-03-01",
      "publisher": "Tech Press",
      "description": "Advanced Python programming techniques",
      "cover_url": "https://example.com/cover3.jpg",
      "average_rating": 4.7,
      "rating_count": 75,
      "authors": [
        {
          "id": 1,
          "name": "John Doe",
          "bio": "Python expert and author"
        }
      ]
    },
    "score": 0.95
  }
]
```

#### `GET /api/books/recommendations/collaborative/{user_id}`

Get collaborative filtering recommendations for a user.

**Parameters:**
- `user_id` (int, required): ID of the user
- `limit` (int, optional): Maximum number of recommendations (default: 10)

**Response:**
```json
[
  {
    "book": {
      "id": 4,
      "title": "Machine Learning Fundamentals",
      "isbn": "9789988776655",
      "publication_date": "2023-04-01",
      "publisher": "AI Press",
      "description": "Introduction to machine learning",
      "cover_url": "https://example.com/cover4.jpg",
      "average_rating": 4.8,
      "rating_count": 120,
      "authors": [
        {
          "id": 3,
          "name": "Bob Johnson",
          "bio": "Machine learning expert"
        }
      ]
    },
    "score": 4.5
  }
]
```

#### `GET /api/books/recommendations/hybrid/{user_id}`

Get hybrid recommendations for a user (combines content-based and collaborative filtering).

**Parameters:**
- `user_id` (int, required): ID of the user
- `book_id` (int, optional): ID of a book to use as context
- `limit` (int, optional): Maximum number of recommendations (default: 10)

**Response:**
```json
[
  {
    "book": {
      "id": 5,
      "title": "Deep Learning Essentials",
      "isbn": "9781237894561",
      "publication_date": "2023-05-01",
      "publisher": "AI Press",
      "description": "Essential concepts in deep learning",
      "cover_url": "https://example.com/cover5.jpg",
      "average_rating": 4.9,
      "rating_count": 150,
      "authors": [
        {
          "id": 3,
          "name": "Bob Johnson",
          "bio": "Machine learning expert"
        }
      ]
    },
    "score": 0.92
  }
]
```

#### `GET /api/books/analyze/{book_id}`

Analyze book content using AI.

**Parameters:**
- `book_id` (int, required): ID of the book to analyze

**Response:**
```json
{
  "summary": "Python Programming is a comprehensive guide that explores key concepts and practical applications in its field.",
  "themes": ["Technology", "Innovation", "Practical Applications", "Future Trends"],
  "target_audience": "Students, professionals, and enthusiasts interested in the subject matter",
  "similar_books": [
    "Introduction to Similar Topics",
    "Advanced Concepts in the Field",
    "Practical Guide to Implementation",
    "Future Trends and Predictions",
    "Case Studies and Real-World Applications"
  ],
  "benefits": [
    "Gain a deep understanding of core concepts",
    "Learn practical skills and techniques",
    "Stay updated with the latest developments",
    "Enhance professional knowledge and expertise",
    "Develop critical thinking and problem-solving abilities"
  ]
}
```

#### `GET /api/books/review/{book_id}`

Generate a book review using AI.

**Parameters:**
- `book_id` (int, required): ID of the book to review

**Response:**
```json
{
  "review": "This is a mock review for Python Programming. Based on the description, this book appears to be a valuable resource for readers interested in the subject matter. With a rating of 4.5/5, it seems to be well-received by readers."
}
```

#### `GET /api/books/concepts/{book_id}`

Extract key concepts from a book using AI.

**Parameters:**
- `book_id` (int, required): ID of the book

**Response:**
```json
{
  "concepts": ["Technology", "Innovation", "Programming", "Development", "Research"]
}
```

### Users

#### `GET /api/users/`

Retrieve a list of users.

**Parameters:**
- `skip` (int, optional): Number of users to skip (default: 0)
- `limit` (int, optional): Maximum number of users to return (default: 100)

**Response:**
```json
[
  {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com"
  }
]
```

#### `POST /api/users/`

Create a new user.

**Request Body:**
```json
{
  "username": "newuser",
  "email": "newuser@example.com",
  "password": "password123"
}
```

**Response:**
```json
{
  "id": 3,
  "username": "newuser",
  "email": "newuser@example.com"
}
```

#### `GET /api/users/{user_id}`

Retrieve a single user by ID.

**Parameters:**
- `user_id` (int, required): ID of the user to retrieve

**Response:**
```json
{
  "id": 1,
  "username": "user1",
  "email": "user1@example.com"
}
```

#### `PUT /api/users/{user_id}`

Update a user by ID.

**Parameters:**
- `user_id` (int, required): ID of the user to update

**Request Body:**
```json
{
  "username": "updateduser",
  "email": "updateduser@example.com",
  "password": "newpassword123"
}
```

**Response:**
```json
{
  "id": 1,
  "username": "updateduser",
  "email": "updateduser@example.com"
}
```

#### `DELETE /api/users/{user_id}`

Delete a user by ID.

**Parameters:**
- `user_id` (int, required): ID of the user to delete

**Response:**
```json
{
  "message": "User deleted successfully"
}
```

### Ratings

#### `GET /api/ratings/`

Retrieve a list of ratings with optional filtering.

**Parameters:**
- `skip` (int, optional): Number of ratings to skip (default: 0)
- `limit` (int, optional): Maximum number of ratings to return (default: 100)
- `user_id` (int, optional): Filter ratings by user ID
- `book_id` (int, optional): Filter ratings by book ID

**Response:**
```json
[
  {
    "id": 1,
    "book_id": 1,
    "rating": 5.0,
    "user": {
      "id": 1,
      "username": "user1",
      "email": "user1@example.com"
    },
    "book": {
      "id": 1,
      "title": "Python Programming",
      "isbn": "9781234567890",
      "publication_date": "2023-01-01",
      "publisher": "Tech Press",
      "description": "A comprehensive guide to Python programming",
      "cover_url": "https://example.com/cover.jpg",
      "average_rating": 4.5,
      "rating_count": 100,
      "authors": [
        {
          "id": 1,
          "name": "John Doe",
          "bio": "Python expert and author"
        }
      ]
    }
  }
]
```

#### `POST /api/ratings/`

Create a new rating.

**Request Body:**
```json
{
  "book_id": 1,
  "rating": 4.5,
  "user_id": 1
}
```

**Response:**
```json
{
  "id": 2,
  "book_id": 1,
  "rating": 4.5,
  "user": {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com"
  },
  "book": {
    "id": 1,
    "title": "Python Programming",
    "isbn": "9781234567890",
    "publication_date": "2023-01-01",
    "publisher": "Tech Press",
    "description": "A comprehensive guide to Python programming",
    "cover_url": "https://example.com/cover.jpg",
    "average_rating": 4.75,
    "rating_count": 101,
    "authors": [
      "id": 1,
      "name": "John Doe",
      "bio": "Python expert and author"
    ]
  }
}
```

#### `GET /api/ratings/{rating_id}`

Retrieve a single rating by ID.

**Parameters:**
- `rating_id` (int, required): ID of the rating to retrieve

**Response:**
```json
{
  "id": 1,
  "book_id": 1,
  "rating": 5.0,
  "user": {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com"
  },
  "book": {
    "id": 1,
    "title": "Python Programming",
    "isbn": "9781234567890",
    "publication_date": "2023-01-01",
    "publisher": "Tech Press",
    "description": "A comprehensive guide to Python programming",
    "cover_url": "https://example.com/cover.jpg",
    "average_rating": 4.5,
    "rating_count": 100,
    "authors": [
      "id": 1,
      "name": "John Doe",
      "bio": "Python expert and author"
    ]
  }
}
```

#### `PUT /api/ratings/{rating_id}`

Update a rating by ID.

**Parameters:**
- `rating_id` (int, required): ID of the rating to update

**Request Body:**
```json
{
  "book_id": 1,
  "rating": 5.0,
  "user_id": 1
}
```

**Response:**
```json
{
  "id": 1,
  "book_id": 1,
  "rating": 5.0,
  "user": {
    "id": 1,
    "username": "user1",
    "email": "user1@example.com"
  },
  "book": {
    "id": 1,
    "title": "Python Programming",
    "isbn": "9781234567890",
    "publication_date": "2023-01-01",
    "publisher": "Tech Press",
    "description": "A comprehensive guide to Python programming",
    "cover_url": "https://example.com/cover.jpg",
    "average_rating": 4.8,
    "rating_count": 100,
    "authors": [
      "id": 1,
      "name": "John Doe",
      "bio": "Python expert and author"
    ]
  }
}
```

#### `DELETE /api/ratings/{rating_id}`

Delete a rating by ID.

**Parameters:**
- `rating_id` (int, required): ID of the rating to delete

**Response:**
```json
{
  "message": "Rating deleted successfully"
}
```

## Data Models

### Book

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| title | String | Book title |
| isbn | String | International Standard Book Number |
| publication_date | Date | Publication date |
| publisher | String | Publisher name |
| description | String | Book description |
| cover_url | String | URL to book cover image |
| average_rating | Float | Average rating from users |
| rating_count | Integer | Number of ratings |
| authors | List[Author] | List of authors |

### Author

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| name | String | Author name |
| bio | String | Author biography |
| books | List[Book] | List of books written by the author |

### User

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| username | String | Unique username |
| email | String | Unique email address |
| password_hash | String | Hashed password |
| ratings | List[Rating] | List of ratings made by the user |

### Rating

| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | Foreign key to User |
| book_id | Integer | Foreign key to Book |
| rating | Float | Rating value (1-5) |

## Recommendation System

The API implements three types of recommendation systems:

1. **Content-based filtering**: Recommends books similar to a given book based on content (title, description, authors).

2. **Collaborative filtering**: Recommends books based on the preferences of similar users.

3. **Hybrid filtering**: Combines both content-based and collaborative filtering for more accurate recommendations.

## AI Analysis Features

The API includes several AI-powered features:

1. **Book content analysis**: Analyzes book content to provide summaries, key themes, target audience, similar book recommendations, and potential benefits.

2. **Book review generation**: Generates reviews based on book metadata and ratings.

3. **Key concept extraction**: Extracts key concepts from book descriptions.

## Error Handling

The API uses standard HTTP status codes to indicate errors:

| Status Code | Description |
|-------------|-------------|
| 400 | Bad request |
| 404 | Resource not found |
| 500 | Internal server error |

## Examples

### Example 1: Get book recommendations

```bash
curl "http://localhost:8000/api/books/recommendations/1?limit=5"
```

### Example 2: Create a new book

```bash
curl -X POST "http://localhost:8000/api/books/" \
  -H "Content-Type: application/json" \
  -d '{
    "title": "Machine Learning for Beginners",
    "isbn": "9781234567891",
    "publication_date": "2023-06-01",
    "publisher": "AI Press",
    "description": "A beginner-friendly introduction to machine learning",
    "cover_url": "https://example.com/ml-beginners.jpg",
    "author_ids": [1, 3]
  }'
```

### Example 3: Analyze a book

```bash
curl "http://localhost:8000/api/books/analyze/1"
```

## Deployment

### Local Development

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the server:
   ```bash
   uvicorn main:app --reload
   ```

### Production Deployment

1. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

2. Start the server with production settings:
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
   ```

### Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| DATABASE_URL | Database connection URL | sqlite:///./books.db |
| OPENAI_API_KEY | API key for OpenAI (optional) | None |
