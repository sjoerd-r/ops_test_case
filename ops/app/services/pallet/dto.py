from typing import Any
from datetime import datetime, date
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
    inbounded: int = Field(..., description="Inbounded quantity")
    forecasted: int = Field(..., description="Forecasted quantity")
    reserved: int = Field(default=0, description="Reserved quantity")
    allocated: int = Field(default=0, description="Allocated quantity")
    available: int = Field(default=0, description="Available quantity")
    location_id: int | None = Field(None, description="Location ID (bin position)")
    received: date | None = Field(None, description="Received date")
    counted: date | None = Field(None, description="Counted date")
    moved: date | None = Field(None, description="Moved date")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    @model_validator(mode="before")
    @classmethod
    def transform_shopify_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data


class PalletStockInput(PalletStock):
    pallet_id: int | None = Field(None, description="Pallet ID")
    inbounded: int | None = Field(None, description="Inbounded quantity")
    forecasted: int | None = Field(None, description="Forecasted quantity")


class PalletStockFilter(BaseModel):
    id: int | None = Field(None, description="Pallet Stock ID to filter by")
    pallet_id: int | None = Field(None, description="Pallet ID to filter by")


class PalletRelated(BaseModel):
    stocks: list[PalletStockInput] = Field(
        default_factory=list, description="Related pallet stocks"
    )

