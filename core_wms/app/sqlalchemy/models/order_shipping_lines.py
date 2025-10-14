from datetime import datetime, UTC
from decimal import Decimal
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import BigInteger, Column, JSON


class OrderShippingLine(SQLModel, table=True):
    __tablename__ = "order_shipping_lines"
    __table_args__ = (
        Index(
            "idx_shipping_lines_shopify",
            "order_id",
            "shopify_shipping_line_id",
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", nullable=False)
    shopify_shipping_line_id: int | None = Field(
        sa_column=Column(BigInteger, default=None)
    )
    title: str | None = Field(default=None)
    price: Decimal | None = Field(default=None)
    code: str | None = Field(default=None)
    source: str | None = Field(default=None)
    carrier_identifier: str | None = Field(default=None)
    delivery_category: str | None = Field(default=None)
    discounted_price: Decimal | None = Field(default=None)
    phone: str | None = Field(default=None)
    requested_fulfillment_service_id: int | None = Field(
        sa_column=Column(BigInteger, default=None)
    )
    tax_lines: list | None = Field(default=None, sa_column=Column(JSON))
    price_set: dict | None = Field(default=None, sa_column=Column(JSON))
    discounted_price_set: dict | None = Field(
        default=None, sa_column=Column(JSON)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
