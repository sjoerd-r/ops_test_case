from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Index, Column, BigInteger, JSON
from sqlalchemy import BigInteger, Column
from core_wms.app.sqlalchemy.models.location_addresses import LocationAddress

class Location(SQLModel, table=True):
    __tablename__ = "locations"
    __table_args__ = (
        Index("idx_locations_shopify_id", "store_id", "shopify_location_id"),
        Index("idx_locations_handle", "handle"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    store_id: int = Field(foreign_key="stores.id", nullable=False)
    shopify_location_id: int = Field(sa_column=Column(BigInteger, nullable=False))
    name: Optional[str] = Field(default=None)
    address: Optional[LocationAddress] = Field(default=None, sa_column=Column(JSON))
    address_verified: Optional[bool] = Field(default=None)                    
    suggested_addresses: Optional[list] = Field(default=None, sa_column=Column(JSON)) 
    company: Optional[str] = Field(default=None)
    handle: Optional[str] = Field(default=None, index=True)                   
    platform: Optional[str] = Field(default="shopify")                       
    fulfills_online_orders: Optional[bool] = Field(default=None)
    has_active_inventory: Optional[bool] = Field(default=None)
    is_active: Optional[bool] = Field(default=None)
    is_fulfillment_service: Optional[bool] = Field(default=None)
    ships_inventory: Optional[bool] = Field(default=None)
    deactivatable: Optional[bool] = Field(default=True)                      
    activatable: Optional[bool] = Field(default=True)                        
    deletable: Optional[bool] = Field(default=False)                         
    deactivated_at: Optional[datetime] = Field(default=None)                 
    fulfillment_service_id: Optional[int] = Field(sa_column=Column(BigInteger, default=None)) 
    metafields: Optional[dict] = Field(default=None, sa_column=Column(JSON)) 
    legacy_resource_id: Optional[str] = Field(default=None)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)