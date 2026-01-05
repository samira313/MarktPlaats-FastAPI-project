from app.db.database import Base
from sqlalchemy import Column, Integer, String, Float


class Ad(Base):
    """
      ORM model representing an advertisement stored in the database.
      """
    __tablename__ = 'advertisements'
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String(255), nullable=False)
    description = Column(String(1000), nullable=True)
    price = Column(Float, nullable=False)
    category = Column(String(100), nullable=False)
