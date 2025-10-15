import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import Annotated, TypeAlias

RackType: TypeAlias = Annotated[
    "Rack", strawberry.lazy("ops.app.api.graphql.types.rack")
]
BinPositionType: TypeAlias = Annotated[
    "BinPosition", strawberry.lazy("ops.app.api.graphql.types.bin_position")
]
BinType: TypeAlias = Annotated[
    "Bin", strawberry.lazy("ops.app.api.graphql.types.bin")
]

@strawberry.federation.type(keys=["id"])
class Bin:
    id: strawberry.ID
    rack_id: int | None = None
    level: str | None = None
    prefix: str | None = None
    accessible: bool | None = None
    status: str | None = None
    type: str | None = None
    notes: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def positions(
        self, info, parent: strawberry.Parent["Bin"]
    ) -> list[BinPositionType]:
        if not parent.id:
            return None
        return await info.context.loaders.bin.positions.load(parent.id)

    @strawberry.field
    async def rack(
        self, info, parent: strawberry.Parent["Bin"]
    ) -> RackType | None:
        if not parent.rack_id:
            return None
        return await info.context.loaders.bin.rack.load(parent.rack_id)
