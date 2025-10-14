from typing import Any
from datetime import datetime
from pydantic import BaseModel, Field, model_validator


class Rack(BaseModel):
    model_config = {"from_attributes": True}

    id: int | None = Field(None, description="Rack ID")
    aisle_id: int = Field(..., description="Aisle ID")
    position: int = Field(..., description="Rack position")
    description: str | None = Field(None, description="Rack description")
    type: str | None = Field("pallet", description="Rack type")
    active: bool = Field(True, description="Whether the rack is active")
    created_at: datetime | None = Field(None, description="Creation timestamp")
    updated_at: datetime | None = Field(
        None, description="Last update timestamp"
    )

    @model_validator(mode="before")
    @classmethod
    def transform_shopify_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        if isinstance(data, dict) and "id" in data and "rack_id" not in data:
            data["rack_id"] = data["id"]
        return data

    @classmethod
    def from_shopify(cls, data: dict[str, Any], aisle_id: int) -> "Rack":
        return cls.model_validate(
            {
                "aisle_id": aisle_id,
                "position": data.get("position", 0),
                "description": data.get("description"),
                "type": data.get("type", "pallet"),
                "active": data.get("active", True),
            }
        )


class RackInput(Rack):
    pass


class RackFilter(BaseModel):
    id: int | None = Field(None, description="Rack ID to filter by")
    aisle_id: int | None = Field(None, description="Aisle ID to filter by")
    position: int | None = Field(None, description="Position to filter by")
    type: str | None = Field(None, description="Type to filter by")
    active: bool | None = Field(None, description="Active status to filter by")
