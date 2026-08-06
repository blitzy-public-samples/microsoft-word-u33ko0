"""Build the SQLAlchemy engine, session factory and declarative base.

`settings` is requested from `app.core.config`, which never defines it, so importing
this module raises `ImportError`. `app/main.py` also imports `init_db` from here, and
this module declares no such name.

The engine is created at import time from `settings.DATABASE_URL`, with no pool tuning
and no connectivity check. Nothing subclasses `Base`, so no table is mapped, and no
migration tooling is committed. No module calls `get_db`, which leaves this whole path
declared and unused; Firestore carries the application's persistence instead.
"""
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    """Yield a database session and close it when the caller is done.

    Serves as the FastAPI dependency shape for request-scoped sessions.

    Yields:
        One `Session` from `SessionLocal`, configured with autocommit and autoflush both
        off, so a caller must commit explicitly.

    Note:
        The `finally` block closes the session on every path, including an exception, so
        the connection returns to the pool either way. The function is a generator, and
        the `-> Session` annotation names the yielded type rather than the return type.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()