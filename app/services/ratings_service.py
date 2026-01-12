from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List

from app.models.rating import Rating
from app.models.user import User
from app.schemas.rating import RatingCreate


class RatingsService:
    def __init__(self, db: Session):
        self.db = db

    def _require_user_exists(self, user_id: int) -> None:
        user = self.db.query(User).filter(User.id == user_id).first()
        if not user:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f" User {user_id} not found.")

    def _require_not_self_rating(self, from_user_id: int,
                                 to_user_id: int) -> None:
        if from_user_id == to_user_id:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="You can't rate yourself.")

    def _require_not_duplicate(self, from_user_id: int,
                               to_user_id: int) -> None:
        exists = (self.db.query(Rating).
                  filter(Rating.from_user_id == from_user_id,
                         Rating.to_user_id == to_user_id).first())
        if exists:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                                detail="You already rated this user")

    def get_rating_or_404(self, rating_id: int) -> Rating:
        rating = self.db.query(Rating).filter(Rating.id == rating_id).first()
        if not rating:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                                detail=f"Rating {rating_id} not found.")
        return rating

    def _require_owner(self, rating: Rating, current_user_id: int) -> None:
        if rating.from_user_id != current_user_id:
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail="You do not have permission to modify this rating.")

    def list_ratings(self) -> List[Rating]:
        return self.db.query(Rating).all()

    def create_rating(self,
                      payload: RatingCreate,
                      from_user_id: int, ) -> Rating:
        # validations
        self._require_user_exists(payload.to_user_id)
        self._require_not_self_rating(from_user_id, payload.to_user_id)
        self._require_not_duplicate(from_user_id, payload.to_user_id)

        rating = Rating(from_user_id=from_user_id,
                        to_user_id=payload.to_user_id,
                        score=payload.score, )

        self.db.add(rating)
        self.db.commit()
        self.db.refresh(rating)
        return rating

    def get_rating(self, rating_id: int) -> Rating:
        return self.get_rating_or_404(rating_id)

    def update_rating(self, rating_id: int, score: int, current_user_id: int) -> Rating:
        rating = self.get_rating_or_404(rating_id)
        self._require_owner(rating, current_user_id)

        rating.score = score
        self.db.commit()
        self.db.refresh(rating)
        return rating

    def get_user_avg_score(self, user_id: int) -> float | None:
        self._require_user_exists(user_id)

        avg_score = (self.db.query(func.avg(Rating.score)).
                     filter(Rating.to_user_id == user_id
                            ).scalar())
        return float(avg_score) if avg_score is not None else None

    def delete_rating(self, rating_id: int, current_user_id: int) -> None:
        rating = self.get_rating_or_404(rating_id)
        self._require_owner(rating, current_user_id)

        self.db.delete(rating)
        self.db.commit()
