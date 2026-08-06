"""Compose the FastAPI application: lifecycle handlers, CORS and the four routers.

Six imports cannot resolve. The four router modules each export `router`, and this file
requests `auth_router`, `documents_router`, `users_router` and `templates_router`.
`app.core.config` defines only the `Settings` class and a `get_settings` factory, so
`settings` is absent. `app.db.sql` declares no `init_db`.

The documents and templates routers are both mounted without a prefix, and their five
path shapes are identical. Starlette matches in registration order, so the documents
router takes every such request and the template routes never run.

CORS reads `settings.ALLOWED_ORIGINS`, which the `Settings` model does not declare.
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
    """Initialize the SQL connection and verify Firestore, once at startup.

    Returns:
        Nothing. FastAPI calls the handler with no arguments and discards its result.

    See the human-assistance marker at L56-L57 below: the startup path is flagged
    for review because its confidence level falls below 0.8.

    Three defects sit in the body. L60 awaits `init_db()`, and `app.db.sql` never
    defines that name. L63 calls `db.is_connected()`, which the Google Cloud
    Firestore `Client` does not provide. L67 records database migration as
    outstanding work, so no migration runs.

    The handler declares no parameters and no return annotation. FastAPI calls it
    with no arguments and discards its result.

    L69 prints `str(e)`, and the caught exception text can carry connection or
    configuration detail from the failing initialization call, including the
    host, port and credential fragments a driver error quotes back. Intended
    remediation: a redacted structured log record, which the outstanding-work
    comment at L70 already records as unfinished.

    No exception leaves the handler. The `except Exception` at L68 catches every
    error the body raises, including the `Exception` that L64 raises when the
    Firestore check fails, and L69 prints it. Startup therefore continues after a
    failed database check, and the application serves requests against connections
    it never verified.
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

    FastAPI runs this handler once, on the `shutdown` event registered at L72. L110
    is the only statement, and L113 records further cleanup as outstanding work.

    L110 awaits `db.close()` on the object that L21 imports from
    `app.db.firestore`. A Firestore `Client` does carry a `close` method, and that
    method is synchronous: it inherits `close()` from the shared Google Cloud
    client base class, which shuts the underlying transport session and returns
    `None`. The `await` at L110 therefore receives `None`, which is not awaitable,
    so the statement runs the close and then raises
    `TypeError: object NoneType can't be used in 'await' expression`. The close
    takes effect before the error is raised, so the session is already shut when
    shutdown fails.

    No backend dependency manifest is committed, so nothing here pins
    `google-cloud-firestore` and the inherited surface is whatever the resolved
    release provides. The behavior above is what L110 produces against any release
    whose client inherits the synchronous `close` from `google.cloud.client`. A
    release that omitted the method would raise `AttributeError` instead, and no
    committed file settles which release applies. The startup path at L63 differs
    either way: `is_connected` belongs to no version of that surface, so that call
    raises `AttributeError`.

    The handler declares no parameters and no return annotation. FastAPI calls it
    with no arguments and discards its result.

    Raises:
        TypeError: At L110, after the synchronous `close()` has returned `None`,
            because `await` cannot suspend on `None`. The handler wraps L110 in no
            `try` block, so the error propagates to the caller, unlike the startup
            path at L68-L69. A shutdown that raises leaves any remaining cleanup
            undone, and L113 records further cleanup as outstanding work. Neither
            handler runs as committed, because the module fails at import.
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