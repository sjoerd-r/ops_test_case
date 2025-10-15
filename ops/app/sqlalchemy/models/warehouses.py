from datetime import datetime, UTC
from sqlmodel import SQLModel, Field


class Warehouse(SQLModel, table=True):
    __tablename__ = "warehouses"

    id: int | None = Field(default=None, primary_key=True)
    name: str = Field(nullable=False)
    description: str | None = Field(default=None)
    fulfillment_service_id: int | None = Field(default=None, nullable=True)
    active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
