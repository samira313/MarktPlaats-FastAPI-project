from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.rating import RatingCreate, RatingOut, RatingUpdate, RatingAvgOut
from app.models.user import User
from app.core.deps import get_current_user
from app.services.ratings_service import RatingsService

router = APIRouter(prefix="/ratings", tags=["ratings"])


def get_ratings_service(db: Session = Depends(get_db)) -> RatingsService:
    return RatingsService(db)


@router.post("", response_model=RatingOut, status_code=status.HTTP_201_CREATED, summary="Create a new rating"
    , description="Enter an integer value from 1 to 5")
def create_rating(payload: RatingCreate, service: RatingsService = Depends(get_ratings_service)
                  , current_user: User = Depends(get_current_user)):
    return service.create_rating(payload, from_user_id=current_user.id)


@router.get("/", response_model=List[RatingOut], summary="Get all ratings")
def list_ratings(service: RatingsService = Depends(get_ratings_service)):
    return service.list_ratings()


@router.get("/users/{user_id}/avg", response_model=RatingAvgOut, summary="Get average rating for a user")
def get_user_avg(user_id: int, service: RatingsService = Depends(get_ratings_service)):
    avg = service.get_user_avg_score(user_id)
    return {"user_id": user_id, "avg_score": avg}


@router.get("/{rating_id:int}", response_model=RatingOut, summary="Get a rating by id")
def get_rating(rating_id: int, service: RatingsService = Depends(get_ratings_service)):
    return service.get_rating(rating_id)


@router.patch("/{rating_id:int}", response_model=RatingOut, summary="Update a rating")
def update_rating(rating_id: int, payload: RatingUpdate, service: RatingsService = Depends(get_ratings_service),
                  current_user: User = Depends(get_current_user)):
    return (service.update_rating(rating_id, score=payload.score, current_user_id=current_user.id))


@router.delete("/{rating_id:int}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete a rating")
def delete_rating(rating_id: int, service: RatingsService = Depends(get_ratings_service),
                  current_user: User = Depends(get_current_user)):
    service.delete_rating(rating_id, current_user_id=current_user.id)

    return
