from fastapi import FastAPI
from app.routers.ads import router as ads_router
from app.db.db import Base, engine
from app.models.ads import Ad


app = FastAPI()

# create tables
Base.metadata.create_all(bind=engine)

@app.get("/")
def root():
    return {"message": "MarktPlaats API is running"}

# Register routers
app.include_router(ads_router)
