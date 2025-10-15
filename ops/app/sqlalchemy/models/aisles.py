from datetime import datetime, UTC
from sqlmodel import SQLModel, Field


class Aisle(SQLModel, table=True):
    __tablename__ = "aisles"

    id: int | None = Field(default=None, primary_key=True)
    zone_id: int = Field(foreign_key="zones.id", nullable=False, index=True)
    name: str = Field(nullable=False)
    description: str | None = Field(default=None)
    type: str | None = Field(default="storage")
    active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
