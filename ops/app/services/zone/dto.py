from typing import Any
from datetime import datetime
from pydantic import BaseModel, Field, model_validator


class Zone(BaseModel):
    model_config = {"from_attributes": True}

    id: int | None = Field(None, description="Zone ID")
    warehouse_id: int = Field(
        ..., description="Warehouse ID this zone belongs to"
    )
    name: str = Field(..., description="Zone name")
    description: str | None = Field(None, description="Zone description")
    floor: int = Field(1, description="Floor number")
    type: str | None = Field("storage", description="Zone type")
    active: bool = Field(True, description="Whether the zone is active")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    @model_validator(mode="before")
    @classmethod
    def transform_shopify_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        return data

    @classmethod
    def from_shopify(
        cls, data: dict[str, Any], warehouse_id: int | None = None
    ) -> "Zone":
        return cls.model_validate(
            {
                "warehouse_id": warehouse_id,
                "name": data.get("name", ""),
                "description": data.get("description"),
                "floor": data.get("floor", 1),
                "type": data.get("type", "storage"),
                "active": data.get("active", True),
            }
        )


class ZoneInput(Zone):
    id: int | None = Field(None, description="Zone ID")


class ZoneFilter(BaseModel):
    id: int | None = Field(None, description="Zone ID to filter by")
    warehouse_id: int | None = Field(
        None, description="Warehouse ID to filter by"
    )
    name: str | None = Field(None, description="Zone name to filter by")
    floor: int | None = Field(None, description="Floor number to filter by")
    type: str | None = Field(None, description="Zone type to filter by")
    active: bool | None = Field(None, description="Filter by active status")
