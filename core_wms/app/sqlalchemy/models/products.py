from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import BigInteger, Column


class Product(SQLModel, table=True):
    __tablename__ = "products"
    __table_args__ = (
        Index("idx_products_shopify_id", "store_id", "shopify_product_id"),
    )

    id: int | None = Field(
        default=None, sa_column=Column(BigInteger, primary_key=True)
    )
    store_id: int = Field(foreign_key="stores.id", nullable=False)
    shopify_product_id: int = Field(
        sa_column=Column(BigInteger, nullable=False)
    )
    title: str | None = Field(default=None)
    body_html: str | None = Field(default=None)
    vendor: str | None = Field(default=None)
    product_type: str | None = Field(default=None)
    handle: str | None = Field(default=None)
    tags: str | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
