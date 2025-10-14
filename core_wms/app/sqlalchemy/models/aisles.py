from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Index

class Aisle(SQLModel, table=True):
    __tablename__ = "aisles"
    __table_args__ = (
        Index("idx_aisles_zone", "zone_id"),
        Index("idx_aisles_name", "zone_id", "name"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    zone_id: int = Field(foreign_key="zones.id", nullable=False, index=True)
    name: str = Field(nullable=False, index=True)
    description: Optional[str] = Field(default=None)
    type: Optional[str] = Field(default="storage") 
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)