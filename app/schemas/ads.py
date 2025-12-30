# de data vorm die ontvang of stuurt

from pydantic import BaseModel
from typing import Optional
from app.core.config import model_config
class AdsCreate(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str

class AdsUpdate(BaseModel):
    title: Optional[str]
    description: Optional[str]
    price: Optional[float]
    category: Optional[str]

class AdsOut(BaseModel):
    id: int
    title: str
    description: str
    price: float
    category: str




class model_config:
    from_attributes = True