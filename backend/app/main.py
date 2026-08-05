"""Configure the FastAPI application and lifecycle hooks.

Imports auth_router, documents_router, users_router, templates_router,
settings, and init_db, none of which their source modules export.

The module cannot import as committed. The first router import loads
app.api.auth, which imports the absent settings singleton and raises
ImportError, so neither lifecycle handler below is ever reached.

Settings also declares no ALLOWED_ORIGINS field. Every router is mounted
without a prefix. The document routes therefore shadow both `/me` profile
routes and the matching template paths registered after them.
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
    """Attempt database initialization and log startup failures.

    The assistance marker and migration note below apply to this handler.

    The Firestore client defines no `is_connected` method, so the connectivity
    branch raises AttributeError instead of testing a connection. Nothing here
    verifies that Firestore is reachable.

    The `except Exception` clause catches every failure the body produces,
    including the unresolved init_db call and the AttributeError above, and
    only prints the message. Startup therefore cannot fail, and the
    application accepts traffic with no verified database.

    The printed line carries the caught exception text, which can include
    database connection detail from the failing initialization call.

    Side effects:
        Calls the unresolved init_db, reaches for an undefined Firestore
        connectivity method, and writes caught failures to stdout. The handler
        never runs, because the module fails at import.
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
    """Attempt to close the shared Firestore client.

    The cleanup note below records work beyond the attempted client close.

    The Firestore client inherits a synchronous `close` from the Google Cloud
    core client, and that method returns None. Awaiting the result fails, so
    the transport closes and the handler then raises.

    Raises:
        TypeError: `await` receives the None that the synchronous `close`
            returns. The handler never runs, because the module fails at
            import.
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