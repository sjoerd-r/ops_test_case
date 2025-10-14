import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.pallet.main import PalletService
from core_wms.app.services.pallet.dto import Pallet, PalletFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.pallet.stock import PalletStock
    from core_wms.app.graphql.schemas.bin_position.main import BinPosition
    from core_wms.app.graphql.schemas.product.variant import ProductVariant
    from core_wms.app.graphql.schemas.purchase_order.line_item import PurchaseOrderLineItem
    from core_wms.app.graphql.schemas.batch.main import Batch

@strawberry.type
class Pallet:
    id: int | None = None
    code: str | None = None
    bin_position_id: int | None = None
    batch_id: int | None = None
    product_variant_id: int | None = None
    purchase_order_line_item_id: int | None = None
    weight: float | None = None
    status: str | None = None
    type: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def stock(self, info, parent: strawberry.Parent["Pallet"]) -> Annotated["PalletStock", strawberry.lazy("core_wms.app.graphql.schemas.pallet.stock")] | None:
        return await info.context.loaders.pallet.stock.load(parent.id)

    @strawberry.field
    async def bin_position(self, info, parent: strawberry.Parent["Pallet"]) -> Annotated["BinPosition", strawberry.lazy("core_wms.app.graphql.schemas.bin_position.main")] | None:
        return await info.context.loaders.pallet.bin_position.load(parent.bin_position_id)

    @strawberry.field
    async def batch(self, info, parent: strawberry.Parent["Pallet"]) -> Annotated["Batch", strawberry.lazy("core_wms.app.graphql.schemas.batch.main")] | None:
        return await info.context.loaders.pallet.batch.load(parent.batch_id)

    @strawberry.field
    async def product_variant(self, info, parent: strawberry.Parent["Pallet"]) -> Annotated["ProductVariant", strawberry.lazy("core_wms.app.graphql.schemas.product.variant")] | None:
        return await info.context.loaders.pallet.product_variant.load(parent.product_variant_id)

    @strawberry.field
    async def purchase_order_line_item(self, info, parent: strawberry.Parent["Pallet"]) -> Annotated["PurchaseOrderLineItem", strawberry.lazy("core_wms.app.graphql.schemas.purchase_order.line_item")] | None:
        return await info.context.loaders.pallet.purchase_order_line_item.load(parent.purchase_order_line_item_id)

@strawberry.type
class PalletQueries:
    @strawberry.field
    @staticmethod
    async def pallets(info, code: str | None = None) -> List["Pallet"]:
        return await PalletService(info.context.session).get_pallets(
            PalletFilter(code=code)
        )

    @strawberry.field
    @staticmethod
    async def pallet(info, code: str) -> "Pallet" | None:
        return await PalletService(info.context.session).get_pallet(
            PalletFilter(code=code)
        )

@strawberry.type
class PalletMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_pallet(
        info,
        code: str,
        bin_position_id: int | None = None,
        batch_id: int | None = None,
        product_variant_id: int | None = None,
        purchase_order_line_item_id: int | None = None,
        weight: float | None = None,
        status: str | None = None,
        type: str | None = None,
    ) -> "Pallet":
        return await PalletService(info.context.session).upsert_pallet(
            Pallet(
                code=code,
                bin_position_id=bin_position_id,
                batch_id=batch_id,
                product_variant_id=product_variant_id,
                purchase_order_line_item_id=purchase_order_line_item_id,
                weight=weight,
                status=status,
                type=type,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_pallet(info, code: str) -> bool:
        return await PalletService(info.context.session).delete_pallet(
            Pallet(code=code)
        )

@strawberry.type
class PalletSubscriptions:
    @strawberry.subscription
    async def pallet_created(self, info) -> AsyncGenerator[Pallet, None]:
        yield

    @strawberry.subscription
    async def pallet_updated(self, info) -> AsyncGenerator[Pallet, None]:
        yield

    @strawberry.subscription
    async def pallet_deleted(self, info) -> AsyncGenerator[str, None]:
        yield
