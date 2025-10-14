from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import BigInteger, Column


class Store(SQLModel, table=True):
    __tablename__ = "stores"
    __table_args__ = (Index("idx_stores_shopify_id", "shopify_store_id"),)

    id: int | None = Field(default=None, primary_key=True)
    shopify_store_id: int = Field(
        sa_column=Column(BigInteger, unique=True, nullable=False)
    )
    access_token: str | None = Field(default=None)
    name: str | None = Field(default=None)
    domain: str | None = Field(default=None)
    country: str | None = Field(default=None)
    currency: str | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
