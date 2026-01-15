# Dockerfile for NSW School Finder
# This file tells Docker how to build a container image for our application

# Use Python 3.12 slim image as base
# Slim images are smaller and faster
FROM python:3.12-slim

# Set working directory inside the container
# All commands will run from this directory
WORKDIR /app

# Set environment variables
# Prevents Python from writing .pyc files
ENV PYTHONDONTWRITEBYTECODE=1
# Prevents Python from buffering stdout/stderr (shows logs immediately)
ENV PYTHONUNBUFFERED=1

# Install system dependencies
# These are needed for building Python packages and SQLite
RUN apt-get update && apt-get install -y \
    gcc \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements file first
# This allows Docker to cache the pip install step
# If requirements.txt doesn't change, Docker won't reinstall packages
COPY requirements.txt .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application code
COPY . .

# Create directory for database files
# Fly.io volumes will mount here for persistent storage
RUN mkdir -p /data

# Expose port 8000
# This is the port FastAPI will run on
EXPOSE 8000

# Set the default command to run uvicorn
# This starts the FastAPI application
CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]

