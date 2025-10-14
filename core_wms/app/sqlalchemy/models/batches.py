from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import Column, JSON

class Batch(SQLModel, table=True):
    __tablename__ = "batches"
    __table_args__ = (
        Index("idx_batches_warehouse", "warehouse_id"),             
        Index("idx_batches_supplier", "supplier_id"),               
        Index("idx_batches_variant", "product_variant_id"),         
        Index("idx_batches_lot", "lot"),                            
        Index("idx_batches_status", "status"),                      
        Index("idx_batches_expiry", "expiry_date"),

        Index("idx_batches_warehouse_status", "warehouse_id", "status"),
        Index("idx_batches_expiry_status", "expiry_date", "status"), 
        Index("idx_batches_variant_status", "product_variant_id", "status"),
        Index("idx_batches_supplier_lot", "supplier_id", "lot"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    warehouse_id: int = Field(foreign_key="warehouses.id", nullable=False, index=True)
    supplier_id: Optional[int] = Field(foreign_key="suppliers.id", nullable=True, index=True)  
    product_variant_id: int = Field(foreign_key="product_variants.id", nullable=False, index=True)
    lot: str = Field(nullable=False, index=True)
    manufacturing_date: Optional[datetime] = Field(default=None, nullable=True)
    expiry_date: Optional[datetime] = Field(default=None, nullable=True)
    status: str = Field(default="active", nullable=False, index=True) 
    additional: Optional[dict] = Field(default=None, sa_column=Column(JSON)) 
    notes: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)