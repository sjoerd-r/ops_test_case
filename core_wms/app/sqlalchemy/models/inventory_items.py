from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import BigInteger, Column, ForeignKey, JSON

class InventoryItem(SQLModel, table=True):
    __tablename__ = "inventory_items"
    __table_args__ = (
        Index("idx_inventory_item_variant", "variant_id"),
        Index("idx_inventory_item_shopify", "shopify_inventory_item_id"),  # For Shopify GID lookups
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    variant_id: int = Field(sa_column=Column(BigInteger, ForeignKey("product_variants.id"), nullable=False))
    shopify_inventory_item_id: Optional[int] = Field(sa_column=Column(BigInteger, default=None, unique=True))
    sku: Optional[str] = Field(default=None, index=True)
    tracked: Optional[bool] = Field(default=True)
    requires_shipping: Optional[bool] = Field(default=None)
    unit_cost: Optional[float] = Field(default=None)
    country_code_of_origin: Optional[str] = Field(default=None)
    province_code_of_origin: Optional[str] = Field(default=None)
    harmonized_system_code: Optional[str] = Field(default=None)
    country_harmonized_system_codes: Optional[dict] = Field(sa_column=Column(JSON, default=None))
    measurement_weight: Optional[float] = Field(default=None)
    measurement_unit: Optional[str] = Field(default=None)
    measurement: Optional[dict] = Field(sa_column=Column(JSON, default=None))
    tracked_editable: Optional[dict] = Field(sa_column=Column(JSON, default=None))
    barcode: Optional[str] = Field(default=None, index=True)
    multipack: Optional[bool] = Field(default=False)
    case_upc: Optional[str] = Field(default=None)
    legacy_resource_id: Optional[str] = Field(default=None)
    duplicate_sku_count: Optional[int] = Field(default=None)
    inventory_history_url: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)