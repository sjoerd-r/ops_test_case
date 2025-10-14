from datetime import datetime, UTC
from decimal import Decimal
from sqlmodel import SQLModel, Field, Index
from sqlalchemy import JSON, Column, BigInteger, ForeignKey


class ProductVariant(SQLModel, table=True):
    __tablename__ = "product_variants"
    __table_args__ = (
        Index("idx_variants_shopify_id", "product_id", "shopify_variant_id"),
        Index("idx_variants_shopify_variant_id", "shopify_variant_id"),
    )

    id: int | None = Field(default=None, primary_key=True)
    product_id: int = Field(
        sa_column=Column(BigInteger, ForeignKey("products.id"), nullable=False)
    )
    shopify_variant_id: int = Field(
        sa_column=Column(BigInteger, nullable=False)
    )
    inventory_item_id: int | None = Field(
        sa_column=Column(
            BigInteger, ForeignKey("inventory_items.id"), nullable=True
        )
    )
    sku: str | None = Field(default=None, index=True)
    barcode: str | None = Field(default=None, index=True)
    title: str | None = Field(default=None)
    option1: str | None = Field(default=None)
    option2: str | None = Field(default=None)
    option3: str | None = Field(default=None)
    price: Decimal | None = Field(default=None)
    compare_at_price: Decimal | None = Field(default=None)
    inventory_quantity: int | None = Field(default=None)
    weight: float | None = Field(default=None)
    weight_unit: str | None = Field(default=None)
    requires_shipping: bool | None = Field(default=None)
    taxable: bool | None = Field(default=None)
    position: int | None = Field(default=None)
    image_id: int | None = Field(
        sa_column=Column(
            BigInteger, ForeignKey("product_media.id"), nullable=True
        )
    )
    available_for_sale: bool | None = Field(default=None)
    inventory_policy: str | None = Field(default=None)
    inventory_management: str | None = Field(default=None)
    fulfillment_service: str | None = Field(default=None)
    tax_code: str | None = Field(default=None)
    unit_price: Decimal | None = Field(default=None)
    unit_price_measurement: dict | None = Field(
        default_factory=dict, sa_column=Column(JSON)
    )
    selected_options: list[dict] | None = Field(
        default_factory=list, sa_column=Column(JSON)
    )
    metafields: dict | None = Field(
        default_factory=dict, sa_column=Column(JSON)
    )
    legacy_resource_id: int | None = Field(default=None)
    created_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
    updated_at: datetime = Field(
        default_factory=lambda: datetime.now(UTC), nullable=False
    )
