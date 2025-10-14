import strawberry
from strawberry.field_extensions import InputMutationExtension

from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated
from datetime import datetime
from decimal import Decimal

from core_wms.app.services.order.discount import OrderDiscountService
from core_wms.app.services.order.dto import OrderDiscount, OrderDiscountFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.order.main import Order

@strawberry.type
class OrderDiscount:
    id: int | None = None
    order_id: int | None = None
    shopify_discount_application_id: str | None = None
    allocation_method: str | None = None
    target_selection: str | None = None
    target_type: str | None = None
    value_type: str | None = None
    code: str | None = None
    amount: Decimal | None = None
    value: Decimal | None = None
    title: str | None = None
    description: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def order(self, info, parent: strawberry.Parent["OrderDiscount"]) -> Annotated["Order", strawberry.lazy("core_wms.app.graphql.schemas.order.main")] | None:
        return await info.context.loaders.order_discount.order.load(parent.order_id)

@strawberry.type
class OrderDiscountQueries:
    @strawberry.field
    @staticmethod
    async def order_discounts(info, id: int | None = None, order_id: int | None = None) -> List["OrderDiscount"]:
        return await OrderDiscountService(info.context.session).get_order_discounts(
            OrderDiscountFilter(id=id, order_id=order_id)
        )
    
    @strawberry.field
    @staticmethod
    async def order_discount(info, id: int | None = None, order_id: int | None = None) -> "OrderDiscount" | None:
        return await OrderDiscountService(info.context.session).get_order_discount(
            OrderDiscountFilter(id=id, order_id=order_id)
        )

@strawberry.type
class OrderDiscountMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_order_discount(
        info,
        order_id: int,
        id: int | None = None,
        shopify_discount_application_id: str | None = None,
        allocation_method: str | None = None,
        target_selection: str | None = None,
        target_type: str | None = None,
        value_type: str | None = None,
        code: str | None = None,
        amount: Decimal | None = None,
        value: Decimal | None = None,
        title: str | None = None,
        description: str | None = None,
    ) -> "OrderDiscount":
        return await OrderDiscountService(info.context.session).upsert_order_discount(
            OrderDiscount(
                id=id,
                order_id=order_id,
                shopify_discount_application_id=shopify_discount_application_id,
                allocation_method=allocation_method,
                target_selection=target_selection,
                target_type=target_type,
                value_type=value_type,
                code=code,
                amount=amount,
                value=value,
                title=title,
                description=description,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_order_discount(info, id: int) -> bool:
        return await OrderDiscountService(info.context.session).delete_order_discount(
            OrderDiscount(id=id)
        )

@strawberry.type
class OrderDiscountSubscriptions:
    @strawberry.subscription
    async def order_discount_created(self, info) -> AsyncGenerator[OrderDiscount, None]:
        yield

    @strawberry.subscription
    async def order_discount_updated(self, info) -> AsyncGenerator[OrderDiscount, None]:
        yield

    @strawberry.subscription
    async def order_discount_deleted(self, info) -> AsyncGenerator[int, None]:
        yield