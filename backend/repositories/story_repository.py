from typing import Optional, List
from datetime import datetime
from models.story import Story, StoryView
from .base import BaseRepository, IRepository
import logging

logger = logging.getLogger(__name__)


class IStoryRepository(IRepository[Story]):
    """
    Story repository interface defining story-specific operations.
    Follows Interface Segregation Principle (ISP).
    """
    
    async def get_active_stories(self, skip: int = 0, limit: int = 100) -> List[Story]:
        """Get active stories"""
        pass
    
    async def get_expired_stories(self, skip: int = 0, limit: int = 100) -> List[Story]:
        """Get expired stories"""
        pass
    
    async def get_by_author(self, author_id: str, skip: int = 0, limit: int = 100) -> List[Story]:
        """Get stories by author"""
        pass
    
    async def expire_old_stories(self) -> int:
        """Expire old stories"""
        pass


class IStoryViewRepository(IRepository[StoryView]):
    """
    Story view repository interface defining story view-specific operations.
    Follows Interface Segregation Principle (ISP).
    """
    
    async def get_by_story(self, story_id: str, skip: int = 0, limit: int = 100) -> List[StoryView]:
        """Get views by story"""
        pass
    
    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[StoryView]:
        """Get views by user"""
        pass
    
    async def get_view_by_user_and_story(self, user_id: str, story_id: str) -> Optional[StoryView]:
        """Get view by user and story"""
        pass


class StoryRepository(BaseRepository[Story], IStoryRepository):
    """
    Story repository implementation providing story-specific data access operations.
    Follows Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP).
    """
    
    def __init__(self):
        super().__init__("stories", Story)
    
    async def get_active_stories(self, skip: int = 0, limit: int = 100) -> List[Story]:
        """Get active stories ordered by creation date"""
        try:
            current_time = datetime.utcnow()
            filter_dict = {
                "is_active": True,
                "expires_at": {"$gt": current_time}
            }
            
            cursor = self.collection.find(filter_dict).sort("created_at", -1).skip(skip).limit(limit)
            documents = await cursor.to_list(length=limit)
            
            return [Story(**self._convert_document(doc)) for doc in documents]
            
        except Exception as e:
            logger.error(f"Error getting active stories: {e}")
            return []
    
    async def get_expired_stories(self, skip: int = 0, limit: int = 100) -> List[Story]:
        """Get expired stories"""
        try:
            current_time = datetime.utcnow()
            filter_dict = {
                "$or": [
                    {"expires_at": {"$lte": current_time}},
                    {"is_active": False}
                ]
            }
            
            cursor = self.collection.find(filter_dict).sort("created_at", -1).skip(skip).limit(limit)
            documents = await cursor.to_list(length=limit)
            
            return [Story(**self._convert_document(doc)) for doc in documents]
            
        except Exception as e:
            logger.error(f"Error getting expired stories: {e}")
            return []
    
    async def get_by_author(self, author_id: str, skip: int = 0, limit: int = 100) -> List[Story]:
        """Get stories by author"""
        try:
            return await self.find_by_filter({"author_id": author_id}, skip, limit)
            
        except Exception as e:
            logger.error(f"Error getting stories by author {author_id}: {e}")
            return []
    
    async def expire_old_stories(self) -> int:
        """Expire old stories that have passed their expiration time"""
        try:
            current_time = datetime.utcnow()
            result = await self.collection.update_many(
                {
                    "expires_at": {"$lte": current_time},
                    "is_active": True
                },
                {"$set": {"is_active": False, "updated_at": current_time}}
            )
            
            expired_count = result.modified_count
            if expired_count > 0:
                logger.info(f"Expired {expired_count} stories")
            
            return expired_count
            
        except Exception as e:
            logger.error(f"Error expiring old stories: {e}")
            return 0
    
    async def increment_views_count(self, story_id: str) -> Optional[Story]:
        """Increment views count for a story"""
        try:
            return await self.update(story_id, {"$inc": {"views_count": 1}})
            
        except Exception as e:
            logger.error(f"Error incrementing views count for story {story_id}: {e}")
            return None
    
    async def get_stories_by_author_active(self, author_id: str, skip: int = 0, limit: int = 100) -> List[Story]:
        """Get active stories by author"""
        try:
            current_time = datetime.utcnow()
            filter_dict = {
                "author_id": author_id,
                "is_active": True,
                "expires_at": {"$gt": current_time}
            }
            
            cursor = self.collection.find(filter_dict).sort("created_at", -1).skip(skip).limit(limit)
            documents = await cursor.to_list(length=limit)
            
            return [Story(**self._convert_document(doc)) for doc in documents]
            
        except Exception as e:
            logger.error(f"Error getting active stories by author {author_id}: {e}")
            return []


class StoryViewRepository(BaseRepository[StoryView], IStoryViewRepository):
    """
    Story view repository implementation providing story view-specific data access operations.
    Follows Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP).
    """
    
    def __init__(self):
        super().__init__("story_views", StoryView)
    
    async def get_by_story(self, story_id: str, skip: int = 0, limit: int = 100) -> List[StoryView]:
        """Get views by story"""
        try:
            return await self.find_by_filter({"story_id": story_id}, skip, limit)
            
        except Exception as e:
            logger.error(f"Error getting views for story {story_id}: {e}")
            return []
    
    async def get_by_user(self, user_id: str, skip: int = 0, limit: int = 100) -> List[StoryView]:
        """Get views by user"""
        try:
            return await self.find_by_filter({"user_id": user_id}, skip, limit)
            
        except Exception as e:
            logger.error(f"Error getting views by user {user_id}: {e}")
            return []
    
    async def get_view_by_user_and_story(self, user_id: str, story_id: str) -> Optional[StoryView]:
        """Get view by user and story"""
        try:
            document = await self.collection.find_one({
                "user_id": user_id,
                "story_id": story_id
            })
            
            if document:
                return StoryView(**self._convert_document(document))
            return None
            
        except Exception as e:
            logger.error(f"Error getting view by user {user_id} and story {story_id}: {e}")
            return None 