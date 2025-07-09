from enum import Enum
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, field_validator
from .base import BaseEntity, BaseResponse


class UserRole(str, Enum):
    """User roles enumeration"""
    ORGANIZER = "organizer"
    PARTICIPANT = "participant"


class User(BaseEntity):
    """
    User model implementing business logic for user management.
    Follows Single Responsibility Principle (SRP) and Liskov Substitution Principle (LSP).
    """
    
    email: EmailStr = Field(..., description="User email address")
    password_hash: str = Field(..., description="Hashed password")
    full_name: str = Field(..., min_length=2, max_length=100, description="User full name")
    bio: Optional[str] = Field(None, max_length=500, description="User biography")
    allergies: Optional[List[str]] = Field(default_factory=list, description="User allergies")
    role: UserRole = Field(default=UserRole.PARTICIPANT, description="User role")
    is_active: bool = Field(default=True, description="User active status")
    fcm_token: Optional[str] = Field(None, description="Firebase Cloud Messaging token")
    profile_image_url: Optional[str] = Field(None, description="Profile image URL")
    
    @field_validator('email')
    @classmethod
    def validate_email(cls, v):
        """Validate email format"""
        if not v or '@' not in v:
            raise ValueError('Invalid email format')
        return v.lower()
    
    @field_validator('full_name')
    @classmethod
    def validate_full_name(cls, v):
        """Validate full name"""
        if not v or len(v.strip()) < 2:
            raise ValueError('Full name must be at least 2 characters long')
        return v.strip()
    
    def validate_business_rules(self) -> bool:
        """Validate user business rules"""
        if not self.email or not self.password_hash:
            return False
        if not self.full_name or len(self.full_name.strip()) < 2:
            return False
        return True
    
    def is_organizer(self) -> bool:
        """Check if user is an organizer"""
        return self.role == UserRole.ORGANIZER
    
    def is_participant(self) -> bool:
        """Check if user is a participant"""
        return self.role == UserRole.PARTICIPANT
    
    def can_create_posts(self) -> bool:
        """Check if user can create posts"""
        return self.is_organizer() and self.is_active
    
    def can_interact_with_posts(self) -> bool:
        """Check if user can like and comment on posts"""
        return self.is_participant() and self.is_active
    
    def update_profile(self, full_name: Optional[str] = None, 
                      bio: Optional[str] = None, 
                      allergies: Optional[List[str]] = None) -> None:
        """Update user profile"""
        if full_name:
            self.full_name = full_name
        if bio is not None:
            self.bio = bio
        if allergies is not None:
            self.allergies = allergies
        self.mark_as_updated()


class UserCreate(BaseModel):
    """User creation request model"""
    
    email: EmailStr
    password: str = Field(..., min_length=8, description="Password must be at least 8 characters")
    full_name: str = Field(..., min_length=2, max_length=100)
    role: UserRole = UserRole.PARTICIPANT
    
    @field_validator('password')
    @classmethod
    def validate_password(cls, v):
        """Validate password strength"""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        return v


class UserLogin(BaseModel):
    """User login request model"""
    
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    """User update request model"""
    
    full_name: Optional[str] = Field(None, min_length=2, max_length=100)
    bio: Optional[str] = Field(None, max_length=500)
    allergies: Optional[List[str]] = None
    profile_image_url: Optional[str] = None
    fcm_token: Optional[str] = None


class UserResponse(BaseResponse):
    """User response model"""
    
    data: Optional[User] = None


class UserListResponse(BaseResponse):
    """User list response model"""
    
    data: Optional[List[User]] = None


class TokenResponse(BaseResponse):
    """Token response model"""
    
    data: Optional[dict] = None 