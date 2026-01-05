# Import column types used to define database fields
from sqlalchemy import Column, Integer, String, DateTime

# Import SQL functions such as NOW() for default timestamps
from sqlalchemy.sql import func

# Import the shared SQLAlchemy Base class
from app.db.database import Base


# SQLAlchemy model representing the 'advertisements' table
class Advertisement(Base):

    # Name of the database table
    __tablename__ = "advertisements"

    # Primary key: unique identifier for each advertisement
    id = Column(Integer, primary_key=True, index=True)

    # Title of the advertisement (required field)
    title = Column(String, nullable=False)

    # Category of the advertisement (required field)
    category = Column(String, nullable=False)

    # Timestamp indicating when the advertisement was created
    # Defaults to the current time when the record is inserted
    created_at = Column(
        DateTime(timezone=True),
        server_default=func.now()
    )
