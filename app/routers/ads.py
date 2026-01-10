from fastapi import APIRouter, Depends, status
from sqlalchemy.orm import Session
from typing import List

from app.db.database import get_db
from app.schemas.ads import AdOut, AdCreate, AdUpdate
from app.core.deps import get_current_user
from app.services.ads_service import AdsService

router = APIRouter(prefix="/ads", tags=["ads"])


def get_ads_service(db: Session = Depends(get_db)):
    return AdsService(db)


# 1- create ad
@router.post("/", response_model=AdOut, status_code=status.HTTP_201_CREATED,
             summary="Create a new advertisement",
             description="""
             Creates a new advertisement for the currently authenticated user.

             Requirements:
             - User must be logged in.
             - The advertisement will automatically be linked to the logged-in user.

             Validation rules:
             - title: required
             - price: must be a positive number
             - category: must be a list of strings

             Notes:
             - The owner of the ad is determined from the JWT token.
             """)
def create_ad_endpoint(payload: AdCreate, current_user=Depends(get_current_user),
                       service: AdsService = Depends(get_ads_service)):
    return service.create_ad(payload, current_user.id)


# 2- get id ad
@router.get("/{ad_id:int}", response_model=AdOut,
            summary="Get advertisement by ID",
            description="""
            Returns a single advertisement by its ID.

            Notes:
            - The ID must be an integer.
            - This endpoint is public and does not require authentication.

            Errors:
            - 404 if the advertisement does not exist.
            """)
def get_ad_by_id(ad_id: int,
                 service: AdsService = Depends(get_ads_service)):
    return service.get_ad_or_404(ad_id)


# 3- update ad
@router.patch("/{ad_id:int}", response_model=AdOut,
              summary="Update an existing advertisement",
              description="""
              Updates an existing advertisement.

              Requirements:
              - User must be logged in.
              - Only the owner of the advertisement can update it.

              Validation rules:
              - Only provided fields will be updated.
              - price must be a positive number if provided.
              - category must be a list of strings if provided.

              Errors:
              - 401 if user is not authenticated.
              - 403 if user is not the owner of the advertisement.
              - 404 if the advertisement does not exist.
              """)
def update_ad(ad_id: int, payload: AdUpdate, current_user=Depends(get_current_user),
              service: AdsService = Depends(get_ads_service)):
    return service.update_ad(ad_id, payload, current_user.id)


# 4- delete ad
@router.delete("/{ad_id:int}", status_code=status.HTTP_204_NO_CONTENT,
               summary="Delete an advertisement",
               description="""
               Deletes an advertisement by its ID.

               Requirements:
               - User must be logged in.
               - Only the owner of the advertisement can delete it.

               Errors:
               - 401 if user is not authenticated.
               - 403 if user is not the owner of the advertisement.
               - 404 if the advertisement does not exist.
               """)
def delete_ad_endpoint(ad_id: int, current_user=Depends(get_current_user),
                       service: AdsService = Depends(get_ads_service), ):
    service.delete_ad(ad_id, current_user.id)
    return None


# 5- get all ads
@router.get("/", response_model=List[AdOut],
            summary="List all advertisements",
            description="""
            Returns a list of all advertisements.

            Notes:
            - This endpoint is public.
            - Each advertisement includes the owner's username and the timestamp when the advertisement was created.
            """)
def get_all_ads(service: AdsService = Depends(get_ads_service), ):
    return service.list_ads()
