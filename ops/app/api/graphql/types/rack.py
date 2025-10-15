import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import Annotated, TypeAlias
from collections.abc import AsyncGenerator
from datetime import datetime

RackType: TypeAlias = Annotated[
    "Rack", strawberry.lazy("ops.app.api.graphql.types.rack")
]
AisleType: TypeAlias = Annotated[
    "Aisle", strawberry.lazy("ops.app.api.graphql.types.aisle")
]

from ops.app.api.graphql.types.bin import Bin

@strawberry.federation.type(keys=["id"])
class Rack:
    id: strawberry.ID
    aisle_id: int | None = None
    position: int | None = None
    description: str | None = None
    type: str | None = None
    active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def bins(self, info, parent: strawberry.Parent["Rack"]) -> list[Bin]:
        if not parent.id:
            return None
        return await info.context.loaders.rack.bins.load(parent.id)

    @strawberry.field
    async def aisle(
        self, info, parent: strawberry.Parent["Rack"]
    ) -> AisleType | None:
        if not parent.aisle_id:
            return None
        return await info.context.loaders.rack.aisle.load(parent.aisle_id)
