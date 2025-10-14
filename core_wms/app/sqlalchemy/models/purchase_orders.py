from datetime import datetime, date, UTC
from sqlmodel import SQLModel, Field, Index


class PurchaseOrder(SQLModel, table=True):
    __tablename__ = "purchase_orders"
    __table_args__ = (
        Index("idx_purchase_orders_supplier", "supplier_id"),
        Index("idx_purchase_orders_warehouse", "warehouse_id"),
        Index("idx_purchase_orders_po_id", "purchase_order_id"),
        Index("idx_purchase_orders_status", "status"),
        Index("idx_purchase_orders_shipment_status", "shipment_status"),
        Index(
            "idx_purchase_orders_expected_delivery", "expected_delivery_date"
        ),
    )

    id: int | None = Field(default=None, primary_key=True)
    purchase_order_id: str = Field(nullable=False, unique=True, index=True)
    supplier_id: int = Field(
        foreign_key="suppliers.id", nullable=False, index=True
    )
    warehouse_id: int = Field(
        foreign_key="warehouses.id", nullable=False, index=True
    )
    status: str = Field(default="draft", nullable=False)
    shipment_status: str = Field(default="pending", nullable=False)
    expected_delivery_date: date | None = Field(default=None, index=True)
    delivery_date: date | None = Field(default=None)
    tracking_number: str | None = Field(default=None, index=True)
    tracking_url: str | None = Field(default=None)
    carrier: str | None = Field(default=None)
    notes: str | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
