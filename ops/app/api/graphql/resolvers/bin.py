import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator

from ops.app.services.bin.main import BinService
from ops.app.services.bin.dto import BinInput, BinFilter
from ops.app.api.graphql.types.bin import Bin

BinType: TypeAlias = Annotated[
    "Bin", strawberry.lazy("ops.app.api.graphql.types.bin")
]


@strawberry.type
class BinQueries:
    @strawberry.field
    @staticmethod
    async def bins(info) -> list["Bin"]:
        return await BinService(info.context.session).get_bins()

    @strawberry.field
    @staticmethod
    async def bin(info, id: int) -> Optional["Bin"]:
        return await BinService(info.context.session).get_bin(BinFilter(id=id))


@strawberry.type
class BinMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_bin(
        info,
        rack_id: int,
        level: str | None = None,
        prefix: str | None = None,
        accessible: bool | None = True,
        status: str | None = "available",
        type: str | None = "standard",
        notes: str | None = None,
    ) -> "Bin":
        return await BinService(info.context.session).upsert_bin(
            BinInput(
                rack_id=rack_id,
                level=level,
                prefix=prefix,
                accessible=accessible,
                status=status,
                type=type,
                notes=notes,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_bin(info, id: int) -> bool:
        return await BinService(info.context.session).delete_bin(
            BinInput(id=id)
        )


@strawberry.type
class BinSubscriptions:
    @strawberry.subscription
    async def bin_created(self, info) -> AsyncGenerator[BinType, None]:
        yield

    @strawberry.subscription
    async def bin_updated(self, info) -> AsyncGenerator[BinType, None]:
        yield

    @strawberry.subscription
    async def bin_deleted(self, info) -> AsyncGenerator[int, None]:
        yield
