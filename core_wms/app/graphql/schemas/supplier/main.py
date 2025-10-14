import strawberry
from datetime import datetime
from strawberry.field_extensions import InputMutationExtension
from typing import TYPE_CHECKING, AsyncGenerator, List, Annotated

from core_wms.app.services.supplier.main import SupplierService
from core_wms.app.graphql.schemas.purchase_order.main import PurchaseOrder

from core_wms.app.services.supplier.dto import Supplier, SupplierFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.supplier.main import Supplier

@strawberry.type
class Supplier:
    id: int | None = None
    code: str | None = None
    name: str | None = None
    email: str | None = None
    phone: str | None = None
    address_line_1: str | None = None
    address_line_2: str | None = None
    city: str | None = None
    province: str | None = None
    postal_code: str | None = None
    country: str | None = None
    status: str | None = None
    notes: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def purchase_orders(self, info, parent: strawberry.Parent["Supplier"]) -> Annotated["PurchaseOrder", strawberry.lazy("core_wms.app.graphql.schemas.purchase_order.main")] | None:
        return await info.context.loaders.supplier.purchase_orders.load(parent.id)

@strawberry.type
class SupplierQueries:
    @strawberry.field
    @staticmethod
    async def suppliers(info, id: str | None = None) -> List["Supplier"]:
        return await SupplierService(info.context.session).get_suppliers(
            SupplierFilter(id=id)
        )

    @strawberry.field
    @staticmethod
    async def supplier(info, id: int) -> "Supplier" | None:
        return await SupplierService(info.context.session).get_supplier(
            SupplierFilter(id=id)
        )

@strawberry.type
class SupplierMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_supplier(
        info,
        code: str,
        name: str,
        email: str | None = None,
        phone: str | None = None,
        address_line_1: str | None = None,
        address_line_2: str | None = None,
        city: str | None = None,
        province: str | None = None,
        postal_code: str | None = None,
        country: str | None = None,
        status: str | None = None,
        notes: str | None = None,
        id: int | None = None,
    ) -> "Supplier":
        return await SupplierService(info.context.session).upsert_supplier(
            Supplier(
                code=code,
                name=name,
                email=email,
                phone=phone,
                address_line_1=address_line_1,
                address_line_2=address_line_2,
                city=city,
                province=province,
                postal_code=postal_code,
                country=country,
                status=status,
                notes=notes,
                id=id,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_supplier(info, id: int) -> bool:
        return await SupplierService(info.context.session).delete_supplier(
            Supplier(id=id)
        )

@strawberry.type
class SupplierSubscriptions:
    @strawberry.subscription
    async def supplier_created(self, info) -> AsyncGenerator["Supplier", None]:
        yield

    @strawberry.subscription
    async def supplier_updated(self, info) -> AsyncGenerator["Supplier", None]:
        yield

    @strawberry.subscription
    async def supplier_deleted(self, info) -> AsyncGenerator[int, None]:
        yield