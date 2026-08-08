"""Compose the FastAPI application: lifecycle hooks, CORS and the routers.

The module cannot import as committed. Five imported names do not exist:
`auth_router`, `documents_router`, `users_router` and `templates_router`,
because each router module exports the name `router`, and `settings`,
because `app.core.config` defines only the `Settings` class and
`get_settings()`. `init_db` is imported from `app.db.sql`, which defines no
such name.

Every router is mounted without a prefix, so the document and template
routes claim the same two paths. See ./README.md for the mounting order and
the resulting collision.
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
    """Initialise the SQL schema and check the Firestore connection.

    Neither step can run. `init_db` does not exist, and the Firestore
    `Client` exposes no `is_connected()`. The `except` below catches both
    failures and prints them, so startup finishes and the application
    reports itself healthy. See the HUMAN ASSISTANCE NEEDED marker below.

    Returns:
        None. FastAPI runs this on the `startup` event.
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
    """Close the database connections during shutdown.

    `db.close()` is awaited on the Firestore `Client` built at
    `app/db/firestore.py:L20`. No manifest pins `google-cloud-firestore`, so
    two questions about the resolved client surface decide the outcome and
    neither is settled here: whether `close()` exists, and whether it returns
    something `await` accepts. A synchronous `close()` returns `None`, and
    `await None` raises `TypeError`.

    Returns:
        None. FastAPI runs this on the `shutdown` event.
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