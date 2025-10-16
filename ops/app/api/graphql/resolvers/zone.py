import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator

from ops.app.services.zone.main import ZoneService
from ops.app.services.zone.dto import ZoneInput, ZoneFilter
from ops.app.api.graphql.types.zone import Zone

ZoneType: TypeAlias = Annotated[
    "Zone", strawberry.lazy("ops.app.api.graphql.types.zone")
]


@strawberry.type
class ZoneQueries:
    @strawberry.field
    @staticmethod
    async def zones(info) -> list["Zone"]:
        return await ZoneService(info.context.session).get_zones()

    @strawberry.field
    @staticmethod
    async def zone(info, id: int) -> Optional["Zone"]:
        return await ZoneService(info.context.session).get_zone(
            ZoneFilter(id=id)
        )


@strawberry.type
class ZoneMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_zone(
        info,
        warehouse_id: int,
        name: str,
        description: str | None = None,
        floor: int | None = 1,
        type: str | None = "storage",
        active: bool | None = True,
        id: int | None = None,
    ) -> "Zone":
        return await ZoneService(info.context.session).upsert_zone(
            ZoneInput(
                warehouse_id=warehouse_id,
                name=name,
                description=description,
                floor=floor,
                type=type,
                active=active,
                id=id,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_zone(info, id: int) -> bool:
        return await ZoneService(info.context.session).delete_zone(
            ZoneInput(id=id)
        )


@strawberry.type
class ZoneSubscriptions:
    @strawberry.subscription
    async def zone_created(self, info) -> AsyncGenerator[ZoneType, None]:
        yield

    @strawberry.subscription
    async def zone_updated(self, info) -> AsyncGenerator[ZoneType, None]:
        yield

    @strawberry.subscription
    async def zone_deleted(self, info) -> AsyncGenerator[int, None]:
        yield
