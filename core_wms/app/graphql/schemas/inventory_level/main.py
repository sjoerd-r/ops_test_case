import strawberry
from strawberry.field_extensions import InputMutationExtension
from strawberry.scalars import JSON
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.inventory_level.main import InventoryLevelService
from core_wms.app.services.inventory_level.dto import InventoryLevel, InventoryLevelFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.inventory_item.main import InventoryItem
    from core_wms.app.graphql.schemas.location.main import Location

@strawberry.type
class InventoryLevel:
    id: int | None = None
    inventory_item_id: int | None = None
    location_id: int | None = None
    shopify_inventory_level_id: int | None = None
    shopify_inventory_item_id: int | None = None
    shopify_location_id: int | None = None
    can_deactivate: bool | None = None
    deactivation_alert: str | None = None
    quantities: JSON | None = None # type: ignore[misc]
    scheduled_changes: JSON | None = None # type: ignore[misc]
    legacy_resource_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def inventory_item(self, info, parent: strawberry.Parent["InventoryLevel"]) -> Annotated["InventoryItem", strawberry.lazy("core_wms.app.graphql.schemas.inventory_item.main")] | None:
        return await info.context.loaders.inventory_level.inventory_item.load(parent.inventory_item_id)

    @strawberry.field
    async def location(self, info, parent: strawberry.Parent["InventoryLevel"]) -> Annotated["Location", strawberry.lazy("core_wms.app.graphql.schemas.location.main")] | None:
        return await info.context.loaders.inventory_level.location.load(parent.location_id)

@strawberry.type
class InventoryLevelQueries:
    @strawberry.field
    @staticmethod
    async def inventory_levels(info, shopify_inventory_level_id: int | None = None) -> List["InventoryLevel"]:
        return await InventoryLevelService(info.context.session).get_inventory_levels(
            InventoryLevelFilter(shopify_inventory_level_id=shopify_inventory_level_id)
        )

    @strawberry.field
    @staticmethod
    async def inventory_level(info, id: int) -> "InventoryLevel" | None:
        return await InventoryLevelService(info.context.session).get_inventory_level(
            InventoryLevelFilter(id=id)
        )

@strawberry.type
class InventoryLevelMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_inventory_level(
        info,
        inventory_item_id: int,
        location_id: int,
        id: int | None = None,
        shopify_inventory_level_id: int | None = None,
        shopify_inventory_item_id: int | None = None,
        shopify_location_id: int | None = None,
        can_deactivate: bool | None = None,
        deactivation_alert: str | None = None,
        quantities: JSON | None = None, # type: ignore[misc]
        scheduled_changes: JSON | None = None, # type: ignore[misc]
        legacy_resource_id: str | None = None,
    ) -> "InventoryLevel":
        return await InventoryLevelService(info.context.session).upsert_inventory_level(
            InventoryLevel(
                id=id,
                inventory_item_id=inventory_item_id,
                location_id=location_id,
                shopify_inventory_level_id=shopify_inventory_level_id,
                shopify_inventory_item_id=shopify_inventory_item_id,
                shopify_location_id=shopify_location_id,
                can_deactivate=can_deactivate,
                deactivation_alert=deactivation_alert,
                quantities=quantities,
                scheduled_changes=scheduled_changes,
                legacy_resource_id=legacy_resource_id,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_inventory_level(info, id: int) -> bool:
        return await InventoryLevelService(info.context.session).delete_inventory_level(
            InventoryLevel(id=id)
        )

@strawberry.type
class InventoryLevelSubscriptions:
    @strawberry.subscription
    async def inventory_level_created(self, info) -> AsyncGenerator[InventoryLevel, None]:
        yield

    @strawberry.subscription
    async def inventory_level_updated(self, info) -> AsyncGenerator[InventoryLevel, None]:
        yield

    @strawberry.subscription
    async def inventory_level_deleted(self, info) -> AsyncGenerator[int, None]:
        yield