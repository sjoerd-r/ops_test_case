import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from decimal import Decimal
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.graphql.schemas.order.line_item import OrderLineItem
from core_wms.app.graphql.schemas.order.address import OrderAddress
from core_wms.app.graphql.schemas.order.fulfillment import OrderFulfillment
from core_wms.app.graphql.schemas.order.refund import OrderRefund
from core_wms.app.graphql.schemas.order.order_return import OrderReturn
from core_wms.app.graphql.schemas.order.tax import OrderTax
from core_wms.app.graphql.schemas.order.discount import OrderDiscount
from core_wms.app.graphql.schemas.order.shipping_line import OrderShippingLine

from core_wms.app.services.order.main import OrderService
from core_wms.app.services.order.dto import Order, OrderFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.customer.main import Customer
    from core_wms.app.graphql.schemas.store.main import Store

@strawberry.type
class Order:
    id: int | None = None
    store_id: int | None = None
    shopify_order_id: int | None = None
    customer_id: int | None = None
    location_id: int | None = None
    order_number: int | None = None
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    total_price: Decimal | None = None
    subtotal_price: Decimal | None = None
    total_tax: Decimal | None = None
    total_discounts: Decimal | None = None
    total_line_items_price: Decimal | None = None
    total_weight: Decimal | None = None
    currency: str | None = None
    presentment_currency: str | None = None
    taxes_included: bool | None = None
    financial_status: str | None = None
    fulfillment_status: str | None = None
    tags: str | None = None
    note: str | None = None
    note_attributes: str | None = None
    source_name: str | None = None
    source_identifier: str | None = None
    source_url: str | None = None
    app_id: int | None = None
    user_id: int | None = None
    device_id: str | None = None
    browser_ip: str | None = None
    landing_site: str | None = None
    referring_site: str | None = None
    customer_locale: str | None = None
    cart_token: str | None = None
    checkout_token: str | None = None
    confirmed: bool | None = None
    test: bool | None = None
    processed_at: datetime | None = None
    closed_at: datetime | None = None
    cancelled_at: datetime | None = None
    cancel_reason: str | None = None
    payment_gateway_names: List[str] | None = None
    payment_terms: str | None = None
    order_status_url: str | None = None
    order_edit_url: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def line_items(self, info, parent: strawberry.Parent["Order"]) -> List[OrderLineItem]:
        return await info.context.loaders.order.line_items.load(parent.id)

    @strawberry.field
    async def billing_address(self, info, parent: strawberry.Parent["Order"]) -> OrderAddress | None:
        return await info.context.loaders.order.billing_address.load(parent.id)

    @strawberry.field
    async def shipping_address(self, info, parent: strawberry.Parent["Order"]) -> OrderAddress | None:
        return await info.context.loaders.order.shipping_address.load(parent.id)

    @strawberry.field
    async def fulfillments(self, info, parent: strawberry.Parent["Order"]) -> List[OrderFulfillment]:
        return await info.context.loaders.order.fulfillments.load(parent.id)

    @strawberry.field
    async def refunds(self, info, parent: strawberry.Parent["Order"]) -> List[OrderRefund]:
        return await info.context.loaders.order.refunds.load(parent.id)

    @strawberry.field
    async def returns(self, info, parent: strawberry.Parent["Order"]) -> List[OrderReturn]:
        return await info.context.loaders.order.returns.load(parent.id)

    @strawberry.field
    async def taxes(self, info, parent: strawberry.Parent["Order"]) -> List[OrderTax]:
        return await info.context.loaders.order.taxes.load(parent.id)

    @strawberry.field
    async def discounts(self, info, parent: strawberry.Parent["Order"]) -> List[OrderDiscount]:
        return await info.context.loaders.order.discounts.load(parent.id)

    @strawberry.field
    async def shipping_lines(self, info, parent: strawberry.Parent["Order"]) -> List[OrderShippingLine]:
        return await info.context.loaders.order.shipping_lines.load(parent.id)

    @strawberry.field
    async def customer(self, info, parent: strawberry.Parent["Order"]) -> Annotated["Customer", strawberry.lazy("core_wms.app.graphql.schemas.customer.main")] | None:
        return await info.context.loaders.order.customer.load(parent.customer_id)

    @strawberry.field
    async def store(self, info, parent: strawberry.Parent["Order"]) -> Annotated["Store", strawberry.lazy("core_wms.app.graphql.schemas.store.main")] | None:
        return await info.context.loaders.order.store.load(parent.store_id)

@strawberry.type
class OrderQueries:  
    @strawberry.field
    @staticmethod
    async def orders(info, store_id: int | None = None, shopify_order_id: int | None = None) -> List["Order"]:
        return await OrderService(info.context.session).get_orders(
            OrderFilter(store_id=store_id, shopify_order_id=shopify_order_id)
        )

    @strawberry.field
    @staticmethod
    async def order(info, store_id: int, shopify_order_id: int) -> "Order" | None:
        return await OrderService(info.context.session).get_order(
            OrderFilter(store_id=store_id, shopify_order_id=shopify_order_id)
        )


@strawberry.type
class OrderMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_order(
        info,
        store_id: int,
        shopify_order_id: int,
        id: int | None = None,
        customer_id: int | None = None,
        location_id: int | None = None,
        order_number: int | None = None,
        name: str | None = None,
        email: str | None = None,
        phone: str | None = None,
        total_price: Decimal | None = None,
        subtotal_price: Decimal | None = None,
        total_tax: Decimal | None = None,
        currency: str | None = None,
        financial_status: str | None = None,
        fulfillment_status: str | None = None,
        tags: str | None = None,
        note: str | None = None,
        source_name: str | None = None,
        processed_at: datetime | None = None,
        total_discounts: Decimal | None = None,
        total_line_items_price: Decimal | None = None,
        total_weight: Decimal | None = None,
        presentment_currency: str | None = None,
        taxes_included: bool | None = None,
        source_identifier: str | None = None,
        source_url: str | None = None,
        app_id: int | None = None,
        user_id: int | None = None,
        device_id: str | None = None,
        browser_ip: str | None = None,
        landing_site: str | None = None,
        referring_site: str | None = None,
        customer_locale: str | None = None,
        cart_token: str | None = None,
        checkout_token: str | None = None,
        confirmed: bool | None = None,
        test: bool | None = None,
        closed_at: datetime | None = None,
        cancelled_at: datetime | None = None,
        cancel_reason: str | None = None,
        payment_gateway_names: List[str] | None = None,
        payment_terms: str | None = None,
        order_status_url: str | None = None,
        order_edit_url: str | None = None,
    ) -> "Order":
        return await OrderService(info.context.session).upsert_order(
            Order(
                id=id,
                store_id=store_id,
                shopify_order_id=shopify_order_id,
                customer_id=customer_id,
                location_id=location_id,
                order_number=order_number,
                name=name,
                email=email,
                phone=phone,
                total_price=total_price,
                subtotal_price=subtotal_price,
                total_tax=total_tax,
                currency=currency,
                financial_status=financial_status,
                fulfillment_status=fulfillment_status,
                tags=tags,
                note=note,
                source_name=source_name,
                processed_at=processed_at,
                total_discounts=total_discounts,
                total_line_items_price=total_line_items_price,
                total_weight=total_weight,
                presentment_currency=presentment_currency,
                taxes_included=taxes_included,
                source_identifier=source_identifier,
                source_url=source_url,
                app_id=app_id,
                user_id=user_id,
                device_id=device_id,
                browser_ip=browser_ip,
                landing_site=landing_site,
                referring_site=referring_site,
                customer_locale=customer_locale,
                cart_token=cart_token,
                checkout_token=checkout_token,
                confirmed=confirmed,
                test=test,
                closed_at=closed_at,
                cancelled_at=cancelled_at,
                cancel_reason=cancel_reason,
                payment_gateway_names=payment_gateway_names,
                payment_terms=payment_terms,
                order_status_url=order_status_url,
                order_edit_url=order_edit_url,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_order(info, store_id: int, shopify_order_id: int) -> bool:
        return await OrderService(info.context.session).delete_order(
            Order(store_id=store_id, shopify_order_id=shopify_order_id)
        )

@strawberry.type
class OrderSubscriptions:
    @strawberry.subscription
    async def order_created(self, info) -> AsyncGenerator[Order, None]:
        yield

    @strawberry.subscription
    async def order_updated(self, info) -> AsyncGenerator[Order, None]:
        yield

    @strawberry.subscription
    async def order_deleted(self, info) -> AsyncGenerator[int, None]:
        yield