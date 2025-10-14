from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import ARRAY, String, Column
from sqlalchemy import BigInteger


class ShippingZone(SQLModel, table=True):
    __tablename__ = "shipping_zones"
    __table_args__ = (
        Index("idx_zones_shopify_id", "store_id", "shopify_zone_id"),
    )

    id: int | None = Field(default=None, primary_key=True)
    store_id: int = Field(foreign_key="stores.id", nullable=False)
    shopify_zone_id: int = Field(sa_column=Column(BigInteger, nullable=False))
    name: str | None = Field(default=None)
    countries: list[str] = Field(
        sa_column=Column(ARRAY(String)), default_factory=list
    )
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
