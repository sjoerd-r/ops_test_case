import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated

from core_wms.app.services.order.refund import OrderRefundService
from core_wms.app.services.order.dto import OrderRefund, OrderRefundFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.order.main import Order

@strawberry.type
class OrderRefund:
    id: int | None = None
    order_id: int | None = None
    shopify_refund_id: int | None = None
    shopify_order_id: int | None = None
    order_refund_id: str | None = None
    amount: float | None = None
    currency: str | None = None
    reason: str | None = None
    note: str | None = None
    processed_at: datetime | None = None
    restock: bool | None = None
    admin_graphql_api_id: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def order(self, parent: strawberry.Parent["OrderRefund"], info) -> Annotated["Order", strawberry.lazy("core_wms.app.graphql.schemas.order.main")] | None:
        return await info.context.loaders.order_refund.order.load(parent.order_id)

@strawberry.type
class OrderRefundQueries:
    @strawberry.field
    @staticmethod
    async def order_refunds(info, id: int | None = None, order_id: int | None = None) -> List["OrderRefund"]:
        return await OrderRefundService(info.context.session).get_order_refunds(
            OrderRefundFilter(id=id, order_id=order_id)
        )
    
    @strawberry.field
    @staticmethod
    async def order_refund(info, id: int | None = None, order_id: int | None = None) -> "OrderRefund" | None:
        return await OrderRefundService(info.context.session).get_order_refund(
            OrderRefundFilter(id=id, order_id=order_id)
        )
    
@strawberry.type
class OrderRefundMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_order_refund(
        info,
        order_id: int,
        id: int | None = None,
        shopify_refund_id: int | None = None,
        shopify_order_id: int | None = None,
        order_refund_id: str | None = None,
        amount: float | None = None,
        currency: str | None = None,
        reason: str | None = None,
        note: str | None = None,
        processed_at: datetime | None = None,
        restock: bool | None = None,
        admin_graphql_api_id: str | None = None,
    ) -> "OrderRefund":
        return await OrderRefundService(info.context.session).upsert_order_refund(
            OrderRefund(
                id=id,
                order_id=order_id,
                shopify_refund_id=shopify_refund_id,
                shopify_order_id=shopify_order_id,
                order_refund_id=order_refund_id,
                amount=amount,
                currency=currency,
                reason=reason,
                note=note,
                processed_at=processed_at,
                restock=restock,
                admin_graphql_api_id=admin_graphql_api_id,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_order_refund(info, id: int) -> bool:
        return await OrderRefundService(info.context.session).delete_order_refund(
            OrderRefund(id=id)
        )

@strawberry.type
class OrderRefundSubscriptions:
    @strawberry.subscription
    async def order_refund_created(self, info) -> AsyncGenerator[OrderRefund, None]:
        yield

    @strawberry.subscription
    async def order_refund_updated(self, info) -> AsyncGenerator[OrderRefund, None]:
        yield

    @strawberry.subscription
    async def order_refund_deleted(self, info) -> AsyncGenerator[int, None]:
        yield