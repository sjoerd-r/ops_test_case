import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator

from ops.app.services.rack.main import RackService
from ops.app.services.rack.dto import RackInput, RackFilter
from ops.app.api.graphql.types.rack import Rack

RackType: TypeAlias = Annotated[
    "Rack", strawberry.lazy("ops.app.api.graphql.types.rack")
]


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
