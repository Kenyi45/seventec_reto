from typing import Optional
from motor.motor_asyncio import AsyncIOMotorClient, AsyncIOMotorDatabase
from pymongo.errors import ConnectionFailure
from config.settings import settings
import logging

logger = logging.getLogger(__name__)


class DatabaseConnection:
    """
    Database connection class implementing Singleton pattern.
    Follows Single Responsibility Principle (SRP) and Dependency Inversion Principle (DIP).
    """
    
    _instance: Optional['DatabaseConnection'] = None
    _client: Optional[AsyncIOMotorClient] = None
    _database: Optional[AsyncIOMotorDatabase] = None
    
    def __new__(cls) -> 'DatabaseConnection':
        """Singleton pattern implementation"""
        if cls._instance is None:
            cls._instance = super().__new__(cls)
        return cls._instance
    
    async def connect(self) -> None:
        """Connect to MongoDB database"""
        try:
            if self._client is None:
                self._client = AsyncIOMotorClient(settings.database_url)
                self._database = self._client[settings.database_name]
                
                # Test connection
                await self._client.admin.command('ping')
                logger.info(f"Connected to MongoDB database: {settings.database_name}")
                
        except ConnectionFailure as e:
            logger.error(f"Failed to connect to MongoDB: {e}")
            raise
        except Exception as e:
            logger.error(f"Unexpected error connecting to MongoDB: {e}")
            raise
    
    async def disconnect(self) -> None:
        """Disconnect from MongoDB database"""
        if self._client:
            self._client.close()
            self._client = None
            self._database = None
            logger.info("Disconnected from MongoDB")
    
    @property
    def database(self) -> AsyncIOMotorDatabase:
        """Get database instance"""
        if self._database is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._database
    
    @property
    def client(self) -> AsyncIOMotorClient:
        """Get client instance"""
        if self._client is None:
            raise RuntimeError("Database not connected. Call connect() first.")
        return self._client
    
    async def health_check(self) -> bool:
        """Check database health"""
        try:
            await self._client.admin.command('ping')
            return True
        except Exception:
            return False


# Singleton instance
db_connection = DatabaseConnection() 