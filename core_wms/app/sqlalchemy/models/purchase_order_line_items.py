from datetime import datetime, UTC
from sqlmodel import SQLModel, Field, Index


class PurchaseOrderLineItem(SQLModel, table=True):
    __tablename__ = "purchase_order_line_items"
    __table_args__ = (
        Index("idx_po_line_items_po", "purchase_order_id"),
        Index("idx_po_line_items_variant", "product_variant_id"),
        Index("idx_po_line_items_status", "status"),
        Index(
            "idx_po_line_items_po_variant",
            "purchase_order_id",
            "product_variant_id",
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    purchase_order_id: int = Field(
        foreign_key="purchase_orders.id", nullable=False, index=True
    )
    product_variant_id: int = Field(
        foreign_key="product_variants.id", nullable=False, index=True
    )
    ordered: int = Field(nullable=False)
    received: int = Field(default=0, nullable=False)
    outstanding: int = Field(default=0, nullable=False)
    status: str = Field(default="pending", nullable=False)
    first_delivery_date: datetime | None = Field(default=None)
    last_delivery_date: datetime | None = Field(default=None)
    expected_completion_date: datetime | None = Field(default=None)
    notes: str | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
