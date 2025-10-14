import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.batch.main import BatchService
from core_wms.app.services.batch.dto import Batch, BatchFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.warehouse.main import Warehouse
    from core_wms.app.graphql.schemas.supplier.main import Supplier
    from core_wms.app.graphql.schemas.product.variant import ProductVariant
    from core_wms.app.graphql.schemas.pallet.main import Pallet

@strawberry.type
class Batch:
    id: int | None = None
    warehouse_id: int | None = None
    supplier_id: int | None = None
    product_variant_id: int | None = None
    lot: str | None = None
    manufacturing_date: datetime | None = None
    expiry_date: datetime | None = None
    status: str | None = None
    additional: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def warehouse(self, info, parent: strawberry.Parent["Batch"]) -> Annotated["Warehouse", strawberry.lazy("core_wms.app.graphql.schemas.warehouse")] | None:
        return await info.context.loaders.batch.warehouse.load(parent.warehouse_id)

    @strawberry.field
    async def supplier(self, info, parent: strawberry.Parent["Batch"]) -> Annotated["Supplier", strawberry.lazy("core_wms.app.graphql.schemas.supplier")] | None:
        return await info.context.loaders.batch.supplier.load(parent.supplier_id)

    @strawberry.field
    async def product_variant(self, info, parent: strawberry.Parent["Batch"]) -> Annotated["ProductVariant", strawberry.lazy("core_wms.app.graphql.schemas.product.variant")] | None:
        return await info.context.loaders.batch.product_variant.load(parent.product_variant_id)

    @strawberry.field
    async def pallets(self, info, parent: strawberry.Parent["Batch"]) -> List[Annotated["Pallet", strawberry.lazy("core_wms.app.graphql.schemas.pallet")]]:
        return await info.context.loaders.batch.pallets.load(parent.id)

@strawberry.type
class BatchQueries:
    @strawberry.field
    @staticmethod
    async def batches(info, id: int | None = None, warehouse_id: int | None = None) -> List["Batch"]:
        return await BatchService(info.context.session).get_batches(
            BatchFilter(id=id, warehouse_id=warehouse_id)
        )

    @strawberry.field
    @staticmethod
    async def batch(info, id: int) -> "Batch" | None:
        return await BatchService(info.context.session).get_batch(
            BatchFilter(id=id)
        )

@strawberry.type
class BatchMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_batch(
        info,
        warehouse_id: int | None = None,
        supplier_id: int | None = None,
        product_variant_id: int | None = None,
        lot: str | None = None,
        manufacturing_date: datetime | None = None,
        expiry_date: datetime | None = None,
        status: str | None = None,
        additional: str | None = None,
    ) -> "Batch":
        return await BatchService(info.context.session).upsert_batch(
            Batch(
                warehouse_id=warehouse_id,
                supplier_id=supplier_id,
                product_variant_id=product_variant_id,
                lot=lot,
                manufacturing_date=manufacturing_date,
                expiry_date=expiry_date,
                status=status,
                additional=additional,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_batch(info, id: int) -> bool:
        return await BatchService(info.context.session).delete_batch(
            Batch(id=id)
        )

@strawberry.type
class BatchSubscriptions:
    @strawberry.subscription
    async def batch_created(self, info) -> AsyncGenerator[Batch, None]:
        yield

    @strawberry.subscription
    async def batch_updated(self, info) -> AsyncGenerator[Batch, None]:
        yield

    @strawberry.subscription
    async def batch_deleted(self, info) -> AsyncGenerator[int, None]:
        yield