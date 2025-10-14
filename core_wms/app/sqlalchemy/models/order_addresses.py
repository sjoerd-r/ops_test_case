from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field

class OrderAddress(SQLModel, table=True):
    __tablename__ = "order_addresses"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", nullable=False)
    address_type: str = Field(nullable=False)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    address1: Optional[str] = Field(default=None)
    address2: Optional[str] = Field(default=None)
    city: Optional[str] = Field(default=None)
    province: Optional[str] = Field(default=None)
    province_code: Optional[str] = Field(default=None)
    country: Optional[str] = Field(default=None)
    country_code: Optional[str] = Field(default=None)
    zip: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    company: Optional[str] = Field(default=None)
    latitude: Optional[float] = Field(default=None)
    longitude: Optional[float] = Field(default=None)
    name: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)