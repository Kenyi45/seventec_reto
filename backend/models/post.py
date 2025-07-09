from typing import Optional, List
from pydantic import BaseModel, Field, field_validator
from .base import BaseEntity, BaseResponse, PyObjectId


class Comment(BaseEntity):
    """
    Comment model for posts.
    Follows Single Responsibility Principle (SRP).
    """
    
    post_id: PyObjectId = Field(..., description="Post ID")
    user_id: PyObjectId = Field(..., description="User ID")
    user_name: str = Field(..., description="User name")
    content: str = Field(..., min_length=1, max_length=500, description="Comment content")
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        """Validate comment content"""
        if not v or len(v.strip()) < 1:
            raise ValueError('Comment content cannot be empty')
        return v.strip()
    
    def validate_business_rules(self) -> bool:
        """Validate comment business rules"""
        return bool(self.content and self.user_id and self.post_id)


class Like(BaseEntity):
    """
    Like model for posts.
    Follows Single Responsibility Principle (SRP).
    """
    
    post_id: PyObjectId = Field(..., description="Post ID")
    user_id: PyObjectId = Field(..., description="User ID")
    user_name: str = Field(..., description="User name")
    
    def validate_business_rules(self) -> bool:
        """Validate like business rules"""
        return bool(self.user_id and self.post_id)


class Post(BaseEntity):
    """
    Post model implementing business logic for post management.
    Follows Single Responsibility Principle (SRP) and Open/Closed Principle (OCP).
    """
    
    title: str = Field(..., min_length=1, max_length=200, description="Post title")
    content: str = Field(..., min_length=1, max_length=2000, description="Post content")
    image_url: Optional[str] = Field(None, description="Post image URL")
    author_id: PyObjectId = Field(..., description="Author ID")
    author_name: str = Field(..., description="Author name")
    author_role: str = Field(..., description="Author role")
    likes_count: int = Field(default=0, description="Number of likes")
    comments_count: int = Field(default=0, description="Number of comments")
    likes: Optional[List[str]] = Field(default=None, description="List of user IDs who liked the post")
    comments: Optional[List[Comment]] = Field(default=None, description="List of comments for the post")
    is_active: bool = Field(default=True, description="Post active status")
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        """Validate post title"""
        if not v or len(v.strip()) < 1:
            raise ValueError('Post title cannot be empty')
        return v.strip()
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        """Validate post content"""
        if not v or len(v.strip()) < 1:
            raise ValueError('Post content cannot be empty')
        return v.strip()
    
    def validate_business_rules(self) -> bool:
        """Validate post business rules"""
        if not self.title or not self.content:
            return False
        if not self.author_id or not self.author_name:
            return False
        return True
    
    def increment_likes(self) -> None:
        """Increment likes count"""
        self.likes_count += 1
        self.mark_as_updated()
    
    def decrement_likes(self) -> None:
        """Decrement likes count"""
        if self.likes_count > 0:
            self.likes_count -= 1
            self.mark_as_updated()
    
    def increment_comments(self) -> None:
        """Increment comments count"""
        self.comments_count += 1
        self.mark_as_updated()
    
    def decrement_comments(self) -> None:
        """Decrement comments count"""
        if self.comments_count > 0:
            self.comments_count -= 1
            self.mark_as_updated()
    
    def deactivate(self) -> None:
        """Deactivate post"""
        self.is_active = False
        self.mark_as_updated()


class PostCreate(BaseModel):
    """Post creation request model"""
    
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=1, max_length=2000)
    image_url: Optional[str] = None
    
    @field_validator('title')
    @classmethod
    def validate_title(cls, v):
        """Validate post title"""
        if not v or len(v.strip()) < 1:
            raise ValueError('Post title cannot be empty')
        return v.strip()
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        """Validate post content"""
        if not v or len(v.strip()) < 1:
            raise ValueError('Post content cannot be empty')
        return v.strip()


class PostUpdate(BaseModel):
    """Post update request model"""
    
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=1, max_length=2000)
    image_url: Optional[str] = None
    is_active: Optional[bool] = None


class CommentCreate(BaseModel):
    """Comment creation request model"""
    
    content: str = Field(..., min_length=1, max_length=500)
    
    @field_validator('content')
    @classmethod
    def validate_content(cls, v):
        """Validate comment content"""
        if not v or len(v.strip()) < 1:
            raise ValueError('Comment content cannot be empty')
        return v.strip()


class PostResponse(BaseResponse):
    """Post response model"""
    
    data: Optional[Post] = None


class PostListResponse(BaseResponse):
    """Post list response model"""
    
    data: Optional[List[Post]] = None


class CommentResponse(BaseResponse):
    """Comment response model"""
    
    data: Optional[Comment] = None


class CommentListResponse(BaseResponse):
    """Comment list response model"""
    
    data: Optional[List[Comment]] = None


class LikeResponse(BaseResponse):
    """Like response model"""
    
    data: Optional[Like] = None 