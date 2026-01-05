# Used to represent date and time values (e.g. when the ad was created)
from datetime import datetime

# BaseModel is the core class used by Pydantic to define schemas
from pydantic import BaseModel


class AdvertisementOut(BaseModel):
    """
    This schema defines the structure of an advertisement
    returned by the API responses.
    """

    # Unique identifier of the advertisement
    id: int

    # Title of the advertisement
    title: str

    # Category of the advertisement (e.g. electronics, furniture)
    category: str

    # Timestamp indicating when the advertisement was created
    created_at: datetime

    # Pydantic v2 configuration:
    # Allows Pydantic to read data directly from SQLAlchemy ORM objects.
