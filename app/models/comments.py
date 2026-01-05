import datetime
from db.database import Base
from sqlalchemy import Column, Integer, String, Date


class DbComment(Base):
    __tablename__ = "Comments"

    comment_id = Column(Integer, primary_key=True, index=True)  # benzersiz olarak otomatik üretilir.
    comment = Column(String(100), nullable=False)
    create_by_id = Column(Integer, nullable=False)
    sent_to_id = Column(Integer, nullable=False)
    date = Column(Date, default=datetime.date.today)