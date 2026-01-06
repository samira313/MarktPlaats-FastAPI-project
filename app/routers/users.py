from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.user import User
from app.models.token_blacklist import TokenBlacklist
from app.core.jwt import decode_token
from app.core.deps import get_current_user, oauth2_scheme
from app.schemas.register import UserOut

router = APIRouter(prefix="/users", tags=["Users"])


@router.get("/me", response_model=UserOut)
def read_me(current_user: User = Depends(get_current_user)):
    return current_user

