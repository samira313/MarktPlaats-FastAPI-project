import pytest
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.db.database import Base
from app.services.ads_service import AdsService


@pytest.fixture()
def db_session():
    engine = create_engine(
        "sqlite:///:memory:",
        connect_args={"check_same_thread": False},
    )
    TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
    Base.metadata.create_all(bind=engine)

    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()


@pytest.fixture()
def service(db_session):
    return AdsService(db_session)


class CreatePayload:
    def __init__(self, **data):
        self._data = data

    def model_dump(self, **kwargs):
        return dict(self._data)


class UpdatePayload:
    def __init__(self, **data):
        self._data = data

    def model_dump(self, exclude_unset=False, **kwargs):
        return dict(self._data) if exclude_unset else dict(self._data)


@pytest.fixture()
def create_payload():
    return CreatePayload


@pytest.fixture()
def update_payload():
    return UpdatePayload
