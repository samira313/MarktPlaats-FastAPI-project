# Import FastAPI tools for creating routers and handling dependencies
from fastapi import APIRouter, Depends, Query

# Import SQLAlchemy session type
from sqlalchemy.orm import Session

# Import typing helpers
from typing import List, Optional

# Import the database session dependency
from app.db.database import get_db

# Import the Advertisement SQLAlchemy model
from app.models.advertisements import Advertisement

# Import the response schema
from app.schemas.advertisements import AdvertisementOut


# Create a router for advertisement-related endpoints
router = APIRouter(
    prefix="/advertisements",
    tags=["Advertisements"]
)


@router.get("/", response_model=List[AdvertisementOut])
def get_advertisements(
    # Optional query parameter to filter advertisements by category
    category: Optional[str] = Query(
        None, description="Filter advertisements by category"
    ),

    # Optional query parameter to search in the advertisement title
    search: Optional[str] = Query(
        None, description="Search advertisements by title"
    ),

    # Database session, injected using FastAPI dependency system
    db: Session = Depends(get_db)
):
    """
    Retrieve a list of advertisements from the database.

    - Filters advertisements by category (if provided)
    - Searches advertisements by title (if provided)
    - Sorts advertisements by creation date (newest first)
    """

    # Start a base SQLAlchemy query on the Advertisement table
    query = db.query(Advertisement)

    # Apply category filter if a category is provided
    if category:
        query = query.filter(Advertisement.category == category)

    # Apply search filter if a search term is provided
    # 'ilike' is used for case-insensitive matching
    if search:
        query = query.filter(Advertisement.title.ilike(f"%{search}%"))

    # Order advertisements by creation date (most recent first)
    query = query.order_by(Advertisement.created_at.desc())

    # Execute the query and return the results
    return query.all()

