from datetime import datetime, UTC
from sqlmodel import SQLModel, Field


class BinPosition(SQLModel, table=True):
    __tablename__ = "bin_positions"

    id: int | None = Field(default=None, primary_key=True)
    bin_id: int = Field(foreign_key="bins.id", nullable=False, index=True)
    position: int = Field(nullable=False)  # 1, 2, 3, 4
    location: str = Field(nullable=False, unique=True)  # "1-AB-009"
    status: str = Field(default="available", nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
