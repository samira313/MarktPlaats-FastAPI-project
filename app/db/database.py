from sqlalchemy import create_engine
from sqlalchemy.orm import declarative_base, sessionmaker

# Database connection URL (SQLite database file)
DATABASE_URL = "sqlite:///./marktplaats.db"

# Create the SQLAlchemy engine
# check_same_thread=False is required for SQLite when used with FastAPI

engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)

# Create a session factory for database connections
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Base class for all ORM models || All database models should inherit from this Base
Base = declarative_base()


def get_db():
    """
       Dependency that provides a database session.
       The session is opened when the request starts
       and closed automatically after the request ends.
       """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
