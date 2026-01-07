import app.core.config
from fastapi import FastAPI

from app.routers.ads import router as ads_crud_router
from app.routers.ad_search import router as ad_search_router

from app.routers.register import router as register_router
from app.routers.login import router as login_router

from app.db.database import Base, engine
from app.models.ads import Ad
from app.models import user

app = FastAPI(
    title="Marktplaats API",
    description="Backend API for the Marktplaats project",
    version="1.0.0"
)

# create tables
Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "MarktPlaats API is running"}


# Register routers
app.include_router(ads_crud_router)  # CRUD/ads
app.include_router(ad_search_router)  # /ads/search
app.include_router(register_router)
app.include_router(login_router)
#app.include_router(register_router) #duplicat
