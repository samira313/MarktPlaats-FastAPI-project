from pydantic import (BaseModel
, ConfigDict, PositiveFloat)
from typing import Optional, List, Literal
from datetime import datetime





class OwnerOut(BaseModel):
    username: str
    model_config = ConfigDict(from_attributes=True)


class AdBase(BaseModel):
    """Shared fields for advertisement schemas."""
    title: str
    description: Optional[str] = None
    price: PositiveFloat
    category: List[str]

class AdOut(AdBase):
    """Schema returned to the client."""
    id: int
    status: Literal["available", "reserved", "sold"]  #
    created_at: datetime
    owner: OwnerOut

    model_config = ConfigDict(from_attributes=True)


class AdCreate(AdBase):
    """Schema used when creating a new advertisement."""
    pass


class AdUpdate(BaseModel):
    """
       Schema used for updating an advertisement.
       All fields are optional because partial updates are allowed.
       """
    title: Optional[str] = None
    description: Optional[str] = None
    price: Optional[PositiveFloat] = None
    category: Optional[List[str]] = None


class AdOut(AdBase):
    """Schema returned to the client."""
    id: int
    status: Literal["available", "reserved", "sold"]
    created_at: datetime
    owner: OwnerOut


    # Allows returning SQLAlchemy objects directly (ORM mode in Pydantic v2)
    model_config = ConfigDict(from_attributes=True)
