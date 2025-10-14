from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import BigInteger, Column

class FulfillmentService(SQLModel, table=True):
    __tablename__ = "fulfillment_services"
    __table_args__ = (
        Index("idx_fulfillment_services_store", "store_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    store_id: int = Field(foreign_key="stores.id", nullable=False)
    shopify_fulfillment_service_id: Optional[int] = Field(sa_column=Column(BigInteger, default=None))
    name: str = Field(nullable=False)
    handle: str = Field(nullable=False, index=True)
    callback_url: Optional[str] = Field(default=None)
    active: bool = Field(default=True)
    tracking_support: Optional[bool] = Field(default=True)
    permits_sku_sharing: Optional[bool] = Field(default=True)
    requires_shipping_method: Optional[bool] = Field(default=True)
    fulfillment_orders_opt_in: Optional[bool] = Field(default=True)
    include_pending_stock: Optional[bool] = Field(default=False)
    inventory_management: Optional[bool] = Field(default=False)
    email: Optional[str] = Field(default=None)
    location_id: Optional[int] = Field(foreign_key="locations.id", nullable=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)