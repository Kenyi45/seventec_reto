from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, Any, List
from models.post import (
    PostCreate, PostUpdate, CommentCreate, 
    PostResponse, PostListResponse, CommentResponse, CommentListResponse
)
from models.base import BaseResponse
from services.post_service import PostService, get_post_service
from middleware.auth_middleware import (
    get_current_active_user, require_organizer_role, 
    require_participant_role
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/posts",
    tags=["posts"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
async def create_post(
    post_data: PostCreate,
    current_user: Dict[str, Any] = Depends(require_organizer_role),
    post_service: PostService = Depends(get_post_service)
) -> PostResponse:
    """
    Create a new post.
    
    Only organizers can create posts.
    
    - **title**: Post title (required)
    - **content**: Post content (required)
    - **image_url**: Post image URL (optional)
    
    Requires valid JWT token with organizer role.
    """
    try:
        post = await post_service.create_post(post_data, current_user["user_id"])
        
        return PostResponse(
            success=True,
            message="Publicación creada exitosamente",
            data=post
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_post endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/", response_model=PostListResponse)
async def get_posts(
    skip: int = Query(0, ge=0, description="Number of posts to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of posts to return"),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    post_service: PostService = Depends(get_post_service)
) -> PostListResponse:
    """
    Get active posts with pagination.
    
    - **skip**: Number of posts to skip (default: 0)
    - **limit**: Number of posts to return (default: 20, max: 100)
    
    Requires valid JWT token.
    """
    try:
        posts = await post_service.get_posts(skip, limit)
        
        return PostListResponse(
            success=True,
            message="Publicaciones obtenidas exitosamente",
            data=posts
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_posts endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/{post_id}", response_model=PostResponse)
async def get_post(
    post_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    post_service: PostService = Depends(get_post_service)
) -> PostResponse:
    """
    Get a specific post by ID.
    
    - **post_id**: Post ID
    
    Requires valid JWT token.
    """
    try:
        post = await post_service.get_post_by_id(post_id)
        
        return PostResponse(
            success=True,
            message="Publicación obtenida exitosamente",
            data=post
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_post endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.put("/{post_id}", response_model=PostResponse)
async def update_post(
    post_id: str,
    update_data: PostUpdate,
    current_user: Dict[str, Any] = Depends(require_organizer_role),
    post_service: PostService = Depends(get_post_service)
) -> PostResponse:
    """
    Update a post.
    
    Only the author can update their own posts.
    
    - **post_id**: Post ID
    - **title**: New post title (optional)
    - **content**: New post content (optional)
    - **image_url**: New post image URL (optional)
    - **is_active**: Post active status (optional)
    
    Requires valid JWT token with organizer role.
    """
    try:
        post = await post_service.update_post(post_id, update_data, current_user["user_id"])
        
        return PostResponse(
            success=True,
            message="Publicación actualizada exitosamente",
            data=post
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_post endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.delete("/{post_id}", response_model=BaseResponse)
async def delete_post(
    post_id: str,
    current_user: Dict[str, Any] = Depends(require_organizer_role),
    post_service: PostService = Depends(get_post_service)
) -> BaseResponse:
    """
    Delete a post.
    
    Only the author can delete their own posts.
    
    - **post_id**: Post ID
    
    Requires valid JWT token with organizer role.
    """
    try:
        deleted = await post_service.delete_post(post_id, current_user["user_id"])
        
        if deleted:
            return BaseResponse(
                success=True,
                message="Publicación eliminada exitosamente"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Publicación no encontrada"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_post endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/{post_id}/like", response_model=BaseResponse)
async def like_post(
    post_id: str,
    current_user: Dict[str, Any] = Depends(require_participant_role),
    post_service: PostService = Depends(get_post_service)
) -> BaseResponse:
    """
    Like a post.
    
    Only participants can like posts.
    
    - **post_id**: Post ID
    
    Requires valid JWT token with participant role.
    """
    try:
        result = await post_service.like_post(post_id, current_user["user_id"])
        
        return BaseResponse(
            success=True,
            message=result["message"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in like_post endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.delete("/{post_id}/like", response_model=BaseResponse)
async def unlike_post(
    post_id: str,
    current_user: Dict[str, Any] = Depends(require_participant_role),
    post_service: PostService = Depends(get_post_service)
) -> BaseResponse:
    """
    Unlike a post.
    
    Only participants can unlike posts.
    
    - **post_id**: Post ID
    
    Requires valid JWT token with participant role.
    """
    try:
        result = await post_service.unlike_post(post_id, current_user["user_id"])
        
        return BaseResponse(
            success=True,
            message=result["message"]
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in unlike_post endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/{post_id}/comments", response_model=CommentResponse, status_code=status.HTTP_201_CREATED)
async def add_comment(
    post_id: str,
    comment_data: CommentCreate,
    current_user: Dict[str, Any] = Depends(require_participant_role),
    post_service: PostService = Depends(get_post_service)
) -> CommentResponse:
    """
    Add a comment to a post.
    
    Only participants can comment on posts.
    
    - **post_id**: Post ID
    - **content**: Comment content (required)
    
    Requires valid JWT token with participant role.
    """
    try:
        comment = await post_service.add_comment(post_id, comment_data, current_user["user_id"])
        
        return CommentResponse(
            success=True,
            message="Comentario agregado exitosamente",
            data=comment
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in add_comment endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/{post_id}/comments", response_model=CommentListResponse)
async def get_post_comments(
    post_id: str,
    skip: int = Query(0, ge=0, description="Number of comments to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of comments to return"),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    post_service: PostService = Depends(get_post_service)
) -> CommentListResponse:
    """
    Get comments for a post.
    
    - **post_id**: Post ID
    - **skip**: Number of comments to skip (default: 0)
    - **limit**: Number of comments to return (default: 50, max: 100)
    
    Requires valid JWT token.
    """
    try:
        comments = await post_service.get_post_comments(post_id, skip, limit)
        
        return CommentListResponse(
            success=True,
            message="Comentarios obtenidos exitosamente",
            data=comments
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_post_comments endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/{post_id}/likes", response_model=BaseResponse)
async def get_post_likes(
    post_id: str,
    skip: int = Query(0, ge=0, description="Number of likes to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of likes to return"),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    post_service: PostService = Depends(get_post_service)
) -> BaseResponse:
    """
    Get likes for a post.
    
    - **post_id**: Post ID
    - **skip**: Number of likes to skip (default: 0)
    - **limit**: Number of likes to return (default: 50, max: 100)
    
    Requires valid JWT token.
    """
    try:
        likes = await post_service.get_post_likes(post_id, skip, limit)
        
        return BaseResponse(
            success=True,
            message="Likes obtenidos exitosamente",
            data=likes
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_post_likes endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        ) 