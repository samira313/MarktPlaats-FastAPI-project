import datetime
from app.db.database import Base

from sqlalchemy import Column, Integer, String, Date, Float
from sqlalchemy.orm import relationship


class DbComment(Base):
    __tablename__ = "comments"

    comment_id = Column(Integer, primary_key=True, index=True)  # uniqe id
    comment = Column(String(100), nullable=False)
    create_by_id = Column(Integer, nullable=False)
    sent_to_id = Column(Integer, nullable=False)
    date = Column(Date, default=datetime.date.today)
    #advertisements = relationship("Ad", back_populates="comment")
