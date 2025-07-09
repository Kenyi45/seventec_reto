from datetime import datetime, timedelta
from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from .base import BaseEntity, BaseResponse, PyObjectId


class Story(BaseEntity):
    """
    Story model for temporary content (24 hours).
    Implements the plus feature requirement.
    Follows Single Responsibility Principle (SRP).
    """
    
    content: str = Field(..., min_length=1, max_length=1000, description="Story content")
    image_url: Optional[str] = Field(None, description="Story image URL")
    author_id: PyObjectId = Field(..., description="Author ID")
    author_name: str = Field(..., description="Author name")
    author_role: str = Field(..., description="Author role")
    views_count: int = Field(default=0, description="Number of views")
    expires_at: datetime = Field(default_factory=lambda: datetime.utcnow() + timedelta(hours=24), 
                                description="Story expiration time")
    is_active: bool = Field(default=True, description="Story active status")
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        """Validate story content"""
        if not v or len(v.strip()) < 1:
            raise ValueError('Story content cannot be empty')
        return v.strip()
    
    def validate_business_rules(self) -> bool:
        """Validate story business rules"""
        if not self.content:
            return False
        if not self.author_id or not self.author_name:
            return False
        return True
    
    def is_expired(self) -> bool:
        """Check if story is expired"""
        return datetime.utcnow() > self.expires_at
    
    def increment_views(self) -> None:
        """Increment views count"""
        self.views_count += 1
        self.mark_as_updated()
    
    def expire(self) -> None:
        """Mark story as expired"""
        self.is_active = False
        self.mark_as_updated()
    
    def get_time_remaining(self) -> timedelta:
        """Get time remaining before expiration"""
        if self.is_expired():
            return timedelta(0)
        return self.expires_at - datetime.utcnow()
    
    def get_time_remaining_hours(self) -> int:
        """Get time remaining in hours"""
        remaining = self.get_time_remaining()
        return int(remaining.total_seconds() / 3600)


class StoryView(BaseEntity):
    """
    Story view model to track who viewed each story.
    Follows Single Responsibility Principle (SRP).
    """
    
    story_id: PyObjectId = Field(..., description="Story ID")
    user_id: PyObjectId = Field(..., description="User ID")
    user_name: str = Field(..., description="User name")
    
    def validate_business_rules(self) -> bool:
        """Validate story view business rules"""
        return bool(self.story_id and self.user_id)


class StoryCreate(BaseModel):
    """Story creation request model"""
    
    content: str = Field(..., min_length=1, max_length=1000)
    image_url: Optional[str] = None
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        """Validate story content"""
        if not v or len(v.strip()) < 1:
            raise ValueError('Story content cannot be empty')
        return v.strip()


class StoryUpdate(BaseModel):
    """Story update request model"""
    
    content: Optional[str] = Field(None, min_length=1, max_length=1000)
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class StoryResponse(BaseResponse):
    """Story response model"""
    
    data: Optional[Story] = None


class StoryListResponse(BaseResponse):
    """Story list response model"""
    
    data: Optional[List[Story]] = None


class StoryViewResponse(BaseResponse):
    """Story view response model"""
    
    data: Optional[StoryView] = None


class StoryViewListResponse(BaseResponse):
    """Story view list response model"""
    
    data: Optional[List[StoryView]] = None 