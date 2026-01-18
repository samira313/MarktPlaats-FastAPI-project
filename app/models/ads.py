from app.db.database import Base
from sqlalchemy import (Column, Integer, String, Float,
                        ForeignKey, DateTime, func, JSON)
from sqlalchemy.orm import relationship


class Ad(Base):
    """
      ORM model representing an advertisement stored in the database.
      """
    __tablename__ = 'advertisements'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    price = Column(Float, nullable=False)
    category = Column(JSON, nullable=False)
    status = Column(String(20), default="available", nullable=False)

    owner_id = Column(Integer, ForeignKey("users.id"),nullable=False, index=True)
    owner = relationship("User")

    created_at = Column(DateTime(timezone=True),server_default=func.now(),nullable=False)

    updated_at = Column(DateTime(timezone=True),server_default=func.now(),onupdate=func.now(),
                        nullable=False)
