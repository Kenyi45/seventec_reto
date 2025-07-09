from fastapi import APIRouter, Depends, HTTPException, status
from typing import Dict, Any
from models.user import UserCreate, UserLogin, UserUpdate, TokenResponse, UserResponse
from services.user_service import UserService, get_user_service
from middleware.auth_middleware import get_current_user, get_current_active_user
import logging

logger = logging.getLogger(__name__)

router = APIRouter(
    prefix="/auth",
    tags=["authentication"],
    responses={404: {"description": "Not found"}},
)


@router.post("/register", response_model=TokenResponse, status_code=status.HTTP_201_CREATED)
async def register(
    user_data: UserCreate,
    user_service: UserService = Depends(get_user_service)
) -> TokenResponse:
    """
    Register a new user.
    
    - **email**: Valid email address
    - **password**: Password (minimum 8 characters)
    - **full_name**: Full name of the user
    - **role**: User role (organizer or participant)
    """
    try:
        result = await user_service.register_user(user_data)
        
        return TokenResponse(
            success=True,
            message="Usuario registrado exitosamente",
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in register endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/login", response_model=TokenResponse)
async def login(
    login_data: UserLogin,
    user_service: UserService = Depends(get_user_service)
) -> TokenResponse:
    """
    Login user with email and password.
    
    - **email**: User email address
    - **password**: User password
    """
    try:
        result = await user_service.login_user(login_data)
        
        return TokenResponse(
            success=True,
            message="Inicio de sesión exitoso",
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in login endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.get("/me", response_model=UserResponse)
async def get_current_user_profile(
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Get current user profile.
    
    Requires valid JWT token.
    """
    try:
        user = await user_service.get_user_profile(current_user["user_id"])
        
        return UserResponse(
            success=True,
            message="Perfil obtenido exitosamente",
            data=user
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in get_current_user_profile endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.put("/me", response_model=UserResponse)
async def update_current_user_profile(
    update_data: UserUpdate,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Update current user profile.
    
    - **full_name**: New full name (optional)
    - **bio**: User biography (optional)
    - **allergies**: List of allergies (optional)
    - **profile_image_url**: Profile image URL (optional)
    - **fcm_token**: Firebase Cloud Messaging token (optional)
    
    Requires valid JWT token.
    """
    try:
        user = await user_service.update_user_profile(current_user["user_id"], update_data)
        
        return UserResponse(
            success=True,
            message="Perfil actualizado exitosamente",
            data=user
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_current_user_profile endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/refresh", response_model=TokenResponse)
async def refresh_token(
    current_user: Dict[str, Any] = Depends(get_current_user),
    user_service: UserService = Depends(get_user_service)
) -> TokenResponse:
    """
    Refresh access token.
    
    Requires valid JWT token.
    """
    try:
        # Get user from database to ensure it's still active
        user = await user_service.get_user_profile(current_user["user_id"])
        
        # Create new access token
        from utils.auth import auth_service
        access_token = auth_service.create_access_token(
            str(user.id),
            user.email,
            user.role.value
        )
        
        result = {
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
        
        return TokenResponse(
            success=True,
            message="Token renovado exitosamente",
            data=result
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in refresh_token endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        )


@router.post("/fcm-token", response_model=UserResponse)
async def update_fcm_token(
    fcm_token: str,
    current_user: Dict[str, Any] = Depends(get_current_active_user),
    user_service: UserService = Depends(get_user_service)
) -> UserResponse:
    """
    Update FCM token for push notifications.
    
    - **fcm_token**: Firebase Cloud Messaging token
    
    Requires valid JWT token.
    """
    try:
        user = await user_service.update_fcm_token(current_user["user_id"], fcm_token)
        
        return UserResponse(
            success=True,
            message="Token FCM actualizado exitosamente",
            data=user
        )
        
    except HTTPException:
        raise
    except Exception as e:
        logger.error(f"Error in update_fcm_token endpoint: {e}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Error interno del servidor"
        ) 