from typing import Any
from datetime import datetime
from pydantic import BaseModel, Field, model_validator


class Aisle(BaseModel):
    model_config = {"from_attributes": True}

    id: int | None = Field(None, description="Aisle ID")
    zone_id: int = Field(..., description="Zone ID")
    name: str = Field(..., description="Aisle name")
    description: str | None = Field(None, description="Aisle description")
    type: str | None = Field("storage", description="Aisle type")
    active: bool = Field(True, description="Whether the aisle is active")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    @model_validator(mode="before")
    @classmethod
    def transform_shopify_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        if isinstance(data, dict) and "id" in data and "aisle_id" not in data:
            data["aisle_id"] = data["id"]
        return data

    @classmethod
    def from_shopify(cls, data: dict[str, Any], zone_id: int) -> "Aisle":
        return cls.model_validate(
            {
                "zone_id": zone_id,
                "name": data.get("name", ""),
                "description": data.get("description"),
                "type": data.get("type", "storage"),
                "active": data.get("active", True),
            }
        )


class AisleInput(Aisle):
    pass


class AisleFilter(BaseModel):
    id: int | None = Field(None, description="Aisle ID to filter by")
    zone_id: int | None = Field(None, description="Zone ID to filter by")
    name: str | None = Field(None, description="Aisle name to filter by")
