from fastapi import (APIRouter, Depends, HTTPException, status)
from sqlalchemy.orm import Session
from typing import List
from app.db.database import get_db
from app.models.ads import Ad
from app.schemas.ads import AdOut, AdCreate, AdUpdate

router = APIRouter(prefix="/ads", tags=["ads"])


def get_ad_or_404(db: Session, ad_id: int) -> Ad:
    # ad = db.get(Ad, ad_id)  # query/filter
    ad = db.query(Ad).filter(Ad.id == ad_id).first()

    if not ad:
        raise HTTPException(status_code=404, detail=f"Ad {ad_id} not found")
    return ad


# 1- create ad
@router.post("/", response_model=AdOut,
             status_code=status.HTTP_201_CREATED, summary="Create ad", )
def create_ad(payload: AdCreate, db: Session = Depends(get_db)):
    # 1) Convert Pydantic schema -> dict
    data = payload.model_dump()

    # 2) Create ORM object (represents a row in the table)
    ad = Ad(**data)

    # 3) Add + commit (save to DB)
    db.add(ad)
    db.commit()

    # 4) Refresh to load generated fields (like id) from DB
    db.refresh(ad)

    # 5) Return ORM object (Pydantic will serialize it using AdOut)
    return ad


# 2- get id ad
@router.get("/{ad_id:int}", response_model=AdOut,
            summary="Get ad by id", description="Get an advertisement by id.")
def get_ad_by_id(ad_id: int, db: Session = Depends(get_db)):
    ad = get_ad_or_404(db, ad_id)
    return ad


# 3- update ad
@router.patch("/{ad_id:int}", response_model=AdOut,
              summary="Update ad", description="Update an advertisement.")
def update_ad(ad_id: int,
              payload: AdUpdate, db: Session = Depends(get_db)):
    # 1) Get the current ad from DB
    ad = get_ad_or_404(db, ad_id)

    # 2) Convert payload to dict, but only include fields the client actually sent
    data = payload.model_dump(exclude_unset=True)
    if not data:
        raise HTTPException(status_code=400, detail="No fields provided to update")

    # 3) Apply only provided fields to the ORM object
    for key, value in data.items():
        setattr(ad, key, value)

    # 4) Save changes
    db.commit()
    db.refresh(ad)

    # 5) Return updated ad
    return ad


# 4- delete ad
@router.delete("/{ad_id:int}", status_code=status.HTTP_204_NO_CONTENT, summary="Delete ad",
               description="Delete an advertisement.")
def delete_ad(ad_id: int, db: Session = Depends(get_db)):
    # 1) Get ad from DB
    ad = get_ad_or_404(db, ad_id)

    # 2) Delete ad
    db.delete(ad)
    db.commit()

    # 3) No content returned
    return


# 5- get all ads
@router.get("/", response_model=List[AdOut],
            summary="List ads", description="Return a list of ads.")
def get_all_ads(db: Session = Depends(get_db)):
    ads = db.query(Ad).all()
    return ads
