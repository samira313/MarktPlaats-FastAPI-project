from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from app.models.ads import Ad
from typing import Literal


class AdsService:
    def __init__(self, db: Session):
        self.db = db

    def _require_owner(self, ad: Ad, current_user_id: int, action: Literal["update", "delete"]):
        if ad.owner_id != current_user_id:
            message = {
                "update": "You do not have permission to update this advertisement.",
                "delete": "You do not have permission to delete this advertisement.", }
            raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                                detail=message[action])

    def get_ad_or_404(self, ad_id: int) -> Ad:
        ad = self.db.query(Ad).filter(Ad.id == ad_id).first()
        if not ad:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Ad {ad_id} not found")
        return ad

    def create_ad(self, payload, current_user_id: int):
        data = payload.model_dump()
        data["owner_id"] = current_user_id  # de eigenaar van de token

        ad = Ad(**data)
        self.db.add(ad)
        self.db.commit()
        self.db.refresh(ad)
        return ad

    def update_ad(self, ad_id: int, payload, current_user_id: int):
        ad = self.get_ad_or_404(ad_id)
        self._require_owner(ad, current_user_id, action="update")

        updates = payload.model_dump(exclude_unset=True)
        for key, value in updates.items():
            setattr(ad, key, value)

        self.db.commit()
        self.db.refresh(ad)
        return ad

    def delete_ad(self, ad_id: int, current_user_id: int):
        ad = self.get_ad_or_404(ad_id)
        self._require_owner(ad, current_user_id, action="delete")

        self.db.delete(ad)
        self.db.commit()

    def list_ads(self):
        return self.db.query(Ad).all()
