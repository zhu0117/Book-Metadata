from sqlalchemy.orm import Session
from models import Book, Author, User, Rating
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
import string

class RecommendationEngine:
    def __init__(self, db: Session):
        self.db = db
        # 延迟下载NLTK资源，避免启动时的权限问题
        try:
            nltk.download('stopwords', quiet=True)
            nltk.download('wordnet', quiet=True)
            self.lemmatizer = WordNetLemmatizer()
            self.stop_words = set(stopwords.words('english'))
        except Exception as e:
            print(f"Warning: NLTK data download failed: {e}")
            # 使用备用方法
            self.lemmatizer = None
            self.stop_words = set()
    
    def preprocess_text(self, text: str) -> str:
        """预处理文本，用于内容相似度计算"""
        if not text:
            return ''
        
        # 转换为小写
        text = text.lower()
        
        # 移除标点符号
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        # 分词
        words = text.split()
        
        # 移除停用词并进行词形还原（如果NLTK资源可用）
        if self.lemmatizer and self.stop_words:
            words = [self.lemmatizer.lemmatize(word) for word in words if word not in self.stop_words]
        
        return ' '.join(words)
    
    def get_content_based_recommendations(self, book_id: int, top_n: int = 10):
        """基于内容的推荐"""
        # 获取所有书籍
        books = self.db.query(Book).all()
        
        if not books:
            return []
        
        # 准备文本数据
        book_texts = []
        book_ids = []
        
        for book in books:
            # 合并标题、描述和作者信息
            author_names = ' '.join([author.name for author in book.authors])
            text = f"{book.title} {book.description} {author_names}"
            book_texts.append(self.preprocess_text(text))
            book_ids.append(book.id)
        
        # 使用TF-IDF向量化
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(book_texts)
        
        # 找到目标书籍的索引
        try:
            target_index = book_ids.index(book_id)
        except ValueError:
            return []
        
        # 计算相似度
        cosine_similarities = cosine_similarity(tfidf_matrix[target_index:target_index+1], tfidf_matrix).flatten()
        
        # 排序并获取最相似的书籍
        similar_indices = cosine_similarities.argsort()[:-top_n-1:-1]
        
        # 排除自身
        similar_indices = [idx for idx in similar_indices if idx != target_index]
        
        # 获取推荐书籍
        recommended_books = []
        for idx in similar_indices:
            book = self.db.query(Book).filter(Book.id == book_ids[idx]).first()
            if book:
                recommended_books.append((book, cosine_similarities[idx]))
        
        return recommended_books
    
    def get_collaborative_filtering_recommendations(self, user_id: int, top_n: int = 10):
        """基于协同过滤的推荐"""
        # 获取所有用户和书籍
        users = self.db.query(User).all()
        books = self.db.query(Book).all()
        
        if not users or not books:
            return []
        
        # 创建用户-书籍评分矩阵
        user_ids = [user.id for user in users]
        book_ids = [book.id for book in books]
        
        # 初始化评分矩阵
        rating_matrix = np.zeros((len(user_ids), len(book_ids)))
        
        # 填充评分矩阵
        for rating in self.db.query(Rating).all():
            if rating.user_id in user_ids and rating.book_id in book_ids:
                user_idx = user_ids.index(rating.user_id)
                book_idx = book_ids.index(rating.book_id)
                rating_matrix[user_idx, book_idx] = rating.rating
        
        # 找到目标用户的索引
        try:
            user_idx = user_ids.index(user_id)
        except ValueError:
            return []
        
        # 计算用户相似度
        user_similarities = np.zeros(len(user_ids))
        for i in range(len(user_ids)):
            if i != user_idx:
                # 找到两个用户都评分过的书籍
                common_books = np.logical_and(rating_matrix[user_idx] > 0, rating_matrix[i] > 0)
                if np.any(common_books):
                    # 计算余弦相似度
                    user_similarities[i] = cosine_similarity(
                        rating_matrix[user_idx][common_books].reshape(1, -1),
                        rating_matrix[i][common_books].reshape(1, -1)
                    )[0][0]
        
        # 排序并获取最相似的用户
        similar_user_indices = user_similarities.argsort()[:-top_n-1:-1]
        
        # 计算推荐分数
        book_scores = np.zeros(len(book_ids))
        for i in similar_user_indices:
            if user_similarities[i] > 0:
                # 对目标用户未评分的书籍进行评分预测
                for j in range(len(book_ids)):
                    if rating_matrix[user_idx, j] == 0 and rating_matrix[i, j] > 0:
                        book_scores[j] += user_similarities[i] * rating_matrix[i, j]
        
        # 排序并获取推荐书籍
        recommended_indices = book_scores.argsort()[:-top_n-1:-1]
        
        recommended_books = []
        for idx in recommended_indices:
            if book_scores[idx] > 0:
                book = self.db.query(Book).filter(Book.id == book_ids[idx]).first()
                if book:
                    recommended_books.append((book, book_scores[idx]))
        
        return recommended_books
    
    def get_hybrid_recommendations(self, user_id: int, book_id: int = None, top_n: int = 10):
        """混合推荐，结合内容和协同过滤"""
        # 获取内容推荐
        content_recs = []
        if book_id:
            content_recs = self.get_content_based_recommendations(book_id, top_n)
        
        # 获取协同过滤推荐
        collaborative_recs = self.get_collaborative_filtering_recommendations(user_id, top_n)
        
        # 合并推荐结果
        all_recs = {}
        
        # 内容推荐权重
        for book, score in content_recs:
            all_recs[book.id] = {'book': book, 'score': score * 0.4}
        
        # 协同过滤推荐权重
        for book, score in collaborative_recs:
            if book.id in all_recs:
                all_recs[book.id]['score'] += score * 0.6
            else:
                all_recs[book.id] = {'book': book, 'score': score * 0.6}
        
        # 排序并获取推荐
        sorted_recs = sorted(all_recs.values(), key=lambda x: x['score'], reverse=True)[:top_n]
        
        return [(rec['book'], rec['score']) for rec in sorted_recs]