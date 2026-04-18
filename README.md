# Book Metadata and Recommendation API

## Project Links

- **GitHub Repository**: [https://github.com/zhu0117/Book-Metadata.git](https://github.com/zhu0117/Book-Metadata.git)
- **API Documentation (PDF)**: [To be added]
- **Technical Report (PDF)**: [To be added]
- **Presentation Slides (PPTX)**: [To be added]
- **Deployment URL**: https://book-metadata-production.up.railway.app

## Project Overview

This is a book metadata management API developed using FastAPI framework, providing the following features:

- Books CRUD operations (Create, Read, Update, Delete)
- User management and authentication system
- User rating functionality
- Book recommendation system (popular, author-based, collaborative filtering)
- Automatically generated API documentation

## Technology Stack

- **Backend Framework**: FastAPI
- **Database**: SQLite (default) / PostgreSQL
- **ORM**: SQLAlchemy
- **Data Validation**: Pydantic
- **API Documentation**: Swagger UI, ReDoc

## Installation Steps

1. Clone the repository

2. Install dependencies
   ```bash
   pip install -r requirements.txt
   ```

3. Import test data
   ```bash
   python import_data.py
   ```

4. Start the server
   ```bash
   uvicorn main:app --reload
   ```

## API Access

- API root path: http://localhost:8000
- Swagger UI documentation: http://localhost:8000/docs
- ReDoc documentation: http://localhost:8000/redoc

## API Endpoints

### Books
- `GET /api/books/` - Get book list
- `POST /api/books/` - Create new book
- `GET /api/books/{book_id}` - Get book details
- `PUT /api/books/{book_id}` - Update book information
- `DELETE /api/books/{book_id}` - Delete book

### Users
- `GET /api/users/` - Get user list
- `POST /api/users/` - Create new user
- `GET /api/users/{user_id}` - Get user details
- `PUT /api/users/{user_id}` - Update user information
- `DELETE /api/users/{user_id}` - Delete user

### Ratings
- `GET /api/ratings/` - Get rating list
- `POST /api/ratings/` - Create new rating
- `GET /api/ratings/{rating_id}` - Get rating details
- `PUT /api/ratings/{rating_id}` - Update rating
- `DELETE /api/ratings/{rating_id}` - Delete rating

### Recommendations
- `GET /recommendations/popular` - Get popular book recommendations
- `GET /recommendations/authors/{user_id}` - Author-based recommendations
- `GET /recommendations/collaborative/{user_id}` - Collaborative filtering recommendations
- `GET /recommendations/hybrid/{user_id}` - Hybrid recommendations

## Test Data

Running the `import_data.py` script will automatically create sample data, including test users and book information.

## Environment Variables

You can configure the following environment variables through a `.env` file:

- `DATABASE_URL` - Database connection URL (default: sqlite:///./books.db)

## Project Structure

```
.
├── main.py              # Main application file
├── import_data.py       # Data import script
├── requirements.txt     # Dependencies file
├── README.md            # Project description
├── API_DOCUMENTATION.md # API detailed documentation
├── TECHNICAL_REPORT.md   # Technical report
├── PRESENTATION_SLIDES.md # Presentation slides
├── api/                 # API layer
│   ├── endpoints/       # Route endpoints
│   └── deps.py         # Dependency injection
├── core/               # Core configuration
│   ├── config.py       # Application configuration
│   ├── security.py    # JWT security
│   └── exceptions.py   # Exception handling
└── db/                  # Database layer
    ├── models/         # SQLAlchemy models
    ├── schemas/        # Pydantic schemas
    ├── base.py         # Database base class
    ├── session.py      # Database session
    └── init_db.py      # Database initialization
```

## Database Schema

### books (Books Table)

| Field | Type | Constraint | Description |
|------|------|------|------|
| `id` | Integer | PK, Index | Book unique identifier |
| `title` | String | Index | Book title |
| `isbn` | String | **Unique** | International Standard Book Number |
| `publication_year` | Integer | - | Publication year |
| `cover_url` | String | - | Cover image URL |
| `language_code` | String | - | Language code (e.g., en, en-US) |
| `average_rating` | Float | Default 0.0 | Average rating |
| `rating_count` | Integer | Default 0 | Number of ratings |

### authors (Authors Table)

| Field | Type | Constraint | Description |
|------|------|------|------|
| `id` | Integer | PK, Index | Author unique identifier |
| `name` | String | Index | Author name |

### book_author (Book-Author Association Table)

| Field | Type | Constraint | Description |
|------|------|------|------|
| `book_id` | Integer | PK, FK | Associated book ID |
| `author_id` | Integer | PK, FK | Associated author ID |

### users (Users Table)

| Field | Type | Constraint | Description |
|------|------|------|------|
| `id` | Integer | PK, Index | User unique identifier |
| `username` | String | **Unique**, Index | Username |
| `email` | String | **Unique**, Index | Email address |
| `password_hash` | String | - | Password hash |

### ratings (Ratings Table)

| Field | Type | Constraint | Description |
|------|------|------|------|
| `id` | Integer | PK, Index | Rating record ID |
| `user_id` | Integer | FK | Rating user ID |
| `book_id` | Integer | FK | Rated book ID |
| `rating` | Float | - | Rating value (1.0-5.0) |

## Data Source

This project uses the [GoodBooks-10K](https://github.com/zygmuntz/goodbooks-10k) dataset, which contains metadata, ratings, and tag information for 10,000 popular books.

Run the following commands to import data:
```bash
python import_data.py        # Import users
python import_books_from_csv.py  # Import books
python generate_test_ratings.py  # Generate test rating data
```