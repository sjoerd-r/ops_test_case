import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import Annotated, TypeAlias

BinType: TypeAlias = Annotated[
    "Bin", strawberry.lazy("ops.app.api.graphql.types.bin")
]
PalletType: TypeAlias = Annotated[
    "Pallet", strawberry.lazy("ops.app.api.graphql.types.pallet")
]
BinPositionType: TypeAlias = Annotated[
    "BinPosition", strawberry.lazy("ops.app.api.graphql.types.bin_position")
]

@strawberry.federation.type(keys=["id"])
class BinPosition:
    id: strawberry.ID
    bin_id: int | None = None
    position: str | None = None
    location: str | None = None
    status: str | None = None
    is_available: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def bin(
        self, info, parent: strawberry.Parent["BinPosition"]
    ) -> BinType | None:
        if not parent.bin_id:
            return None
        return await info.context.loaders.bin_position.bin.load(parent.bin_id)

    @strawberry.field
    async def pallets(
        self, info, parent: strawberry.Parent["BinPosition"]
    ) -> list[PalletType]:
        if not parent.id:
            return None
        return await info.context.loaders.bin_position.pallets.load(parent.id)
