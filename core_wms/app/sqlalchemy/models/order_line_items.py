from datetime import datetime, UTC
from typing import Any
from decimal import Decimal
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import Column
from sqlalchemy import JSON
from sqlalchemy import BigInteger, ForeignKey


class OrderLineItem(SQLModel, table=True):
    __tablename__ = "order_line_items"
    __table_args__ = (
        Index(
            "idx_order_line_items_shopify", "order_id", "shopify_line_item_id"
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", nullable=False)
    product_id: int | None = Field(
        sa_column=Column(BigInteger, ForeignKey("products.id"), nullable=True)
    )
    variant_id: int | None = Field(
        sa_column=Column(
            BigInteger, ForeignKey("product_variants.id"), nullable=True
        )
    )
    shopify_line_item_id: int = Field(
        sa_column=Column(BigInteger, nullable=False)
    )
    quantity: int | None = Field(default=None)
    price: Decimal | None = Field(default=None)
    title: str | None = Field(default=None)
    sku: str | None = Field(default=None, index=True)
    variant_title: str | None = Field(default=None)
    vendor: str | None = Field(default=None)
    fulfillment_status: str | None = Field(default=None)
    discount_allocations: Any | None = Field(
        default=None, sa_column=Column(JSON)
    )
    tax_lines: Any | None = Field(default=None, sa_column=Column(JSON))
    fulfillable_quantity: int | None = Field(default=None)
    grams: int | None = Field(default=None)
    gift_card: bool | None = Field(default=False)
    requires_shipping: bool | None = Field(default=True)
    taxable: bool | None = Field(default=True)
    product_exists: bool | None = Field(default=True)
    total_discount: Decimal | None = Field(default=None)
    discounted_price: Decimal | None = Field(default=None)
    properties: list | None = Field(sa_column=Column(JSON))
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
