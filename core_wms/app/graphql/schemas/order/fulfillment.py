import strawberry
from strawberry.field_extensions import InputMutationExtension
from strawberry.scalars import JSON
from datetime import datetime
from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated

from core_wms.app.services.order.fulfillment import OrderFulfillmentService
from core_wms.app.services.order.dto import OrderFulfillment, OrderFulfillmentFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.order.main import Order

@strawberry.type
class OrderFulfillment:
    id: int | None = None
    order_id: int | None = None
    shopify_fulfillment_id: int | None = None
    shopify_order_id: int | None = None
    order_fulfillment_id: str | None = None
    origin: str | None = None
    status: str | None = None
    shipment_status: str | None = None
    tracking_company: str | None = None
    tracking_number: str | None = None
    tracking_url: str | None = None
    tracking_numbers: List[str] | None = None
    tracking_urls: List[str] | None = None
    shopify_location_id: int | None = None
    location_id: int | None = None
    warehouse_id: int | None = None
    service: str | None = None
    receipt: JSON | None = None  # type: ignore[misc]
    carrier_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def order(self, info, parent: strawberry.Parent["OrderFulfillment"]) -> Annotated["Order", strawberry.lazy("core_wms.app.graphql.schemas.order.main")] | None:
        return await info.context.loaders.order_fulfillment.order.load(parent.order_id)

@strawberry.type
class OrderFulfillmentQueries:
    @strawberry.field
    @staticmethod
    async def order_fulfillments(info, id: int | None = None, order_id: int | None = None) -> List["OrderFulfillment"]:
        return await OrderFulfillmentService(info.context.session).get_order_fulfillments(
            OrderFulfillmentFilter(id=id, order_id=order_id)
        )
    
    @strawberry.field
    @staticmethod
    async def order_fulfillment(info, id: int | None = None, order_id: int | None = None) -> "OrderFulfillment" | None:
        return await OrderFulfillmentService(info.context.session).get_order_fulfillment(
            OrderFulfillmentFilter(id=id, order_id=order_id)
        )
    
@strawberry.type
class OrderFulfillmentMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_order_fulfillment(
        info,
        order_id: int,
        id: int | None = None,
        shopify_fulfillment_id: int | None = None,
        shopify_order_id: int | None = None,
        order_fulfillment_id: str | None = None,
        origin: str | None = None,
        status: str | None = None,
        shipment_status: str | None = None,
        tracking_company: str | None = None,
        tracking_number: str | None = None,
        tracking_url: str | None = None,
        tracking_numbers: List[str] | None = None,
        tracking_urls: List[str] | None = None,
        shopify_location_id: int | None = None,
        location_id: int | None = None,
        warehouse_id: int | None = None,
        service: str | None = None,
        receipt: JSON | None = None,  # type: ignore[misc]
        carrier_id: int | None = None,
    ) -> "OrderFulfillment":
        return await OrderFulfillmentService(info.context.session).upsert_order_fulfillment(
            OrderFulfillment(
                id=id,
                order_id=order_id,
                shopify_fulfillment_id=shopify_fulfillment_id,
                shopify_order_id=shopify_order_id,
                order_fulfillment_id=order_fulfillment_id,
                origin=origin,
                status=status,
                shipment_status=shipment_status,
                tracking_company=tracking_company,
                tracking_number=tracking_number,
                tracking_url=tracking_url,
                tracking_numbers=tracking_numbers,
                tracking_urls=tracking_urls,
                shopify_location_id=shopify_location_id,
                location_id=location_id,
                warehouse_id=warehouse_id,
                service=service,
                receipt=receipt,
                carrier_id=carrier_id,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_order_fulfillment(info, id: int) -> bool:
        return await OrderFulfillmentService(info.context.session).delete_order_fulfillment(
            OrderFulfillment(id=id)
        )

@strawberry.type
class OrderFulfillmentSubscriptions:
    @strawberry.subscription
    async def order_fulfillment_created(self, info) -> AsyncGenerator[OrderFulfillment, None]:
        yield

    @strawberry.subscription
    async def order_fulfillment_updated(self, info) -> AsyncGenerator[OrderFulfillment, None]:
        yield

    @strawberry.subscription
    async def order_fulfillment_deleted(self, info) -> AsyncGenerator[int, None]:
        yield