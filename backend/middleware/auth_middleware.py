from fastapi import Request, HTTPException, status, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from typing import Optional, Dict, Any
from utils.auth import auth_service
from models.user import UserRole
import logging

logger = logging.getLogger(__name__)

# Security scheme for JWT
security = HTTPBearer()


class AuthMiddleware:
    """
    Authentication middleware for JWT token validation.
    Follows Single Responsibility Principle (SRP).
    """
    
    @staticmethod
    def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
        """
        Get current user from JWT token.
        This function is used as a dependency in FastAPI endpoints.
        """
        try:
            token = credentials.credentials
            user_info = auth_service.get_user_from_token(token)
            
            if not user_info:
                raise HTTPException(
                    status_code=status.HTTP_401_UNAUTHORIZED,
                    detail="Token inválido o expirado",
                    headers={"WWW-Authenticate": "Bearer"},
                )
            
            return user_info
            
        except HTTPException:
            raise
        except Exception as e:
            logger.error(f"Error getting current user: {e}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Error de autenticación",
                headers={"WWW-Authenticate": "Bearer"},
            )
    
    @staticmethod
    def get_current_active_user(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        """
        Get current active user.
        Extends get_current_user to add active user validation.
        """
        # Note: In a real application, you would check if the user is active
        # by querying the database. For simplicity, we assume all users are active.
        return current_user
    
    @staticmethod
    def require_role(required_role: UserRole):
        """
        Create a dependency that requires a specific user role.
        This is a factory function that returns a dependency function.
        """
        def role_checker(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
            user_role = current_user.get("role")
            
            if user_role != required_role.value:
                raise HTTPException(
                    status_code=status.HTTP_403_FORBIDDEN,
                    detail=f"Acceso denegado. Se requiere rol: {required_role.value}",
                )
            
            return current_user
        
        return role_checker
    
    @staticmethod
    def require_organizer_role(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        """
        Require organizer role.
        Convenience function for organizer-only endpoints.
        """
        user_role = current_user.get("role")
        
        if user_role != UserRole.ORGANIZER.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado. Solo organizadores pueden realizar esta acción",
            )
        
        return current_user
    
    @staticmethod
    def require_participant_role(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
        """
        Require participant role.
        Convenience function for participant-only endpoints.
        """
        user_role = current_user.get("role")
        
        if user_role != UserRole.PARTICIPANT.value:
            raise HTTPException(
                status_code=status.HTTP_403_FORBIDDEN,
                detail="Acceso denegado. Solo participantes pueden realizar esta acción",
            )
        
        return current_user
    
    @staticmethod
    def optional_auth(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[Dict[str, Any]]:
        """
        Optional authentication for endpoints that work with or without authentication.
        """
        if not credentials:
            return None
        
        try:
            token = credentials.credentials
            user_info = auth_service.get_user_from_token(token)
            return user_info
        except Exception as e:
            logger.warning(f"Optional auth failed: {e}")
            return None


# Convenience functions for use as dependencies
def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)) -> Dict[str, Any]:
    """Get current user from JWT token"""
    return AuthMiddleware.get_current_user(credentials)


def get_current_active_user(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Get current active user"""
    return AuthMiddleware.get_current_active_user(current_user)


def require_organizer_role(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Require organizer role"""
    return AuthMiddleware.require_organizer_role(current_user)


def require_participant_role(current_user: Dict[str, Any] = Depends(get_current_user)) -> Dict[str, Any]:
    """Require participant role"""
    return AuthMiddleware.require_participant_role(current_user)


def optional_auth(credentials: Optional[HTTPAuthorizationCredentials] = Depends(security)) -> Optional[Dict[str, Any]]:
    """Optional authentication"""
    return AuthMiddleware.optional_auth(credentials)


# Role-based access control decorators
def require_role(required_role: UserRole):
    """Create a dependency that requires a specific user role"""
    return AuthMiddleware.require_role(required_role) 