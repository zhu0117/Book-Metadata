import csv
from sqlalchemy.orm import Session
from db.session import SessionLocal, engine
from db.base import Base
from db.models.book import Book, Author
from db.models.user import User

Base.metadata.create_all(bind=engine)


def parse_authors(author_string):
    if not author_string:
        return []
    authors = []
    for name in author_string.split(','):
        name = name.strip()
        if name and name != 'Unknown':
            authors.append(name)
    return authors


def convert_isbn(isbn_value):
    if not isbn_value:
        return None
    try:
        isbn_str = str(isbn_value)
        if '.' in isbn_str:
            isbn_str = isbn_str.split('.')[0]
        isbn_str = isbn_str.replace(' ', '').replace('-', '')
        if len(isbn_str) == 10 or len(isbn_str) == 13:
            return isbn_str
        return None
    except:
        return None


def convert_year(year_value):
    if not year_value:
        return None
    try:
        year = int(float(year_value))
        if 1800 <= year <= 2025:
            return year
        return None
    except:
        return None


def import_books_from_csv(csv_path, limit=200):
    db = SessionLocal()
    imported_count = 0
    skipped_count = 0

    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)

            for row in reader:
                if imported_count >= limit:
                    break

                title = row.get('title', '').strip()
                if not title:
                    skipped_count += 1
                    continue

                isbn = convert_isbn(row.get('isbn', ''))
                author_names = parse_authors(row.get('authors', ''))

                if not author_names:
                    author_names = ['Unknown Author']

                try:
                    average_rating = float(row.get('average_rating', 0) or 0)
                    ratings_count = int(float(row.get('ratings_count', 0) or 0))
                except:
                    average_rating = 0.0
                    ratings_count = 0

                publication_year = convert_year(row.get('original_publication_year', ''))
                language_code = row.get('language_code', '') or 'en'

                image_url = row.get('image_url', '')
                if not image_url or image_url == '':
                    image_url = row.get('small_image_url', '')

                existing_book = None
                if isbn:
                    existing_book = db.query(Book).filter(Book.isbn == isbn).first()

                if existing_book:
                    skipped_count += 1
                    continue

                book = Book(
                    title=title,
                    isbn=isbn if isbn else f"NOISBN-{imported_count}",
                    publication_year=publication_year,
                    cover_url=image_url,
                    language_code=language_code,
                    average_rating=average_rating,
                    rating_count=ratings_count
                )

                for author_name in author_names:
                    author = db.query(Author).filter(Author.name == author_name).first()
                    if not author:
                        author = Author(name=author_name)
                        db.add(author)
                        db.flush()

                    book.authors.append(author)

                db.add(book)
                imported_count += 1

                if imported_count % 20 == 0:
                    db.commit()
                    print(f"  Imported {imported_count} books...")

            db.commit()

    except Exception as e:
        print(f"Error during import: {e}")
        db.rollback()
        raise
    finally:
        db.close()

    return imported_count, skipped_count


if __name__ == "__main__":
    csv_path = "data/books.csv"
    limit = 200

    print(f"Importing {limit} books from {csv_path}...")
    imported, skipped = import_books_from_csv(csv_path, limit)

    print(f"\n{'='*50}")
    print(f"Import completed!")
    print(f"  Successfully imported: {imported} books")
    print(f"  Skipped (duplicate/empty): {skipped} books")
    print(f"{'='*50}")
