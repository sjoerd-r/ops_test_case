import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import TYPE_CHECKING, Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator
from datetime import datetime

from ops.app.services.rack.main import RackService
from ops.app.services.rack.dto import RackInput, RackFilter

if TYPE_CHECKING:
    from ops.app.graphql.schemas.aisle.main import Aisle

from ops.app.graphql.schemas.bin.main import Bin

AisleType: TypeAlias = Annotated[
    "Aisle", strawberry.lazy("ops.app.graphql.schemas.aisle.main")
]
RackType: TypeAlias = Annotated[
    "Rack", strawberry.lazy("ops.app.graphql.schemas.rack.main")
]


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


@strawberry.type
class RackQueries:
    @strawberry.field
    @staticmethod
    async def racks(info) -> list["Rack"]:
        return await RackService(info.context.session).get_racks()

    @strawberry.field
    @staticmethod
    async def rack(info, id: int) -> Optional["Rack"]:
        return await RackService(info.context.session).get_rack(
            RackFilter(id=id)
        )


@strawberry.type
class RackMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_rack(
        info,
        aisle_id: int,
        position: int,
        description: str | None = None,
        type: str | None = "pallet",
        active: bool | None = True,
    ) -> "Rack":
        return await RackService(info.context.session).upsert_rack(
            RackInput(
                aisle_id=aisle_id,
                position=position,
                description=description,
                type=type,
                active=active,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_rack(info, id: int) -> bool:
        return await RackService(info.context.session).delete_rack(
            RackInput(id=id)
        )


@strawberry.type
class RackSubscriptions:
    @strawberry.subscription
    async def rack_created(self, info) -> AsyncGenerator[RackType, None]:
        yield

    @strawberry.subscription
    async def rack_updated(self, info) -> AsyncGenerator[RackType, None]:
        yield

    @strawberry.subscription
    async def rack_deleted(self, info) -> AsyncGenerator[int, None]:
        yield
