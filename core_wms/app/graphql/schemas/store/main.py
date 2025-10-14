import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.store.main import StoreService
from core_wms.app.services.store.dto import Store, StoreFilter

from core_wms.app.graphql.schemas.carrier.main import Carrier
from core_wms.app.graphql.schemas.channel.main import Channel
from core_wms.app.graphql.schemas.location.main import Location
from core_wms.app.graphql.schemas.shipping_zone.main import ShippingZone
from core_wms.app.graphql.schemas.fulfillment_service.main import FulfillmentService

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.order.main import Order
    from core_wms.app.graphql.schemas.customer.main import Customer
    from core_wms.app.graphql.schemas.product.main import Product

@strawberry.type
class Store:
    id: int | None = None
    shopify_store_id: int | None = None
    access_token: str | None = None
    name: str | None = None
    domain: str | None = None
    country: str | None = None
    currency: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def orders(self, info, parent: strawberry.Parent["Store"]) -> List[Annotated["Order", strawberry.lazy("core_wms.app.graphql.schemas.order.main")]]:
        return await info.context.loaders.store.orders.load(parent.id)
    
    @strawberry.field
    async def customers(self, info, parent: strawberry.Parent["Store"]) -> List[Annotated["Customer", strawberry.lazy("core_wms.app.graphql.schemas.customer.main")]]:
        return await info.context.loaders.store.customers.load(parent.id)
    
    @strawberry.field
    async def products(self, info, parent: strawberry.Parent["Store"]) -> List[Annotated["Product", strawberry.lazy("core_wms.app.graphql.schemas.product.main")]]:
        return await info.context.loaders.store.products.load(parent.id)

    @strawberry.field
    async def carriers(self, info, parent: strawberry.Parent["Store"]) -> List[Carrier]:
        return await info.context.loaders.store.carriers.load(parent.id)

    @strawberry.field
    async def channels(self, info, parent: strawberry.Parent["Store"]) -> List[Channel]:
        return await info.context.loaders.store.channels.load(parent.id)

    @strawberry.field
    async def locations(self, info, parent: strawberry.Parent["Store"]) -> List[Location]:
        return await info.context.loaders.store.locations.load(parent.id)

    @strawberry.field
    async def shipping_zones(self, info, parent: strawberry.Parent["Store"]) -> List[ShippingZone]:
        return await info.context.loaders.store.shipping_zones.load(parent.id)

    @strawberry.field
    async def fulfillment_services(self, info, parent: strawberry.Parent["Store"]) -> List[FulfillmentService]:
        return await info.context.loaders.store.fulfillment_services.load(parent.id)

@strawberry.type
class StoreQueries:
    @strawberry.field
    @staticmethod
    async def stores(info, shopify_store_id: int | None = None) -> List["Store"]:
        return await StoreService(info.context.session).get_stores(
            StoreFilter(shopify_store_id=shopify_store_id)
        )

    @strawberry.field
    @staticmethod
    async def store(info, id: int) -> "Store" | None:
        return await StoreService(info.context.session).get_store(
            StoreFilter(id=id)
        )

@strawberry.type
class StoreMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_store(
        info,
        id: int | None = None,
        shopify_store_id: int | None = None,
        access_token: str | None = None,
        name: str | None = None,
        domain: str | None = None,
        country: str | None = None,
        currency: str | None = None,
    ) -> "Store":
        return await StoreService(info.context.session).upsert_store(
            Store(
                id=id,
                shopify_store_id=shopify_store_id,
                access_token=access_token,
                name=name,
                domain=domain,
                country=country,
                currency=currency,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_store(info, id: int) -> bool:
        return await StoreService(info.context.session).delete_store(
            Store(id=id)
        )

@strawberry.type
class StoreSubscriptions:
    @strawberry.subscription
    async def store_created(self, info) -> AsyncGenerator[Store, None]:
        yield

    @strawberry.subscription
    async def store_updated(self, info) -> AsyncGenerator[Store, None]:
        yield

    @strawberry.subscription
    async def store_deleted(self, info) -> AsyncGenerator[int, None]:
        yield