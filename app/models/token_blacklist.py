from sqlalchemy import Column, Integer, String, DateTime, func

from app.db.database import Base


class TokenBlacklist(Base):
    __tablename__ = "token_blacklist"

    id = Column(Integer, primary_key=True, index=True)

    # JWT ID - unique identifier for each token
    jti = Column(String(64), unique=True, index=True, nullable=False)

    # When the token expires (so we can later clean up if needed)
    expires_at = Column(DateTime(timezone=True), nullable=False)

    # When the token was blacklisted
    created_at = Column(DateTime(timezone=True), server_default=func.now(), nullable=False)
