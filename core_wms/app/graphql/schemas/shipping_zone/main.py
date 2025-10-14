import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.shipping_zone.main import ShippingZoneService
from core_wms.app.services.shipping_zone.dto import ShippingZone, ShippingZoneFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.store.main import Store

@strawberry.type
class ShippingZone:
    id: int | None = None
    store_id: int | None = None
    shopify_zone_id: int | None = None
    name: str | None = None
    countries: List[str] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def store(self, info, parent: strawberry.Parent["ShippingZone"]) -> Annotated["Store", strawberry.lazy("core_wms.app.graphql.schemas.store.main")] | None:
        return await info.context.loaders.shipping_zone.store.load(parent.store_id)

@strawberry.type
class ShippingZoneQueries:
    @strawberry.field
    @staticmethod
    async def shipping_zones(info, store_id: int | None = None, shopify_zone_id: int | None = None) -> List["ShippingZone"]:
        return await ShippingZoneService(info.context.session).get_shipping_zones(
            ShippingZoneFilter(store_id=store_id, shopify_zone_id=shopify_zone_id)
        )

    @strawberry.field
    @staticmethod
    async def shipping_zone(info, id: int) -> "ShippingZone" | None:
        return await ShippingZoneService(info.context.session).get_shipping_zone(
            ShippingZoneFilter(id=id)
        )

@strawberry.type
class ShippingZoneMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_shipping_zone(
        info,
        store_id: int,
        name: str,
        shopify_zone_id: int | None = None,
        countries: List[str] | None = None,
    ) -> "ShippingZone":
        return await ShippingZoneService(info.context.session).upsert_shipping_zone(
            ShippingZone(
                store_id=store_id,
                name=name,
                shopify_zone_id=shopify_zone_id,
                countries=countries,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_shipping_zone(info, id: int) -> bool:
        return await ShippingZoneService(info.context.session).delete_shipping_zone(
            ShippingZone(id=id)
        )

@strawberry.type
class ShippingZoneSubscriptions:
    @strawberry.subscription
    async def shipping_zone_created(self, info) -> AsyncGenerator[ShippingZone, None]:
        yield

    @strawberry.subscription
    async def shipping_zone_updated(self, info) -> AsyncGenerator[ShippingZone, None]:
        yield

    @strawberry.subscription
    async def shipping_zone_deleted(self, info) -> AsyncGenerator[int, None]:
        yield