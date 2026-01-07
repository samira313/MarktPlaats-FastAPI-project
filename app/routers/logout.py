from datetime import datetime, timezone

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.db.database import get_db
from app.models.token_blacklist import TokenBlacklist
from app.core.jwt import decode_token
from app.core.deps import get_current_user, oauth2_scheme
from app.models.user import User


router = APIRouter(prefix="/users", tags=["Users"])

@router.post("/logout")
def logout(
    token: str = Depends(oauth2_scheme),
    db: Session = Depends(get_db),
    current_user: User = Depends(get_current_user),
):
    """
    Logout = blacklist the current token (jti) so it can no longer be used.
    """
    payload = decode_token(token)

    jti = payload.get("jti")
    exp = payload.get("exp")

    if not jti or not exp:
        return {"message": "Token is missing jti/exp (cannot logout safely)."}

    # exp can be int timestamp
    expires_at = datetime.fromtimestamp(exp, tz=timezone.utc)

    # if already blacklisted, do not crash
    exists = db.query(TokenBlacklist).filter(TokenBlacklist.jti == jti).first()
    if exists:
        return {"message": "Already logged out."}

    db_token = TokenBlacklist(jti=jti, expires_at=expires_at)
    db.add(db_token)
    db.commit()

    return {"message": "Logged out successfully."}
