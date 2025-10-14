from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import BigInteger, Column

class FulfillmentEvent(SQLModel, table=True):
    __tablename__ = "fulfillment_events"
    __table_args__ = (
        Index("idx_fulfillment_events_fulfillment", "order_fulfillment_id"),
        Index("idx_fulfillment_events_shopify", "shopify_fulfillment_event_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    order_fulfillment_id: int = Field(foreign_key="order_fulfillments.id", nullable=False)
    shopify_fulfillment_event_id: Optional[int] = Field(sa_column=Column(BigInteger, default=None))
    status: str = Field(nullable=False)
    message: Optional[str] = Field(default=None)
    happened_at: datetime = Field(nullable=False)
    city: Optional[str] = Field(default=None)
    province: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    zip: Optional[str] = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    shop_id: Optional[int] = Field(sa_column=Column(BigInteger, default=None))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)