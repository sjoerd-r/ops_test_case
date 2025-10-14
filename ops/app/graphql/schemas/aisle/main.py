import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator

from ops.app.services.aisle.main import AisleService
from ops.app.services.aisle.dto import AisleInput, AisleFilter

if TYPE_CHECKING:
    from ops.app.graphql.schemas.zone.main import Zone
    from ops.app.graphql.schemas.rack.main import Rack

ZoneType: TypeAlias = Annotated[
    "Zone", strawberry.lazy("ops.app.graphql.schemas.zone.main")
]
RackType: TypeAlias = Annotated[
    "Rack", strawberry.lazy("ops.app.graphql.schemas.rack.main")
]
AisleType: TypeAlias = Annotated[
    "Aisle", strawberry.lazy("ops.app.graphql.schemas.aisle.main")
]

@strawberry.federation.type(keys=["id"])
class Aisle:
    id: strawberry.ID
    zone_id: int | None = None
    name: str | None = None
    description: str | None = None
    type: str | None = None
    active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def racks(
        self, info, parent: strawberry.Parent["Aisle"]
    ) -> RackType | None:
        if not parent.id:
            return None
        return await info.context.loaders.aisle.racks.load(parent.id)

    @strawberry.field
    async def zone(
        self, info, parent: strawberry.Parent["Aisle"]
    ) -> ZoneType | None:
        if not parent.zone_id:
            return None
        return await info.context.loaders.aisle.zone.load(parent.zone_id)


@strawberry.type
class AisleQueries:
    @strawberry.field
    @staticmethod
    async def aisles(info) -> list["Aisle"]:
        return await AisleService(info.context.session).get_aisles()

    @strawberry.field
    @staticmethod
    async def aisle(info, id: int) -> Optional["Aisle"]:
        return await AisleService(info.context.session).get_aisle(
            AisleFilter(id=id)
        )


@strawberry.type
class AisleMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_aisle(
        info,
        zone_id: int,
        name: str | None = None,
        description: str | None = None,
        type: str | None = "standard",
        active: bool | None = True,
    ) -> "Aisle":
        return await AisleService(info.context.session).upsert_aisle(
            AisleInput(
                zone_id=zone_id,
                name=name,
                description=description,
                type=type,
                active=active,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_aisle(info, id: int) -> bool:
        return await AisleService(info.context.session).delete_aisle(
            AisleInput(id=id)
        )


@strawberry.type
class AisleSubscriptions:
    @strawberry.subscription
    async def aisle_created(self, info) -> AsyncGenerator[AisleType, None]:
        yield

    @strawberry.subscription
    async def aisle_updated(self, info) -> AsyncGenerator[AisleType, None]:
        yield

    @strawberry.subscription
    async def aisle_deleted(self, info) -> AsyncGenerator[int, None]:
        yield
