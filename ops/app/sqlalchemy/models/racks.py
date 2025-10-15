from datetime import datetime, UTC
from sqlmodel import SQLModel, Field

class Rack(SQLModel, table=True):
    __tablename__ = "racks"

    id: int | None = Field(default=None, primary_key=True)
    aisle_id: int = Field(foreign_key="aisles.id", nullable=False, index=True)
    position: int = Field(nullable=False)
    description: str | None = Field(default=None)
    type: str | None = Field(default="pallet")
    active: bool = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
