from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import BigInteger, Column

class FulfillmentOrderLineItem(SQLModel, table=True):
    __tablename__ = "fulfillment_order_line_items"
    __table_args__ = (
        Index("idx_fulfillment_order_line_items_order", "fulfillment_order_id"),
        Index("idx_fulfillment_order_line_items_line", "order_line_item_id"),
        Index("idx_fulfillment_order_line_items_shopify", "shopify_fulfillment_order_line_item_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    fulfillment_order_id: int = Field(foreign_key="fulfillment_orders.id", nullable=False)
    order_line_item_id: int = Field(foreign_key="order_line_items.id", nullable=False)
    shopify_fulfillment_order_line_item_id: Optional[int] = Field(sa_column=Column(BigInteger, default=None))
    quantity: int = Field(nullable=False)
    fulfillable_quantity: Optional[int] = Field(default=None)
    variant_id: Optional[int] = Field(sa_column=Column(BigInteger, default=None))
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)