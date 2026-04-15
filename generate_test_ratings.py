from sqlalchemy.orm import Session
from db.session import SessionLocal
from db.models.book import Book, Rating
from db.models.user import User
import random


def generate_test_ratings():
    db = SessionLocal()
    try:
        users = db.query(User).all()
        books = db.query(Book).all()

        print("Creating additional users for testing...")
        test_usernames = ["user3", "user4", "user5", "user6", "user7"]
        for username in test_usernames:
            existing = db.query(User).filter(User.username == username).first()
            if not existing:
                user = User(
                    username=username,
                    email=f"{username}@example.com",
                    password_hash="password123"
                )
                db.add(user)
        db.commit()

        users = db.query(User).all()
        print(f"  Total users now: {len(users)}")

        books = db.query(Book).all()
        print(f"  Total books: {len(books)}")

        existing_ratings = db.query(Rating).count()
        print(f"  Existing ratings: {existing_ratings}")

        db.query(Rating).delete()
        db.commit()
        print("Cleared existing ratings for clean test data")

        print("\nGenerating test ratings...")
        rating_count = 0
        test_books = random.sample(books, min(80, len(books)))

        user_profiles = {
            "user3": {"liked_books": [], "disliked_books": []},
            "user4": {"liked_books": [], "disliked_books": []},
            "user5": {"liked_books": [], "disliked_books": []},
            "user6": {"liked_books": [], "disliked_books": []},
            "user7": {"liked_books": [], "disliked_books": []},
        }

        for username, profile in user_profiles.items():
            user = db.query(User).filter(User.username == username).first()
            if not user:
                continue

            num_liked = random.randint(5, 10)
            num_disliked = random.randint(2, 5)

            profile["liked_books"] = random.sample(test_books, min(num_liked, len(test_books)))
            remaining = [b for b in test_books if b not in profile["liked_books"]]
            profile["disliked_books"] = random.sample(remaining, min(num_disliked, len(remaining)))

            for book in profile["liked_books"]:
                existing = db.query(Rating).filter(
                    Rating.user_id == user.id,
                    Rating.book_id == book.id
                ).first()
                if not existing:
                    rating = Rating(user_id=user.id, book_id=book.id, rating=random.uniform(4.0, 5.0))
                    db.add(rating)
                    rating_count += 1

            for book in profile["disliked_books"]:
                existing = db.query(Rating).filter(
                    Rating.user_id == user.id,
                    Rating.book_id == book.id
                ).first()
                if not existing:
                    rating = Rating(user_id=user.id, book_id=book.id, rating=random.uniform(1.0, 2.5))
                    db.add(rating)
                    rating_count += 1

        for user in users[:2]:
            num_ratings = random.randint(3, 8)
            user_books = random.sample(test_books, min(num_ratings, len(test_books)))
            for book in user_books:
                existing = db.query(Rating).filter(
                    Rating.user_id == user.id,
                    Rating.book_id == book.id
                ).first()
                if not existing:
                    rating = Rating(
                        user_id=user.id,
                        book_id=book.id,
                        rating=round(random.uniform(1.5, 5.0), 1)
                    )
                    db.add(rating)
                    rating_count += 1

        db.commit()

        for user in users:
            user_ratings = db.query(Rating).filter(Rating.user_id == user.id).all()
            if user_ratings:
                avg_rating = sum(r.rating for r in user_ratings) / len(user_ratings)
                for r in user_ratings:
                    book = db.query(Book).filter(Book.id == r.book_id).first()
                    if book:
                        book.rating_count = db.query(Rating).filter(Rating.book_id == book.id).count()
                        book_ratings = db.query(Rating).filter(Rating.book_id == book.id).all()
                        book.average_rating = sum(br.rating for br in book_ratings) / len(book_ratings)
        db.commit()

        print(f"  Added {rating_count} new ratings")
        total_ratings = db.query(Rating).count()
        print(f"  Total ratings now: {total_ratings}")

        print("\nRatings per user:")
        for user in users:
            count = db.query(Rating).filter(Rating.user_id == user.id).count()
            print(f"  {user.username}: {count} ratings")

    except Exception as e:
        print(f"Error: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    generate_test_ratings()