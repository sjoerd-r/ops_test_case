import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator

from ops.app.services.bin.main import BinService
from ops.app.services.bin.dto import BinInput, BinFilter

if TYPE_CHECKING:
    from ops.app.graphql.schemas.rack.main import Rack
    from ops.app.graphql.schemas.bin.position import BinPosition

RackType: TypeAlias = Annotated[
    "Rack", strawberry.lazy("ops.app.graphql.schemas.rack.main")
]
BinPositionType: TypeAlias = Annotated[
    "BinPosition",
    strawberry.lazy("ops.app.graphql.schemas.bin.position"),
]
BinType: TypeAlias = Annotated[
    "Bin", strawberry.lazy("ops.app.graphql.schemas.bin.main")
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
