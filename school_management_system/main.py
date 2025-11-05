import os
import sys
import uvicorn
import logging
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from starlette.middleware.cors import CORSMiddleware
from sqlalchemy.future import select

# Apply bcrypt patch before importing any other modules
from school_management_system.utils.bcrypt_patch import apply_patch
apply_patch()

from school_management_system.config import settings
from school_management_system.api.endpoints import (
    users,
    students,
    admissions,
    subjects,
    timetables,
    exams,
    payments,
    reports,
)
from school_management_system.web.routes import router as web_router
from school_management_system.database.init_db import init_db
from school_management_system.database.session import AsyncSessionLocal
from school_management_system.models.user import User

app = FastAPI(
    title=settings.PROJECT_NAME,
    openapi_url=f"{settings.API_V1_STR}/openapi.json",
)

# Set up CORS
# For production, we'll use environment variables to configure allowed origins
origins = os.getenv("CORS_ORIGINS", "*").split(",")
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Get the base directory for the application
BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Mount static files - use absolute paths for Vercel compatibility
static_dir = os.path.join(BASE_DIR, "school_management_system", "web", "static")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")
else:
    # Fallback for development environment
    app.mount("/static", StaticFiles(directory="web/static"), name="static")

# Set up templates - use absolute paths for Vercel compatibility
templates_dir = os.path.join(BASE_DIR, "school_management_system", "web", "templates")
if os.path.exists(templates_dir):
    templates = Jinja2Templates(directory=templates_dir)
else:
    # Fallback for development environment
    templates = Jinja2Templates(directory="web/templates")

# Make templates available to routes
import school_management_system.web.routes
school_management_system.web.routes.templates = templates

# Include API routers
app.include_router(users.router, prefix=f"{settings.API_V1_STR}/users", tags=["users"])
app.include_router(students.router, prefix=f"{settings.API_V1_STR}/students", tags=["students"])
app.include_router(admissions.router, prefix=f"{settings.API_V1_STR}/admissions", tags=["admissions"])
app.include_router(subjects.router, prefix=f"{settings.API_V1_STR}/subjects", tags=["subjects"])
app.include_router(timetables.router, prefix=f"{settings.API_V1_STR}/timetables", tags=["timetables"])
app.include_router(exams.router, prefix=f"{settings.API_V1_STR}/exams", tags=["exams"])
app.include_router(payments.router, prefix=f"{settings.API_V1_STR}/payments", tags=["payments"])
app.include_router(reports.router, prefix=f"{settings.API_V1_STR}/reports", tags=["reports"])

# Include web routes
app.include_router(web_router)

@app.on_event("startup")
async def startup_event():
    """Initialize the database on startup."""
    try:
        await init_db()
    except Exception as e:
        import logging
        logging.error(f"Error initializing database: {e}")
        # In serverless environments, we don't want to crash the application
        # if database initialization fails, as it might be a temporary issue
        # that will resolve on the next request
        pass

# For Vercel serverless, we need to ensure the database is initialized
# This middleware will check if the database is initialized on each request
@app.middleware("http")
async def db_session_middleware(request, call_next):
    # Only try to initialize the database if we're in a Vercel environment
    # and using SQLite in-memory database
    if os.environ.get("RENDER") or os.environ.get("SERVERLESS") and settings.USE_SQLITE_MEMORY:
        try:
            # Quick check to see if the database is initialized
            # We'll just try to get the first user
            async with AsyncSessionLocal() as session:
                result = await session.execute(select(User).limit(1))
                user = result.scalars().first()
                
                # If no users exist, initialize the database
                if not user:
                    await init_db()
        except Exception as e:
            # If there's an error, try to initialize the database
            try:
                await init_db()
            except Exception as inner_e:
                import logging
                logging.error(f"Error initializing database in middleware: {inner_e}")
                # Continue anyway, as the error might be temporary
                pass
    
    response = await call_next(request)
    return response

@app.get("/api")
async def api_root():
    """API root endpoint."""
    return {"message": "Welcome to the College Management System API"}

if __name__ == "__main__":
    uvicorn.run("school_management_system.main:app", host="0.0.0.0", port=8000, reload=True)
