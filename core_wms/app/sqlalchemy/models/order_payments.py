from datetime import datetime, UTC
from decimal import Decimal
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import JSON, Column


class OrderPayment(SQLModel, table=True):
    __tablename__ = "order_payments"
    __table_args__ = (
        Index("idx_order_payments_order", "order_id"),
        Index("idx_order_payments_shopify", "shopify_payment_id"),
    )

    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id")
    shopify_payment_id: int | None = Field(default=None)
    gateway: str | None = Field(default=None)
    status: str | None = Field(default=None)
    kind: str | None = Field(default=None)
    amount: Decimal | None = Field(
        default=None, max_digits=10, decimal_places=2
    )
    currency: str | None = Field(default=None)
    authorization: str | None = Field(default=None)
    receipt: dict | None = Field(default=None, sa_column=Column(JSON))
    processed_at: datetime | None = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
    updated_at: datetime = Field(default_factory=lambda: datetime.now(UTC))
