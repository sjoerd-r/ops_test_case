import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator

from ops.app.services.bin.position import BinPositionService
from ops.app.services.bin.dto import (
    BinPositionInput,
    BinPositionFilter,
)

if TYPE_CHECKING:
    from ops.app.graphql.schemas.pallet.main import Pallet
    from ops.app.graphql.schemas.bin.main import Bin

BinType: TypeAlias = Annotated[
    "Bin", strawberry.lazy("ops.app.graphql.schemas.bin.main")
]
PalletType: TypeAlias = Annotated[
    "Pallet", strawberry.lazy("ops.app.graphql.schemas.pallet.main")
]
BinPositionType: TypeAlias = Annotated[
    "BinPosition",
    strawberry.lazy("ops.app.graphql.schemas.bin.position"),
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
        if not parent.bind_id:
            return None
        return await info.context.loaders.bin_position.bin.load(parent.bin_id)

    @strawberry.field
    async def pallets(
        self, info, parent: strawberry.Parent["BinPosition"]
    ) -> list[PalletType]:
        if not parent.id:
            return None
        return await info.context.loaders.bin_position.pallets.load(parent.id)


@strawberry.type
class BinPositionQueries:
    @strawberry.field
    @staticmethod
    async def bin_positions(info) -> list["BinPosition"]:
        return await BinPositionService(
            info.context.session
        ).get_bin_positions()

    @strawberry.field
    @staticmethod
    async def bin_position(info, id: int) -> Optional["BinPosition"]:
        return await BinPositionService(info.context.session).get_bin_position(
            BinPositionFilter(id=id)
        )


@strawberry.type
class BinPositionMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_bin_position(
        info,
        bin_id: int,
        position: str | None = None,
        location: str | None = None,
        status: str | None = "available",
        is_available: bool | None = True,
    ) -> "BinPosition":
        return await BinPositionService(
            info.context.session
        ).upsert_bin_position(
            BinPositionInput(
                bin_id=bin_id,
                position=position,
                location=location,
                status=status,
                is_available=is_available,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_bin_position(info, id: int) -> bool:
        return await BinPositionService(
            info.context.session
        ).delete_bin_position(BinPositionInput(id=id))


@strawberry.type
class BinPositionSubscriptions:
    @strawberry.subscription
    async def bin_position_created(
        self, info
    ) -> AsyncGenerator[BinPositionType, None]:
        yield

    @strawberry.subscription
    async def bin_position_updated(
        self, info
    ) -> AsyncGenerator[BinPositionType, None]:
        yield

    @strawberry.subscription
    async def bin_position_deleted(self, info) -> AsyncGenerator[int, None]:
        yield
