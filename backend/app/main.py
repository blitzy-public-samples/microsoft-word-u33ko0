"""Compose the FastAPI application for the Microsoft Word backend.

Create the application object, register Cross-Origin Resource Sharing (CORS)
middleware, mount four routers, and define the startup and shutdown handlers.

Six of the nine imports below name symbols the referenced modules never
define, so `import app.main` fails:

- `auth_router`, `documents_router`, `users_router` and `templates_router`.
  Every router module exports the bare name `router` instead, at
  `app/api/auth.py:L38`, `app/api/documents.py:L51`, `app/api/users.py:L21`
  and `app/api/templates.py:L41`.
- `settings`. `app.core.config` defines the `Settings` class
  (`app/core/config.py:L21`) and a `get_settings()` factory (`:L76`), and
  binds no module-level `settings`. `app.api.auth`, `app.db.firestore` and
  `app.db.sql` import the same absent name, so the first of them raises
  `ImportError: cannot import name 'settings' from 'app.core.config'` before
  this module reaches its own `settings` import.
- `init_db`. `app.db.sql` defines `engine`, `SessionLocal`, `Base` and
  `get_db()`, and nothing named `init_db`.

`add_middleware` reads `settings.ALLOWED_ORIGINS`, a name absent from the
nine fields `Settings` declares (`app/core/config.py:L56-L64`). The four
`include_router` calls pass no prefix, so every route keeps the path its own
router declared. The five document paths then collide with the five template
paths, because a path parameter matches by position rather than by name.

Intended behavior per documentation/Technical Specifications.md, SYSTEM
DESIGN > API DESIGN: the route diagram at L406-L433 places the four route
groups under the `/auth`, `/documents`, `/users` and `/templates` prefixes.
"""

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.api.auth import auth_router
from app.api.documents import documents_router
from app.api.users import users_router
from app.api.templates import templates_router
from app.core.config import settings
from app.db.firestore import db
from app.db.sql import init_db

app = FastAPI()

@app.on_event("startup")
async def startup_event():
    """Initialize the database connections on application startup.

    FastAPI runs this handler once, on the `startup` event. The handler takes
    no argument and returns no value. See the human-assistance marker below,
    which covers the whole body.

    Neither database call in the body resolves. `init_db()` does not exist,
    because `app.db.sql` defines no such name, and this module's import of it
    fails before the handler can run at all. `db.is_connected()` is not a
    method on the Google Cloud Firestore `Client` constructed at
    `app/db/firestore.py:L44`, so that call raises `AttributeError`. The body
    runs no migration, and the comment below records that work as still open.

    The `except Exception` clause catches every exception the body raises,
    including the explicit `Exception("Failed to connect to Firestore")`, and
    prints the message. Nothing propagates to FastAPI, so a failed Firestore
    check does not stop the application from starting.
    """
    # HUMAN ASSISTANCE NEEDED
    # The following code block has a confidence level below 0.8 and may need review
    try:
        # Initialize SQL database connection
        await init_db()
        
        # Verify Firestore connection
        if not db.is_connected():
            raise Exception("Failed to connect to Firestore")
        
        # Perform any necessary database migrations
        # TODO: Implement database migration logic
    except Exception as e:
        print(f"Startup error: {str(e)}")
        # Consider implementing proper error handling and logging

@app.on_event("shutdown")
async def shutdown_event():
    """Release the database connections on application shutdown.

    FastAPI runs this handler once, on the `shutdown` event. The handler takes
    no argument and returns no value.

    The single statement in the body awaits `db.close()`. The Google Cloud
    Firestore `Client` constructed at `app/db/firestore.py:L44` does define a
    `close` method, and that method is synchronous and returns `None`. The
    `await` therefore raises `TypeError: object NoneType can't be used in
    'await' expression`. Cleanup beyond closing the client stays open, as the
    comment below records.
    """
    # Close database connections
    await db.close()
    
    # Perform any necessary cleanup tasks
    # TODO: Add any additional cleanup tasks if needed

# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.ALLOWED_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routers
app.include_router(auth_router)
app.include_router(documents_router)
app.include_router(users_router)
app.include_router(templates_router)

# Configure application settings
app.title = "Microsoft Word Backend"
app.version = "1.0.0"