from sqlalchemy.orm import Session
from sqlalchemy import func
from db.models import Book, Author, User, Rating
from typing import List, Optional


class RecommendationEngine:
    def __init__(self, db: Session):
        self.db = db

    def get_popular_books(self, limit: int = 10, min_rating_count: int = 5) -> List[Book]:
        """获取热门书籍 - 评分高且评分人数多的书"""
        return self.db.query(Book).filter(
            Book.rating_count >= min_rating_count
        ).order_by(
            Book.average_rating.desc(),
            Book.rating_count.desc()
        ).limit(limit).all()

    def get_books_by_popular_authors(self, user_id: int, limit: int = 10) -> List[Book]:
        """基于用户喜欢的作者推荐书籍"""
        user_ratings = self.db.query(Rating).filter(Rating.user_id == user_id).all()

        if not user_ratings:
            return []

        rated_book_ids = [r.book_id for r in user_ratings]
        rated_books = self.db.query(Book).filter(Book.id.in_(rated_book_ids)).all()

        if not rated_books:
            return []

        author_ids = set()
        for book in rated_books:
            for author in book.authors:
                author_ids.add(author.id)

        if not author_ids:
            return []

        recommended_books = self.db.query(Book).filter(
            Book.id.notin_(rated_book_ids),
            Book.authors.any(Author.id.in_(author_ids))
        ).order_by(
            Book.average_rating.desc()
        ).limit(limit).all()

        return recommended_books

    def get_user_based_recommendations(self, user_id: int, limit: int = 10) -> List[dict]:
        """基于用户的协同过滤推荐 - 找到相似用户喜欢的书"""
        target_user_ratings = self.db.query(Rating).filter(Rating.user_id == user_id).all()

        if not target_user_ratings:
            return []

        target_book_ids = {r.book_id for r in target_user_ratings}
        target_ratings_dict = {r.book_id: r.rating for r in target_user_ratings}

        all_users = self.db.query(User).filter(User.id != user_id).all()

        similarities = []
        for user in all_users:
            user_ratings = self.db.query(Rating).filter(Rating.user_id == user.id).all()
            if not user_ratings:
                continue

            common_books = []
            for r in user_ratings:
                if r.book_id in target_book_ids:
                    common_books.append((r.rating, target_ratings_dict[r.book_id]))

            if len(common_books) >= 2:
                similarity = self._calculate_similarity(common_books)
                if similarity > 0:
                    similarities.append((user.id, user.username, similarity, user_ratings))

        similarities.sort(key=lambda x: x[2], reverse=True)

        top_similar_users = similarities[:5]

        recommended_books = []
        for user_id_sim, username, sim_score, user_ratings in top_similar_users:
            for rating in user_ratings:
                if rating.book_id not in target_book_ids:
                    book = self.db.query(Book).filter(Book.id == rating.book_id).first()
                    if book:
                        recommended_books.append({
                            "book": book,
                            "similar_user": username,
                            "similarity_score": round(sim_score, 2),
                            "rating_from_similar_user": rating.rating
                        })

        recommended_books.sort(key=lambda x: (x["similarity_score"], x["book"].average_rating), reverse=True)

        return recommended_books[:limit]

    def _calculate_similarity(self, common_ratings: List[tuple]) -> float:
        """计算两个用户评分习惯的相似度（皮尔逊相关系数）"""
        if len(common_ratings) < 2:
            return 0.0

        ratings_a = [r[0] for r in common_ratings]
        ratings_b = [r[1] for r in common_ratings]

        mean_a = sum(ratings_a) / len(ratings_a)
        mean_b = sum(ratings_b) / len(ratings_b)

        numerator = sum((r_a - mean_a) * (r_b - mean_b) for r_a, r_b in zip(ratings_a, ratings_b))

        denom_a = sum((r_a - mean_a) ** 2 for r_a in ratings_a)
        denom_b = sum((r_b - mean_b) ** 2 for r_b in ratings_b)

        denominator = (denom_a * denom_b) ** 0.5

        if denominator == 0:
            return 0.0

        return numerator / denominator

    def get_all_ratings_for_book(self, book_id: int) -> List[Rating]:
        """获取某本书的所有评分"""
        return self.db.query(Rating).filter(Rating.book_id == book_id).all()

    def get_all_ratings_for_user(self, user_id: int) -> List[Rating]:
        """获取某用户的所有评分"""
        return self.db.query(Rating).filter(Rating.user_id == user_id).all()

    def get_hybrid_recommendations(self, user_id: int, limit: int = 10) -> List[Book]:
        """混合推荐：结合热门推荐和作者推荐"""
        author_books = self.get_books_by_popular_authors(user_id=user_id, limit=limit)
        popular_books = self.get_popular_books(limit=limit, min_rating_count=3)

        seen_ids = set()
        unique_books = []
        for book in author_books:
            if book.id not in seen_ids:
                seen_ids.add(book.id)
                unique_books.append(book)

        for book in popular_books:
            if book.id not in seen_ids:
                seen_ids.add(book.id)
                unique_books.append(book)
            if len(unique_books) >= limit:
                break

        return unique_books[:limit]
