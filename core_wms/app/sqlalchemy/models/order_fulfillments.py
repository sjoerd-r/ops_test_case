from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import BigInteger, Column, JSON

class OrderFulfillment(SQLModel, table=True):
    __tablename__ = "order_fulfillments"
    __table_args__ = (
        Index("idx_fulfillments_shopify", "order_id", "shopify_fulfillment_id"),
        Index("idx_fulfillments_order", "order_id", "order_fulfillment_id"),
        Index("idx_fulfillments_status", "status"),
        Index("idx_fulfillments_tracking", "tracking_number"),
        Index("idx_fulfillments_location", "location_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", nullable=False)
    shopify_fulfillment_id: Optional[int] = Field(sa_column=Column(BigInteger, default=None))
    shopify_order_id: Optional[int] = Field(sa_column=Column(BigInteger, default=None))
    order_fulfillment_id: Optional[str] = Field(default=None, unique=True, index=True)
    origin: Optional[str] = Field(default="shopify") 
    status: Optional[str] = Field(default=None)
    shipment_status: Optional[str] = Field(default=None)
    tracking_company: Optional[str] = Field(default=None)
    tracking_number: Optional[str] = Field(default=None)
    tracking_url: Optional[str] = Field(default=None)
    tracking_numbers: Optional[list] = Field(sa_column=Column(JSON))
    tracking_urls: Optional[list] = Field(sa_column=Column(JSON))
    shopify_location_id: Optional[int] = Field(sa_column=Column(BigInteger, default=None))
    location_id: Optional[int] = Field(foreign_key="locations.id", nullable=True)
    warehouse_id: Optional[int] = Field(foreign_key="warehouses.id", nullable=True)
    service: Optional[str] = Field(default=None)
    receipt: Optional[dict] = Field(sa_column=Column(JSON))    
    carrier_id: Optional[int] = Field(foreign_key="carriers.id", nullable=True)
    admin_graphql_api_id: Optional[str] = Field(default=None)
    notify_customer: Optional[bool] = Field(default=True) 
    created_by: Optional[str] = Field(default=None)  
    order_edit_id: Optional[str] = Field(default=None)  
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)