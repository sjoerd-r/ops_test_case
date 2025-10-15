from typing import Any
from datetime import datetime
from pydantic import BaseModel, Field, model_validator


class Warehouse(BaseModel):
    model_config = {"from_attributes": True}

    id: int | None = Field(None, description="Warehouse ID")
    name: str = Field(..., description="Warehouse name")
    description: str | None = Field(None, description="Warehouse description")
    location_id: int | None = Field(
        None, description="Location ID associated with this warehouse"
    )
    fulfillment_service_id: int | None = Field(
        None,
        description="Fulfillment service ID associated with this warehouse",
    )
    active: bool = Field(True, description="Whether the warehouse is active")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    @model_validator(mode="before")
    @classmethod
    def transform_shopify_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data

    @classmethod
    def from_shopify(
        cls,
        data: dict[str, Any],
        location_id: int | None = None,
        fulfillment_service_id: int | None = None,
    ) -> "Warehouse":
        return cls.model_validate(
            {
                "name": data.get("name", ""),
                "description": data.get("description"),
                "location_id": data.get("location_id"),
                "fulfillment_service_id": data.get("fulfillment_service_id"),
                "active": data.get("active", True),
            }
        )


class WarehouseInput(Warehouse):
    id: int | None = Field(None, description="Warehouse ID")


class WarehouseFilter(BaseModel):
    id: int | None = Field(None, description="Warehouse ID to filter by")
    name: str | None = Field(None, description="Warehouse name to filter by")
    location_id: int | None = Field(
        None, description="Location ID to filter by"
    )
    active: bool | None = Field(None, description="Filter by active status")
