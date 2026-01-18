from pydantic import BaseModel, field_validator
from typing import Optional, Literal

class AdSearch(BaseModel):
    title: Optional[str] = None
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    status: Optional[Literal["available", "reserved", "sold"]] = None

    @field_validator("max_price")
    @classmethod
    def validate_price_range(cls, v, info):
        min_price = info.data.get("min_price")
        if v is not None and min_price is not None and v < min_price:
            raise ValueError("max_price cannot be less than min_price")
        return v

