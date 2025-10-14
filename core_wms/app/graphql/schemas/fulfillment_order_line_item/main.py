import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.fulfillment_order.line_item import FulfillmentOrderLineItemService
from core_wms.app.services.fulfillment_order.line_item.dto import FulfillmentOrderLineItem, FulfillmentOrderLineItemFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.fulfillment_order.main import FulfillmentOrder
    from core_wms.app.graphql.schemas.order.line_item import OrderLineItem

@strawberry.type
class FulfillmentOrderLineItem:
    id: int | None = None
    fulfillment_order_id: int | None = None
    order_line_item_id: int | None = None
    shopify_fulfillment_order_line_item_id: int | None = None
    quantity: int | None = None
    fulfillable_quantity: int | None = None
    variant_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def fulfillment_order(self, info, parent: strawberry.Parent["FulfillmentOrderLineItem"]) -> Annotated["FulfillmentOrder", strawberry.lazy("core_wms.app.graphql.schemas.fulfillment_order")] | None:
        return await info.context.loaders.fulfillment_order_line_item.fulfillment_order.load(parent.fulfillment_order_id)

    @strawberry.field
    async def order_line_item(self, info, parent: strawberry.Parent["FulfillmentOrderLineItem"]) -> Annotated["OrderLineItem", strawberry.lazy("core_wms.app.graphql.schemas.order.line_item")] | None:
        return await info.context.loaders.fulfillment_order_line_item.order_line_item.load(parent.order_line_item_id)

@strawberry.type
class FulfillmentOrderLineItemQueries:
    @strawberry.field
    @staticmethod
    async def fulfillment_order_line_items(info, fulfillment_order_id: int | None = None) -> List["FulfillmentOrderLineItem"]:
        return await FulfillmentOrderLineItemService(info.context.session).get_fulfillment_order_line_items(
            FulfillmentOrderLineItemFilter(fulfillment_order_id=fulfillment_order_id)
        )

    @strawberry.field
    @staticmethod
    async def fulfillment_order_line_item(info, id: int) -> "FulfillmentOrderLineItem" | None:
        return await FulfillmentOrderLineItemService(info.context.session).get_fulfillment_order_line_item(
            FulfillmentOrderLineItemFilter(id=id)
        )

@strawberry.type
class FulfillmentOrderLineItemMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_fulfillment_order_line_item(
        info,
        fulfillment_order_id: int,
        order_line_item_id: int,
        shopify_fulfillment_order_line_item_id: int | None = None,
        quantity: int | None = None,
        fulfillable_quantity: int | None = None,
        variant_id: int | None = None,
    ) -> "FulfillmentOrderLineItem":
        return await FulfillmentOrderLineItemService(info.context.session).upsert_fulfillment_order_line_item(
            FulfillmentOrderLineItem(
                fulfillment_order_id=fulfillment_order_id,
                order_line_item_id=order_line_item_id,
                shopify_fulfillment_order_line_item_id=shopify_fulfillment_order_line_item_id,
                quantity=quantity,
                fulfillable_quantity=fulfillable_quantity,
                variant_id=variant_id,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_fulfillment_order_line_item(info, id: int) -> bool:
        return await FulfillmentOrderLineItemService(info.context.session).delete_fulfillment_order_line_item(
            FulfillmentOrderLineItem(id=id)
        )

@strawberry.type
class FulfillmentOrderLineItemSubscriptions:
    @strawberry.subscription
    async def fulfillment_order_line_item_created(self, info) -> AsyncGenerator[FulfillmentOrderLineItem, None]:
        yield

    @strawberry.subscription
    async def fulfillment_order_line_item_updated(self, info) -> AsyncGenerator[FulfillmentOrderLineItem, None]:
        yield

    @strawberry.subscription
    async def fulfillment_order_line_item_deleted(self, info) -> AsyncGenerator[int, None]:
        yield