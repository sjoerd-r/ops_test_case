from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import BigInteger, Column, JSON


class OrderReturn(SQLModel, table=True):
    __tablename__ = "order_returns"
    __table_args__ = (
        Index("idx_returns_shopify", "order_id", "shopify_return_id"),
    )

    id: int | None = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", nullable=False)
    shopify_return_id: int = Field(
        sa_column=Column(BigInteger, nullable=False)
    )
    status: str | None = Field(default=None)
    note: str | None = Field(default=None)
    processed_at: datetime | None = Field(default=None)
    restock: bool | None = Field(default=True)
    return_line_items: list | None = Field(
        default=None, sa_column=Column(JSON)
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
