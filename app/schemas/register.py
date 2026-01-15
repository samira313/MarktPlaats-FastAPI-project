from pydantic import BaseModel, EmailStr, Field, field_validator, ConfigDict
from datetime import datetime


class UserCreate(BaseModel):
    """
    Input schema for creating a new user.
    Notes:
    - bcrypt has a hard limit of 72 BYTES (UTF-8).
    - We validate bytes length to avoid server crashes.
    """
    username: str = Field(..., min_length=3, max_length=50)
    email: EmailStr | None = None
    password: str = Field(..., min_length=6, max_length=200)  # allow chars, but we validate bytes

    @field_validator("password")
    @classmethod
    def password_max_72_bytes(cls, v: str) -> str:
        # Normalize accidental spaces/newlines
        v = v.strip()

        # bcrypt limit is BYTES, not characters
        if len(v.encode("utf-8")) > 72:
            raise ValueError("Password must be 72 bytes or less (bcrypt limitation).")
        return v


class UserOut(BaseModel):
    """
    Output schema for returning safe user data.
    Never include password/hashed_password here.
    """
    id: int
    username: str
    email: EmailStr | None = None
    # created_at: datetime  # if you have it
    created_at: datetime

    # class Config:
    #     """
    #     Allows Pydantic to read data from SQLAlchemy objects.
    #     """
    #     from_attributes = True
    model_config = ConfigDict(from_attributes=True)