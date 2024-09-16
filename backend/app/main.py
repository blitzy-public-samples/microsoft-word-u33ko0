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