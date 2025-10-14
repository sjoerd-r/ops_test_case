from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import BigInteger, Column, JSON

class FulfillmentOrder(SQLModel, table=True):
    __tablename__ = "fulfillment_orders"
    __table_args__ = (
        Index("idx_fulfillment_orders_shopify", "order_id", "shopify_fulfillment_order_id"),
        Index("idx_fulfillment_orders_channel", "channel_id"),
        Index("idx_fulfillment_orders_location", "assigned_location_id"),
    )
    
    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", nullable=False)
    shopify_fulfillment_order_id: int = Field(sa_column=Column(BigInteger, nullable=False))
    assigned_location_id: Optional[int] = Field(foreign_key="locations.id", nullable=True)
    channel_id: Optional[int] = Field(foreign_key="channels.id", nullable=True)
    status: Optional[str] = Field(default=None)
    request_status: Optional[str] = Field(default=None)
    supported_actions: Optional[list] = Field(sa_column=Column(JSON, default=None))
    destination: Optional[dict] = Field(sa_column=Column(JSON, default=None)) 
    delivery_method: Optional[dict] = Field(sa_column=Column(JSON, default=None))
    fulfill_at: Optional[datetime] = Field(default=None)
    fulfill_by: Optional[datetime] = Field(default=None)
    merchant_requests: Optional[list] = Field(sa_column=Column(JSON, default=None)) 
    fulfillment_holds: Optional[list] = Field(sa_column=Column(JSON, default=None)) 
    international_duties: Optional[dict] = Field(sa_column=Column(JSON, default=None)) 
    order_name: Optional[str] = Field(default=None)
    order_processed_at: Optional[datetime] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)