from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import select, exists, func, column
from typing import List

from app.db.database import get_db
from app.models.ads import Ad
from app.schemas.ads import AdOut
from app.schemas.ad_search import AdSearch

router = APIRouter(
    prefix="/ads",
    tags=["ads"]
)


@router.get("/search", response_model=List[AdOut])
def search_ads(
        params: AdSearch = Depends(),
        db: Session = Depends(get_db)
):
    query = db.query(Ad)

    if params.title:
        query = query.filter(Ad.title.ilike(f"%{params.title}%"))

    if params.category:
        je = func.json_each(Ad.category)
        query = query.filter(
            exists(select(1).select_from(je).
            where(column("value") == params.category)))

    if params.min_price is not None:
        query = query.filter(Ad.price >= params.min_price)

    if params.max_price is not None:
        query = query.filter(Ad.price <= params.max_price)

    return query.order_by(Ad.id.desc()).all()
