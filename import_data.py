import requests
import json
from sqlalchemy.orm import Session
from db.session import SessionLocal, engine
from db.base import Base
from db.models.book import Book, Author, Rating
from db.models.user import User
from datetime import datetime

# 创建数据库表
Base.metadata.create_all(bind=engine)

def get_books_from_api(query, max_results=10):
    """从Google Books API获取书籍数据"""
    url = f"https://www.googleapis.com/books/v1/volumes?q={query}&maxResults={max_results}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        print(f"Error fetching data: {response.status_code}")
        return {}

def parse_book_data(book_data):
    """解析书籍数据"""
    books = []
    if 'items' in book_data:
        for item in book_data['items']:
            volume_info = item.get('volumeInfo', {})
            book = {
                'title': volume_info.get('title', ''),
                'isbn': '',
                'publication_date': None,
                'publisher': volume_info.get('publisher', ''),
                'description': volume_info.get('description', ''),
                'cover_url': volume_info.get('imageLinks', {}).get('thumbnail', ''),
                'authors': volume_info.get('authors', [])
            }
            
            # 获取ISBN
            industry_identifiers = volume_info.get('industryIdentifiers', [])
            for identifier in industry_identifiers:
                if identifier.get('type') == 'ISBN_13':
                    book['isbn'] = identifier.get('identifier', '')
                    break
            if not book['isbn']:
                for identifier in industry_identifiers:
                    if identifier.get('type') == 'ISBN_10':
                        book['isbn'] = identifier.get('identifier', '')
                        break
            
            # 解析出版日期
            published_date = volume_info.get('publishedDate', '')
            if published_date:
                try:
                    if len(published_date) == 4:
                        book['publication_date'] = datetime.strptime(published_date, '%Y')
                    elif len(published_date) == 7:
                        book['publication_date'] = datetime.strptime(published_date, '%Y-%m')
                    else:
                        book['publication_date'] = datetime.strptime(published_date, '%Y-%m-%d')
                except ValueError:
                    pass
            
            books.append(book)
    return books

def import_data():
    """导入数据到数据库"""
    db = SessionLocal()
    try:
        # 导入书籍数据
        queries = ['python programming', 'data science', 'machine learning', 'artificial intelligence']
        for query in queries:
            print(f"Fetching books for: {query}")
            book_data = get_books_from_api(query, max_results=5)
            parsed_books = parse_book_data(book_data)
            
            for book_info in parsed_books:
                # 检查书籍是否已存在
                existing_book = db.query(Book).filter(Book.isbn == book_info['isbn']).first()
                if existing_book:
                    print(f"Book already exists: {book_info['title']}")
                    continue
                
                # 创建书籍
                book = Book(
                    title=book_info['title'],
                    isbn=book_info['isbn'],
                    publication_date=book_info['publication_date'],
                    publisher=book_info['publisher'],
                    description=book_info['description'],
                    cover_url=book_info['cover_url']
                )
                
                # 添加作者
                for author_name in book_info['authors']:
                    # 检查作者是否已存在
                    author = db.query(Author).filter(Author.name == author_name).first()
                    if not author:
                        author = Author(name=author_name)
                        db.add(author)
                        db.commit()
                        db.refresh(author)
                    book.authors.append(author)
                
                db.add(book)
                print(f"Added book: {book_info['title']}")
            
            db.commit()
        
        # 创建测试用户
        test_users = [
            {'username': 'user1', 'email': 'user1@example.com', 'password': 'password123'},
            {'username': 'user2', 'email': 'user2@example.com', 'password': 'password123'}
        ]
        
        for user_info in test_users:
            existing_user = db.query(User).filter(User.username == user_info['username']).first()
            if not existing_user:
                user = User(
                    username=user_info['username'],
                    email=user_info['email'],
                    password_hash=user_info['password']
                )
                db.add(user)
                print(f"Added user: {user_info['username']}")
        
        db.commit()
        
        # 为测试用户添加一些评分
        users = db.query(User).all()
        books = db.query(Book).limit(10).all()
        
        ratings = [
            (1, 1, 5.0),
            (1, 2, 4.5),
            (1, 3, 4.0),
            (2, 1, 4.5),
            (2, 4, 5.0),
            (2, 5, 3.5)
        ]
        
        for user_id, book_id, rating_value in ratings:
            existing_rating = db.query(Rating).filter(
                Rating.user_id == user_id,
                Rating.book_id == book_id
            ).first()
            if not existing_rating:
                rating = Rating(
                    user_id=user_id,
                    book_id=book_id,
                    rating=rating_value
                )
                db.add(rating)
                print(f"Added rating: User {user_id} rated Book {book_id} with {rating_value}")
        
        db.commit()
        
        # 更新书籍的平均评分
        for book in books:
            book_ratings = db.query(Rating).filter(Rating.book_id == book.id).all()
            if book_ratings:
                total_rating = sum(r.rating for r in book_ratings)
                rating_count = len(book_ratings)
                book.average_rating = total_rating / rating_count
                book.rating_count = rating_count
        
        db.commit()
        print("Data import completed successfully!")
        
    except Exception as e:
        print(f"Error during data import: {e}")
        db.rollback()
    finally:
        db.close()

if __name__ == "__main__":
    import_data()