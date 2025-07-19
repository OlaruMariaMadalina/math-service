from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.utils.config import settings


# Create SQLAlchemy engine using the configured database URL
engine = create_engine(
    settings.db_url,
    connect_args={"check_same_thread": False}
)


# Session factory for database access
SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)


# Base class for all models
Base = declarative_base()


# Initialize database tables
def init_db():
    Base.metadata.create_all(engine)


# Dependency for providing a database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
