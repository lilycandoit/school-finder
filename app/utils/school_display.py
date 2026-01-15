"""Helper functions to transform school data for user-friendly display."""
from typing import Optional, List
from app.models.school import School


def format_gender(gender: Optional[str]) -> str:
    """Convert gender codes to plain English."""
    if not gender:
        return "Not available"

    mapping = {
        "Coed": "Boys & Girls",
        "Co-ed": "Boys & Girls",
        "Co-educational": "Boys & Girls",
        "Boys": "Boys Only",
        "Girls": "Girls Only",
    }
    return mapping.get(gender, gender)


def format_school_size(enrolment: Optional[float]) -> str:
    """Convert enrolment numbers to size categories."""
    if enrolment is None:
        return "Not available"

    if enrolment < 300:
        return "Small School"
    elif enrolment <= 800:
        return "Medium School"
    else:
        return "Large School"


def format_lbote(lbote_pct: Optional[str]) -> str:
    """Format LBOTE percentage for migrant parents."""
    if not lbote_pct or lbote_pct.lower() == "np":
        return "Data not available"

    try:
        pct = float(lbote_pct)
        return f"{pct:.0f}% Multi-lingual background"
    except ValueError:
        return "Data not available"


def format_intensive_english(value: Optional[str]) -> Optional[str]:
    """Return label if school has intensive English support."""
    if value and value.upper() == "Y":
        return "English Language Support Centre"
    return None


def format_opportunity_class(value: Optional[str]) -> Optional[str]:
    """Return label if school has opportunity classes."""
    if value and value.upper() == "Y":
        return "Advanced Classes (OC)"
    return None


def format_specialty(value: Optional[str]) -> Optional[str]:
    """Return specialty type if available, with friendly labels."""
    if not value or not value.strip():
        return None

    # Comprehensive is standard curriculum, make it clearer
    if value.strip().lower() == "comprehensive":
        return "Comprehensive (standard curriculum)"

    return value.strip()


def transform_school_for_display(school: School) -> dict:
    """
    Transform a School object into a display-friendly dictionary.

    Returns all fields needed for comparison, with plain English values.
    """
    # Build special features list
    special_features = []

    intensive_english = format_intensive_english(school.intensive_english_centre)
    if intensive_english:
        special_features.append(intensive_english)

    opportunity_class = format_opportunity_class(school.opportunity_class)
    if opportunity_class:
        special_features.append(opportunity_class)

    specialty = format_specialty(school.school_specialty_type)
    if specialty:
        special_features.append(specialty)

    return {
        "id": school.id,
        "school_name": school.school_name or "Not available",
        "level_of_schooling": school.level_of_schooling or "Not available",
        "town_suburb": school.town_suburb or "Not available",
        "postcode": school.postcode,
        "street": school.street or "Not available",
        "gender": format_gender(school.school_gender),
        "school_size": format_school_size(school.latest_year_enrolment_fte),
        "enrolment_raw": school.latest_year_enrolment_fte,
        "community": format_lbote(school.lbote_pct),
        "special_features": special_features,
        "has_intensive_english": school.intensive_english_centre and school.intensive_english_centre.upper() == "Y",
        "has_opportunity_class": school.opportunity_class and school.opportunity_class.upper() == "Y",
        "specialty_type": school.school_specialty_type,
        "selective_school": school.selective_school or "Not available",
        "icsea_value": school.icsea_value,
        "phone": school.phone,
        "school_email": school.school_email,
        "website": school.website,
    }


def transform_schools_for_comparison(schools: List[School]) -> List[dict]:
    """Transform multiple schools for the comparison page."""
    return [transform_school_for_display(school) for school in schools]
