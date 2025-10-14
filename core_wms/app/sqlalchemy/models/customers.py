from datetime import datetime, timezone
from typing import Optional
from decimal import Decimal
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import BigInteger, Column, JSON

class Customer(SQLModel, table=True):
    __tablename__ = "customers"
    __table_args__ = (
        Index("idx_customers_shopify_id", "store_id", "shopify_customer_id"),
        Index("idx_customers_email", "store_id", "email"), 
        Index("idx_customers_phone", "store_id", "phone"), 
    )

    id: Optional[int] = Field(default=None, sa_column=Column(BigInteger, primary_key=True))
    store_id: int = Field(foreign_key="stores.id", nullable=False)
    shopify_customer_id: int = Field(sa_column=Column(BigInteger, nullable=False))
    email: Optional[str] = Field(default=None, index=True)
    first_name: Optional[str] = Field(default=None)
    last_name: Optional[str] = Field(default=None)
    phone: Optional[str] = Field(default=None)
    accepts_marketing: Optional[bool] = Field(default=False)
    accepts_marketing_updated_at: Optional[datetime] = Field(default=None)
    email_marketing_consent: Optional[dict] = Field(default=None, sa_column=Column(JSON))
    sms_marketing_consent: Optional[dict] = Field(default=None, sa_column=Column(JSON)) 
    marketing_opt_in_level: Optional[str] = Field(default=None)  
    state: Optional[str] = Field(default="ENABLED")  
    verified_email: Optional[bool] = Field(default=False)
    tax_exempt: Optional[bool] = Field(default=False)
    tags: Optional[str] = Field(default=None)  
    note: Optional[str] = Field(default=None)  
    currency: Optional[str] = Field(default="EUR")  
    multipass_identifier: Optional[str] = Field(default=None)  
    orders_count: Optional[int] = Field(default=0)
    total_spent: Optional[Decimal] = Field(default=0)
    last_order_id: Optional[int] = Field(default=None, sa_column=Column(BigInteger, nullable=True))
    last_order_name: Optional[str] = Field(default=None) 
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)