import strawberry
from strawberry.field_extensions import InputMutationExtension
from strawberry.scalars import JSON
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.fulfillment_order.main import FulfillmentOrderService
from core_wms.app.services.fulfillment_order.dto import FulfillmentOrder, FulfillmentOrderFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.fulfillment_order_line_item.main import FulfillmentOrderLineItem
    from core_wms.app.graphql.schemas.order.main import Order

@strawberry.type
class FulfillmentOrder:
    id: int | None = None
    order_id: int | None = None
    shopify_fulfillment_order_id: int | None = None
    assigned_location_id: int | None = None
    channel_id: int | None = None
    status: str | None = None
    request_status: str | None = None
    supported_actions: JSON | None = None # type: ignore[misc]
    destination: JSON | None = None # type: ignore[misc]
    delivery_method: JSON | None = None # type: ignore[misc]
    fulfill_at: datetime | None = None
    fulfill_by: datetime | None = None
    merchant_requests: JSON | None = None # type: ignore[misc]
    fulfillment_holds: JSON | None = None # type: ignore[misc]
    international_duties: JSON | None = None # type: ignore[misc]
    order_name: str | None = None
    order_processed_at: datetime | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def line_items(self, info, parent: strawberry.Parent["FulfillmentOrder"]) -> List[Annotated["FulfillmentOrderLineItem", strawberry.lazy("core_wms.app.graphql.schemas.fulfillment_order_line_item")]]:
        return await info.context.loaders.fulfillment_order.line_items.load(parent.id)

    @strawberry.field
    async def order(self, info, parent: strawberry.Parent["FulfillmentOrder"]) -> Annotated["Order", strawberry.lazy("core_wms.app.graphql.schemas.order")] | None:
        return await info.context.loaders.fulfillment_order.order.load(parent.order_id)

@strawberry.type
class FulfillmentOrderQueries:
    @strawberry.field
    @staticmethod
    async def fulfillment_orders(info, order_id: int | None = None) -> List["FulfillmentOrder"]:
        return await FulfillmentOrderService(info.context.session).get_fulfillment_orders(
            FulfillmentOrderFilter(order_id=order_id)
        )

    @strawberry.field
    @staticmethod
    async def fulfillment_order(info, id: int) -> "FulfillmentOrder" | None:
        return await FulfillmentOrderService(info.context.session).get_fulfillment_order(
            FulfillmentOrderFilter(id=id)
        )

@strawberry.type
class FulfillmentOrderMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_fulfillment_order(
        info,
        order_id: int,
        shopify_fulfillment_order_id: int | None = None,
        assigned_location_id: int | None = None,
        channel_id: int | None = None,
        status: str | None = None,
        request_status: str | None = None,
        supported_actions: JSON | None = None,  # type: ignore[misc]
        destination: JSON | None = None, # type: ignore[misc]
        delivery_method: JSON | None = None, # type: ignore[misc]
        fulfill_at: datetime | None = None,
        fulfill_by: datetime | None = None,
        merchant_requests: JSON | None = None, # type: ignore[misc]
        fulfillment_holds: JSON | None = None, # type: ignore[misc]
        international_duties: JSON | None = None, # type: ignore[misc]
        order_name: str | None = None,
        order_processed_at: datetime | None = None,
    ) -> "FulfillmentOrder":
        return await FulfillmentOrderService(info.context.session).upsert_fulfillment_order(
            FulfillmentOrder(
                order_id=order_id,
                shopify_fulfillment_order_id=shopify_fulfillment_order_id,
                assigned_location_id=assigned_location_id,
                channel_id=channel_id,
                status=status,
                request_status=request_status,
                supported_actions=supported_actions,
                destination=destination,
                delivery_method=delivery_method,
                fulfill_at=fulfill_at,
                fulfill_by=fulfill_by,
                merchant_requests=merchant_requests,
                fulfillment_holds=fulfillment_holds,
                international_duties=international_duties,
                order_name=order_name,
                order_processed_at=order_processed_at,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_fulfillment_order(info, id: int) -> bool:
        return await FulfillmentOrderService(info.context.session).delete_fulfillment_order(
            FulfillmentOrder(id=id)
        )

@strawberry.type
class FulfillmentOrderSubscriptions:
    @strawberry.subscription
    async def fulfillment_order_created(self, info) -> AsyncGenerator[FulfillmentOrder, None]:
        yield

    @strawberry.subscription
    async def fulfillment_order_updated(self, info) -> AsyncGenerator[FulfillmentOrder, None]:
        yield

    @strawberry.subscription
    async def fulfillment_order_deleted(self, info) -> AsyncGenerator[int, None]:
        yield