from datetime import datetime, timezone
from typing import Optional
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import BigInteger, Column

class Channel(SQLModel, table=True):
    __tablename__ = "channels"
    __table_args__ = (
        Index("idx_channels_shopify_channel_id", "shopify_channel_id"),
        Index("idx_channels_store_handle", "store_id", "handle"),
    )

    id: Optional[int] = Field(default=None, primary_key=True)
    store_id: int = Field(foreign_key="stores.id", nullable=False, index=True)
    shopify_channel_id: Optional[int] = Field(sa_column=Column(BigInteger, default=None, unique=True))
    name: str = Field(nullable=False)
    channel_type: Optional[str] = Field(default=None)  
    handle: Optional[str] = Field(default=None, index=True)
    platform: Optional[str] = Field(default=None)
    app_id: Optional[int] = Field(default=None)
    active: bool = Field(default=True)
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc), nullable=False)