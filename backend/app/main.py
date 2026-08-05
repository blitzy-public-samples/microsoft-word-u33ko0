"""Assemble the FastAPI application: middleware, routers and lifecycle hooks.

The module is the composition root. L11 creates the application object, L40-L46
registers Cross-Origin Resource Sharing (CORS) middleware, L49-L52 mount the four
routers, L54-L56 set the title and version, and L13-L37 define the two lifecycle
handlers.

Line references below point at the committed revision 06be74c, which numbers this
file as it stood before these docstrings existed.

Unresolved imports. Six of the nine imports name symbols the referenced modules
never define, so importing this module fails:

- L3-L6 request `auth_router`, `documents_router`, `users_router` and
  `templates_router`. All four router modules export the bare name `router`
  instead, at `api/auth.py:L12`, `api/documents.py:L8`, `api/users.py:L6` and
  `api/templates.py:L8`.
- L7 requests `settings` from `app.core.config`. That module defines the
  `Settings` class at `core/config.py:L4` and the `get_settings()` factory at
  `core/config.py:L19`, and never creates a module-level instance. Eight modules
  import the absent name: `api/auth.py:L6`, `db/firestore.py:L3`, `db/sql.py:L3`,
  L7 here, `services/collaboration_service.py:L4`,
  `services/document_service.py:L5`, `services/export_service.py:L3` and
  `tasks/background_tasks.py:L3`. `core/security.py:L6` imports the
  `get_settings` factory instead, and that factory does exist.
- L9 requests `init_db` from `app.db.sql`, which never defines it. L19 awaits it.

`import app.main` therefore fails at L3, then at `api/auth.py:L6`, reporting
`ImportError: cannot import name 'settings' from 'app.core.config'`.

Undeclared configuration. L42 reads `settings.ALLOWED_ORIGINS` to populate the
CORS allow-list. `Settings` declares nine fields at `core/config.py:L5-L13`, and
`ALLOWED_ORIGINS` is not one of them, so the read raises `AttributeError` once
the L7 import resolves.

Route collision. L49-L52 pass no `prefix` to any `include_router` call, so all
fourteen handlers mount at the application root. Starlette matches path templates
positionally, so `/{document_id}` in `api/documents.py` and `/{template_id}` in
`api/templates.py` compile to the same single-segment pattern. L50 mounts the
document router before L52 mounts the template router, so the five template
routes are unreachable. Intended behavior per
`documentation/Technical Specifications.md`, SYSTEM DESIGN > API DESIGN: the
route surface is prefixed per resource, with `/auth`, `/documents`, `/users` and
`/templates` separating the four groups.

Ordering. L55 and L56 assign `app.title` and `app.version` after the middleware
and the routers are already installed.
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
    """Initialize the database connections when the application starts.

    FastAPI runs this handler once, on the `startup` event registered at L13. The
    body opens the relational connection at L19, checks the Firestore connection
    at L22, and leaves migration work outstanding at L26.

    See the human-assistance marker at L15-L16 below: the startup path is flagged
    for review because its confidence level falls below 0.8.

    Three defects sit in the body. L19 awaits `init_db()`, and `app.db.sql` never
    defines that name. L22 calls `db.is_connected()`, which the Google Cloud
    Firestore `Client` does not provide. L26 records database migration as
    outstanding work, so no migration runs.

    The handler declares no parameters and no return annotation. FastAPI calls it
    with no arguments and discards its result.

    Raises:
        Nothing. The `except Exception` at L27 catches every error the body
            raises, including the `Exception` that L23 raises when the Firestore
            check fails, and L28 prints it. Startup therefore continues after a
            failed database check, and the application serves requests against
            connections it never verified.
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
    """Close the database connections when the application shuts down.

    FastAPI runs this handler once, on the `shutdown` event registered at L31. L34
    is the only statement, and L37 records further cleanup as outstanding work.

    L34 awaits `db.close()` on the object that L8 imports from
    `app.db.firestore`. The declared call contradicts the runtime object twice.
    The Google Cloud Firestore `Client` provides no `close` method, and the client
    is synchronous, so `await` has nothing to suspend on. L34 raises
    `AttributeError` at shutdown.

    The handler declares no parameters and no return annotation. FastAPI calls it
    with no arguments and discards its result.

    Raises:
        AttributeError: At L34, because the Firestore `Client` declares no
            `close` method. The handler wraps L34 in no `try` block, so the error
            propagates to the caller, unlike the startup path at L27-L28.
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