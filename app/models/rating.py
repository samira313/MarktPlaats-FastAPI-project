from sqlalchemy import Column, Integer, ForeignKey, UniqueConstraint
from app.db.database import Base


class Rating(Base):
    __tablename__ = 'ratings'

    id = Column(Integer, primary_key=True, index=True)

    from_user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    to_user_id = Column(Integer, ForeignKey('users.id'), nullable=False, index=True)

    score = Column(Integer, nullable=False)

    __table_args__ = (UniqueConstraint("from_user_id",
                                       "to_user_id", name="uq_from_to_user_rating"),)
