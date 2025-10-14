import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.fulfillment_line_item.main import FulfillmentLineItemService
from core_wms.app.services.fulfillment_line_item.dto import FulfillmentLineItem, FulfillmentLineItemFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.order.fulfillment import OrderFulfillment
    from core_wms.app.graphql.schemas.order.line_item import OrderLineItem

@strawberry.type
class FulfillmentLineItem:
    id: int | None = None
    order_fulfillment_id: int | None = None
    order_line_item_id: int | None = None
    shopify_fulfillment_line_item_id: int | None = None
    shopify_order_id: int | None = None
    quantity: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def order_fulfillment(self, info, parent: strawberry.Parent["FulfillmentLineItem"]) -> Annotated["OrderFulfillment", strawberry.lazy("core_wms.app.graphql.schemas.order.fulfillment")] | None:
        return await info.context.loaders.fulfillment_line_item.order_fulfillment.load(parent.order_fulfillment_id)

    @strawberry.field
    async def order_line_item(self, info, parent: strawberry.Parent["FulfillmentLineItem"]) -> Annotated["OrderLineItem", strawberry.lazy("core_wms.app.graphql.schemas.order.line_item")] | None:
        return await info.context.loaders.fulfillment_line_item.order_line_item.load(parent.order_line_item_id)

@strawberry.type
class FulfillmentLineItemQueries:
    @strawberry.field
    @staticmethod
    async def fulfillment_line_items(info, order_fulfillment_id: int | None = None) -> List["FulfillmentLineItem"]:
        return await FulfillmentLineItemService(info.context.session).get_fulfillment_line_items(
            FulfillmentLineItemFilter(order_fulfillment_id=order_fulfillment_id)
        )

    @strawberry.field
    @staticmethod
    async def fulfillment_line_item(info, id: int) -> "FulfillmentLineItem" | None:
        return await FulfillmentLineItemService(info.context.session).get_fulfillment_line_item(
            FulfillmentLineItemFilter(id=id)
        )

@strawberry.type
class FulfillmentLineItemMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_fulfillment_line_item(
        info,
        order_fulfillment_id: int,
        order_line_item_id: int,
        quantity: int | None = None,
        shopify_fulfillment_line_item_id: int | None = None,
        shopify_order_id: int | None = None,
    ) -> "FulfillmentLineItem":
        return await FulfillmentLineItemService(info.context.session).upsert_fulfillment_line_item(
            FulfillmentLineItem(
                order_fulfillment_id=order_fulfillment_id,
                order_line_item_id=order_line_item_id,
                quantity=quantity,
                shopify_fulfillment_line_item_id=shopify_fulfillment_line_item_id,
                shopify_order_id=shopify_order_id,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_fulfillment_line_item(info, id: int) -> bool:
        return await FulfillmentLineItemService(info.context.session).delete_fulfillment_line_item(
            FulfillmentLineItem(id=id)
        )

@strawberry.type
class FulfillmentLineItemSubscriptions:
    @strawberry.subscription
    async def fulfillment_line_item_created(self, info) -> AsyncGenerator[FulfillmentLineItem, None]:
        yield

    @strawberry.subscription
    async def fulfillment_line_item_updated(self, info) -> AsyncGenerator[FulfillmentLineItem, None]:
        yield

    @strawberry.subscription
    async def fulfillment_line_item_deleted(self, info) -> AsyncGenerator[int, None]:
        yield