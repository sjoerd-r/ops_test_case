import strawberry
from strawberry.field_extensions import InputMutationExtension
from strawberry.scalars import JSON
from decimal import Decimal
from datetime import datetime
from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated

from core_wms.app.services.order.line_item import OrderLineItemService
from core_wms.app.services.order.dto import OrderLineItem, OrderLineItemFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.order.main import Order
    from core_wms.app.graphql.schemas.product.variant import ProductVariant

@strawberry.type
class OrderLineItem:
    id: int | None = None
    order_id: int | None = None
    shopify_order_line_item_id: int | None = None
    product_variant_id: int | None = None
    quantity: int | None = None
    price: Decimal | None = None
    total_discount: Decimal | None = None
    title: str | None = None
    variant_title: str | None = None
    sku: str | None = None
    vendor: str | None = None
    product_id: int | None = None
    requires_shipping: bool | None = None
    taxable: bool | None = None
    gift_card: bool | None = None
    fulfillment_service: str | None = None
    grams: int | None = None
    tax_lines: JSON | None = None  # type: ignore[misc]
    tip_payment_gateway: str | None = None
    tip_payment_method: str | None = None
    total_discount_set: JSON | None = None  # type: ignore[misc]
    discount_allocations: JSON | None = None  # type: ignore[misc]
    duties: JSON | None = None  # type: ignore[misc]
    admin_graphql_api_id: str | None = None
    fulfillable_quantity: int | None = None
    fulfillment_status: str | None = None
    pre_tax_price: Decimal | None = None
    pre_tax_price_set: JSON | None = None  # type: ignore[misc]
    price_set: JSON | None = None  # type: ignore[misc]
    properties: JSON | None = None  # type: ignore[misc]
    attributed_staffs: JSON | None = None  # type: ignore[misc]
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def order(self, info, parent: strawberry.Parent["OrderLineItem"]) -> Annotated["Order", strawberry.lazy("core_wms.app.graphql.schemas.order.main")] | None:
        return await info.context.loaders.order_line_item.order.load(parent.order_id)

    @strawberry.field
    async def product_variant(self, info, parent: strawberry.Parent["OrderLineItem"]) -> Annotated["ProductVariant", strawberry.lazy("core_wms.app.graphql.schemas.product.variant")] | None:
        return await info.context.loaders.order_line_item.product_variant.load(parent.product_variant_id)

@strawberry.type
class OrderLineItemQueries:
    @strawberry.field
    @staticmethod
    async def order_line_items(info, id: int | None = None, order_id: int | None = None) -> List["OrderLineItem"]:
        return await OrderLineItemService(info.context.session).get_order_line_items(
            OrderLineItemFilter(id=id, order_id=order_id)
        )
    
    @strawberry.field
    @staticmethod
    async def order_line_item(info, id: int | None = None, order_id: int | None = None) -> "OrderLineItem" | None:
        return await OrderLineItemService(info.context.session).get_order_line_item(
            OrderLineItemFilter(id=id, order_id=order_id)
        )

@strawberry.type
class OrderLineItemMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_order_line_item(
        info,
        order_id: int,
        id: int | None = None,
        shopify_order_line_item_id: int | None = None,
        product_variant_id: int | None = None,
        quantity: int | None = None,
        price: Decimal | None = None,
    ) -> "OrderLineItem":
        return await OrderLineItemService(info.context.session).upsert_order_line_item(
            OrderLineItem(
                id=id,
                order_id=order_id,
                shopify_order_line_item_id=shopify_order_line_item_id,
                product_variant_id=product_variant_id,
                quantity=quantity,
                price=price,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_order_line_item(info, id: int) -> bool:
        return await OrderLineItemService(info.context.session).delete_order_line_item(
            OrderLineItem(id=id)
        )

@strawberry.type
class OrderLineItemSubscriptions:
    @strawberry.subscription
    async def order_line_item_created(self, info) -> AsyncGenerator[OrderLineItem, None]:
        yield

    @strawberry.subscription
    async def order_line_item_updated(self, info) -> AsyncGenerator[OrderLineItem, None]:
        yield

    @strawberry.subscription
    async def order_line_item_deleted(self, info) -> AsyncGenerator[int, None]:
        yield