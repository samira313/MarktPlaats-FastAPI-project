import app.core.config
from fastapi import FastAPI
from app.models import messages, ads, user # needed to register models

from  fastapi.templating import Jinja2Templates
from fastapi.requests import Request
from fastapi.responses import HTMLResponse


from app.db.database import Base, engine

from app.routers.ads import router as ads_crud_router
from app.routers.ad_search import router as ad_search_router
from app.routers.register import router as register_router
from app.routers.login import router as login_router
from app.routers.comments import router as comments_router

from app.routers.logout import router as logout_router
from app.routers.users import router as users_router
from app.routers.messages import router as messages_router
from app.routers.ws_messages import router as ws_messages_router
from app.routers.ad_search import router as ads_router



from app.db.database import Base, engine

templates = Jinja2Templates(directory="app/templates")
app = FastAPI(
    title="Marktplaats API",
    description="Backend API for the Marktplaats project",
    version="1.0.0"
)

Base.metadata.create_all(bind=engine)


@app.get("/")
def root():
    return {"message": "Marktplaats API is running"}

@app.get("/demo-chat", response_class=HTMLResponse)
def demo_chat(request: Request):
    return templates.TemplateResponse("demo_chat.html", {"request": request})
# Register routers
app.include_router(register_router)
app.include_router(login_router)
app.include_router(users_router)
app.include_router(logout_router)
app.include_router(ads_crud_router)  # CRUD/ads
app.include_router(ad_search_router)  # /ads/search
app.include_router(comments_router)

app.include_router(users_router)
app.include_router(logout_router)
app.include_router(messages_router)
app.include_router(ws_messages_router)




