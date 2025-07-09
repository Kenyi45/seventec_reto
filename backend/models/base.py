from abc import ABC, abstractmethod
from datetime import datetime
from typing import Optional, Dict, Any, Union
from pydantic import BaseModel, Field, ConfigDict, model_serializer, GetCoreSchemaHandler
from pydantic_core import core_schema
from bson import ObjectId


class PyObjectId(ObjectId):
    """Custom ObjectId type for Pydantic models"""
    
    @classmethod
    def __get_pydantic_core_schema__(cls, source_type: Any, handler: GetCoreSchemaHandler) -> core_schema.CoreSchema:
        return core_schema.with_info_after_validator_function(
            cls._validate,
            core_schema.str_schema(),
            serialization=core_schema.str_schema(),
        )
    
    @classmethod
    def _validate(cls, v: Union[str, ObjectId], handler) -> ObjectId:
        if isinstance(v, ObjectId):
            return v
        if isinstance(v, str):
            if not ObjectId.is_valid(v):
                raise ValueError("Invalid ObjectId")
            return ObjectId(v)
        raise ValueError("Invalid ObjectId")
    
    @classmethod
    def __get_pydantic_json_schema__(cls, field_schema, field):
        field_schema.update(type="string")
        return field_schema


def generate_object_id():
    """Generate a new ObjectId for default values"""
    return PyObjectId()


class BaseEntity(BaseModel, ABC):
    """
    Base entity class implementing common functionality.
    Follows the Single Responsibility Principle (SRP) and Open/Closed Principle (OCP).
    """
    
    model_config = ConfigDict(
        populate_by_name=True,
        arbitrary_types_allowed=True
    )
    
    id: Optional[PyObjectId] = Field(default_factory=generate_object_id, alias="_id")
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = None
    
    @model_serializer
    def ser_model(self) -> Dict[str, Any]:
        """Custom serializer to handle ObjectId serialization"""
        data = {}
        for key, value in self.__dict__.items():
            if isinstance(value, ObjectId):
                data[key] = str(value)
            else:
                data[key] = value
        return data
    
    def to_dict(self) -> Dict[str, Any]:
        """Convert model to dictionary"""
        return self.model_dump(by_alias=True, exclude_unset=True)
    
    @abstractmethod
    def validate_business_rules(self) -> bool:
        """
        Abstract method to validate business rules.
        Each entity must implement its own validation logic.
        """
        pass
    
    def mark_as_updated(self) -> None:
        """Mark entity as updated"""
        self.updated_at = datetime.utcnow()


class BaseResponse(BaseModel):
    """Base response model for API responses"""
    
    success: bool = True
    message: str = "Operation completed successfully"
    data: Optional[Any] = None
    errors: Optional[Dict[str, str]] = None 