from typing import Optional, List
from models.user import User
from .base import BaseRepository, IRepository
import logging

logger = logging.getLogger(__name__)


class IUserRepository(IRepository[User]):
    """
    User repository interface defining user-specific operations.
    Follows Interface Segregation Principle (ISP).
    """
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        pass
    
    async def get_by_role(self, role: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by role"""
        pass
    
    async def update_fcm_token(self, user_id: str, fcm_token: str) -> Optional[User]:
        """Update user FCM token"""
        pass
    
    async def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get active users"""
        pass


class UserRepository(BaseRepository[User], IUserRepository):
    """
    User repository implementation providing user-specific data access operations.
    Follows Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP).
    """
    
    def __init__(self):
        super().__init__("users", User)
    
    async def get_by_email(self, email: str) -> Optional[User]:
        """Get user by email"""
        try:
            document = await self.collection.find_one({"email": email.lower()})
            
            if document:
                converted_doc = self._convert_document(document)
                return User(**converted_doc)
            return None
            
        except Exception as e:
            logger.error(f"Error getting user by email {email}: {e}")
            return None
    
    async def get_by_role(self, role: str, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by role"""
        try:
            return await self.find_by_filter({"role": role}, skip, limit)
            
        except Exception as e:
            logger.error(f"Error getting users by role {role}: {e}")
            return []
    
    async def update_fcm_token(self, user_id: str, fcm_token: str) -> Optional[User]:
        """Update user FCM token"""
        try:
            update_data = {"fcm_token": fcm_token}
            return await self.update(user_id, update_data)
            
        except Exception as e:
            logger.error(f"Error updating FCM token for user {user_id}: {e}")
            return None
    
    async def get_active_users(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get active users"""
        try:
            return await self.find_by_filter({"is_active": True}, skip, limit)
            
        except Exception as e:
            logger.error(f"Error getting active users: {e}")
            return []
    
    async def get_participants_with_fcm_token(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get participants with FCM token for notifications"""
        try:
            filter_dict = {
                "role": "participant",
                "is_active": True,
                "fcm_token": {"$ne": None, "$exists": True}
            }
            return await self.find_by_filter(filter_dict, skip, limit)
            
        except Exception as e:
            logger.error(f"Error getting participants with FCM token: {e}")
            return []
    
    async def activate_user(self, user_id: str) -> Optional[User]:
        """Activate user account"""
        try:
            update_data = {"is_active": True}
            return await self.update(user_id, update_data)
            
        except Exception as e:
            logger.error(f"Error activating user {user_id}: {e}")
            return None
    
    async def deactivate_user(self, user_id: str) -> Optional[User]:
        """Deactivate user account"""
        try:
            update_data = {"is_active": False}
            return await self.update(user_id, update_data)
            
        except Exception as e:
            logger.error(f"Error deactivating user {user_id}: {e}")
            return None
    
    async def email_exists(self, email: str) -> bool:
        """Check if email already exists"""
        try:
            count = await self.collection.count_documents({"email": email.lower()})
            return count > 0
            
        except Exception as e:
            logger.error(f"Error checking email existence {email}: {e}")
            return False 