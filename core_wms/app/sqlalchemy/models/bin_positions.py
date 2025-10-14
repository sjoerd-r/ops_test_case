from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Index

class BinPosition(SQLModel, table=True):
    __tablename__ = "bin_positions"
    __table_args__ = (
        Index("idx_bin_positions_bin", "bin_id"),
        Index("idx_bin_positions_location", "location"), 
        Index("idx_bin_positions_status", "status"),
        Index("idx_bin_positions_position", "bin_id", "position"),
        
        Index("idx_bin_positions_location_status", "location", "status"),   
        Index("idx_bin_positions_status_bin", "status", "bin_id"),           
        Index("idx_bin_positions_bin_status", "bin_id", "status"),           
        
        Index("idx_bin_positions_location_prefix", "location", postgresql_ops={"location": "varchar_pattern_ops"}),  # ⚡ LIKE queries
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    bin_id: int = Field(foreign_key="bins.id", nullable=False, index=True)
    position: int = Field(nullable=False)  # 1, 2, 3, 4
    location: str = Field(nullable=False, unique=True, index=True)  # "1-AB-009"
    status: str = Field(default="available", nullable=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)