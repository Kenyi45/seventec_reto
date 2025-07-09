from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from jose import JWTError, jwt
from passlib.context import CryptContext
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class PasswordManager:
    """
    Password management class for hashing and verifying passwords.
    Follows Single Responsibility Principle (SRP).
    """
    
    def __init__(self):
        self.pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
    
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return self.pwd_context.hash(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash"""
        return self.pwd_context.verify(plain_password, hashed_password)


class JWTManager:
    """
    JWT management class for creating and validating tokens.
    Follows Single Responsibility Principle (SRP).
    """
    
    def __init__(self):
        self.secret_key = settings.jwt_secret
        self.algorithm = settings.jwt_algorithm
        self.access_token_expire_hours = settings.jwt_expiration_hours
    
    def create_access_token(self, data: Dict[str, Any], expires_delta: Optional[timedelta] = None) -> str:
        """Create JWT access token"""
        try:
            to_encode = data.copy()
            
            if expires_delta:
                expire = datetime.utcnow() + expires_delta
            else:
                expire = datetime.utcnow() + timedelta(hours=self.access_token_expire_hours)
            
            to_encode.update({"exp": expire})
            
            encoded_jwt = jwt.encode(to_encode, self.secret_key, algorithm=self.algorithm)
            return encoded_jwt
            
        except Exception as e:
            logger.error(f"Error creating access token: {e}")
            raise
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify JWT token and return payload"""
        try:
            payload = jwt.decode(token, self.secret_key, algorithms=[self.algorithm])
            return payload
            
        except JWTError as e:
            logger.warning(f"JWT verification failed: {e}")
            return None
        except Exception as e:
            logger.error(f"Error verifying token: {e}")
            return None
    
    def decode_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Decode JWT token without verification (for debugging)"""
        try:
            payload = jwt.decode(token, options={"verify_signature": False})
            return payload
            
        except Exception as e:
            logger.error(f"Error decoding token: {e}")
            return None
    
    def get_token_expiry(self, token: str) -> Optional[datetime]:
        """Get token expiry date"""
        try:
            payload = self.decode_token(token)
            if payload and "exp" in payload:
                return datetime.fromtimestamp(payload["exp"])
            return None
            
        except Exception as e:
            logger.error(f"Error getting token expiry: {e}")
            return None
    
    def is_token_expired(self, token: str) -> bool:
        """Check if token is expired"""
        try:
            expiry = self.get_token_expiry(token)
            if expiry:
                return datetime.utcnow() > expiry
            return True
            
        except Exception as e:
            logger.error(f"Error checking token expiry: {e}")
            return True


class AuthService:
    """
    Authentication service combining password and JWT management.
    Follows Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP).
    """
    
    def __init__(self):
        self.password_manager = PasswordManager()
        self.jwt_manager = JWTManager()
    
    def hash_password(self, password: str) -> str:
        """Hash a password"""
        return self.password_manager.hash_password(password)
    
    def verify_password(self, plain_password: str, hashed_password: str) -> bool:
        """Verify a password"""
        return self.password_manager.verify_password(plain_password, hashed_password)
    
    def create_access_token(self, user_id: str, email: str, role: str) -> str:
        """Create access token for user"""
        data = {
            "sub": user_id,
            "email": email,
            "role": role,
            "iat": datetime.utcnow()
        }
        return self.jwt_manager.create_access_token(data)
    
    def verify_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Verify access token"""
        return self.jwt_manager.verify_token(token)
    
    def get_user_from_token(self, token: str) -> Optional[Dict[str, Any]]:
        """Extract user information from token"""
        try:
            payload = self.verify_token(token)
            if payload:
                return {
                    "user_id": payload.get("sub"),
                    "email": payload.get("email"),
                    "role": payload.get("role")
                }
            return None
            
        except Exception as e:
            logger.error(f"Error extracting user from token: {e}")
            return None
    
    def refresh_token(self, token: str) -> Optional[str]:
        """Refresh access token"""
        try:
            user_info = self.get_user_from_token(token)
            if user_info:
                return self.create_access_token(
                    user_info["user_id"],
                    user_info["email"],
                    user_info["role"]
                )
            return None
            
        except Exception as e:
            logger.error(f"Error refreshing token: {e}")
            return None


# Singleton instances
auth_service = AuthService()
password_manager = PasswordManager()
jwt_manager = JWTManager() 