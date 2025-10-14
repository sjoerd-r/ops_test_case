from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Index


class Pallet(SQLModel, table=True):
    __tablename__ = "pallets"
    __table_args__ = (
        Index("idx_pallets_code", "code"),
        Index("idx_pallets_position", "bin_position_id"),
        Index("idx_pallets_status", "status"),
        Index("idx_pallets_batch", "batch_id"),
        Index("idx_pallets_variant", "product_variant_id"),
        Index("idx_pallets_po_line", "purchase_order_line_item_id"),
    )

    id: int | None = Field(default=None, primary_key=True)
    code: str = Field(nullable=False, unique=True, index=True)
    bin_position_id: int | None = Field(
        foreign_key="bin_positions.id", nullable=True
    )
    batch_id: int | None = Field(
        foreign_key="batches.id", nullable=True, index=True
    )
    product_variant_id: int | None = Field(
        foreign_key="product_variants.id", nullable=True, index=True
    )
    purchase_order_line_item_id: int | None = Field(
        foreign_key="purchase_order_line_items.id", nullable=True, index=True
    )
    weight: float | None = Field(default=0.0)
    status: str = Field(default="inbound", nullable=False)
    type: str | None = Field(default="euro", nullable=False)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
