import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator

from ops.app.services.bin.position import BinPositionService
from ops.app.services.bin.dto import (
    BinPositionInput,
    BinPositionFilter,
)
from ops.app.api.graphql.types.bin_position import BinPosition

BinPositionType: TypeAlias = Annotated[
    "BinPosition", strawberry.lazy("ops.app.api.graphql.types.bin_position")
]


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
