from typing import Any
from datetime import datetime
from pydantic import BaseModel, Field, model_validator


class Bin(BaseModel):
    model_config = {"from_attributes": True}

    id: int | None = Field(None, description="Bin ID")
    rack_id: int = Field(..., description="Rack ID")
    level: str = Field(..., description="Bin level (e.g., 'A', 'B', 'C', 'D')")
    prefix: str = Field(..., description="Bin prefix (e.g., '1-AA')")
    accessible: bool = Field(True, description="Whether the bin is accessible")
    status: str = Field("available", description="Bin status")
    type: str | None = Field("standard", description="Bin type")
    notes: str | None = Field(None, description="Bin notes")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    @model_validator(mode="before")
    @classmethod
    def transform_shopify_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        if isinstance(data, dict) and "id" in data and "bin_id" not in data:
            data["bin_id"] = data["id"]
        return data

    @classmethod
    def from_shopify(cls, data: dict[str, Any], rack_id: int) -> "Bin":
        return cls.model_validate(
            {
                "rack_id": rack_id,
                "level": data.get("level", ""),
                "prefix": data.get("prefix", ""),
                "accessible": data.get("accessible", True),
                "status": data.get("status", "available"),
                "type": data.get("type", "standard"),
                "notes": data.get("notes"),
            }
        )


class BinInput(Bin):
    pass


class BinFilter(BaseModel):
    id: int | None = Field(None, description="Bin ID to filter by")
    rack_id: int | None = Field(None, description="Rack ID to filter by")
    level: str | None = Field(None, description="Bin level to filter by")
    prefix: str | None = Field(None, description="Bin prefix to filter by")
    status: str | None = Field(None, description="Status to filter by")


class BinPosition(BaseModel):
    model_config = {"from_attributes": True}

    id: int | None = Field(None, description="Bin Position ID")
    bin_id: int = Field(..., description="Bin ID")
    position: int = Field(..., description="Position number")
    location: str = Field(
        ..., description="Position location (e.g., '1-AB-009')"
    )
    status: str = Field("available", description="Position status")
    created_at: datetime = Field(default_factory=datetime.utcnow, description="Creation timestamp")
    updated_at: datetime = Field(default_factory=datetime.utcnow, description="Last update timestamp")

    @model_validator(mode="before")
    @classmethod
    def transform_shopify_fields(cls, data: dict[str, Any]) -> dict[str, Any]:
        if (
            isinstance(data, dict)
            and "id" in data
            and "position_id" not in data
        ):
            data["position_id"] = data["id"]
        return data

    @classmethod
    def from_shopify(cls, data: dict[str, Any], bin_id: int) -> "BinPosition":
        return cls.model_validate(
            {
                "bin_id": bin_id,
                "position": data.get("position", 1),
                "location": data.get("location"),
                "status": data.get("status", "available"),
            }
        )


class BinPositionInput(BinPosition):
    pass


class BinPositionFilter(BaseModel):
    id: int | None = Field(None, description="Bin position ID to filter by")
    bin_id: int | None = Field(None, description="Bin ID to filter by")
    position: int | None = Field(
        None, description="Position number to filter by"
    )
    location: str | None = Field(None, description="Location to filter by")
    status: str | None = Field(None, description="Status to filter by")


class BinRelated(BaseModel):
    positions: list[BinPosition] = Field(
        default_factory=list, description="Bin positions"
    )

    @classmethod
    def from_shopify(cls, data: dict[str, Any], bin_id: int) -> "BinRelated":
        positions = [
            BinPosition.from_shopify(position, bin_id)
            for position in data.get("positions", [])
        ]

        return cls(positions=positions)
