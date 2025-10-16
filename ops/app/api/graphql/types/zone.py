import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator
from datetime import datetime

from ops.app.services.zone.main import ZoneService
from ops.app.services.zone.dto import ZoneInput, ZoneFilter

AisleType: TypeAlias = Annotated[
    "Aisle", strawberry.lazy("ops.app.api.graphql.types.aisle")
]
WarehouseType: TypeAlias = Annotated[
    "Warehouse", strawberry.lazy("ops.app.api.graphql.types.warehouse")
]
ZoneType: TypeAlias = Annotated[
    "Zone", strawberry.lazy("ops.app.api.graphql.types.zone")
]


@strawberry.federation.type(keys=["id"])
class Zone:
    id: strawberry.ID
    warehouse_id: int | None = None
    name: str | None = None
    description: str | None = None
    floor: int | None = None
    type: str | None = None
    active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def aisles(
        self, info, parent: strawberry.Parent["Zone"]
    ) -> AisleType | None:
        if not parent.id:
            return None
        return await info.context.loaders.zone.aisles.load(parent.id)

    @strawberry.field
    async def warehouse(
        self, info, parent: strawberry.Parent["Zone"]
    ) -> WarehouseType | None:
        if not parent.warehouse_id:
            return None
        return await info.context.loaders.zone.warehouse.load(
            parent.warehouse_id
        )
