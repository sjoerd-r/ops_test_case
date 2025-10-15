import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import Annotated, TypeAlias

ZoneType: TypeAlias = Annotated[
    "Zone", strawberry.lazy("ops.app.api.graphql.types.zone")
]
RackType: TypeAlias = Annotated[
    "Rack", strawberry.lazy("ops.app.api.graphql.types.rack")
]
AisleType: TypeAlias = Annotated[
    "Aisle", strawberry.lazy("ops.app.api.graphql.types.aisle")
]

@strawberry.federation.type(keys=["id"])
class Aisle:
    id: strawberry.ID
    zone_id: int | None = None
    name: str | None = None
    description: str | None = None
    type: str | None = None
    active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def racks(
        self, info, parent: strawberry.Parent["Aisle"]
    ) -> RackType | None:
        if not parent.id:
            return None
        return await info.context.loaders.aisle.racks.load(parent.id)

    @strawberry.field
    async def zone(
        self, info, parent: strawberry.Parent["Aisle"]
    ) -> ZoneType | None:
        if not parent.zone_id:
            return None
        return await info.context.loaders.aisle.zone.load(parent.zone_id)
