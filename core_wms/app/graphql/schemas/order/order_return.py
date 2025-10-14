import strawberry
from strawberry.field_extensions import InputMutationExtension
from strawberry.scalars import JSON

from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated
from datetime import datetime

from core_wms.app.services.order.order_return import OrderReturnService
from core_wms.app.services.order.dto import OrderReturn, OrderReturnFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.order.main import Order

@strawberry.type
class OrderReturn:
    id: int | None = None
    order_id: int | None = None
    shopify_return_id: int | None = None
    status: str | None = None
    note: str | None = None
    processed_at: datetime | None = None
    restock: bool | None = None
    return_line_items: JSON | None = None  # type: ignore[misc]
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def order(self, parent: strawberry.Parent["OrderReturn"], info) -> Annotated["Order", strawberry.lazy("core_wms.app.graphql.schemas.order.main")] | None:
        return await info.context.loaders.order_return.order.load(parent.order_id)

@strawberry.type
class OrderReturnQueries:
    @strawberry.field
    @staticmethod
    async def order_returns(info, id: int | None = None, order_id: int | None = None) -> List["OrderReturn"]:
        return await OrderReturnService(info.context.session).get_order_returns(
            OrderReturnFilter(id=id, order_id=order_id)
        )
    
    @strawberry.field
    @staticmethod
    async def order_return(info, id: int | None = None, order_id: int | None = None) -> "OrderReturn" | None:
        return await OrderReturnService(info.context.session).get_order_return(
            OrderReturnFilter(id=id, order_id=order_id)
        )
    
@strawberry.type
class OrderReturnMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_order_return(
        info,
        order_id: int,
        shopify_return_id: int,
        id: int | None = None,
        status: str | None = None,
        note: str | None = None,
        processed_at: datetime | None = None,
        restock: bool | None = True,
        return_line_items: JSON | None = None  # type: ignore[misc]
    ) -> "OrderReturn":
        return await OrderReturnService(info.context.session).upsert_order_return(
            OrderReturn(
                id=id,
                order_id=order_id,
                shopify_return_id=shopify_return_id,
                status=status,
                note=note,
                processed_at=processed_at,
                restock=restock,
                return_line_items=return_line_items,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_order_return(info, id: int) -> bool:
        return await OrderReturnService(info.context.session).delete_order_return(
            OrderReturn(id=id)
        )

@strawberry.type
class OrderReturnSubscriptions:
    @strawberry.subscription
    async def order_return_created(self, info) -> AsyncGenerator[OrderReturn, None]:
        yield

    @strawberry.subscription
    async def order_return_updated(self, info) -> AsyncGenerator[OrderReturn, None]:
        yield
        
    @strawberry.subscription
    async def order_return_deleted(self, info) -> AsyncGenerator[int, None]:
        yield