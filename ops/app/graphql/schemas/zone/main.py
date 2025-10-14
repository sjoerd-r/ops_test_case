import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import TYPE_CHECKING, Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator
from datetime import datetime

from ops.app.services.zone.main import ZoneService
from ops.app.services.zone.dto import ZoneInput, ZoneFilter

if TYPE_CHECKING:
    from ops.app.graphql.schemas.aisle.main import Aisle
    from ops.app.graphql.schemas.warehouse.main import Warehouse

AisleType: TypeAlias = Annotated[
    "Aisle", strawberry.lazy("ops.app.graphql.schemas.aisle.main")
]
WarehouseType: TypeAlias = Annotated[
    "Warehouse", strawberry.lazy("ops.app.graphql.schemas.warehouse.main")
]
ZoneType: TypeAlias = Annotated[
    "Zone", strawberry.lazy("ops.app.graphql.schemas.zone.main")
]


@strawberry.federation.type(keys=["id"])
class Zone:
    id: strawberry.ID
    warehouse_id: int | None = None
    name: str | None = None
    description: str | None = None
    floor: int | None = None
    type: str | None = None
    active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def aisles(
        self, info, parent: strawberry.Parent["Zone"]
    ) -> AisleType | None:
        if not parent.id:
            return None
        return await info.context.loaders.zone.aisles.load(parent.id)

    @strawberry.field
    async def warehouse(
        self, info, parent: strawberry.Parent["Zone"]
    ) -> WarehouseType | None:
        if not parent.warehouse_id:
            return None
        return await info.context.loaders.zone.warehouse.load(
            parent.warehouse_id
        )


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
