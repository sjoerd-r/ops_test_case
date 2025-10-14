from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import BigInteger, Column, ForeignKey


class ProductMedia(SQLModel, table=True):
    __tablename__ = "product_media"
    __table_args__ = (
        Index("idx_media_shopify_id", "product_id", "shopify_media_id"),
    )

    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(
        sa_column=Column(BigInteger, ForeignKey("products.id"), nullable=False)
    )
    shopify_media_id: int = Field(sa_column=Column(BigInteger, nullable=False))
    media_type: str | None = Field(default=None)
    src: str | None = Field(default=None)
    position: int | None = Field(default=None)
    alt: str | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
