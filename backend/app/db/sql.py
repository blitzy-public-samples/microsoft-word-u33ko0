"""Configure SQLAlchemy engine and session objects.

The imported settings singleton and the init_db symbol expected by app.main
are unresolved.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    """Yield a database session and close it after use.

    Yields:
        Session: A session created by SessionLocal.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()