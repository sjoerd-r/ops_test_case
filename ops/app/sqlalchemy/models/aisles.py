from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Index


class Aisle(table=True):
    __tablename__ = "aisles"
    __table_args__ = (
        Index("idx_aisles_zone", "zone_id"),
        Index("idx_aisles_name", "zone_id", "name"),
    )

    id: int | None = Field(default=None, primary_key=True)
    zone_id: int = Field(foreign_key="zones.id", nullable=False, index=True)
    name: str = Field(nullable=False, index=True)
    description: str | None = Field(default=None)
    type: str | None = Field(default="storage")
    active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
