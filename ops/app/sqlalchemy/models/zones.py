from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Index


class Zone(SQLModel, table=True):
    __tablename__ = "zones"
    __table_args__ = (
        Index("idx_zones_warehouse", "warehouse_id"),
        Index("idx_zones_floor", "warehouse_id", "floor"),
        Index("idx_zones_name", "warehouse_id", "name"),
    )

    id: int | None = Field(default=None, primary_key=True)
    warehouse_id: int = Field(
        foreign_key="warehouses.id", nullable=False, index=True
    )
    name: str = Field(nullable=False, index=True)
    description: str | None = Field(default=None)
    floor: int = Field(default=1, nullable=False, index=True)
    type: str | None = Field(default="storage")
    active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
