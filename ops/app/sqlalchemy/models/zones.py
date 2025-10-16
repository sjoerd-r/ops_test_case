from datetime import datetime, UTC
from sqlmodel import SQLModel, Field


class Zone(SQLModel, table=True):
    __tablename__ = "zones"

    id: int | None = Field(default=None, primary_key=True)
    warehouse_id: int = Field(
        foreign_key="warehouses.id", nullable=False, index=True
    )
    name: str = Field(nullable=False)
    floor: int = Field(default=1, nullable=False)
    type: str | None = Field(default="storage")
    active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow, nullable=False
    )
