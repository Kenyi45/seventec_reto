from typing import Optional, List, Dict, Any
from models.story import Story, StoryView, StoryCreate, StoryUpdate
from models.user import User, UserRole
from repositories.story_repository import StoryRepository, StoryViewRepository
from repositories.user_repository import UserRepository
from utils.notifications import notification_service
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


class StoryService:
    """
    Story service implementing business logic for story management.
    Implements the plus feature for temporary stories (24 hours).
    Follows Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP).
    """
    
    def __init__(self):
        self.story_repository = StoryRepository()
        self.story_view_repository = StoryViewRepository()
        self.user_repository = UserRepository()
    
    async def create_story(self, story_data: StoryCreate, author_id: str) -> Story:
        """Create a new story"""
        try:
            # Get author information
            author = await self.user_repository.get_by_id(author_id)
            if not author:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Check if user can create stories (only organizers)
            if not author.can_create_posts():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo los organizadores pueden crear historias"
                )
            
            # Create story entity
            story = Story(
                content=story_data.content,
                image_url=story_data.image_url,
                author_id=author_id,  # Use the string user_id directly
                author_name=author.full_name,
                author_role=author.role.value
            )
            
            # Save story to database
            created_story = await self.story_repository.create(story)
            
            # Send notification to participants (async)
            await self._send_new_story_notification(created_story)
            
            logger.info(f"Story created successfully: {created_story.id}")
            return created_story
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating story: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_active_stories(self, skip: int = 0, limit: int = 20) -> List[Story]:
        """Get active stories"""
        try:
            return await self.story_repository.get_active_stories(skip, limit)
            
        except Exception as e:
            logger.error(f"Error getting active stories: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_story_by_id(self, story_id: str) -> Story:
        """Get story by ID"""
        try:
            story = await self.story_repository.get_by_id(story_id)
            if not story:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Historia no encontrada"
                )
            
            # Check if story is expired
            if story.is_expired():
                raise HTTPException(
                    status_code=status.HTTP_410_GONE,
                    detail="Historia expirada"
                )
            
            return story
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting story: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def view_story(self, story_id: str, user_id: str) -> Dict[str, Any]:
        """View a story and track the view"""
        try:
            logger.info(f"Viewing story: {story_id} by user: {user_id}")
            
            # Get story
            story = await self.story_repository.get_by_id(story_id)
            if not story:
                logger.error(f"Story not found: {story_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Historia no encontrada"
                )
            
            logger.info(f"Story found: {story.id}, content: {story.content[:50]}...")
            
            # Check if story is expired
            if story.is_expired():
                logger.warning(f"Story expired: {story_id}")
                raise HTTPException(
                    status_code=status.HTTP_410_GONE,
                    detail="Historia expirada"
                )
            
            # Get user
            user = await self.user_repository.get_by_id(user_id)
            if not user:
                logger.error(f"User not found: {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            logger.info(f"User found: {user.full_name}")
            
            # Check if user already viewed this story
            existing_view = await self.story_view_repository.get_view_by_user_and_story(user_id, story_id)
            if not existing_view:
                logger.info(f"Creating new view record for story: {story_id}")
                # Create view record
                story_view = StoryView(
                    story_id=str(story.id),  # Convert ObjectId to string
                    user_id=user_id,  # Use the string user_id directly
                    user_name=user.full_name
                )
                
                # Save view and increment story views count
                await self.story_view_repository.create(story_view)
                await self.story_repository.increment_views_count(story_id)
                
                logger.info(f"Story viewed successfully: {story_id} by {user_id}")
            else:
                logger.info(f"User already viewed story: {story_id}")
            
            return {
                "story": story,
                "time_remaining_hours": story.get_time_remaining_hours()
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error viewing story: {e}", exc_info=True)
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def update_story(self, story_id: str, update_data: StoryUpdate, user_id: str) -> Story:
        """Update story"""
        try:
            # Get current story
            story = await self.story_repository.get_by_id(story_id)
            if not story:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Historia no encontrada"
                )
            
            # Check if user is the author
            if str(story.author_id) != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo el autor puede editar la historia"
                )
            
            # Check if story is expired
            if story.is_expired():
                raise HTTPException(
                    status_code=status.HTTP_410_GONE,
                    detail="No se puede editar una historia expirada"
                )
            
            # Prepare update data
            update_dict = {}
            
            if update_data.content is not None:
                update_dict["content"] = update_data.content
            
            if update_data.image_url is not None:
                update_dict["image_url"] = update_data.image_url
            
            if update_data.is_active is not None:
                update_dict["is_active"] = update_data.is_active
            
            # Update story
            if update_dict:
                updated_story = await self.story_repository.update(story_id, update_dict)
                if updated_story:
                    logger.info(f"Story updated successfully: {story_id}")
                    return updated_story
            
            return story
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating story: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def delete_story(self, story_id: str, user_id: str) -> bool:
        """Delete story"""
        try:
            # Get current story
            story = await self.story_repository.get_by_id(story_id)
            if not story:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Historia no encontrada"
                )
            
            # Check if user is the author
            if str(story.author_id) != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo el autor puede eliminar la historia"
                )
            
            # Delete story
            deleted = await self.story_repository.delete(story_id)
            
            if deleted:
                logger.info(f"Story deleted successfully: {story_id}")
            
            return deleted
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting story: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_story_views(self, story_id: str, user_id: str, skip: int = 0, limit: int = 50) -> List[StoryView]:
        """Get views for a story (only author can see views)"""
        try:
            # Get story
            story = await self.story_repository.get_by_id(story_id)
            if not story:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Historia no encontrada"
                )
            
            # Check if user is the author
            if str(story.author_id) != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo el autor puede ver las visualizaciones"
                )
            
            return await self.story_view_repository.get_by_story(story_id, skip, limit)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting story views: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_stories_by_author(self, author_id: str, skip: int = 0, limit: int = 20) -> List[Story]:
        """Get stories by author"""
        try:
            return await self.story_repository.get_stories_by_author_active(author_id, skip, limit)
            
        except Exception as e:
            logger.error(f"Error getting stories by author: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def expire_old_stories(self) -> int:
        """Expire old stories (used by scheduled job)"""
        try:
            expired_count = await self.story_repository.expire_old_stories()
            
            if expired_count > 0:
                logger.info(f"Expired {expired_count} old stories")
            
            return expired_count
            
        except Exception as e:
            logger.error(f"Error expiring old stories: {e}")
            return 0
    
    async def _send_new_story_notification(self, story: Story) -> None:
        """Send notification for new story to participants"""
        try:
            # Get participants with FCM tokens
            participants = await self.user_repository.get_participants_with_fcm_token()
            
            if participants:
                # Extract FCM tokens
                fcm_tokens = [user.fcm_token for user in participants if user.fcm_token]
                
                if fcm_tokens:
                    # Send notification
                    notification_service.send_new_story_notification(
                        fcm_tokens,
                        story.author_name,
                        str(story.id)
                    )
                    
        except Exception as e:
            logger.error(f"Error sending new story notification: {e}")
            # Don't raise exception here as notification failure shouldn't affect story creation


# Dependency injection
def get_story_service() -> StoryService:
    """Get story service instance"""
    return StoryService() 