import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated
from datetime import datetime

from core_wms.app.services.purchase_order_line_item.main import PurchaseOrderLineItemService
from core_wms.app.services.purchase_order_line_item.dto import PurchaseOrderLineItem, PurchaseOrderLineItemFilter

from core_wms.app.graphql.schemas.product.variant import ProductVariant

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.purchase_order.main import PurchaseOrder
    from core_wms.app.graphql.schemas.pallet.main import Pallet

@strawberry.type
class PurchaseOrderLineItem:
    id: int | None = None
    purchase_order_id: int | None = None
    product_variant_id: int | None = None
    ordered: int | None = None
    received: int | None = None
    outstanding: int | None = None
    status: str | None = None
    first_delivery_date: datetime | None = None
    last_delivery_date: datetime | None = None
    expected_completion_date: datetime | None = None
    notes: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def purchase_order(self, info, parent: strawberry.Parent["PurchaseOrderLineItem"]) -> Annotated["PurchaseOrder", strawberry.lazy("core_wms.app.graphql.schemas.purchase_order.main")] | None:
        return await info.context.loaders.purchase_order_line_item.purchase_order.load(parent.purchase_order_id)

    @strawberry.field
    async def product_variant(self, info, parent: strawberry.Parent["PurchaseOrderLineItem"]) -> ProductVariant | None:
        return await info.context.loaders.purchase_order_line_item.product_variant.load(parent.product_variant_id)

    @strawberry.field
    async def pallets(self, info, parent: strawberry.Parent["PurchaseOrderLineItem"]) -> Annotated["Pallet", strawberry.lazy("core_wms.app.graphql.schemas.pallet.main")] | None:
        return await info.context.loaders.purchase_order_line_item.pallets.load(parent.id)

@strawberry.type
class PurchaseOrderLineItemQueries:
    @strawberry.field
    @staticmethod
    async def purchase_order_line_items(info, purchase_order_id: int | None = None) -> List["PurchaseOrderLineItem"]:
        return await PurchaseOrderLineItemService(info.context.session).get_purchase_order_line_items(
            PurchaseOrderLineItemFilter(purchase_order_id=purchase_order_id)
        )
    
    @strawberry.field
    @staticmethod
    async def purchase_order_line_item(info, id: int) -> "PurchaseOrderLineItem" | None:
        return await PurchaseOrderLineItemService(info.context.session).get_purchase_order_line_item(
            PurchaseOrderLineItemFilter(id=id)
        )

@strawberry.type
class PurchaseOrderLineItemMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_purchase_order_line_item(
        info,
        purchase_order_id: int,
        product_variant_id: int,
        ordered: int,
        id: int | None = None,
        received: int | None = 0,
        outstanding: int | None = 0,
        status: str | None = "pending",
        first_delivery_date: datetime | None = None,
        last_delivery_date: datetime | None = None,
        expected_completion_date: datetime | None = None,
        notes: str | None = None,
    ) -> "PurchaseOrderLineItem":
        return await PurchaseOrderLineItemService(info.context.session).upsert_purchase_order_line_item(
            PurchaseOrderLineItem(
                id=id,
                purchase_order_id=purchase_order_id,
                product_variant_id=product_variant_id,
                ordered=ordered,
                received=received,
                outstanding=outstanding,
                status=status,
                first_delivery_date=first_delivery_date,
                last_delivery_date=last_delivery_date,
                expected_completion_date=expected_completion_date,
                notes=notes
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_purchase_order_line_item(info, id: int) -> bool:
        return await PurchaseOrderLineItemService(info.context.session).delete_purchase_order_line_item(
            PurchaseOrderLineItemFilter(id=id)
        )

@strawberry.type
class PurchaseOrderLineItemSubscriptions:
    @strawberry.subscription
    async def purchase_order_line_item_created(self, info) -> AsyncGenerator[PurchaseOrderLineItem, None]:
        yield

    @strawberry.subscription
    async def purchase_order_line_item_updated(self, info) -> AsyncGenerator[PurchaseOrderLineItem, None]:
        yield

    @strawberry.subscription
    async def purchase_order_line_item_deleted(self, info) -> AsyncGenerator[int, None]:
        yield