from pydantic import BaseModel, ConfigDict
from typing import Optional


class AdBase(BaseModel):
    """Shared fields for advertisement schemas."""
    title: str
    description: Optional[str] = None
    price: float
    category: str


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
    price: Optional[float] = None
    category: Optional[str] = None


class AdOut(AdBase):
    """Schema returned to the client."""
    id: int
    # Allows returning SQLAlchemy objects directly (ORM mode in Pydantic v2)
    model_config = ConfigDict(from_attributes=True)
