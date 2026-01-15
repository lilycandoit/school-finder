"""School search and filtering logic."""
from typing import List, Optional
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from app.models.school import School
from app.controllers.distance import haversine


async def find_schools_nearby(
    db: AsyncSession,
    latitude: float,
    longitude: float,
    radius_km: float,
    filters: Optional[dict] = None,
    limit: int = 50,
) -> List[dict]:
    """
    Find schools within radius, optionally filtered by various criteria.

    Args:
        db: Database session
        latitude: Center latitude
        longitude: Center longitude
        radius_km: Search radius in kilometers
        filters: Optional dict with filter criteria:
            - level: School level (e.g., "Primary School")
            - has_preschool: Filter for schools with preschool
            - has_intensive_english: Filter for schools with intensive English
            - has_opportunity_class: Filter for schools with opportunity class
            - not_selective: Filter for non-selective schools
            - has_distance_education: Filter for schools with distance education
        limit: Maximum number of results

    Returns:
        List of school dictionaries with distance calculated
    """
    if filters is None:
        filters = {}

    # Build base query
    query = select(School).where(
        School.latitude.isnot(None),
        School.longitude.isnot(None)
    )

    # Apply level filter if provided
    if filters.get("level"):
        query = query.where(School.level_of_schooling == filters["level"])

    # Apply program/support filters
    if filters.get("has_preschool"):
        query = query.where(School.preschool_ind == "Y")

    if filters.get("has_intensive_english"):
        query = query.where(School.intensive_english_centre == "Y")

    if filters.get("has_opportunity_class"):
        query = query.where(School.opportunity_class == "Y")

    if filters.get("not_selective"):
        query = query.where(
            (School.selective_school == "Not Selective") |
            (School.selective_school.is_(None))
        )

    if filters.get("has_distance_education"):
        query = query.where(School.distance_education == "Y")

    # Execute query
    result = await db.execute(query)
    all_schools = result.scalars().all()

    # Calculate distances and filter by radius
    schools_with_distance = []
    for school in all_schools:
        if school.latitude is None or school.longitude is None:
            continue

        distance = haversine(
            latitude, longitude, school.latitude, school.longitude
        )

        if distance <= radius_km:
            school_dict = {
                "id": school.id,
                "school_code": school.school_code,
                "school_name": school.school_name,
                "street": school.street,
                "town_suburb": school.town_suburb,
                "postcode": school.postcode,
                "phone": school.phone,
                "school_email": school.school_email,
                "website": school.website,
                "latest_year_enrolment_fte": school.latest_year_enrolment_fte,
                "indigenous_pct": school.indigenous_pct,
                "lbote_pct": school.lbote_pct,
                "icsea_value": school.icsea_value,
                "level_of_schooling": school.level_of_schooling,
                "selective_school": school.selective_school,
                "school_specialty_type": school.school_specialty_type,
                "school_subtype": school.school_subtype,
                "school_gender": school.school_gender,
                "latitude": school.latitude,
                "longitude": school.longitude,
                "distance": round(distance, 2),
                # Add filter-relevant fields for display
                "preschool_ind": school.preschool_ind,
                "intensive_english_centre": school.intensive_english_centre,
                "opportunity_class": school.opportunity_class,
                "distance_education": school.distance_education,
            }
            schools_with_distance.append(school_dict)

    # Sort by distance (closest first)
    schools_with_distance.sort(key=lambda x: x["distance"])

    # Limit results
    return schools_with_distance[:limit]


async def get_school_by_id(db: AsyncSession, school_id: int) -> Optional[School]:
    """Get a single school by ID."""
    result = await db.execute(select(School).where(School.id == school_id))
    return result.scalar_one_or_none()


async def get_schools_by_ids(
    db: AsyncSession, school_ids: List[int]
) -> List[School]:
    """Get multiple schools by IDs."""
    result = await db.execute(select(School).where(School.id.in_(school_ids)))
    return list(result.scalars().all())


async def get_distinct_levels(db: AsyncSession) -> List[str]:
    """Get distinct school levels for filtering."""
    result = await db.execute(
        select(School.level_of_schooling).distinct().where(
            School.level_of_schooling.isnot(None)
        )
    )
    levels = [row[0] for row in result.all() if row[0]]
    return sorted(levels)
