from datetime import datetime, UTC
from sqlmodel import SQLModel, Field


class Pallet(SQLModel, table=True):
    __tablename__ = "pallets"

    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(nullable=False, unique=True, index=True)
    bin_position_id: int | None = Field(
        foreign_key="bin_positions.id", nullable=True
    )
    weight: float | None = Field(default=0.0)
    status: str = Field(default="inbound", nullable=False)
    type: str | None = Field(default="euro", nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
