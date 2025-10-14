from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Index


class Warehouse(table=True):
    __tablename__ = "warehouses"
    __table_args__ = (
        Index("idx_warehouses_location", "location_id"),
        Index("idx_warehouses_name", "name"),
    )

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False, index=True)
    description: str | None = Field(default=None)
    location_id: int | None = Field(foreign_key="locations.id", nullable=True)
    fulfillment_service_id: int | None = Field(
        foreign_key="fulfillment_services.id", nullable=True
    )
    active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
