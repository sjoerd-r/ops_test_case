import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.aisle.main import AisleService
from core_wms.app.services.aisle.dto import Aisle, AisleFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.zone.main import Zone
    from core_wms.app.graphql.schemas.rack.main import Rack

@strawberry.type
class Aisle:
    id: int | None = None
    zone_id: int | None = None
    name: str | None = None
    description: str | None = None
    type: str | None = None
    active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def racks(self, info, parent: strawberry.Parent["Aisle"]) -> Annotated["Rack", strawberry.lazy("core_wms.app.graphql.schemas.rack.main")] | None:
        return await info.context.loaders.aisle.racks.load(parent.id)

    @strawberry.field
    async def zone(self, info, parent: strawberry.Parent["Aisle"]) -> Annotated["Zone", strawberry.lazy("core_wms.app.graphql.schemas.zone.main")] | None:
        return await info.context.loaders.aisle.zone.load(parent.zone_id)

@strawberry.type
class AisleQueries:
    @strawberry.field
    @staticmethod
    async def aisles(info, id: int | None = None, zone_id: int | None = None) -> List["Aisle"]:
        return await AisleService(info.context.session).get_aisles(
            AisleFilter(id=id, zone_id=zone_id)
        )

    @strawberry.field
    @staticmethod
    async def aisle(info, id: int) -> "Aisle" | None:
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
            Aisle(
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
            Aisle(id=id)
        )

@strawberry.type
class AisleSubscriptions:
    @strawberry.subscription
    async def aisle_created(self, info) -> AsyncGenerator[Aisle, None]:
        yield

    @strawberry.subscription
    async def aisle_updated(self, info) -> AsyncGenerator[Aisle, None]:
        yield

    @strawberry.subscription
    async def aisle_deleted(self, info) -> AsyncGenerator[int, None]:
        yield