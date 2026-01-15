#!/usr/bin/env python3
"""Script to load CSV data into SQLite database."""
import asyncio
import sys
from pathlib import Path

# Add parent directory to path
sys.path.insert(0, str(Path(__file__).parent.parent))

from app.utils.data_loader import main

if __name__ == "__main__":
    asyncio.run(main())
