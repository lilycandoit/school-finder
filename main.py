"""FastAPI application entry point."""
import os
from pathlib import Path
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Import models to ensure they're registered with SQLModel
from app.models import school, postcode  # noqa: F401

from app.utils.database import init_db
from app.routes.school_routes import router

# Get the directory where main.py is located
BASE_DIR = Path(__file__).resolve().parent


@asynccontextmanager
async def lifespan(app: FastAPI):
    """Manage application lifespan."""
    # Startup: Initialize database
    await init_db()
    yield
    # Shutdown: Nothing needed for now


app = FastAPI(
    title="NSW School Finder",
    description="Find and compare schools near you in NSW",
    version="1.0.0",
    lifespan=lifespan,
)

# Mount static files - use absolute path for Vercel compatibility
static_dir = BASE_DIR / "app" / "static"
app.mount("/static", StaticFiles(directory=str(static_dir)), name="static")

# Include routers
app.include_router(router)

# CORS middleware (restrict in production)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Change to specific origins in production
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
