# Book Metadata API - Presentation Slides

## Slide 1: Title Slide

**Title:** Book Metadata API
**Subtitle:** RESTful API for Book Management
**Author:** [Your Name]
**Date:** [Presentation Date]

## Slide 2: Project Overview

**Key Points:**
- RESTful API for managing book metadata
- User authentication and authorization system
- Rating functionality for books
- Built with FastAPI and SQLAlchemy

## Slide 3: Technical Stack

**Backend:**
- FastAPI (Python)
- SQLAlchemy (ORM)
- SQLite / PostgreSQL (Database)
- Pydantic (Data Validation)

**Security:**
- JWT Authentication
- Password Hashing

## Slide 4: System Architecture

**Diagram:**
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

## Slide 5: API Endpoints

**Books Endpoints:**
- `GET /api/books/` - Get book list with filtering
- `POST /api/books/` - Create new book
- `GET /api/books/{id}` - Get book details
- `PUT /api/books/{id}` - Update book
- `DELETE /api/books/{id}` - Delete book

**Authentication Endpoints:**
- `POST /api/auth/register` - Register new user
- `POST /api/auth/login` - Login and get token

## Slide 6: Data Models

**Core Entities:**
- **Book** - title, isbn, rating, language, cover, authors
- **Author** - name, books
- **User** - username, email, password
- **Rating** - user ratings for books

**Book Fields:**
- title, isbn, publication_year
- language_code, cover_url
- average_rating, rating_count

## Slide 7: Authentication

**Features:**
- JWT-based authentication
- Secure password hashing
- Bearer token authorization

**Flow:**
1. User registers with username/password
2. User logs in to receive access token
3. Token is sent with protected requests

## Slide 8: API Documentation

**Documentation Options:**
- **Swagger UI** - Interactive API documentation
- **ReDoc** - Clean, responsive documentation
- **Markdown Documentation** - Comprehensive API guide

## Slide 9: Key Features

**Book Management:**
- Create, read, update, delete books
- Filter by title, author, language
- Sort by various fields
- Pagination support

**User Management:**
- User registration and login
- Secure password storage
- JWT token authentication

## Slide 10: Conclusion

**Key Achievements:**
- Fully functional RESTful API
- Clean, modular architecture
- Comprehensive documentation
- Secure authentication

## Slide 11: Q&A

**Title:** Questions & Answers
**Contact Information:** [Your Email / GitHub]
