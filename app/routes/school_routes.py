"""School finder routes."""
from typing import Optional
from fastapi import APIRouter, Request, Depends, HTTPException, Form, Query
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy.ext.asyncio import AsyncSession

from app.utils.database import get_db
from app.controllers.geocoding import geocode_location
from app.controllers.school_controller import (
    find_schools_nearby,
    get_school_by_id,
    get_schools_by_ids,
    get_distinct_levels,
)
from app.utils.school_display import transform_schools_for_comparison

router = APIRouter()
templates = Jinja2Templates(directory="app/templates")


@router.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Home page with location input form."""
    return templates.TemplateResponse("index.html", {"request": request})


@router.post("/results", response_class=HTMLResponse)
async def results(
    request: Request,
    suburb: Optional[str] = Form(None),
    postcode: Optional[str] = Form(None),
    radius: float = Form(5.0),
    level: Optional[str] = Form(None),
    has_preschool: Optional[str] = Form(None),
    has_intensive_english: Optional[str] = Form(None),
    has_opportunity_class: Optional[str] = Form(None),
    not_selective: Optional[str] = Form(None),
    has_distance_education: Optional[str] = Form(None),
    db: AsyncSession = Depends(get_db),
):
    """Results page showing schools near location."""
    # Validate input
    if not suburb and not postcode:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "Please enter a suburb or postcode.",
            },
        )

    # Geocode location
    location = await geocode_location(db, suburb=suburb, postcode=postcode)

    if not location:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": f"Could not find location for {suburb or ''} {postcode or ''}. Please try again.",
                "suburb": suburb,
                "postcode": postcode,
            },
        )

    latitude, longitude = location

    # Build filters dict
    filters = {
        "level": level if level else None,
        "has_preschool": has_preschool == "Y",
        "has_intensive_english": has_intensive_english == "Y",
        "has_opportunity_class": has_opportunity_class == "Y",
        "not_selective": not_selective == "Y",
        "has_distance_education": has_distance_education == "Y",
    }

    # Find schools
    schools = await find_schools_nearby(
        db, latitude, longitude, radius, filters=filters
    )

    # Get distinct levels for filter
    distinct_levels = await get_distinct_levels(db)

    return templates.TemplateResponse(
        "results.html",
        {
            "request": request,
            "schools": schools,
            "suburb": suburb,
            "postcode": postcode,
            "radius": radius,
            "selected_level": level,
            "distinct_levels": distinct_levels,
            "result_count": len(schools),
            "filters": filters,
        },
    )


@router.get("/school/{school_id}", response_class=HTMLResponse)
async def school_detail(
    request: Request,
    school_id: int,
    db: AsyncSession = Depends(get_db),
):
    """School detail page."""
    school = await get_school_by_id(db, school_id)

    if not school:
        raise HTTPException(status_code=404, detail="School not found")

    return templates.TemplateResponse(
        "detail.html",
        {
            "request": request,
            "school": school,
        },
    )


@router.get("/compare", response_class=HTMLResponse)
async def compare(
    request: Request,
    ids: Optional[str] = Query(None),
    distances: Optional[str] = Query(None),
    db: AsyncSession = Depends(get_db),
):
    """Compare up to 3 schools."""
    if not ids:
        return templates.TemplateResponse(
            "index.html",
            {
                "request": request,
                "error": "Please select schools to compare.",
            },
        )

    # Parse school IDs
    try:
        school_ids = [int(id.strip()) for id in ids.split(",") if id.strip()][:3]
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid school IDs")

    if not school_ids:
        raise HTTPException(status_code=400, detail="No valid school IDs provided")

    # Parse distances (optional)
    distance_list = []
    if distances:
        try:
            distance_list = [float(d.strip()) for d in distances.split(",") if d.strip()][:3]
        except ValueError:
            distance_list = []

    # Get schools
    schools = await get_schools_by_ids(db, school_ids)

    if len(schools) != len(school_ids):
        raise HTTPException(
            status_code=404, detail="One or more schools not found"
        )

    # Transform schools for user-friendly display
    display_schools = transform_schools_for_comparison(schools)

    # Add distances to display schools (matching by order)
    for i, school in enumerate(display_schools):
        if i < len(distance_list):
            school["distance"] = distance_list[i]
        else:
            school["distance"] = None

    return templates.TemplateResponse(
        "compare.html",
        {
            "request": request,
            "schools": display_schools,
        },
    )
