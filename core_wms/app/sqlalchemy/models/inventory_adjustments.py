from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Index

class InventoryAdjustment(SQLModel, table=True):
    __tablename__ = "inventory_adjustments"
    __table_args__ = (
        Index("idx_inventory_adj_level", "inventory_level_id"),
        Index("idx_inventory_adj_reason", "reason"),
        Index("idx_inventory_adj_created", "created_at"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    inventory_level_id: int = Field(foreign_key="inventory_levels.id", nullable=False)
    quantity_adjusted: int = Field(nullable=False)
    state: Optional[str] = Field(default="available")
    reason: Optional[str] = Field(default=None)
    reference_document_uri: Optional[str] = Field(default=None)
    app_id: Optional[int] = Field(default=None)
    user_id: Optional[int] = Field(default=None)
    note: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)