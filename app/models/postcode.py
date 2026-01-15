"""Postcode database model."""
from typing import Optional
from sqlmodel import SQLModel, Field


class Postcode(SQLModel, table=True):
    """Database model for NSW postcode centroids."""

    __tablename__ = "postcodes"

    postcode: str = Field(primary_key=True, index=True)
    latitude: float = Field(index=True)
    longitude: float = Field(index=True)
    suburb: Optional[str] = Field(default=None, index=True)
