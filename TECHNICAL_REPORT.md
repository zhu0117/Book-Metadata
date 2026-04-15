# Book Metadata API - Technical Report

## 1. Introduction

The Book Metadata API is a RESTful API designed to manage book metadata, user authentication, and ratings. This report outlines the technical design decisions and implementation details of the project.

## 2. Technology Stack

### 2.1 Backend Framework

**FastAPI** was chosen as the backend framework because:
- **Performance**: Built on Starlette and Pydantic with asynchronous capabilities
- **Automatic Documentation**: Generates interactive API documentation using Swagger UI and ReDoc
- **Type Safety**: Uses Pydantic for data validation and type hints
- **Modern Python Features**: Leverages Python 3.7+ features including type annotations

### 2.2 Database

**SQLite** for development/testing:
- **Simplicity**: No separate server process required
- **Portability**: Single file database, easy to distribute

**PostgreSQL** supported for production:
- **Scalability**: Better performance for large datasets
- **Reliability**: Robust ACID compliance

### 2.3 ORM

**SQLAlchemy** provides:
- **Flexibility**: Multiple database backend support
- **Relationship Management**: Handles complex data relationships
- **Migration Support**: Schema migrations through Alembic

## 3. System Architecture

### 3.1 Architecture Diagram

```
┌─────────────────┐
│   Client Apps   │
└─────────┬───────┘
          │
┌─────────▼───────┐
│  FastAPI Server │
└─────────┬───────┘
          │
┌─────────▼───────┐
│  API Endpoints  │
└─────────┬───────┘
          │
┌─────────▼───────┐
│  Data Models    │
└─────────┬───────┘
          │
┌─────────▼───────┐
│   Database      │
└─────────────────┘
```

### 3.2 Component Details

#### API Endpoints
- **Books Endpoints**: CRUD operations for books with filtering and searching
- **Auth Endpoints**: User registration and JWT authentication
- **Rating Endpoints**: User ratings for books
- **Recommendation Endpoints**: Popular books, author-based, and collaborative filtering

#### Data Models
- **Book**: Stores book metadata and author relationships
- **Author**: Manages author information
- **User**: Handles user profiles and authentication
- **Rating**: Tracks user ratings for books

## 4. Data Model Design

### 4.1 Database Schema

**Books Table:**
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| title | String | Book title |
| isbn | String | ISBN (unique) |
| publication_year | Integer | Publication year |
| cover_url | String | Cover image URL |
| language_code | String | Language code |
| average_rating | Float | Average rating |
| rating_count | Integer | Rating count |

**Authors Table:**
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| name | String | Author name |

**Users Table:**
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| username | String | Unique username |
| email | String | Unique email |
| password_hash | String | Hashed password |

**Ratings Table:**
| Field | Type | Description |
|-------|------|-------------|
| id | Integer | Primary key |
| user_id | Integer | FK to User |
| book_id | Integer | FK to Book |
| rating | Float | Rating (1-5) |

### 4.2 Relationships

- **Book ↔ Author**: Many-to-Many (via book_author table)
- **User → Rating**: One-to-Many
- **Book → Rating**: One-to-Many

## 5. API Design

### 5.1 RESTful Principles

- **Resource-Oriented**: Endpoints organized around resources
- **Consistent Naming**: Standard naming conventions
- **Proper Status Codes**: Appropriate HTTP status codes
- **Error Handling**: Clear error messages

### 5.2 Key Features

- **Pagination**: Page-based result sets
- **Filtering**: By title, author, language
- **Sorting**: Ascending/descending order
- **Authentication**: JWT Bearer token

## 6. Security

### 6.1 Authentication

- **JWT Tokens**: Stateless authentication
- **Password Hashing**: Secure password storage using bcrypt
- **Token Expiration**: 30-minute token lifetime

### 6.2 Authorization

- **Protected Endpoints**: Write operations require valid JWT
- **User Isolation**: Users can only modify their own data

## 7. Testing

### 7.1 Test Coverage

- **CRUD Operations**: Create, read, update, delete for books
- **Authentication**: Registration and login flows
- **Error Handling**: Invalid input handling

### 7.2 Testing Tools

- **pytest**: Unit testing framework
- **TestClient**: API endpoint testing

## 8. Recommendation System

### 8.1 Algorithm Overview

The recommendation system implements three recommendation strategies:

1. **Popular Books Recommendation**
   - Filters books by minimum rating count
   - Sorts by average rating and rating count
   - Returns highly-rated books with sufficient user engagement

2. **Author-Based Recommendation**
   - Analyzes user's rated books to identify preferred authors
   - Recommends other books by the same authors
   - Excludes books the user has already rated

3. **Collaborative Filtering**
   - Implements user-based collaborative filtering using Pearson correlation coefficient
   - Finds similar users based on rating patterns
   - Recommends books liked by similar users that the target user hasn't rated

### 8.2 Similarity Calculation

The system uses Pearson correlation coefficient to measure user similarity:

```
r = Σ((x_i - x̄)(y_i - ȳ)) / √(Σ(x_i - x̄)² × Σ(y_i - ȳ)²)
```

Where:
- x_i and y_i are ratings given by two users for the same book
- x̄ and ȳ are the mean ratings of each user

### 8.3 Hybrid Approach

The hybrid recommendation combines popular books and author-based recommendations to provide diverse, high-quality suggestions.

## 9. Future Development

### 9.1 Planned Features

- [x] Book recommendation system (Implemented)
- AI-powered book analysis
- Enhanced search functionality
- User profile management

### 9.2 Technical Roadmap

1. [x] Add recommendation algorithms (Implemented)
2. Integrate AI analysis features
3. Implement advanced search
4. Add social features

## 10. Conclusion

The Book Metadata API provides a solid foundation for book management with:
- Clean, modular architecture
- Secure authentication
- Comprehensive documentation
- Extensible design for future features
- [x] Book recommendation system with multiple algorithms

## 11. References

- FastAPI: https://fastapi.tiangolo.com/
- SQLAlchemy: https://docs.sqlalchemy.org/
- Pydantic: https://docs.pydantic.dev/
