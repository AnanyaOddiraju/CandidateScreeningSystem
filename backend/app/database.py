from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session

from app.models import Base
from app.core.config import settings


engine = create_engine(
    settings.DATABASE_URL,
    pool_pre_ping=True,
    pool_size=10,
    max_overflow=20,
)

SessionLocal = sessionmaker(
    bind=engine,
    autoflush=False,
    expire_on_commit=False
)


def get_db():
    db: Session = SessionLocal()

    try:
        yield db

    finally:
        db.close()