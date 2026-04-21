# Book Metadata API - Technical Report

## 1. Introduction
The Book Metadata API is a comprehensive RESTful API designed to manage book metadata, user authentication, and ratings. This report outlines the technical design decisions, implementation details, and deployment strategy of the project, providing a complete overview of the system architecture and functionality.

## 2. Technology Stack
### 2.1 Backend Framework
**FastAPI** was chosen as the backend framework for its performance (built on Starlette and Pydantic with asynchronous capabilities), automatic documentation generation using Swagger UI and ReDoc, type safety through Pydantic for data validation, and support for modern Python features including type annotations and async/await.

### 2.2 Database
**SQLite** is used for development and testing due to its simplicity (no separate server process), portability (single file database), and speed for development workflows. **PostgreSQL** is supported for production, offering better scalability for large datasets, robust ACID compliance, and advanced features for complex queries.

### 2.3 ORM
**SQLAlchemy** was selected as the ORM tool for its flexibility (support for multiple database backends), ability to handle complex data relationships and foreign keys, schema migration support through Alembic, and powerful SQL expression language for complex queries.

## 3. System Architecture
### 3.1 Architecture Diagram
```
┌─────────────────┐     ┌─────────────────┐     ┌─────────────────┐
│   Client Apps   │────>│  FastAPI Server │────>│  API Endpoints  │
└─────────────────┘<────└─────────────────┘<────└─────────────────┘
                                    │
                                    ▼
                              ┌─────────────────┐     ┌─────────────────┐
                              │  Data Models    │────>│   Database      │
                              └─────────────────┘<────└─────────────────┘
```

### 3.2 Component Details
#### API Endpoints
The API includes books endpoints for CRUD operations with filtering, sorting, and pagination; authentication endpoints for user registration and JWT-based authentication; rating endpoints for user ratings with validation; and recommendation endpoints offering multiple algorithms for personalized suggestions.

#### Data Models
The data models include Book (storing comprehensive metadata and author relationships), Author (managing author information with many-to-many relationship to books), User (handling profiles and secure authentication), and Rating (tracking user ratings with proper foreign key relationships).

#### Recommendation System
The recommendation system implements multiple algorithms for diverse strategies and provides a hybrid approach for balanced personalization and discovery.

## 4. Data Model Design
### 4.1 Database Schema
**Books Table**:
- id (Integer, Primary Key)
- title (String, Book title)
- isbn (String, Unique ISBN)
- publication_year (Integer, Year of publication)
- cover_url (String, Cover image URL)
- language_code (String, Language identifier)
- average_rating (Float, Average user rating)
- rating_count (Integer, Number of user ratings)

**Authors Table**:
- id (Integer, Primary Key)
- name (String, Author name)

**Users Table**:
- id (Integer, Primary Key)
- username (String, Unique username)
- email (String, Unique email address)
- password_hash (String, Securely hashed password)

**Ratings Table**:
- id (Integer, Primary Key)
- user_id (Integer, Foreign Key to User)
- book_id (Integer, Foreign Key to Book)
- rating (Float, User rating 1-5)

### 4.2 Relationships
- **Book ↔ Author**: Many-to-Many relationship via intermediate book_author table
- **User → Rating**: One-to-Many relationship (one user can rate multiple books)
- **Book → Rating**: One-to-Many relationship (one book can have multiple ratings)

## 5. API Design
### 5.1 RESTful Principles
The API follows standard RESTful design principles, including resource-oriented endpoints organized around books, users, and ratings; consistent naming conventions; appropriate HTTP status codes; and clear error messages.

### 5.2 Key Features
Key features include page-based pagination with configurable page size, filtering by title, author, and language, sorting capabilities, JWT Bearer token authentication for protected endpoints, and comprehensive data validation using Pydantic models.

## 6. Security
### 6.1 Authentication
Authentication uses JWT tokens for stateless verification, secure password hashing with bcrypt, 30-minute token expiration, and support for token refresh without re-login.

### 6.2 Authorization
Authorization ensures write operations require valid JWT tokens, users can only modify their own ratings and profile, and provides a foundation for future role-based permissions.

## 7. Testing
### 7.1 Test Coverage
Test coverage includes CRUD operations, authentication flows, error handling for invalid inputs, and various recommendation scenarios.

### 7.2 Testing Tools
Testing tools include pytest for unit and integration tests, FastAPI's TestClient for API endpoint testing, and SQLite in-memory database for fast, isolated testing.

## 8. Recommendation System
### 8.1 Algorithm Overview
The recommendation system implements three distinct recommendation strategies:

1. **Popular Books Recommendation**
   - Filters books by minimum rating count threshold
   - Sorts by weighted combination of average rating and rating count
   - Returns highly-rated books with sufficient user engagement

2. **Author-Based Recommendation**
   - Analyzes user's rated books to identify preferred authors
   - Recommends other books by the same authors
   - Excludes books the user has already rated

3. **Collaborative Filtering**
   - Implements user-based collaborative filtering using Pearson correlation coefficient
   - Finds similar users based on rating patterns
   - Recommends books liked by similar users that the target user hasn't rated

### 8.2 Hybrid Approach
The hybrid recommendation system combines multiple strategies:
- **Priority Order**: Collaborative Filtering > Author-Based > Popular Books
- **Result Deduplication**: Ensures diverse recommendations
- **Result Limiting**: Returns optimal number of recommendations

## 9. Data Sources
### 9.1 Dataset Information
The project uses the **GoodBooks-10K** dataset, which contains comprehensive metadata and ratings for 10,000 popular books. The dataset is sourced from `https://github.com/zygmuntz/goodbooks-10k` and includes 10,000 books with metadata, ratings, and tags in CSV format, totaling approximately 200MB.

### 9.2 License Information
The dataset is licensed under the MIT License, which allows commercial use, modification, distribution, and private use, with conditions to include copyright and license notices.

## 10. Challenges and Lessons Learned
### 10.1 Challenges Faced
Challenges included significant data preprocessing for the GoodBooks-10K dataset to handle missing values, computational complexity in implementing collaborative filtering with Pearson correlation, ensuring secure JWT implementation, and balancing SQLite for development with PostgreSQL for production.

### 10.2 Testing Methods
Testing methods included unit tests for individual components, integration tests for API endpoints and database interactions, performance testing for concurrent requests, and security testing for authentication flows.

### 10.3 Lessons Learned
Lessons learned include the value of early investment in modular architecture, the importance of comprehensive documentation, the benefits of test-driven development, and the advantages of implementing security measures from the beginning.

## 11. Limitations and Future Improvements
### 11.1 Current Limitations
Current limitations include scalability issues with collaborative filtering for large user bases, reliance on static dataset import rather than real-time updates, incomplete advanced book metadata features, and lack of a dedicated frontend application.

### 11.2 Potential Improvements
Potential improvements include integrating more advanced ML-based recommendation algorithms, adding support for real-time data updates and user contributions, implementing social features like book clubs, developing mobile applications, and optimizing cloud deployment with auto-scaling.

## 12. Deployment Information
The project has been successfully deployed to the Railway platform, providing a production-ready environment with automatic scaling and deployment pipelines.

- **GitHub Repository**: `https://github.com/zhu0117/Book-Metadata.git`
- **Deployment URL**: `https://book-metadata-production.up.railway.app`
- **API Test Page**: `https://book-metadata-production.up.railway.app/docs`
- **ReDoc Documentation**: `https://book-metadata-production.up.railway.app/redoc`

## 13. References
- FastAPI Documentation: `https://fastapi.tiangolo.com/`
- SQLAlchemy Documentation: `https://docs.sqlalchemy.org/`
- Pydantic Documentation: `https://docs.pydantic.dev/`
- GoodBooks-10K Dataset: `https://github.com/zygmuntz/goodbooks-10k`
- MIT License: `https://opensource.org/licenses/MIT`
- JWT Authentication: `https://jwt.io/`
- Bcrypt Password Hashing: `https://pypi.org/project/bcrypt/`

---

# Appendices

## Appendix A: GenAI Usage Declaration

### A.1 Tools Used
- **Microsoft Copilot**: Used for dataset analysis, data model design assistance, and API framework guidance
- **ChatGPT**: Used for technical documentation writing and best practice recommendations
- **Doubao (豆包)**: Used for technology stack research and dataset recommendations

### A.2 Usage Scenarios
1. **Dataset Search and Analysis**:
   - Assisted in finding and analyzing the GoodBooks-10K dataset
   - Helped with data preprocessing and cleaning strategies
   - Provided insights on dataset structure and potential use cases

2. **Data Model Design**:
   - Supported the design of database schemas for books, authors, users, and ratings
   - Assisted in defining relationships between entities
   - Recommended best practices for data normalization

3. **API Framework Development**:
   - Provided guidance on RESTful API design principles
   - Assisted in structuring the FastAPI application
   - Recommended authentication and security approaches

4. **Technical Research**:
   - Helped understand recommendation system algorithms
   - Provided information on Pearson correlation coefficient implementation
   - Assisted with understanding JWT authentication concepts

## Appendix B: Conversation Logs

**Conversation Link**: `https://www.doubao.com/thread/w99a7cf5c0c93f313`

## Appendix C: API Documentation

- **API Documentation (PDF)**: API_Documentation.pdf (in GitHub repository)
- **Swagger UI**: `https://book-metadata-production.up.railway.app/docs`
- **ReDoc Documentation**: `https://book-metadata-production.up.railway.app/redoc`

## Appendix D: Presentation Slides

- **Presentation Slides**: Book Metadata and Recommendation API (New Version).pptx  (in GitHub repository)
- **Hosted Location**: GitHub repository - `https://github.com/zhu0117/Book-Metadata.git`