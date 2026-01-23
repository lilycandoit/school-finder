"""School database model."""
from typing import Optional
from sqlmodel import SQLModel, Field


class School(SQLModel, table=True):
    """Database model for NSW schools."""

    __tablename__ = "schools"

    # Primary key
    id: Optional[int] = Field(default=None, primary_key=True)

    # School identifiers
    school_code: Optional[str] = Field(default=None, index=True)
    age_id: Optional[str] = Field(default=None)
    school_name: Optional[str] = Field(default=None, index=True)

    # Location
    street: Optional[str] = Field(default=None)
    town_suburb: Optional[str] = Field(default=None, index=True)
    postcode: Optional[str] = Field(default=None, index=True)
    latitude: Optional[float] = Field(default=None, index=True)
    longitude: Optional[float] = Field(default=None, index=True)

    # Contact
    phone: Optional[str] = Field(default=None)
    school_email: Optional[str] = Field(default=None)
    website: Optional[str] = Field(default=None)
    fax: Optional[str] = Field(default=None)

    # Enrolment and demographics
    latest_year_enrolment_fte: Optional[float] = Field(default=None)
    indigenous_pct: Optional[str] = Field(default=None)  # Can be "np" for suppressed
    lbote_pct: Optional[str] = Field(default=None)  # Can be "np" for suppressed
    icsea_value: Optional[int] = Field(default=None)

    # School type (indexed fields used in filtering)
    level_of_schooling: Optional[str] = Field(default=None, index=True)
    selective_school: Optional[str] = Field(default=None, index=True)
    opportunity_class: Optional[str] = Field(default=None, index=True)
    school_specialty_type: Optional[str] = Field(default=None)
    school_subtype: Optional[str] = Field(default=None)
    support_classes: Optional[str] = Field(default=None)
    preschool_ind: Optional[str] = Field(default=None, index=True)
    distance_education: Optional[str] = Field(default=None, index=True)
    intensive_english_centre: Optional[str] = Field(default=None, index=True)
    school_gender: Optional[str] = Field(default=None, index=True)
    late_opening_school: Optional[str] = Field(default=None)

    # Dates
    date_1st_teacher: Optional[str] = Field(default=None)
    date_extracted: Optional[str] = Field(default=None)

    # Administrative
    lga: Optional[str] = Field(default=None)
    electorate_from_2023: Optional[str] = Field(default=None)
    electorate_2015_2022: Optional[str] = Field(default=None)
    fed_electorate_from_2025: Optional[str] = Field(default=None)
    fed_electorate_2016_2024: Optional[str] = Field(default=None)
    operational_directorate: Optional[str] = Field(default=None)
    principal_network: Optional[str] = Field(default=None)
    operational_directorate_office: Optional[str] = Field(default=None)
    operational_directorate_office_phone: Optional[str] = Field(default=None)
    operational_directorate_office_address: Optional[str] = Field(default=None)
    facs_district: Optional[str] = Field(default=None)
    local_health_district: Optional[str] = Field(default=None)
    aecg_region: Optional[str] = Field(default=None)
    asgs_remoteness: Optional[str] = Field(default=None)
    assets_unit: Optional[str] = Field(default=None)
    sa4: Optional[str] = Field(default=None)
    foei_value: Optional[int] = Field(default=None)
