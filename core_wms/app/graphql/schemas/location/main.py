import strawberry
from strawberry.field_extensions import InputMutationExtension
from strawberry.scalars import JSON
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.location.main import LocationService
from core_wms.app.services.location.dto import Location, LocationFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.warehouse.main import Warehouse
    from core_wms.app.graphql.schemas.store.main import Store

@strawberry.type
class Location:
    id: int | None = None
    store_id: int | None = None
    shopify_location_id: int | None = None
    name: str | None = None
    address: JSON | None = None # type: ignore[misc]
    address_verified: bool | None = None
    suggested_addresses: JSON | None = None # type: ignore[misc]
    company: str | None = None
    handle: str | None = None
    platform: str | None = None
    fulfills_online_orders: bool | None = None
    has_active_inventory: bool | None = None
    is_active: bool | None = None
    is_fulfillment_service: bool | None = None
    ships_inventory: bool | None = None
    deactivatable: bool | None = None
    activatable: bool | None = None
    deletable: bool | None = None
    deactivated_at: datetime | None = None
    fulfillment_service_id: int | None = None
    metafields: JSON | None = None # type: ignore[misc]
    legacy_resource_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def warehouses(self, info, parent: strawberry.Parent["Location"]) -> List[Annotated["Warehouse", strawberry.lazy("core_wms.app.graphql.schemas.warehouse.main")]] | None:
        return await info.context.loaders.location.warehouses.load(parent.id)

    @strawberry.field
    async def store(self, info, parent: strawberry.Parent["Location"]) -> Annotated["Store", strawberry.lazy("core_wms.app.graphql.schemas.store.main")] | None:
        return await info.context.loaders.location.store.load(parent.store_id)

@strawberry.type
class LocationQueries:
    @strawberry.field
    @staticmethod
    async def locations(info, store_id: int | None = None, shopify_location_id: int | None = None) -> List["Location"]:
        return await LocationService(info.context.session).get_all(
            LocationFilter(store_id=store_id, shopify_location_id=shopify_location_id)
        )

    @strawberry.field
    @staticmethod
    async def location(info, id: int) -> "Location" | None:
        return await LocationService(info.context.session).get(
            LocationFilter(id=id)
        )

@strawberry.type
class LocationMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_location(
        info,
        store_id: int,
        shopify_location_id: int,
        id: int | None = None,
        name: str | None = None,
        address: JSON | None = None, # type: ignore[misc]
        address_verified: bool | None = None,
        suggested_addresses: JSON | None = None, # type: ignore[misc]
        company: str | None = None,
        handle: str | None = None,
        platform: str | None = None,
        fulfills_online_orders: bool | None = None,
        has_active_inventory: bool | None = None,
        is_active: bool | None = None,
        is_fulfillment_service: bool | None = None,
        ships_inventory: bool | None = None,
        deactivatable: bool | None = None,
        activatable: bool | None = None,
        deletable: bool | None = None,
    ) -> "Location":
        return await LocationService(info.context.session).upsert(
            Location(
                id=id,
                store_id=store_id,
                shopify_location_id=shopify_location_id,
                name=name,
                address=address,
                address_verified=address_verified,
                suggested_addresses=suggested_addresses,
                company=company,
                handle=handle,
                platform=platform,
                fulfills_online_orders=fulfills_online_orders,
                has_active_inventory=has_active_inventory,
                is_active=is_active,
                is_fulfillment_service=is_fulfillment_service,
                ships_inventory=ships_inventory,
                deactivatable=deactivatable,
                activatable=activatable,
                deletable=deletable,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_location(info, id: int) -> bool:
        return await LocationService(info.context.session).delete(
            Location(id=id)
        )

@strawberry.type
class LocationSubscriptions:
    @strawberry.subscription
    async def location_created(self, info) -> AsyncGenerator[Location, None]:
        yield

    @strawberry.subscription
    async def location_updated(self, info) -> AsyncGenerator[Location, None]:
        yield

    @strawberry.subscription
    async def location_deleted(self, info) -> AsyncGenerator[int, None]:
        yield