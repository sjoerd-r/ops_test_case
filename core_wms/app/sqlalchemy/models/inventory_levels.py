from datetime import datetime, timezone
from typing import Optional, List
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import BigInteger, Column, ForeignKey, JSON

class InventoryLevel(SQLModel, table=True):
    __tablename__ = "inventory_levels"
    __table_args__ = (
        Index("idx_inventory_item_loc", "inventory_item_id", "location_id"),
        Index("idx_inventory_level_shopify", "shopify_inventory_level_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    inventory_item_id: int = Field(sa_column=Column(BigInteger, ForeignKey("inventory_items.id"), nullable=False))
    location_id: int = Field(foreign_key="locations.id", nullable=False)
    shopify_inventory_level_id: Optional[int] = Field(sa_column=Column(BigInteger, default=None, unique=True))
    shopify_inventory_item_id: Optional[int] = Field(sa_column=Column(BigInteger, default=None))
    shopify_location_id: Optional[int] = Field(sa_column=Column(BigInteger, default=None))
    can_deactivate: Optional[bool] = Field(default=None)
    deactivation_alert: Optional[str] = Field(default=None)
    quantities: Optional[List[dict]] = Field(default=None, sa_column=Column(JSON))
    scheduled_changes: Optional[List[dict]] = Field(default=None, sa_column=Column(JSON))
    legacy_resource_id: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)