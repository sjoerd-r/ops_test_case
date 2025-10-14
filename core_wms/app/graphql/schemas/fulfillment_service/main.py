import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.fulfillment_service.main import FulfillmentServiceService
from core_wms.app.services.fulfillment_service.dto import FulfillmentService, FulfillmentServiceFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.order.main import Order
    from core_wms.app.graphql.schemas.store.main import Store
    from core_wms.app.graphql.schemas.location.main import Location

@strawberry.type
class FulfillmentService:
    id: int | None = None
    store_id: int | None = None
    shopify_fulfillment_service_id: int | None = None
    name: str | None = None
    handle: str | None = None
    callback_url: str | None = None
    active: bool | None = None
    tracking_support: bool | None = None
    permits_sku_sharing: bool | None = None
    requires_shipping_method: bool | None = None
    fulfillment_orders_opt_in: bool | None = None
    include_pending_stock: bool | None = None
    inventory_management: bool | None = None
    email: str | None = None
    location_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def store(self, info, parent: strawberry.Parent["FulfillmentService"]) -> Annotated["Store", strawberry.lazy("core_wms.app.graphql.schemas.store.main")] | None:
        return await info.context.loaders.fulfillment_service.store.load(parent.store_id)

    @strawberry.field
    async def location(self, info, parent: strawberry.Parent["FulfillmentService"]) -> Annotated["Location", strawberry.lazy("core_wms.app.graphql.schemas.location.main")] | None:
        return await info.context.loaders.fulfillment_service.location.load(parent.location_id)

    @strawberry.field
    async def order(self, info, parent: strawberry.Parent["FulfillmentService"]) -> Annotated["Order", strawberry.lazy("core_wms.app.graphql.schemas.order.main")] | None:
        return await info.context.loaders.fulfillment_service.order.load(getattr(parent, "order_id", None))

@strawberry.type
class FulfillmentServiceQueries:
    @strawberry.field
    @staticmethod
    async def fulfillment_services(info, shop_id: int) -> List["FulfillmentService"]:
        return await FulfillmentServiceService(info.context.session).get_fulfillment_services(
            FulfillmentServiceFilter(shop_id=shop_id)
        )

    @strawberry.field
    @staticmethod
    async def fulfillment_service(info, id: int) -> "FulfillmentService" | None:
        return await FulfillmentServiceService(info.context.session).get_fulfillment_service(
            FulfillmentServiceFilter(id=id)
        )

@strawberry.type
class FulfillmentServiceMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_fulfillment_service(
        info,
        store_id: int,
        name: str,
        handle: str,
        id: int | None = None,
        shopify_fulfillment_service_id: int | None = None,
        callback_url: str | None = None,
        active: bool | None = True,
        tracking_support: bool | None = True,
        permits_sku_sharing: bool | None = True,
        requires_shipping_method: bool | None = True,
        fulfillment_orders_opt_in: bool | None = True,
        include_pending_stock: bool | None = False,
        inventory_management: bool | None = False,
        email: str | None = None,
        location_id: int | None = None,
    ) -> "FulfillmentService":
        return await FulfillmentServiceService(info.context.session).upsert_fulfillment_service(
            FulfillmentService(
                id=id,
                store_id=store_id,
                shopify_fulfillment_service_id=shopify_fulfillment_service_id,
                name=name,
                handle=handle,
                callback_url=callback_url,
                active=active,
                tracking_support=tracking_support,
                permits_sku_sharing=permits_sku_sharing,
                requires_shipping_method=requires_shipping_method,
                fulfillment_orders_opt_in=fulfillment_orders_opt_in,
                include_pending_stock=include_pending_stock,
                inventory_management=inventory_management,
                email=email,
                location_id=location_id,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_fulfillment_service(info, id: int) -> bool:
        return await FulfillmentServiceService(info.context.session).delete_fulfillment_service(
            FulfillmentService(id=id)
        )

@strawberry.type
class FulfillmentServiceSubscriptions:
    @strawberry.subscription
    async def fulfillment_service_created(self, info) -> AsyncGenerator[FulfillmentService, None]:
        yield

    @strawberry.subscription
    async def fulfillment_service_updated(self, info) -> AsyncGenerator[FulfillmentService, None]:
        yield

    @strawberry.subscription
    async def fulfillment_service_deleted(self, info) -> AsyncGenerator[int, None]:
        yield