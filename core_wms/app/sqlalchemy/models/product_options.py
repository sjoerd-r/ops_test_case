from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import ARRAY, String, Column, BigInteger, ForeignKey


class ProductOption(SQLModel, table=True):
    __tablename__ = "product_options"
    __table_args__ = (
        Index("idx_options_shopify_id", "product_id", "shopify_option_id"),
    )

    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(
        sa_column=Column(BigInteger, ForeignKey("products.id"), nullable=False)
    )
    shopify_option_id: int = Field(
        sa_column=Column(BigInteger, nullable=False)
    )
    name: str | None = Field(default=None)
    position: int | None = Field(default=None)
    values: list[str] = Field(
        sa_column=Column(ARRAY(String)), default_factory=list
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
