from typing import Generator
import os
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.pool import StaticPool

from school_management_system.config import settings

# For SQLite in-memory in serverless, we need to use a shared in-memory database
# This is a workaround for the fact that each request gets a new connection
# We'll use a shared URI with mode=memory&cache=shared
SQLITE_SHARED_URI = "file:memdb?mode=memory&cache=shared"

# Function to create engine - this ensures a new connection for each serverless invocation
def get_engine():
    if settings.USE_SQLITE_MEMORY:
        # Use SQLite for in-memory database with shared cache for serverless
        if os.environ.get("RENDER") or os.environ.get("SERVERLESS"):
            return create_async_engine(
                f"sqlite+aiosqlite:///{SQLITE_SHARED_URI}",
                echo=False,
                future=True,
                # These are needed for SQLite to work with async
                connect_args={"check_same_thread": False, "uri": True},
                # Use StaticPool to maintain connections between requests
                poolclass=StaticPool,
            )
        else:
            # For local development
            return create_async_engine(
                "sqlite+aiosqlite:///:memory:",
                echo=False,
                future=True,
                connect_args={"check_same_thread": False},
            )
    else:
        # Use PostgreSQL for production
        return create_async_engine(
            str(settings.SQLALCHEMY_DATABASE_URI).replace("postgresql://", "postgresql+asyncpg://"),
            echo=False,
            future=True,
            # Important for serverless: limit connection pool size
            pool_size=1,
            max_overflow=0,
            pool_recycle=3600,
            pool_pre_ping=True,
        )

# Create engine
engine = get_engine()

# Create async session factory
AsyncSessionLocal = sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
)

# Store a reference to the engine for initialization
_engine = engine

async def get_db() -> Generator:
    """
    Dependency for getting async database session.
    For serverless environments, we create a new session for each request.
    """
    # For Vercel serverless with SQLite, we need to ensure tables exist for each new instance
    if os.environ.get("RENDER") or os.environ.get("SERVERLESS") and settings.USE_SQLITE_MEMORY:
        # We'll use the same engine but create a new session
        async with AsyncSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()
    elif os.environ.get("RENDER") or os.environ.get("SERVERLESS"):
        # For Vercel with PostgreSQL, create a new engine for each request
        engine = get_engine()
        async_session = sessionmaker(
            engine, class_=AsyncSession, expire_on_commit=False, autocommit=False, autoflush=False
        )
        async with async_session() as session:
            try:
                yield session
            finally:
                await session.close()
                await engine.dispose()
    else:
        # For development/traditional hosting
        async with AsyncSessionLocal() as session:
            try:
                yield session
            finally:
                await session.close()

# Export the engine for use in init_db
def get_engine_for_init():
    return _engine
