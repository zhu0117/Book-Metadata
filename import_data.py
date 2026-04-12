from sqlalchemy.orm import Session
from db.session import SessionLocal, engine
from db.base import Base
from db.models.book import Book, Author, Rating
from db.models.user import User

Base.metadata.create_all(bind=engine)

SAMPLE_USERS = [
    {"username": "user1", "email": "user1@example.com", "password": "password123"},
    {"username": "user2", "email": "user2@example.com", "password": "password123"},
]


def import_data():
    db = SessionLocal()
    try:
        print("Importing users...")
        user_map = {}
        for user_info in SAMPLE_USERS:
            existing = db.query(User).filter(User.username == user_info["username"]).first()
            if existing:
                user_map[user_info["username"]] = existing
                print(f"  User already exists: {user_info['username']}")
            else:
                user = User(
                    username=user_info["username"],
                    email=user_info["email"],
                    password_hash=user_info["password"]
                )
                db.add(user)
                db.commit()
                db.refresh(user)
                user_map[user_info["username"]] = user
                print(f"  Added user: {user.username}")

        print(f"\n{'='*50}")
        print("Data import completed!")
        print(f"  Users: {len(user_map)}")
        print(f"{'='*50}")

    except Exception as e:
        print(f"Error during data import: {e}")
        db.rollback()
        raise
    finally:
        db.close()


if __name__ == "__main__":
    import_data()
