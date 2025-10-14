from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Index


class Bin(table=True):
    __tablename__ = "bins"
    __table_args__ = (
        Index("idx_bins_rack", "rack_id"),
        Index("idx_bins_prefix", "prefix"),
        Index("idx_bins_status", "status"),
        Index("idx_bins_level", "rack_id", "level"),
        Index("idx_bins_accessibility", "accessible"),
    )

    id: int | None = Field(default=None, primary_key=True)
    rack_id: int = Field(foreign_key="racks.id", nullable=False, index=True)
    level: str = Field(nullable=False, index=True)  # "A", "B", "C", "D"
    prefix: str = Field(nullable=False, index=True)  # "1-AA"
    accessible: bool = Field(default=True)
    status: str = Field(default="available", nullable=False)
    type: str | None = Field(default="standard")
    notes: str | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
