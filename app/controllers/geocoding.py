"""Geocoding: Convert suburb/postcode to latitude/longitude."""
from typing import Optional, Tuple
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from sqlmodel import select as sqlmodel_select

from app.models.postcode import Postcode
from app.models.school import School


async def lookup_postcode(
    db: AsyncSession, postcode: str
) -> Optional[Tuple[float, float]]:
    """
    Lookup postcode in postcode centroid table.

    Args:
        db: Database session
        postcode: Postcode string (may need normalization)

    Returns:
        Tuple of (latitude, longitude) or None if not found
    """
    # Normalize postcode (remove spaces, ensure string)
    postcode_clean = str(postcode).strip()

    result = await db.execute(
        select(Postcode).where(Postcode.postcode == postcode_clean)
    )
    postcode_record = result.scalar_one_or_none()

    if postcode_record:
        return (postcode_record.latitude, postcode_record.longitude)
    return None


async def lookup_suburb(
    db: AsyncSession, suburb: str, postcode: Optional[str] = None
) -> Optional[Tuple[float, float]]:
    """
    Lookup suburb in postcode table (if suburb column exists).

    Args:
        db: Database session
        suburb: Suburb name
        postcode: Optional postcode to narrow search

    Returns:
        Tuple of (latitude, longitude) or None if not found
    """
    suburb_clean = suburb.strip().title()

    query = select(Postcode).where(Postcode.suburb == suburb_clean)
    if postcode:
        query = query.where(Postcode.postcode == str(postcode).strip())

    result = await db.execute(query)
    postcode_record = result.scalar_one_or_none()

    if postcode_record:
        return (postcode_record.latitude, postcode_record.longitude)
    return None


async def compute_suburb_median(
    db: AsyncSession, suburb: str, postcode: Optional[str] = None
) -> Optional[Tuple[float, float]]:
    """
    Compute median latitude/longitude from schools in suburb.

    Args:
        db: Database session
        suburb: Suburb name
        postcode: Optional postcode to narrow search

    Returns:
        Tuple of (median_latitude, median_longitude) or None if no schools found
    """
    from sqlalchemy import func, text

    suburb_clean = suburb.strip().title()
    suburb_lower = suburb_clean.lower()

    # Build query with case-insensitive and whitespace-tolerant matching
    # SQLite's LOWER and TRIM functions handle case and whitespace
    query = sqlmodel_select(
        School.latitude, School.longitude
    ).where(
        func.lower(func.trim(School.town_suburb)) == suburb_lower,
        School.latitude.isnot(None),
        School.longitude.isnot(None)
    )

    if postcode:
        query = query.where(School.postcode == str(postcode).strip())

    result = await db.execute(query)
    schools = result.all()

    if not schools:
        return None

    # Extract valid coordinates
    coords = [
        (float(lat), float(lon))
        for lat, lon in schools
        if lat is not None and lon is not None
    ]

    if not coords:
        return None

    # Calculate median
    lats = sorted([lat for lat, _ in coords])
    lons = sorted([lon for _, lon in coords])

    mid = len(lats) // 2
    if len(lats) % 2 == 0:
        median_lat = (lats[mid - 1] + lats[mid]) / 2
        median_lon = (lons[mid - 1] + lons[mid]) / 2
    else:
        median_lat = lats[mid]
        median_lon = lons[mid]

    return (median_lat, median_lon)


async def geocode_location(
    db: AsyncSession, suburb: Optional[str] = None, postcode: Optional[str] = None
) -> Optional[Tuple[float, float]]:
    """
    Geocode location from suburb and/or postcode.

    Strategy:
    1. If postcode provided, try postcode lookup first
    2. If suburb provided, try suburb lookup in postcode table
    3. Fallback: compute median from schools in suburb

    Args:
        db: Database session
        suburb: Suburb name (optional)
        postcode: Postcode (optional)

    Returns:
        Tuple of (latitude, longitude) or None if not found
    """
    # Try postcode lookup first
    if postcode:
        result = await lookup_postcode(db, postcode)
        if result:
            return result

    # Try suburb lookup in postcode table
    if suburb:
        result = await lookup_suburb(db, suburb, postcode)
        if result:
            return result

        # Fallback: median of schools in suburb
        result = await compute_suburb_median(db, suburb, postcode)
        if result:
            return result

    return None
