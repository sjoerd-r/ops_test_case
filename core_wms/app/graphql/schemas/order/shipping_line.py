import strawberry
from strawberry.field_extensions import InputMutationExtension
from strawberry.scalars import JSON

from decimal import Decimal
from datetime import datetime
from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated

from core_wms.app.services.order.shipping_line import OrderShippingLineService
from core_wms.app.services.order.dto import OrderShippingLine, OrderShippingLineFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.order.main import Order

@strawberry.type
class OrderShippingLine:
    id: int | None = None
    order_id: int | None = None
    shopify_shipping_line_id: int | None = None
    title: str | None = None
    price: Decimal | None = None
    code: str | None = None
    source: str | None = None
    carrier_identifier: str | None = None
    delivery_category: str | None = None
    discounted_price: Decimal | None = None
    phone: str | None = None
    requested_fulfillment_service_id: int | None = None
    tax_lines: JSON | None = None  # type: ignore[misc]
    price_set: JSON | None = None  # type: ignore[misc]
    discounted_price_set: JSON | None = None  # type: ignore[misc]
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def order(self, parent: strawberry.Parent["OrderShippingLine"], info) -> Annotated["Order", strawberry.lazy("core_wms.app.graphql.schemas.order.main")] | None:
        return await info.context.loaders.order_shipping_line.order.load(parent.order_id)

@strawberry.type
class OrderShippingLineQueries:
    @strawberry.field
    @staticmethod
    async def order_shipping_lines(info, id: int | None = None, order_id: int | None = None) -> List["OrderShippingLine"]:
        return await OrderShippingLineService(info.context.session).get_order_shipping_lines(
            OrderShippingLineFilter(id=id, order_id=order_id)
        )
    
    @strawberry.field
    @staticmethod
    async def order_shipping_line(info, id: int | None = None, order_id: int | None = None) -> "OrderShippingLine" | None:
        return await OrderShippingLineService(info.context.session).get_order_shipping_line(
            OrderShippingLineFilter(id=id, order_id=order_id)
        )
    
@strawberry.type
class OrderShippingLineMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_order_shipping_line(
        info,
        order_id: int,
        id: int | None = None,
        shopify_shipping_line_id: int | None = None,
        title: str | None = None,
        price: Decimal | None = None,
        code: str | None = None,
        source: str | None = None,
        carrier_identifier: str | None = None,
        delivery_category: str | None = None,
        discounted_price: Decimal | None = None,
        phone: str | None = None,
        requested_fulfillment_service_id: int | None = None,
        tax_lines: JSON | None = None,  # type: ignore[misc]
        price_set: JSON | None = None,  # type: ignore[misc]
        discounted_price_set: JSON | None = None,  # type: ignore[misc]
    ) -> "OrderShippingLine":
        return await OrderShippingLineService(info.context.session).upsert_order_shipping_line(
            OrderShippingLine(
                id=id,
                order_id=order_id,
                shopify_shipping_line_id=shopify_shipping_line_id,
                title=title,
                price=price,
                code=code,
                source=source,
                carrier_identifier=carrier_identifier,
                delivery_category=delivery_category,
                discounted_price=discounted_price,
                phone=phone,
                requested_fulfillment_service_id=requested_fulfillment_service_id,
                tax_lines=tax_lines,
                price_set=price_set,
                discounted_price_set=discounted_price_set,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_order_shipping_line(info, id: int) -> bool:
        return await OrderShippingLineService(info.context.session).delete_order_shipping_line(
            OrderShippingLine(id=id)
        )

@strawberry.type
class OrderShippingLineSubscriptions:
    @strawberry.subscription
    async def order_shipping_line_created(self, info) -> AsyncGenerator[OrderShippingLine, None]:
        yield

    @strawberry.subscription
    async def order_shipping_line_updated(self, info) -> AsyncGenerator[OrderShippingLine, None]:
        yield

    @strawberry.subscription
    async def order_shipping_line_deleted(self, info) -> AsyncGenerator[int, None]:
        yield