#!/usr/bin/env python3
"""Build script for Vercel - generates SQLite database from CSV at build time."""
import asyncio
import sys
from pathlib import Path

# Add project root to path
sys.path.insert(0, str(Path(__file__).parent))

from app.utils.data_loader import main

if __name__ == "__main__":
    print("Building SQLite database from CSV files...")
    asyncio.run(main())
    print("Database build complete!")

    # Verify database was created
    db_path = Path("./school_finder.db")
    if db_path.exists():
        size_mb = db_path.stat().st_size / (1024 * 1024)
        print(f"Database created: {db_path} ({size_mb:.2f} MB)")
    else:
        print("ERROR: Database was not created!")
        sys.exit(1)
