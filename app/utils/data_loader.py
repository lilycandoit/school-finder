"""Data loading utilities for importing CSV into SQLite."""
import csv
import asyncio
from pathlib import Path
from typing import Optional
from sqlalchemy.ext.asyncio import AsyncSession, create_async_engine
from sqlalchemy.orm import sessionmaker
from sqlmodel import SQLModel

from app.models.school import School
from app.models.postcode import Postcode
from app.utils.database import DATABASE_URL, engine


def parse_float(value: str) -> Optional[float]:
    """Parse float, returning None for empty strings."""
    if not value or value.strip() == "":
        return None
    try:
        return float(value)
    except ValueError:
        return None


def parse_int(value: str) -> Optional[int]:
    """Parse int, returning None for empty strings."""
    if not value or value.strip() == "":
        return None
    try:
        return int(float(value))  # Handle "123.0" format
    except ValueError:
        return None


async def load_schools_csv(csv_path: Path, db_session: AsyncSession) -> int:
    """Load schools from CSV into database."""
    schools = []
    total_count = 0

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            school = School(
                school_code=row.get("School_code") or None,
                age_id=row.get("AgeID") or None,
                school_name=row.get("School_name") or None,
                street=row.get("Street") or None,
                town_suburb=(row.get("Town_suburb") or "").strip() or None,  # Strip whitespace
                postcode=(row.get("Postcode") or "").strip() or None,  # Strip whitespace
                phone=row.get("Phone") or None,
                school_email=row.get("School_Email") or None,
                website=row.get("Website") or None,
                fax=row.get("Fax") or None,
                latest_year_enrolment_fte=parse_float(
                    row.get("latest_year_enrolment_FTE", "")
                ),
                indigenous_pct=row.get("Indigenous_pct") or None,
                lbote_pct=row.get("LBOTE_pct") or None,
                icsea_value=parse_int(row.get("ICSEA_value", "")),
                level_of_schooling=row.get("Level_of_schooling") or None,
                selective_school=row.get("Selective_school") or None,
                opportunity_class=row.get("Opportunity_class") or None,
                school_specialty_type=row.get("School_specialty_type") or None,
                school_subtype=row.get("School_subtype") or None,
                support_classes=row.get("Support_classes") or None,
                preschool_ind=row.get("Preschool_ind") or None,
                distance_education=row.get("Distance_education") or None,
                intensive_english_centre=row.get("Intensive_english_centre") or None,
                school_gender=row.get("School_gender") or None,
                late_opening_school=row.get("Late_opening_school") or None,
                date_1st_teacher=row.get("Date_1st_teacher") or None,
                date_extracted=row.get("Date_extracted") or None,
                lga=row.get("LGA") or None,
                electorate_from_2023=row.get("electorate_from_2023") or None,
                electorate_2015_2022=row.get("electorate_2015_2022") or None,
                fed_electorate_from_2025=row.get("fed_electorate_from_2025") or None,
                fed_electorate_2016_2024=row.get("fed_electorate_2016_2024") or None,
                operational_directorate=row.get("Operational_directorate") or None,
                principal_network=row.get("Principal_network") or None,
                operational_directorate_office=row.get(
                    "Operational_directorate_office"
                )
                or None,
                operational_directorate_office_phone=row.get(
                    "Operational_directorate_office_phone"
                )
                or None,
                operational_directorate_office_address=row.get(
                    "Operational_directorate_office_address"
                )
                or None,
                facs_district=row.get("FACS_district") or None,
                local_health_district=row.get("Local_health_district") or None,
                aecg_region=row.get("AECG_region") or None,
                asgs_remoteness=row.get("ASGS_remoteness") or None,
                latitude=parse_float(row.get("Latitude", "")),
                longitude=parse_float(row.get("Longitude", "")),
                assets_unit=row.get("Assets unit") or None,
                sa4=row.get("SA4") or None,
                foei_value=parse_int(row.get("FOEI_Value", "")),
            )
            schools.append(school)
            total_count += 1

            # Batch insert every 100 records
            if len(schools) >= 100:
                db_session.add_all(schools)
                await db_session.commit()
                schools = []

    # Insert remaining schools
    if schools:
        db_session.add_all(schools)
        await db_session.commit()

    return total_count


async def load_postcodes_csv(csv_path: Path, db_session: AsyncSession) -> int:
    """Load postcodes from CSV into database."""
    postcodes = []
    total_count = 0

    with open(csv_path, "r", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for row in reader:
            postcode = Postcode(
                postcode=str(row.get("postcode", "")).strip(),
                latitude=float(row.get("latitude", 0)),
                longitude=float(row.get("longitude", 0)),
                suburb=row.get("suburb") or None,
            )
            postcodes.append(postcode)
            total_count += 1

            # Batch insert every 100 records
            if len(postcodes) >= 100:
                db_session.add_all(postcodes)
                await db_session.commit()
                postcodes = []

    # Insert remaining postcodes
    if postcodes:
        db_session.add_all(postcodes)
        await db_session.commit()

    return total_count


async def create_indexes(db_session: AsyncSession):
    """Create database indexes for performance."""
    # Indexes are created automatically by SQLModel based on Field(index=True)
    # But we can add composite indexes if needed
    pass


async def main():
    """Main data loading function."""
    # Initialize database
    async with engine.begin() as conn:
        await conn.run_sync(SQLModel.metadata.create_all)

    # Create session
    async_session = sessionmaker(
        engine, class_=AsyncSession, expire_on_commit=False
    )

    async with async_session() as session:
        # Load schools
        schools_path = Path("data/master_dataset.csv")
        if schools_path.exists():
            print(f"Loading schools from {schools_path}...")
            count = await load_schools_csv(schools_path, session)
            print(f"Loaded {count} schools")
        else:
            print(f"Warning: {schools_path} not found")

        # Load postcodes (if available)
        postcodes_path = Path("data/postcodes_nsw.csv")
        if postcodes_path.exists():
            print(f"Loading postcodes from {postcodes_path}...")
            count = await load_postcodes_csv(postcodes_path, session)
            print(f"Loaded {count} postcodes")
        else:
            print(f"Warning: {postcodes_path} not found (will use fallback geocoding)")

    print("Data loading complete!")


if __name__ == "__main__":
    asyncio.run(main())
