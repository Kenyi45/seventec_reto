from fastapi import APIRouter, Depends, HTTPException, status, Query
from typing import Dict, Any, List
from models.story import (
    StoryCreate, StoryUpdate, 
    StoryResponse, StoryListResponse, StoryViewListResponse
)
from models.base import BaseResponse
from services.story_service import StoryService, get_story_service
from middleware.auth_middleware import (
    get_current_active_user, require_organizer_role
)
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/stories",
    tags=["stories"],
    responses={404: {"description": "Not found"}},
)


@router.post("/", response_model=StoryResponse, status_code=status.HTTP_201_CREATED)
async def create_story(
    story_data: StoryCreate,
    current_user: Dict[str, Any] = Depends(require_organizer_role),
    story_service: StoryService = Depends(get_story_service)
) -> StoryResponse:
    """
    Create a new story.
    
    Stories automatically expire after 24 hours.
    Only organizers can create stories.
    
    - **content**: Story content (required)
    - **image_url**: Story image URL (optional)
    
    Requires valid JWT token with organizer role.
    """
    try:
        story = await story_service.create_story(story_data, current_user["user_id"])
        
        return StoryResponse(
            success=True,
            message="Historia creada exitosamente",
            data=story
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in create_story endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/", response_model=StoryListResponse)
async def get_active_stories(
    skip: int = Query(0, ge=0, description="Number of stories to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of stories to return"),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    story_service: StoryService = Depends(get_story_service)
) -> StoryListResponse:
    """
    Get active stories with pagination.
    
    Only returns stories that haven't expired (within 24 hours).
    
    - **skip**: Number of stories to skip (default: 0)
    - **limit**: Number of stories to return (default: 20, max: 100)
    
    Requires valid JWT token.
    """
    try:
        stories = await story_service.get_active_stories(skip, limit)
        
        return StoryListResponse(
            success=True,
            message="Historias activas obtenidas exitosamente",
            data=stories
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_active_stories endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/{story_id}", response_model=BaseResponse)
async def view_story(
    story_id: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    story_service: StoryService = Depends(get_story_service)
) -> BaseResponse:
    """
    View a specific story by ID.
    
    This endpoint tracks the view and increments the view count.
    
    - **story_id**: Story ID
    
    Requires valid JWT token.
    """
    try:
        result = await story_service.view_story(story_id, current_user["user_id"])
        
        return BaseResponse(
            success=True,
            message="Historia obtenida exitosamente",
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in view_story endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.put("/{story_id}", response_model=StoryResponse)
async def update_story(
    story_id: str,
    update_data: StoryUpdate,
    current_user: Dict[str, Any] = Depends(require_organizer_role),
    story_service: StoryService = Depends(get_story_service)
) -> StoryResponse:
    """
    Update a story.
    
    Only the author can update their own stories.
    Cannot update expired stories.
    
    - **story_id**: Story ID
    - **content**: New story content (optional)
    - **image_url**: New story image URL (optional)
    - **is_active**: Story active status (optional)
    
    Requires valid JWT token with organizer role.
    """
    try:
        story = await story_service.update_story(story_id, update_data, current_user["user_id"])
        
        return StoryResponse(
            success=True,
            message="Historia actualizada exitosamente",
            data=story
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_story endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.delete("/{story_id}", response_model=BaseResponse)
async def delete_story(
    story_id: str,
    current_user: Dict[str, Any] = Depends(require_organizer_role),
    story_service: StoryService = Depends(get_story_service)
) -> BaseResponse:
    """
    Delete a story.
    
    Only the author can delete their own stories.
    
    - **story_id**: Story ID
    
    Requires valid JWT token with organizer role.
    """
    try:
        deleted = await story_service.delete_story(story_id, current_user["user_id"])
        
        if deleted:
            return BaseResponse(
                success=True,
                message="Historia eliminada exitosamente"
            )
        else:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Historia no encontrada"
            )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in delete_story endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/{story_id}/views", response_model=StoryViewListResponse)
async def get_story_views(
    story_id: str,
    skip: int = Query(0, ge=0, description="Number of views to skip"),
    limit: int = Query(50, ge=1, le=100, description="Number of views to return"),
    current_user: Dict[str, Any] = Depends(require_organizer_role),
    story_service: StoryService = Depends(get_story_service)
) -> StoryViewListResponse:
    """
    Get views for a story.
    
    Only the story author can see who viewed their story.
    
    - **story_id**: Story ID
    - **skip**: Number of views to skip (default: 0)
    - **limit**: Number of views to return (default: 50, max: 100)
    
    Requires valid JWT token with organizer role.
    """
    try:
        views = await story_service.get_story_views(story_id, current_user["user_id"], skip, limit)
        
        return StoryViewListResponse(
            success=True,
            message="Visualizaciones obtenidas exitosamente",
            data=views
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_story_views endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/author/{author_id}", response_model=StoryListResponse)
async def get_stories_by_author(
    author_id: str,
    skip: int = Query(0, ge=0, description="Number of stories to skip"),
    limit: int = Query(20, ge=1, le=100, description="Number of stories to return"),
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    story_service: StoryService = Depends(get_story_service)
) -> StoryListResponse:
    """
    Get active stories by a specific author.
    
    - **author_id**: Author user ID
    - **skip**: Number of stories to skip (default: 0)
    - **limit**: Number of stories to return (default: 20, max: 100)
    
    Requires valid JWT token.
    """
    try:
        stories = await story_service.get_stories_by_author(author_id, skip, limit)
        
        return StoryListResponse(
            success=True,
            message="Historias del autor obtenidas exitosamente",
            data=stories
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_stories_by_author endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/expire-old", response_model=BaseResponse)
async def expire_old_stories(
    # This endpoint should be called by a scheduled job
    # In production, this would be protected by an internal API key or called from Cloud Functions
    story_service: StoryService = Depends(get_story_service)
) -> BaseResponse:
    """
    Expire old stories that have passed their 24-hour limit.
    
    This endpoint is intended to be called by scheduled jobs (Cloud Scheduler + Cloud Functions).
    In production, this should be protected by internal authentication.
    """
    try:
        expired_count = await story_service.expire_old_stories()
        
        return BaseResponse(
            success=True,
            message=f"Se expiraron {expired_count} historias",
            data={"expired_count": expired_count}
        )
        
    except Exception as e:
        logger.error(f"Error in expire_old_stories endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        ) 