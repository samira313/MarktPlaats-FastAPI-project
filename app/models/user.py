from sqlalchemy import Column, Integer, String, DateTime, func
from app.db.database import Base, engine

class User(Base):
    """
    Database model representing a user.
    Each instance of this class corresponds to a row in the 'users' table.
    """

    __tablename__ = "users"

    # Primary key (unique identifier for each user)
    id = Column(Integer, primary_key=True, index=True)

    # Username must be unique and is required
    username = Column(String(50), unique=True, index=True, nullable=False)

    # Email is optional but must be unique if provided
    email = Column(String(255), unique=True, index=True, nullable=True)

    hashed_password = Column(String(255), nullable=False)

    # Timestamp when the user is created
    # server_default ensures the value is set by the database
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now(),
        nullable=False
    )
