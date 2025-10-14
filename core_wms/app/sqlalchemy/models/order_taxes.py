from datetime import datetime, UTC
from decimal import Decimal
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import JSON, Column


class OrderTax(SQLModel, table=True):
    __tablename__ = "order_taxes"
    __table_args__ = (Index("idx_order_taxes_order", "order_id"),)

    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", nullable=False)
    title: str | None = Field(default=None)
    price: Decimal | None = Field(default=None)
    rate: Decimal | None = Field(default=None)
    price_set: dict | None = Field(default=None, sa_column=Column(JSON))
    channel_liable: bool | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
