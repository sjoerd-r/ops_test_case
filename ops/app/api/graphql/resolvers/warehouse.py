import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator

from ops.app.services.warehouse.main import WarehouseService
from ops.app.services.warehouse.dto import WarehouseInput, WarehouseFilter
from ops.app.api.graphql.types.warehouse import Warehouse

WarehouseType: TypeAlias = Annotated[
    "Warehouse", strawberry.lazy("ops.app.api.graphql.types.warehouse")
]


@strawberry.type
class WarehouseQueries:
    @strawberry.field
    @staticmethod
    async def warehouses(info) -> list["Warehouse"]:
        return await WarehouseService(info.context.session).get_warehouses()

    @strawberry.field
    @staticmethod
    async def warehouse(info, id: int) -> Optional["Warehouse"]:
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
            WarehouseInput(
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
            WarehouseInput(id=id)
        )


@strawberry.type
class WarehouseSubscriptions:
    @strawberry.subscription
    async def warehouse_created(
        self, info
    ) -> AsyncGenerator[WarehouseType, None]:
        yield

    @strawberry.subscription
    async def warehouse_updated(
        self, info
    ) -> AsyncGenerator[WarehouseType, None]:
        yield

    @strawberry.subscription
    async def warehouse_deleted(self, info) -> AsyncGenerator[int, None]:
        yield
