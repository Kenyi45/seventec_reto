from typing import Optional, List, Dict, Any
from models.post import Post, Comment, Like, PostCreate, PostUpdate, CommentCreate
from models.user import User, UserRole
from repositories.post_repository import PostRepository, CommentRepository, LikeRepository
from repositories.user_repository import UserRepository
from utils.notifications import notification_service
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


class PostService:
    """
    Post service implementing business logic for post management.
    Follows Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP).
    """
    
    def __init__(self):
        self.post_repository = PostRepository()
        self.comment_repository = CommentRepository()
        self.like_repository = LikeRepository()
        self.user_repository = UserRepository()
    
    async def create_post(self, post_data: PostCreate, author_id: str) -> Post:
        """Create a new post"""
        try:
            # Get author information
            author = await self.user_repository.get_by_id(author_id)
            if not author:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Check if user can create posts (only organizers)
            if not author.can_create_posts():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo los organizadores pueden crear publicaciones"
                )
            
            # Create post entity
            post = Post(
                title=post_data.title,
                content=post_data.content,
                image_url=post_data.image_url,
                author_id=author_id,  # Use the string user_id directly
                author_name=author.full_name,
                author_role=author.role.value
            )
            
            # Save post to database
            created_post = await self.post_repository.create(post)
            
            # Send notification to participants (async)
            await self._send_new_post_notification(created_post)
            
            logger.info(f"Post created successfully: {created_post.id}")
            return created_post
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error creating post: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_posts(self, skip: int = 0, limit: int = 20) -> List[Post]:
        """Get active posts with likes and comments data"""
        try:
            posts = await self.post_repository.get_active_posts(skip, limit)
            
            # Enrich posts with likes and comments data
            enriched_posts = []
            for post in posts:
                # Get likes for this post
                likes = await self.like_repository.get_by_post(str(post.id))
                likes_user_ids = [str(like.user_id) for like in likes]
                
                # Get comments for this post
                comments = await self.comment_repository.get_by_post(str(post.id))
                
                # Create enriched post with likes and comments
                enriched_post = post.model_copy(deep=True)
                enriched_post.likes = likes_user_ids
                enriched_post.comments = comments
                enriched_post.likes_count = len(likes)
                enriched_post.comments_count = len(comments)
                
                enriched_posts.append(enriched_post)
            
            return enriched_posts
            
        except Exception as e:
            logger.error(f"Error getting posts: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_post_by_id(self, post_id: str) -> Post:
        """Get post by ID with likes and comments data"""
        try:
            post = await self.post_repository.get_by_id(post_id)
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Publicación no encontrada"
                )
            
            # Get likes for this post
            likes = await self.like_repository.get_by_post(post_id)
            likes_user_ids = [str(like.user_id) for like in likes]
            
            # Get comments for this post
            comments = await self.comment_repository.get_by_post(post_id)
            
            # Create enriched post with likes and comments
            enriched_post = post.model_copy(deep=True)
            enriched_post.likes = likes_user_ids
            enriched_post.comments = comments
            enriched_post.likes_count = len(likes)
            enriched_post.comments_count = len(comments)
            
            return enriched_post
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting post: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def update_post(self, post_id: str, update_data: PostUpdate, user_id: str) -> Post:
        """Update post"""
        try:
            # Get current post
            post = await self.post_repository.get_by_id(post_id)
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Publicación no encontrada"
                )
            
            # Check if user is the author
            if str(post.author_id) != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo el autor puede editar la publicación"
                )
            
            # Prepare update data
            update_dict = {}
            
            if update_data.title is not None:
                update_dict["title"] = update_data.title
            
            if update_data.content is not None:
                update_dict["content"] = update_data.content
            
            if update_data.image_url is not None:
                update_dict["image_url"] = update_data.image_url
            
            if update_data.is_active is not None:
                update_dict["is_active"] = update_data.is_active
            
            # Update post
            if update_dict:
                updated_post = await self.post_repository.update(post_id, update_dict)
                if updated_post:
                    logger.info(f"Post updated successfully: {post_id}")
                    return updated_post
            
            return post
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating post: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def delete_post(self, post_id: str, user_id: str) -> bool:
        """Delete post"""
        try:
            # Get current post
            post = await self.post_repository.get_by_id(post_id)
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Publicación no encontrada"
                )
            
            # Check if user is the author
            if str(post.author_id) != user_id:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo el autor puede eliminar la publicación"
                )
            
            # Delete post
            deleted = await self.post_repository.delete(post_id)
            
            if deleted:
                logger.info(f"Post deleted successfully: {post_id}")
            
            return deleted
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deleting post: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def like_post(self, post_id: str, user_id: str) -> Dict[str, Any]:
        """Like a post"""
        try:
            # Get post
            post = await self.post_repository.get_by_id(post_id)
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Publicación no encontrada"
                )
            
            # Get user
            user = await self.user_repository.get_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Check if user can interact with posts (only participants)
            if not user.can_interact_with_posts():
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo los participantes pueden dar like a las publicaciones"
                )
            
            # Check if user already liked this post
            existing_like = await self.like_repository.get_like_by_user_and_post(user_id, post_id)
            if existing_like:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Ya has dado like a esta publicación"
                )
            
            # Create like
            like = Like(
                post_id=str(post_id),  # Convert to string
                user_id=str(user_id),  # Convert to string
                user_name=user.full_name
            )
            
            # Save like and increment post likes count
            created_like = await self.like_repository.create(like)
            await self.post_repository.increment_likes_count(post_id)
            
            logger.info(f"Post liked successfully: {post_id} by {user_id}")
            
            return {"message": "Like agregado exitosamente"}
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error liking post: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def unlike_post(self, post_id: str, user_id: str) -> Dict[str, Any]:
        """Unlike a post"""
        try:
            # Get existing like
            like = await self.like_repository.get_like_by_user_and_post(user_id, post_id)
            if not like:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="No has dado like a esta publicación"
                )
            
            # Delete like and decrement post likes count
            deleted = await self.like_repository.delete(like.id)
            if deleted:
                await self.post_repository.decrement_likes_count(post_id)
            
            logger.info(f"Post unliked successfully: {post_id} by {user_id}")
            
            return {"message": "Like removido exitosamente"}
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error unliking post: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def add_comment(self, post_id: str, comment_data: CommentCreate, user_id: str) -> Comment:
        """Add comment to post"""
        try:
            logger.info(f"Adding comment to post {post_id} by user {user_id}")
            
            # Get post
            post = await self.post_repository.get_by_id(post_id)
            if not post:
                logger.error(f"Post not found: {post_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Publicación no encontrada"
                )
            
            # Get user
            user = await self.user_repository.get_by_id(user_id)
            if not user:
                logger.error(f"User not found: {user_id}")
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Check if user can interact with posts (only participants)
            if not user.can_interact_with_posts():
                logger.error(f"User {user_id} cannot interact with posts")
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail="Solo los participantes pueden comentar las publicaciones"
                )
            
            # Create comment
            comment = Comment(
                post_id=str(post_id),  # Convert to string
                user_id=str(user_id),  # Convert to string
                user_name=user.full_name,
                content=comment_data.content
            )
            
            logger.info(f"Created comment object: {comment.to_dict()}")
            
            # Save comment and increment post comments count
            created_comment = await self.comment_repository.create(comment)
            await self.post_repository.increment_comments_count(post_id)
            
            logger.info(f"Comment added successfully: {created_comment.id}")
            return created_comment
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error adding comment: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_post_comments(self, post_id: str, skip: int = 0, limit: int = 50) -> List[Comment]:
        """Get comments for a post"""
        try:
            # Check if post exists
            post = await self.post_repository.get_by_id(post_id)
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Publicación no encontrada"
                )
            
            return await self.comment_repository.get_by_post(post_id, skip, limit)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting post comments: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_post_likes(self, post_id: str, skip: int = 0, limit: int = 50) -> List[Like]:
        """Get likes for a post"""
        try:
            # Check if post exists
            post = await self.post_repository.get_by_id(post_id)
            if not post:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Publicación no encontrada"
                )
            
            return await self.like_repository.get_by_post(post_id, skip, limit)
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting post likes: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def _send_new_post_notification(self, post: Post) -> None:
        """Send notification for new post to participants"""
        try:
            # Get participants with FCM tokens
            participants = await self.user_repository.get_participants_with_fcm_token()
            
            if participants:
                # Extract FCM tokens
                fcm_tokens = [user.fcm_token for user in participants if user.fcm_token]
                
                if fcm_tokens:
                    # Send notification
                    notification_service.send_new_post_notification(
                        fcm_tokens,
                        post.title,
                        post.author_name,
                        str(post.id)
                    )
                    
        except Exception as e:
            logger.error(f"Error sending new post notification: {e}")
            # Don't raise exception here as notification failure shouldn't affect post creation


# Dependency injection
def get_post_service() -> PostService:
    """Get post service instance"""
    return PostService() 