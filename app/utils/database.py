"""Database configuration and setup."""
import os
from pathlib import Path
from typing import AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine, async_sessionmaker
from sqlmodel import SQLModel

# Determine database path based on environment
if os.environ.get("VERCEL"):
    # Vercel serverless - database bundled with deployment
    DB_PATH = Path(__file__).parent.parent.parent / "school_finder.db"
elif os.path.exists("/opt/school-finder/data"):
    # Production on Oracle Cloud
    DB_PATH = Path("/opt/school-finder/data/school_finder.db")
elif os.path.exists("/data"):
    # Production on Fly.io or Docker
    DB_PATH = Path("/data/school_finder.db")
else:
    # Development
    DB_PATH = Path("./school_finder.db")

DB_PATH.parent.mkdir(parents=True, exist_ok=True)
DATABASE_URL = f"sqlite+aiosqlite:///{DB_PATH}"

# Create async engine
engine = create_async_engine(DATABASE_URL, echo=False)

# Create async session factory
async_session = async_sessionmaker(
    engine, class_=AsyncSession, expire_on_commit=False
)


async def get_db() -> AsyncGenerator[AsyncSession, None]:
    """Get database session."""
    async with async_session() as session:
        yield session


async def init_db() -> None:
    """Initialize database and create tables."""
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)
