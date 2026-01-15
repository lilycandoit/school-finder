"""FastAPI application entry point."""
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware

# Import models to ensure they're registered with SQLModel
from app.models import school, postcode  # noqa: F401

from app.utils.database import init_db
from app.routes.school_routes import router


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

# Mount static files
app.mount("/static", StaticFiles(directory="app/static"), name="static")

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
