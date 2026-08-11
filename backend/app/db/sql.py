"""Declare the SQLAlchemy engine, session factory, base class and dependency.

This path is declared and unused. No module subclasses `Base`, no ORM model
exists anywhere in the tree, no migration tool is committed, and no route
depends on `get_db`. Every stored record reaches Firestore instead, through
`app/db/firestore.py` and the services.

The engine is constructed at import time from `settings.DATABASE_URL`, and
`app.core.config` never creates `settings`. `app/main.py` imports `init_db`
from this module, which defines no such name.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    """Yield a database session and close it when the caller finishes.

    The generator shape suits FastAPI's `Depends`, which runs the code after
    the `yield` once the response is sent. No route declares it. The declared
    return type is `Session`, and the body yields, so calling this returns a
    generator rather than the session the annotation names.

    Yields:
        A `Session` bound to the module-level engine.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()