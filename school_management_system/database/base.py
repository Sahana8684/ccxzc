from typing import Any, Dict, Generic, List, Optional, Type, TypeVar, Union

from pydantic import BaseModel
from sqlalchemy.ext.declarative import declarative_base, DeclarativeMeta

# SQLAlchemy models base
Base = declarative_base()

# Pydantic models
class BaseSchema(BaseModel):
    class Config:
        orm_mode = True
        arbitrary_types_allowed = True


# Generic types for SQLAlchemy models and Pydantic schemas
ModelType = TypeVar("ModelType", bound=Base)
SchemaType = TypeVar("SchemaType", bound=BaseSchema)
CreateSchemaType = TypeVar("CreateSchemaType", bound=BaseSchema)
UpdateSchemaType = TypeVar("UpdateSchemaType", bound=BaseSchema)
