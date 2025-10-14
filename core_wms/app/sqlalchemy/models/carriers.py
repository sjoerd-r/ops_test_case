from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Index

class Carrier(SQLModel, table=True):
    __tablename__ = "carriers"
    __table_args__ = (
        Index("idx_carriers_store", "store_id"),          
        Index("idx_carriers_name", "name"),
        Index("idx_carriers_code", "store_id", "code"),   
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    store_id: int = Field(foreign_key="stores.id", nullable=False)  
    name: str = Field(nullable=False) 
    code: str = Field(nullable=False) 
    tracking_url_template: Optional[str] = Field(default=None) 
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)