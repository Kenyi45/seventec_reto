from typing import Optional, List
from datetime import datetime, timedelta
from models.post import Post, Comment, Like
from .base import BaseRepository, IRepository
import logging

logger = logging.getLogger(__name__)


class IPostRepository(IRepository[Post]):
    """
    Post repository interface defining post-specific operations.
    Follows Interface Segregation Principle (ISP).
    """
    
    async def get_by_author(self, author_id: str, skip: int = 0, limit: int = 100) -> List[Post]:
        """Get posts by author"""
        pass
    
    async def get_active_posts(self, skip: int = 0, limit: int = 100) -> List[Post]:
        """Get active posts"""
        pass
    
    async def get_recent_posts(self, days: int = 7, skip: int = 0, limit: int = 100) -> List[Post]:
        """Get recent posts"""
        pass


class ICommentRepository(IRepository[Comment]):
    """
    Comment repository interface defining comment-specific operations.
    Follows Interface Segregation Principle (ISP).
    """
    
    async def get_by_post(self, post_id: str, skip: int = 0, limit: int = 100) -> List[Comment]:
        """Get comments by post"""
        pass
    
    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Comment]:
        """Get comments by user"""
        pass


class ILikeRepository(IRepository[Like]):
    """
    Like repository interface defining like-specific operations.
    Follows Interface Segregation Principle (ISP).
    """
    
    async def get_by_post(self, post_id: str, skip: int = 0, limit: int = 100) -> List[Like]:
        """Get likes by post"""
        pass
    
    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Like]:
        """Get likes by user"""
        pass
    
    async def get_like_by_user_and_post(self, user_id: str, post_id: str) -> Optional[Like]:
        """Get like by user and post"""
        pass


class PostRepository(BaseRepository[Post], IPostRepository):
    """
    Post repository implementation providing post-specific data access operations.
    Follows Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP).
    """
    
    def __init__(self):
        super().__init__("posts", Post)
    
    async def get_by_author(self, author_id: str, skip: int = 0, limit: int = 100) -> List[Post]:
        """Get posts by author"""
        try:
            return await self.find_by_filter({"author_id": author_id}, skip, limit)
            
        except Exception as e:
            logger.error(f"Error getting posts by author {author_id}: {e}")
            return []
    
    async def get_active_posts(self, skip: int = 0, limit: int = 100) -> List[Post]:
        """Get active posts ordered by creation date"""
        try:
            cursor = self.collection.find({"is_active": True}).sort("created_at", -1).skip(skip).limit(limit)
            documents = await cursor.to_list(length=limit)
            
            return [Post(**self._convert_document(doc)) for doc in documents]
            
        except Exception as e:
            logger.error(f"Error getting active posts: {e}")
            return []
    
    async def get_recent_posts(self, days: int = 7, skip: int = 0, limit: int = 100) -> List[Post]:
        """Get recent posts"""
        try:
            cutoff_date = datetime.utcnow() - timedelta(days=days)
            filter_dict = {
                "is_active": True,
                "created_at": {"$gte": cutoff_date}
            }
            
            cursor = self.collection.find(filter_dict).sort("created_at", -1).skip(skip).limit(limit)
            documents = await cursor.to_list(length=limit)
            
            return [Post(**self._convert_document(doc)) for doc in documents]
            
        except Exception as e:
            logger.error(f"Error getting recent posts: {e}")
            return []
    
    async def increment_likes_count(self, post_id: str) -> Optional[Post]:
        """Increment likes count for a post"""
        try:
            return await self.update(post_id, {"$inc": {"likes_count": 1}})
            
        except Exception as e:
            logger.error(f"Error incrementing likes count for post {post_id}: {e}")
            return None
    
    async def decrement_likes_count(self, post_id: str) -> Optional[Post]:
        """Decrement likes count for a post"""
        try:
            return await self.update(post_id, {"$inc": {"likes_count": -1}})
            
        except Exception as e:
            logger.error(f"Error decrementing likes count for post {post_id}: {e}")
            return None
    
    async def increment_comments_count(self, post_id: str) -> Optional[Post]:
        """Increment comments count for a post"""
        try:
            return await self.update(post_id, {"$inc": {"comments_count": 1}})
            
        except Exception as e:
            logger.error(f"Error incrementing comments count for post {post_id}: {e}")
            return None
    
    async def decrement_comments_count(self, post_id: str) -> Optional[Post]:
        """Decrement comments count for a post"""
        try:
            return await self.update(post_id, {"$inc": {"comments_count": -1}})
            
        except Exception as e:
            logger.error(f"Error decrementing comments count for post {post_id}: {e}")
            return None


class CommentRepository(BaseRepository[Comment], ICommentRepository):
    """
    Comment repository implementation providing comment-specific data access operations.
    Follows Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP).
    """
    
    def __init__(self):
        super().__init__("comments", Comment)
    
    async def get_by_post(self, post_id: str, skip: int = 0, limit: int = 100) -> List[Comment]:
        """Get comments by post ordered by creation date"""
        try:
            cursor = self.collection.find({"post_id": post_id}).sort("created_at", 1).skip(skip).limit(limit)
            documents = await cursor.to_list(length=limit)
            
            return [Comment(**self._convert_document(doc)) for doc in documents]
            
        except Exception as e:
            logger.error(f"Error getting comments for post {post_id}: {e}")
            return []
    
    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Comment]:
        """Get comments by user"""
        try:
            return await self.find_by_filter({"user_id": user_id}, skip, limit)
            
        except Exception as e:
            logger.error(f"Error getting comments by user {user_id}: {e}")
            return []


class LikeRepository(BaseRepository[Like], ILikeRepository):
    """
    Like repository implementation providing like-specific data access operations.
    Follows Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP).
    """
    
    def __init__(self):
        super().__init__("likes", Like)
    
    async def get_by_post(self, post_id: str, skip: int = 0, limit: int = 100) -> List[Like]:
        """Get likes by post"""
        try:
            return await self.find_by_filter({"post_id": post_id}, skip, limit)
            
        except Exception as e:
            logger.error(f"Error getting likes for post {post_id}: {e}")
            return []
    
    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[Like]:
        """Get likes by user"""
        try:
            return await self.find_by_filter({"user_id": user_id}, skip, limit)
            
        except Exception as e:
            logger.error(f"Error getting likes by user {user_id}: {e}")
            return []
    
    async def get_like_by_user_and_post(self, user_id: str, post_id: str) -> Optional[Like]:
        """Get like by user and post"""
        try:
            document = await self.collection.find_one({
                "user_id": user_id,
                "post_id": post_id
            })
            
            if document:
                return Like(**document)
            return None
            
        except Exception as e:
            logger.error(f"Error getting like by user {user_id} and post {post_id}: {e}")
            return None 