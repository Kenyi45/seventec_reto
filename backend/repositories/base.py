from abc import ABC, abstractmethod
from typing import List, Optional, Dict, Any, TypeVar, Generic
from bson import ObjectId
from motor.motor_asyncio import AsyncIOMotorCollection
from database.connection import db_connection
from models.base import BaseEntity
import logging

logger = logging.getLogger(__name__)

T = TypeVar('T', bound=BaseEntity)


class IRepository(ABC, Generic[T]):
    """
    Repository interface defining contract for data access operations.
    Follows Interface Segregation Principle (ISP) and Dependency Inversion Principle (DIP).
    """
    
    @abstractmethod
    async def create(self, entity: T) -> T:
        """Create a new entity"""
        pass
    
    @abstractmethod
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """Get entity by ID"""
        pass
    
    @abstractmethod
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination"""
        pass
    
    @abstractmethod
    async def update(self, entity_id: str, update_data: Dict[str, Any]) -> Optional[T]:
        """Update entity"""
        pass
    
    @abstractmethod
    async def delete(self, entity_id: str) -> bool:
        """Delete entity"""
        pass
    
    @abstractmethod
    async def exists(self, entity_id: str) -> bool:
        """Check if entity exists"""
        pass


class BaseRepository(IRepository[T]):
    """
    Base repository implementation providing common CRUD operations.
    Follows Single Responsibility Principle (SRP) and Don't Repeat Yourself (DRY).
    """
    
    def __init__(self, collection_name: str, entity_class: type):
        self.collection_name = collection_name
        self.entity_class = entity_class
    
    @property
    def collection(self) -> AsyncIOMotorCollection:
        """Get collection instance"""
        return db_connection.database[self.collection_name]
    
    def _convert_document(self, document: Dict[str, Any]) -> Dict[str, Any]:
        """Convert MongoDB document to Pydantic-compatible format"""
        if not document:
            return document
        
        converted = {}
        for key, value in document.items():
            if isinstance(value, ObjectId):
                converted[key] = str(value)
            elif isinstance(value, dict):
                converted[key] = self._convert_document(value)
            elif isinstance(value, list):
                converted[key] = [
                    self._convert_document(item) if isinstance(item, dict) else str(item) if isinstance(item, ObjectId) else item
                    for item in value
                ]
            else:
                converted[key] = value
        
        return converted
    
    async def create(self, entity: T) -> T:
        """Create a new entity"""
        try:
            # Validate business rules
            if not entity.validate_business_rules():
                raise ValueError("Entity validation failed")
            
            # Convert to dict and insert
            entity_dict = entity.to_dict()
            result = await self.collection.insert_one(entity_dict)
            
            # Update entity with generated ID
            if result.inserted_id:
                entity.id = result.inserted_id
            
            logger.info(f"Created {self.entity_class.__name__} with ID: {entity.id}")
            return entity
            
        except Exception as e:
            logger.error(f"Error creating {self.entity_class.__name__}: {e}")
            raise
    
    async def get_by_id(self, entity_id: str) -> Optional[T]:
        """Get entity by ID"""
        try:
            if not ObjectId.is_valid(entity_id):
                return None
            
            document = await self.collection.find_one({"_id": ObjectId(entity_id)})
            
            if document:
                converted_doc = self._convert_document(document)
                return self.entity_class(**converted_doc)
            return None
            
        except Exception as e:
            logger.error(f"Error getting {self.entity_class.__name__} by ID {entity_id}: {e}")
            return None
    
    async def get_all(self, skip: int = 0, limit: int = 100) -> List[T]:
        """Get all entities with pagination"""
        try:
            cursor = self.collection.find().skip(skip).limit(limit)
            documents = await cursor.to_list(length=limit)
            
            return [self.entity_class(**self._convert_document(doc)) for doc in documents]
            
        except Exception as e:
            logger.error(f"Error getting all {self.entity_class.__name__}: {e}")
            return []
    
    async def update(self, entity_id: str, update_data: Dict[str, Any]) -> Optional[T]:
        """Update entity"""
        try:
            if not ObjectId.is_valid(entity_id):
                return None
            
            # Add updated_at timestamp
            from datetime import datetime
            update_data['updated_at'] = datetime.utcnow()
            
            result = await self.collection.update_one(
                {"_id": ObjectId(entity_id)},
                {"$set": update_data}
            )
            
            if result.modified_count > 0:
                return await self.get_by_id(entity_id)
            return None
            
        except Exception as e:
            logger.error(f"Error updating {self.entity_class.__name__} {entity_id}: {e}")
            return None
    
    async def delete(self, entity_id: str) -> bool:
        """Delete entity"""
        try:
            if not ObjectId.is_valid(entity_id):
                return False
            
            result = await self.collection.delete_one({"_id": ObjectId(entity_id)})
            
            if result.deleted_count > 0:
                logger.info(f"Deleted {self.entity_class.__name__} with ID: {entity_id}")
                return True
            return False
            
        except Exception as e:
            logger.error(f"Error deleting {self.entity_class.__name__} {entity_id}: {e}")
            return False
    
    async def exists(self, entity_id: str) -> bool:
        """Check if entity exists"""
        try:
            if not ObjectId.is_valid(entity_id):
                return False
            
            count = await self.collection.count_documents({"_id": ObjectId(entity_id)})
            return count > 0
            
        except Exception as e:
            logger.error(f"Error checking existence of {self.entity_class.__name__} {entity_id}: {e}")
            return False
    
    async def find_by_filter(self, filter_dict: Dict[str, Any], 
                           skip: int = 0, limit: int = 100) -> List[T]:
        """Find entities by filter"""
        try:
            cursor = self.collection.find(filter_dict).skip(skip).limit(limit)
            documents = await cursor.to_list(length=limit)
            
            return [self.entity_class(**self._convert_document(doc)) for doc in documents]
            
        except Exception as e:
            logger.error(f"Error finding {self.entity_class.__name__} with filter: {e}")
            return []
    
    async def count_by_filter(self, filter_dict: Dict[str, Any]) -> int:
        """Count entities by filter"""
        try:
            return await self.collection.count_documents(filter_dict)
            
        except Exception as e:
            logger.error(f"Error counting {self.entity_class.__name__} with filter: {e}")
            return 0 