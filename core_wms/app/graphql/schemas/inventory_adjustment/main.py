import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.inventory_adjustment.main import InventoryAdjustmentService
from core_wms.app.services.inventory_adjustment.dto import InventoryAdjustment, InventoryAdjustmentFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.inventory_level.main import InventoryLevel

@strawberry.type
class InventoryAdjustment:
    id: int | None = None
    inventory_level_id: int | None = None
    quantity_adjusted: int | None = None
    state: str | None = None
    reason: str | None = None
    reference_document_uri: str | None = None
    app_id: int | None = None
    user_id: int | None = None
    note: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def inventory_level(self, info, parent: strawberry.Parent["InventoryAdjustment"]) -> Annotated["InventoryLevel", strawberry.lazy("core_wms.app.graphql.schemas.inventory_level.main")] | None:
        return await info.context.loaders.inventory_adjustment.inventory_level.load(parent.inventory_level_id)


@strawberry.type
class InventoryAdjustmentQueries:
    @strawberry.field
    @staticmethod
    async def inventory_adjustments(info, inventory_level_id: int | None = None) -> List["InventoryAdjustment"]:
        return await InventoryAdjustmentService(info.context.session).get_inventory_adjustments(
            InventoryAdjustmentFilter(inventory_level_id=inventory_level_id)
        )

    @strawberry.field
    @staticmethod
    async def inventory_adjustment(info, id: int) -> "InventoryAdjustment" | None:
        return await InventoryAdjustmentService(info.context.session).get_inventory_adjustment(
            InventoryAdjustmentFilter(id=id)
        )


@strawberry.type
class InventoryAdjustmentMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_inventory_adjustment(
        info,
        inventory_level_id: int,
        quantity_adjusted: int,
        id: int | None = None,
        state: str | None = None,
        reason: str | None = None,
        reference_document_uri: str | None = None,
        app_id: int | None = None,
        user_id: int | None = None,
        note: str | None = None,
    ) -> "InventoryAdjustment":
        return await InventoryAdjustmentService(info.context.session).upsert_inventory_adjustment(
            InventoryAdjustment(
                id=id,
                inventory_level_id=inventory_level_id,
                quantity_adjusted=quantity_adjusted,
                state=state,
                reason=reason,
                reference_document_uri=reference_document_uri,
                app_id=app_id,
                user_id=user_id,
                note=note,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_inventory_adjustment(info, id: int) -> bool:
        return await InventoryAdjustmentService(info.context.session).delete_inventory_adjustment(
            InventoryAdjustment(id=id)
        )

@strawberry.type
class InventoryAdjustmentSubscriptions:
    @strawberry.subscription
    async def inventory_adjustment_created(self, info) -> AsyncGenerator[InventoryAdjustment, None]:
        yield

    @strawberry.subscription
    async def inventory_adjustment_updated(self, info) -> AsyncGenerator[InventoryAdjustment, None]:
        yield

    @strawberry.subscription
    async def inventory_adjustment_deleted(self, info) -> AsyncGenerator[int, None]:
        yield