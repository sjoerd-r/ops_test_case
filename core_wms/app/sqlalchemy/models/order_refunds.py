from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import BigInteger, Column


class OrderRefund(SQLModel, table=True):
    __tablename__ = "order_refunds"
    __table_args__ = (
        Index("idx_refunds_shopify", "order_id", "shopify_refund_id"),
    )

    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", nullable=False)
    shopify_refund_id: int = Field(
        sa_column=Column(BigInteger, nullable=False)
    )
    note: str | None = Field(default=None)
    processed_at: datetime | None = Field(default=None)
    user_id: int | None = Field(sa_column=Column(BigInteger, default=None))
    restock: bool | None = Field(default=True)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
