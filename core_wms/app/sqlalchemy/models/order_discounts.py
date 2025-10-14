from datetime import datetime, timezone
from typing import Optional
from decimal import Decimal
from sqlmodel import SQLModel, Field

class OrderDiscount(SQLModel, table=True):
    __tablename__ = "order_discounts"

    id: Optional[int] = Field(default=None, primary_key=True)
    order_id: int = Field(foreign_key="orders.id", nullable=False)
    shopify_discount_application_id: Optional[str] = Field(default=None) 
    allocation_method: Optional[str] = Field(default=None)
    target_selection: Optional[str] = Field(default=None) 
    target_type: Optional[str] = Field(default=None)
    value_type: Optional[str] = Field(default=None) 
    code: Optional[str] = Field(default=None)  
    amount: Optional[Decimal] = Field(default=None) 
    value: Optional[Decimal] = Field(default=None)  
    title: Optional[str] = Field(default=None)  
    description: Optional[str] = Field(default=None) 
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)