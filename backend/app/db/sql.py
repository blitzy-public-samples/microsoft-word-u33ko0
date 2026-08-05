"""Configure the SQLAlchemy engine, session factory and declarative base.

Line references below (L1 through L15) point at the committed revision 06be74c,
which numbers this file as it stood before these docstrings existed.

The module creates the SQLAlchemy engine at L5, the `SessionLocal` session factory
at L6 and the `Base` declarative class at L8 for the relational database path.
`get_db` at L10 hands callers a per-request Structured Query Language (SQL) session.

Unresolved import: L3 imports `settings` from `app.core.config`, and that module
never defines a module-level `settings`. `app.core.config` defines only the
`Settings` class (core/config.py:L4) and the `get_settings()` factory
(core/config.py:L19), so importing this module fails at L3.

Missing symbol: `backend/app/main.py:L9` runs `from app.db.sql import init_db` and
`main.py:L19` awaits `init_db()`. The module never defines `init_db`.

Import-time side effect: L5 builds the engine from `settings.DATABASE_URL` while
the module loads. A missing or malformed database Uniform Resource Locator (URL)
therefore fails on import rather than at the first query.

The relational path is dead as committed. No class in the repository subclasses
`Base` (L8), so zero Object-Relational Mapping (ORM) models exist. No module
imports `engine`, `SessionLocal`, `Base` or `get_db` from here.
`backend/tests/test_api.py:L5` imports a `get_db` from the absent module
`app.database`, not from this module, and never calls it.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, Session, declarative_base
from app.core.config import settings

engine = create_engine(settings.DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db() -> Session:
    """Yield a database session and close it when the caller finishes.

    The return annotation at L10 declares `Session`, and the body yields at L13,
    so calling `get_db()` returns a generator rather than a `Session`.

    The `finally` block at L14-L15 closes the session, so cleanup runs whether the
    caller finishes normally or raises.

    Yields:
        Session: The session that the `SessionLocal` factory creates at L11,
            which the `yield` at L13 hands to the caller.
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()