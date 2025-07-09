from pydantic_settings import BaseSettings
from typing import Optional


class Settings(BaseSettings):
    """
    Application settings using Pydantic Settings.
    Follows the Single Responsibility Principle (SRP).
    """
    
    # Database settings
    database_url: str = "mongodb://localhost:27017/app_convention"
    database_name: str = "app_convention"
    
    # JWT settings
    jwt_secret: str = "your-super-secret-jwt-key-change-in-production"
    jwt_algorithm: str = "HS256"
    jwt_expiration_hours: int = 24
    
    # Firebase settings
    firebase_credentials_path: Optional[str] = None
    
    # Application settings
    app_name: str = "App Convention"
    app_version: str = "1.0.0"
    debug: bool = True
    
    class Config:
        env_file = ".env"
        case_sensitive = False


# Singleton pattern for settings
settings = Settings() 