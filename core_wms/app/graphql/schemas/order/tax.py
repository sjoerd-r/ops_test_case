import strawberry
from strawberry.field_extensions import InputMutationExtension
from strawberry.scalars import JSON

from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated
from datetime import datetime
from decimal import Decimal

from core_wms.app.services.order.tax import OrderTaxService
from core_wms.app.services.order.dto import OrderTax, OrderTaxFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.order.main import Order

@strawberry.type
class OrderTax:
    id: int | None = None
    order_id: int | None = None
    title: str | None = None
    price: Decimal | None = None
    rate: Decimal | None = None
    price_set: JSON | None = None  # type: ignore[misc]
    channel_liable: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def order(self, parent: strawberry.Parent["OrderTax"], info) -> Annotated["Order", strawberry.lazy("core_wms.app.graphql.schemas.order.main")] | None:
        return await info.context.loaders.order_tax.order.load(parent.order_id)

@strawberry.type
class OrderTaxQueries:
    @strawberry.field
    @staticmethod
    async def order_taxes(info, id: int | None = None, order_id: int | None = None) -> List["OrderTax"]:
        return await OrderTaxService(info.context.session).get_order_taxes(
            OrderTaxFilter(id=id, order_id=order_id)
        )
    
    @strawberry.field
    @staticmethod
    async def order_tax(info, id: int | None = None, order_id: int | None = None) -> "OrderTax" | None:
        return await OrderTaxService(info.context.session).get_order_tax(
            OrderTaxFilter(id=id, order_id=order_id)
        )

@strawberry.type
class OrderTaxMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_order_tax(
        info,
        order_id: int,
        id: int | None = None,
        title: str | None = None,
        price: Decimal | None = None,
        rate: Decimal | None = None,
        price_set: JSON | None = None,  # type: ignore[misc]
        channel_liable: bool | None = None,
    ) -> "OrderTax":
        return await OrderTaxService(info.context.session).upsert_order_tax(
            OrderTax(
                id=id,
                order_id=order_id,
                title=title,
                price=price,
                rate=rate,
                price_set=price_set,
                channel_liable=channel_liable,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_order_tax(info, id: int) -> bool:
        return await OrderTaxService(info.context.session).delete_order_tax(
            OrderTax(id=id)
        )

@strawberry.type
class OrderTaxSubscriptions:
    @strawberry.subscription
    async def order_tax_created(self, info) -> AsyncGenerator[OrderTax, None]:
        yield

    @strawberry.subscription
    async def order_tax_updated(self, info) -> AsyncGenerator[OrderTax, None]:
        yield

    @strawberry.subscription
    async def order_tax_deleted(self, info) -> AsyncGenerator[int, None]:
        yield