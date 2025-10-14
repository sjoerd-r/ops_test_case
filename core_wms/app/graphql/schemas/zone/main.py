import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import TYPE_CHECKING, AsyncGenerator, List, Annotated
from datetime import datetime

from core_wms.app.services.zone.main import ZoneService
from core_wms.app.services.zone.dto import Zone, ZoneFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.aisle.main import Aisle
    from core_wms.app.graphql.schemas.warehouse.main import Warehouse

@strawberry.type
class Zone:
    id: int | None = None
    warehouse_id: int | None = None
    name: str | None = None
    description: str | None = None
    floor: int | None = None
    type: str | None = None
    active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def aisles(self, info, parent: strawberry.Parent["Zone"]) -> Annotated["Aisle", strawberry.lazy("core_wms.app.graphql.schemas.aisle.main")] | None:
        return await info.context.loaders.zone.aisles.load(parent.id)

    @strawberry.field
    async def warehouse(self, info, parent: strawberry.Parent["Zone"]) -> Annotated["Warehouse", strawberry.lazy("core_wms.app.graphql.schemas.warehouse.main")] | None:
        return await info.context.loaders.zone.warehouse.load(parent.warehouse_id)


@strawberry.type
class ZoneQueries:
    @strawberry.field
    @staticmethod
    async def zones(info, id: int | None = None, warehouse_id: int | None = None) -> List["Zone"]:
        return await ZoneService(info.context.session).get_zones(
            ZoneFilter(id=id, warehouse_id=warehouse_id)
        )

    @strawberry.field
    @staticmethod
    async def zone(info, id: int) -> "Zone" | None:
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
            Zone(
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
            Zone(id=id)
        )

@strawberry.type
class ZoneSubscriptions:
    @strawberry.subscription
    async def zone_created(self, info) -> AsyncGenerator["Zone", None]:
        yield

    @strawberry.subscription
    async def zone_updated(self, info) -> AsyncGenerator["Zone", None]:
        yield

    @strawberry.subscription
    async def zone_deleted(self, info) -> AsyncGenerator[int, None]:
        yield