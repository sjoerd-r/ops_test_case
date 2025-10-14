from datetime import datetime, UTC
from decimal import Decimal
from sqlalchemy import BigInteger, Column, JSON
from sqlmodel import SQLModel, Field, Index


class Order(SQLModel, table=True):
    __tablename__ = "orders"
    __table_args__ = (
        Index("idx_orders_store_shopify", "store_id", "shopify_order_id"),
        Index("idx_orders_shopify_id", "shopify_order_id"),
        Index("idx_orders_customer", "customer_id"),
        Index("idx_orders_store", "store_id"),
        Index("idx_orders_status", "financial_status"),
        Index("idx_orders_fulfillment", "fulfillment_status"),
        Index("idx_orders_created", "created_at"),
        Index("idx_orders_processed", "processed_at"),
        Index("idx_orders_store_created", "store_id", "created_at"),
        Index("idx_orders_email", "email"),
        Index("idx_orders_order_number", "order_number"),
    )

    id: int | None = Field(default=None, primary_key=True)
    store_id: int = Field(foreign_key="stores.id", nullable=False)
    shopify_order_id: int = Field(sa_column=Column(BigInteger, nullable=False))
    customer_id: int | None = Field(foreign_key="customers.id", nullable=True)
    location_id: int | None = Field(foreign_key="locations.id", nullable=True)
    order_number: int | None = Field(default=None)
    name: str | None = Field(default=None)
    email: str | None = Field(default=None)
    phone: str | None = Field(default=None)
    total_price: Decimal | None = Field(default=None)
    subtotal_price: Decimal | None = Field(default=None)
    total_tax: Decimal | None = Field(default=None)
    total_discounts: Decimal | None = Field(default=None)
    total_line_items_price: Decimal | None = Field(default=None)
    total_weight: Decimal | None = Field(default=None)
    currency: str | None = Field(default=None)
    presentment_currency: str | None = Field(default=None)
    taxes_included: bool | None = Field(default=None)
    financial_status: str | None = Field(default=None)
    fulfillment_status: str | None = Field(default=None)
    tags: str | None = Field(default=None)
    note: str | None = Field(default=None)
    note_attributes: list | None = Field(default=None, sa_column=Column(JSON))
    source_name: str | None = Field(default=None)
    source_identifier: str | None = Field(default=None)
    source_url: str | None = Field(default=None)
    app_id: int | None = Field(sa_column=Column(BigInteger, nullable=True))
    user_id: int | None = Field(sa_column=Column(BigInteger, nullable=True))
    device_id: str | None = Field(default=None)
    browser_ip: str | None = Field(default=None)
    landing_site: str | None = Field(default=None)
    referring_site: str | None = Field(default=None)
    customer_locale: str | None = Field(default=None)
    cart_token: str | None = Field(default=None)
    checkout_token: str | None = Field(default=None)
    confirmed: bool | None = Field(default=None)
    test: bool | None = Field(default=None)
    processed_at: datetime | None = Field(default=None)
    closed_at: datetime | None = Field(default=None)
    cancelled_at: datetime | None = Field(default=None)
    cancel_reason: str | None = Field(default=None)
    payment_gateway_names: list | None = Field(
        default=None, sa_column=Column(JSON)
    )
    payment_terms: dict | None = Field(default=None, sa_column=Column(JSON))
    order_status_url: str | None = Field(default=None)
    order_edit_url: str | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
