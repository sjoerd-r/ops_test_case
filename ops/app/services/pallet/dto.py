from typing import Any
from datetime import datetime
from pydantic import BaseModel, Field, model_validator


class Pallet(BaseModel):
    model_config = {"from_attributes": True}

    id: int | None = Field(None, description="Pallet ID")
    code: str = Field(..., description="Pallet code")
    bin_position_id: int | None = Field(None, description="Bin Position ID")
    batch_id: int | None = Field(None, description="Batch ID")
    product_variant_id: int | None = Field(
        None, description="Product Variant ID"
    )
    purchase_order_line_item_id: int | None = Field(
        None, description="Purchase Order Line Item ID"
    )
    weight: float | None = Field(0.0, description="Pallet weight")
    status: str = Field("inbound", description="Pallet status")
    type: str | None = Field("euro", description="Pallet type")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    @model_validator(mode="before")
    @classmethod
    def transform_shopify_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data

    @classmethod
    def from_shopify(cls, data: dict[str, Any]) -> "Pallet":
        return cls.model_validate(
            {
                "code": data.get("code", ""),
                "bin_position_id": data.get("bin_position_id"),
                "batch_id": data.get("batch_id"),
                "product_variant_id": data.get("product_variant_id"),
                "purchase_order_line_item_id": data.get(
                    "purchase_order_line_item_id"
                ),
                "weight": data.get("weight", 0.0),
                "status": data.get("status", "inbound"),
                "type": data.get("type", "euro"),
            }
        )


class PalletInput(Pallet):
    pass


class PalletFilter(BaseModel):
    id: int | None = Field(None, description="Pallet ID to filter by")
    code: str | None = Field(None, description="Pallet code to filter by")
    bin_position_id: int | None = Field(
        None, description="Bin Position ID to filter by"
    )
    batch_id: int | None = Field(None, description="Batch ID to filter by")
    product_variant_id: int | None = Field(
        None, description="Product Variant ID to filter by"
    )
    purchase_order_line_item_id: int | None = Field(
        None, description="Purchase Order Line Item ID to filter by"
    )
    status: str | None = Field(None, description="Status to filter by")
    type: str | None = Field(None, description="Type to filter by")


class PalletStock(BaseModel):
    model_config = {"from_attributes": True}

    id: int | None = Field(None, description="Pallet Stock ID")
    pallet_id: int = Field(..., description="Pallet ID")
    inventory_item_id: int = Field(..., description="Inventory Item ID")
    quantity: int = Field(0, description="Quantity")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    @model_validator(mode="before")
    @classmethod
    def transform_shopify_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data

    @classmethod
    def from_shopify(
        cls, data: dict[str, Any], pallet_id: int, inventory_item_id: int
    ) -> "PalletStock":
        return cls.model_validate(
            {
                "pallet_id": pallet_id,
                "inventory_item_id": inventory_item_id,
                "quantity": data.get("quantity", 0),
            }
        )


class PalletStockInput(PalletStock):
    pass


class PalletStockFilter(BaseModel):
    id: int | None = Field(None, description="Pallet Stock ID to filter by")
    pallet_id: int | None = Field(None, description="Pallet ID to filter by")
    inventory_item_id: int | None = Field(
        None, description="Inventory Item ID to filter by"
    )


class PalletRelated(BaseModel):
    stocks: list[PalletStockInput] = Field(
        default_factory=list, description="Related pallet stocks"
    )

    @classmethod
    def from_shopify(
        cls, data: dict[str, Any], pallet_id: int
    ) -> "PalletRelated":
        stocks = []
        for stock_data in data.get("stocks", []):
            stock = PalletStockInput.from_shopify(
                stock_data,
                pallet_id=pallet_id,
                inventory_item_id=stock_data.get("inventory_item_id"),
            )
            stocks.append(stock)

        return cls(stocks=stocks)
