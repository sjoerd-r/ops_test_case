from datetime import datetime, date, UTC
from sqlmodel import SQLModel, Field, Index


class PalletStock(SQLModel, table=True):
    __tablename__ = "pallet_stock"

    id: int | None = Field(default=None, primary_key=True)
    pallet_id: int = Field(
        foreign_key="pallets.id", nullable=False, unique=True
    )
    inbounded: int = Field(nullable=False)
    forecasted: int = Field(nullable=False)
    reserved: int = Field(default=0, nullable=False)
    allocated: int = Field(default=0, nullable=False)
    available: int = Field(default=0, nullable=False)
    location_id: int | None = Field(
        foreign_key="bin_positions.id", nullable=True
    )
    received: date | None = Field(default=None)
    counted: date | None = Field(default=None)
    moved: date | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
