import strawberry
from strawberry.field_extensions import InputMutationExtension
from strawberry.scalars import JSON
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.inventory_item.main import InventoryItemService
from core_wms.app.services.inventory_item.dto import InventoryItem, InventoryItemFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.product.variant import ProductVariant
    from core_wms.app.graphql.schemas.inventory_level.main import InventoryLevel

@strawberry.type
class InventoryItem:
    id: int | None = None
    variant_id: int | None = None
    shopify_inventory_item_id: int | None = None
    sku: str | None = None
    tracked: bool | None = None
    requires_shipping: bool | None = None
    unit_cost: float | None = None
    country_code_of_origin: str | None = None
    province_code_of_origin: str | None = None
    harmonized_system_code: str | None = None
    country_harmonized_system_codes: JSON | None = None # type: ignore[misc]
    measurement_weight: float | None = None
    measurement_unit: str | None = None
    measurement: JSON | None = None # type: ignore[misc]
    tracked_editable: JSON | None = None # type: ignore[misc]
    barcode: str | None = None
    multipack: bool | None = None
    case_upc: str | None = None
    legacy_resource_id: str | None = None
    duplicate_sku_count: int | None = None
    inventory_history_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def variant(self, info, parent: strawberry.Parent["InventoryItem"]) -> Annotated["ProductVariant", strawberry.lazy("core_wms.app.graphql.schemas.product.variant")] | None:
        return await info.context.loaders.inventory_item.variant.load(parent.variant_id)

    @strawberry.field
    async def inventory_levels(self, info, parent: strawberry.Parent["InventoryItem"]) -> List[Annotated["InventoryLevel", strawberry.lazy("core_wms.app.graphql.schemas.inventory_level.main")]] | None:
        return await info.context.loaders.inventory_item.inventory_levels.load(parent.id)

@strawberry.type
class InventoryItemQueries:
    @strawberry.field
    @staticmethod
    async def inventory_items(info, id: int | None = None, shopify_inventory_item_id: int | None = None, sku: str | None = None) -> List["InventoryItem"]:
        return await InventoryItemService(info.context.session).get_inventory_items(
            InventoryItemFilter(id=id, shopify_inventory_item_id=shopify_inventory_item_id, sku=sku)
        )

    @strawberry.field
    @staticmethod
    async def inventory_item(info, id: int) -> "InventoryItem" | None:
        return await InventoryItemService(info.context.session).get_inventory_item(
            InventoryItemFilter(id=id)
        )

@strawberry.type
class InventoryItemMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_inventory_item(
        info,
        variant_id: int,
        id: int | None = None,
        shopify_inventory_item_id: int | None = None,
        sku: str | None = None,
        tracked: bool | None = None,
        requires_shipping: bool | None = None,
        unit_cost: float | None = None,
        country_code_of_origin: str | None = None,
        province_code_of_origin: str | None = None,
        harmonized_system_code: str | None = None,
        country_harmonized_system_codes: JSON | None = None, # type: ignore[misc]
        measurement_weight: float | None = None,
        measurement_unit: str | None = None,
        measurement: JSON | None = None, # type: ignore[misc]
        tracked_editable: JSON | None = None, # type: ignore[misc]
        barcode: str | None = None,
        multipack: bool | None = None,
        case_upc: str | None = None,
        legacy_resource_id: str | None = None,
        duplicate_sku_count: int | None = None,
        inventory_history_url: str | None = None,
    ) -> "InventoryItem":
        return await InventoryItemService(info.context.session).upsert_inventory_item(
            InventoryItem(
                id=id,
                variant_id=variant_id,
                shopify_inventory_item_id=shopify_inventory_item_id,
                sku=sku,
                tracked=tracked,
                requires_shipping=requires_shipping,
                unit_cost=unit_cost,
                country_code_of_origin=country_code_of_origin,
                province_code_of_origin=province_code_of_origin,
                harmonized_system_code=harmonized_system_code,
                country_harmonized_system_codes=country_harmonized_system_codes,
                measurement_weight=measurement_weight,
                measurement_unit=measurement_unit,
                measurement=measurement,
                tracked_editable=tracked_editable,
                barcode=barcode,
                multipack=multipack,
                case_upc=case_upc,
                legacy_resource_id=legacy_resource_id,
                duplicate_sku_count=duplicate_sku_count,
                inventory_history_url=inventory_history_url,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_inventory_item(info, id: int) -> bool:
        return await InventoryItemService(info.context.session).delete_inventory_item(
            InventoryItem(id=id)
        )
@strawberry.type
class InventoryItemSubscriptions:
    @strawberry.subscription
    async def inventory_item_created(self, info) -> AsyncGenerator["InventoryItem", None]:
        yield

    @strawberry.subscription
    async def inventory_item_updated(self, info) -> AsyncGenerator["InventoryItem", None]:
        yield

    @strawberry.subscription
    async def inventory_item_deleted(self, info) -> AsyncGenerator[int, None]:
        yield