import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated
from datetime import datetime, date

from core_wms.app.services.purchase_order.main import PurchaseOrderService
from core_wms.app.services.purchase_order.dto import PurchaseOrder, PurchaseOrderFilter

from core_wms.app.graphql.schemas.purchase_order.line_item import PurchaseOrderLineItem

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.supplier.main import Supplier
    from core_wms.app.graphql.schemas.warehouse.main import Warehouse

@strawberry.type
class PurchaseOrder:
    id: int | None = None
    purchase_order_id: str | None = None
    supplier_id: int | None = None
    warehouse_id: int | None = None
    status: str | None = None
    shipment_status: str | None = None
    expected_delivery_date: date | None = None
    delivery_date: date | None = None
    tracking_number: str | None = None
    tracking_url: str | None = None
    carrier: str | None = None
    notes: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def supplier(self, info, parent: strawberry.Parent["PurchaseOrder"]) -> Annotated["Supplier", strawberry.lazy("core_wms.app.graphql.schemas.supplier.main")] | None:
        return await info.context.loaders.purchase_order.supplier.load(parent.supplier_id)

    @strawberry.field
    async def warehouse(self, info, parent: strawberry.Parent["PurchaseOrder"]) -> Annotated["Warehouse", strawberry.lazy("core_wms.app.graphql.schemas.warehouse.main")] | None:
        return await info.context.loaders.purchase_order.warehouse.load(parent.warehouse_id)

    @strawberry.field
    async def line_items(self, info, parent: strawberry.Parent["PurchaseOrder"]) -> List["PurchaseOrderLineItem"]:        
        return await info.context.loaders.purchase_order.line_items.load(parent.id)

@strawberry.type
class PurchaseOrderQueries:
    @strawberry.field
    @staticmethod
    async def purchase_orders(info, id: int | None = None, supplier_id: int | None = None, warehouse_id: int | None = None) -> List["PurchaseOrder"]:
        return await PurchaseOrderService(info.context.session).get_purchase_orders(
            PurchaseOrderFilter(id=id, supplier_id=supplier_id, warehouse_id=warehouse_id)
        )
    
    @strawberry.field
    @staticmethod
    async def purchase_order(info, id: int | None = None, supplier_id: int | None = None, warehouse_id: int | None = None) -> "PurchaseOrder" | None:
        return await PurchaseOrderService(info.context.session).get_purchase_order(
            PurchaseOrderFilter(id=id, supplier_id=supplier_id, warehouse_id=warehouse_id)
        )

@strawberry.type
class PurchaseOrderMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_purchase_order(
        info,
        id: int | None = None,
        purchase_order_id: str | None = None,
        supplier_id: int | None = None,
        warehouse_id: int | None = None,
        status: str | None = "draft",
        shipment_status: str | None = "pending",
        expected_delivery_date: date | None = None,
        delivery_date: date | None = None,
        tracking_number: str | None = None,
        tracking_url: str | None = None,
        carrier: str | None = None,
        notes: str | None = None,
    ) -> "PurchaseOrder":
        return await PurchaseOrderService(info.context.session).upsert_purchase_order(
            PurchaseOrder(
                id=id,
                purchase_order_id=purchase_order_id,
                supplier_id=supplier_id,
                warehouse_id=warehouse_id,
                status=status,
                shipment_status=shipment_status,
                expected_delivery_date=expected_delivery_date,
                delivery_date=delivery_date,
                tracking_number=tracking_number,
                tracking_url=tracking_url,
                carrier=carrier,
                notes=notes,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_purchase_order(info, id: int) -> bool:
        return await PurchaseOrderService(info.context.session).delete_purchase_order(
            PurchaseOrder(id=id)
        )

@strawberry.type
class PurchaseOrderSubscriptions:
    @strawberry.subscription
    async def purchase_order_created(self, info) -> AsyncGenerator[PurchaseOrder, None]:
        yield

    @strawberry.subscription
    async def purchase_order_updated(self, info) -> AsyncGenerator[PurchaseOrder, None]:
        yield

    @strawberry.subscription
    async def purchase_order_deleted(self, info) -> AsyncGenerator[int, None]:
        yield