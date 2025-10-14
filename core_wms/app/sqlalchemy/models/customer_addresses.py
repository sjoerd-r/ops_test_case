from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import BigInteger, Column

class CustomerAddress(SQLModel, table=True):
    __tablename__ = "customer_addresses"
    __table_args__ = (
        Index("idx_customer_addresses_shopify_id", "shopify_address_id"),
        Index("idx_customer_addresses_customer", "customer_id"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    customer_id: int = Field(foreign_key="customers.id", nullable=False, index=True)
    shopify_address_id: int = Field(sa_column=Column(BigInteger, nullable=False, unique=True))
    shopify_customer_id: Optional[int] = Field(sa_column=Column(BigInteger, default=None))
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    company: Optional[str] = Field(default=None)
    address1: Optional[str] = Field(default=None)
    address2: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    province: Optional[str] = Field(default=None)
    province_code: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    country_code: Optional[str] = Field(default=None)
    zip: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    default: Optional[bool] = Field(default=False)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)