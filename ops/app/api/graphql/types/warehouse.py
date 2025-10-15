import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator
from datetime import datetime

from ops.app.services.warehouse.main import WarehouseService
from ops.app.services.warehouse.dto import WarehouseInput, WarehouseFilter

ZoneType: TypeAlias = Annotated[
    "Zone", strawberry.lazy("ops.app.api.graphql.types.zone")
]
WarehouseType: TypeAlias = Annotated[
    "Warehouse", strawberry.lazy("ops.app.api.graphql.types.warehouse")
]


@strawberry.federation.type(keys=["id"])
class Warehouse:
    id: strawberry.ID
    name: str | None = None
    description: str | None = None
    location_id: int | None = None
    fulfillment_service_id: int | None = None
    active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def zones(
        self, info, parent: strawberry.Parent["Warehouse"]
    ) -> list[ZoneType]:
        if not parent.id:
            return None
        return await info.context.loaders.warehouse.zones.load(parent.id)
