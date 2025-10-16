from datetime import datetime, UTC
from sqlmodel import SQLModel, Field


class Bin(SQLModel, table=True):
    __tablename__ = "bins"

    id: int | None = Field(default=None, primary_key=True)
    rack_id: int = Field(foreign_key="racks.id", nullable=False, index=True)
    level: str = Field(nullable=False)  # "A", "B", "C", "D"
    prefix: str = Field(nullable=False)  # "1-AA"
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
