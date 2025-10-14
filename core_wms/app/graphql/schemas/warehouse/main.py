import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import TYPE_CHECKING, AsyncGenerator, List, Annotated
from datetime import datetime

from core_wms.app.graphql.schemas.batch.main import Batch
from core_wms.app.graphql.schemas.purchase_order.main import PurchaseOrder
from core_wms.app.graphql.schemas.location.main import Location
from core_wms.app.graphql.schemas.fulfillment_service.main import FulfillmentService
from core_wms.app.services.warehouse.main import WarehouseService

from core_wms.app.services.warehouse.dto import Warehouse, WarehouseFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.zone.main import Zone

@strawberry.type
class Warehouse:
    id: int | None = None
    name: str | None = None
    description: str | None = None
    location_id: int | None = None
    fulfillment_service_id: int | None = None
    active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def zones(self, info, parent: strawberry.Parent["Warehouse"]) -> Annotated["Zone", strawberry.lazy("core_wms.app.graphql.schemas.zone.main")] | None:
        return await info.context.loaders.warehouse.zones.load(parent.id)

    @strawberry.field
    async def batches(self, info, parent: strawberry.Parent["Warehouse"]) -> Annotated["Batch", strawberry.lazy("core_wms.app.graphql.schemas.batch.main")] | None:
        return await info.context.loaders.warehouse.batches.load(parent.id)

    @strawberry.field
    async def purchase_orders(self, info, parent: strawberry.Parent["Warehouse"]) -> Annotated["PurchaseOrder", strawberry.lazy("core_wms.app.graphql.schemas.purchase_order.main")] | None:
        return await info.context.loaders.warehouse.purchase_orders.load(parent.id)

    @strawberry.field
    async def location(self, info, parent: strawberry.Parent["Warehouse"]) -> Annotated["Location", strawberry.lazy("core_wms.app.graphql.schemas.location.main")] | None:
        return await info.context.loaders.warehouse.location.load(parent.location_id)

    @strawberry.field
    async def fulfillment_service(self, info, parent: strawberry.Parent["Warehouse"]) -> Annotated["FulfillmentService", strawberry.lazy("core_wms.app.graphql.schemas.fulfillment_service.main")] | None:
        return await info.context.loaders.warehouse.fulfillment_service.load(parent.fulfillment_service_id)


@strawberry.type
class WarehouseQueries:
    @strawberry.field
    @staticmethod
    async def warehouses(info, id: int | None = None, active: bool | None = None) -> List["Warehouse"]:
        return await WarehouseService(info.context.session).get_warehouses(
            WarehouseFilter(id=id, active=active)
        )

    @strawberry.field
    @staticmethod
    async def warehouse(info, id: int) -> "Warehouse" | None:
        return await WarehouseService(info.context.session).get_warehouse(
            WarehouseFilter(id=id)
        )

@strawberry.type
class WarehouseMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_warehouse(
        info,
        name: str,
        description: str | None = None,
        location_id: int | None = None,
        fulfillment_service_id: int | None = None,
        active: bool | None = True,
        id: int | None = None,
    ) -> "Warehouse":
        return await WarehouseService(info.context.session).upsert_warehouse(
            Warehouse(
                name=name,
                description=description,
                location_id=location_id,
                fulfillment_service_id=fulfillment_service_id,
                active=active,
                id=id,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_warehouse(info, id: int) -> bool:
        return await WarehouseService(info.context.session).delete_warehouse(
            Warehouse(id=id)
        )

@strawberry.type
class WarehouseSubscriptions:
    @strawberry.subscription
    async def warehouse_created(self, info) -> AsyncGenerator["Warehouse", None]:
        yield

    @strawberry.subscription
    async def warehouse_updated(self, info) -> AsyncGenerator["Warehouse", None]:
        yield

    @strawberry.subscription
    async def warehouse_deleted(self, info) -> AsyncGenerator[int, None]:
        yield