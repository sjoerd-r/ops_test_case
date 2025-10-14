from datetime import datetime, date, UTC
from sqlmodel import SQLModel, Field, Index


class PalletStock(SQLModel, table=True):
    __tablename__ = "pallet_stock"
    __table_args__ = (
        Index("idx_pallet_stock_pallet", "pallet_id"),
        Index("idx_pallet_stock_variant", "product_variant_id"),
        Index("idx_pallet_stock_available", "available"),
        Index("idx_pallet_stock_location", "location_id"),
        Index("idx_pallet_stock_po_line", "purchase_order_line_item_id"),
        Index(
            "idx_pallet_stock_inbound",
            "purchase_order_line_item_id",
            "inbounded",
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    pallet_id: int = Field(
        foreign_key="pallets.id", nullable=False, unique=True, index=True
    )
    product_variant_id: int = Field(
        foreign_key="product_variants.id", nullable=False, index=True
    )
    purchase_order_line_item_id: int = Field(
        foreign_key="purchase_order_line_items.id", nullable=False, index=True
    )
    inbounded: int = Field(nullable=False)
    forecasted: int = Field(nullable=False)
    reserved: int = Field(default=0, nullable=False)
    allocated: int = Field(default=0, nullable=False)
    available: int = Field(default=0, nullable=False)
    inventory_item_id: int | None = Field(
        foreign_key="inventory_items.id", nullable=True, index=True
    )
    location_id: int | None = Field(
        foreign_key="bin_positions.id", nullable=True, index=True
    )
    received: date | None = Field(default=None)
    counted: date | None = Field(default=None)
    moved: date | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
