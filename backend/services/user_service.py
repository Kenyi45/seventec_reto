from typing import Optional, List, Dict, Any
from models.user import User, UserCreate, UserLogin, UserUpdate, UserRole
from repositories.user_repository import UserRepository, IUserRepository
from utils.auth import auth_service
from fastapi import HTTPException, status
import logging

logger = logging.getLogger(__name__)


class UserService:
    """
    User service implementing business logic for user management.
    Follows Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP).
    """
    
    def __init__(self, user_repository: IUserRepository):
        self.user_repository = user_repository
    
    async def register_user(self, user_data: UserCreate) -> Dict[str, Any]:
        """Register a new user"""
        try:
            # Check if email already exists
            existing_user = await self.user_repository.get_by_email(user_data.email)
            if existing_user:
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail="Email ya está registrado"
                )
            
            # Hash password
            password_hash = auth_service.hash_password(user_data.password)
            
            # Create user entity
            user = User(
                email=user_data.email,
                password_hash=password_hash,
                full_name=user_data.full_name,
                role=user_data.role,
                is_active=True
            )
            
            # Save user to database
            created_user = await self.user_repository.create(user)
            
            # Create access token
            access_token = auth_service.create_access_token(
                str(created_user.id),
                created_user.email,
                created_user.role.value
            )
            
            logger.info(f"User registered successfully: {created_user.email}")
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": str(created_user.id),
                    "email": created_user.email,
                    "full_name": created_user.full_name,
                    "role": created_user.role.value,
                    "is_active": created_user.is_active
                }
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error registering user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def login_user(self, login_data: UserLogin) -> Dict[str, Any]:
        """Login user"""
        try:
            # Get user by email
            user = await self.user_repository.get_by_email(login_data.email)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Email o contraseña incorrectos"
                )
            
            # Check if user is active
            if not user.is_active:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Cuenta desactivada"
                )
            
            # Verify password
            if not auth_service.verify_password(login_data.password, user.password_hash):
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Email o contraseña incorrectos"
                )
            
            # Create access token
            access_token = auth_service.create_access_token(
                str(user.id),
                user.email,
                user.role.value
            )
            
            logger.info(f"User logged in successfully: {user.email}")
            
            return {
                "access_token": access_token,
                "token_type": "bearer",
                "user": {
                    "id": str(user.id),
                    "email": user.email,
                    "full_name": user.full_name,
                    "role": user.role.value,
                    "is_active": user.is_active
                }
            }
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error logging in user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_user_profile(self, user_id: str) -> User:
        """Get user profile"""
        try:
            user = await self.user_repository.get_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            return user
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting user profile: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def update_user_profile(self, user_id: str, update_data: UserUpdate) -> User:
        """Update user profile"""
        try:
            # Get current user
            user = await self.user_repository.get_by_id(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            # Prepare update data
            update_dict = {}
            
            if update_data.full_name is not None:
                update_dict["full_name"] = update_data.full_name
            
            if update_data.bio is not None:
                update_dict["bio"] = update_data.bio
            
            if update_data.allergies is not None:
                update_dict["allergies"] = update_data.allergies
            
            if update_data.profile_image_url is not None:
                update_dict["profile_image_url"] = update_data.profile_image_url
            
            if update_data.fcm_token is not None:
                update_dict["fcm_token"] = update_data.fcm_token
            
            # Update user
            if update_dict:
                updated_user = await self.user_repository.update(user_id, update_dict)
                if updated_user:
                    logger.info(f"User profile updated successfully: {user_id}")
                    return updated_user
            
            return user
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating user profile: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_users_by_role(self, role: UserRole, skip: int = 0, limit: int = 100) -> List[User]:
        """Get users by role"""
        try:
            return await self.user_repository.get_by_role(role.value, skip, limit)
            
        except Exception as e:
            logger.error(f"Error getting users by role: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def get_participants_with_fcm_token(self, skip: int = 0, limit: int = 100) -> List[User]:
        """Get participants with FCM token for notifications"""
        try:
            return await self.user_repository.get_participants_with_fcm_token(skip, limit)
            
        except Exception as e:
            logger.error(f"Error getting participants with FCM token: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def update_fcm_token(self, user_id: str, fcm_token: str) -> User:
        """Update user FCM token"""
        try:
            updated_user = await self.user_repository.update_fcm_token(user_id, fcm_token)
            if not updated_user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            logger.info(f"FCM token updated successfully for user: {user_id}")
            return updated_user
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error updating FCM token: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def deactivate_user(self, user_id: str) -> User:
        """Deactivate user account"""
        try:
            user = await self.user_repository.deactivate_user(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            logger.info(f"User deactivated successfully: {user_id}")
            return user
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error deactivating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )
    
    async def activate_user(self, user_id: str) -> User:
        """Activate user account"""
        try:
            user = await self.user_repository.activate_user(user_id)
            if not user:
                raise HTTPException(
                    status_code=status.HTTP_404_NOT_FOUND,
                    detail="Usuario no encontrado"
                )
            
            logger.info(f"User activated successfully: {user_id}")
            return user
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error activating user: {e}")
            raise HTTPException(
                status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
                detail="Error interno del servidor"
            )


# Dependency injection
def get_user_service() -> UserService:
    """Get user service instance"""
    return UserService(UserRepository()) 