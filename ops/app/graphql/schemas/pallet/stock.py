import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime, date
from typing import TYPE_CHECKING, Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator

from ops.app.services.pallet.stock import PalletStockService
from ops.app.services.pallet.dto import (
    PalletStockFilter,
    PalletStockInput,
)

if TYPE_CHECKING:
    from ops.app.graphql.schemas.pallet.main import Pallet

PalletType: TypeAlias = Annotated[
    "Pallet", strawberry.lazy("ops.app.graphql.schemas.pallet.main")
]
PalletStockType: TypeAlias = Annotated[
    "PalletStock", strawberry.lazy("ops.app.graphql.schemas.pallet.stock")
]

@strawberry.federation.type(keys=["id"])
class PalletStock:
    id: strawberry.ID
    pallet_id: int | None = None
    product_variant_id: int | None = None
    purchase_order_line_item_id: int | None = None
    inbounded: int | None = None
    forecasted: int | None = None
    reserved: int | None = None
    allocated: int | None = None
    available: int | None = None
    inventory_item_id: int | None = None
    location_id: int | None = None
    received: date | None = None
    counted: date | None = None
    moved: date | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def pallet(
        self, info, parent: strawberry.Parent["PalletStock"]
    ) -> PalletType | None:
        if not parent.pallet_id:
            return None
        return await info.context.loaders.pallet_stock.pallet.load(
            parent.pallet_id
        )

@strawberry.type
class PalletStockQueries:
    @strawberry.field
    @staticmethod
    async def pallet_stocks(info) -> list["PalletStock"]:
        return await PalletStockService(
            info.context.session
        ).get_pallet_stocks()

    @strawberry.field
    @staticmethod
    async def pallet_stock(
        info,
        id: int | None = None,
        pallet_id: int | None = None,
        product_variant_id: int | None = None,
    ) -> Optional["PalletStock"]:
        return await PalletStockService(info.context.session).get_pallet_stock(
            PalletStockFilter(
                id=id,
                pallet_id=pallet_id,
                product_variant_id=product_variant_id,
            )
        )

@strawberry.type
class PalletStockMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_pallet_stock(
        info,
        pallet_id: int,
        product_variant_id: int,
        purchase_order_line_item_id: int,
        inbounded: int,
        forecasted: int,
        id: int | None = None,
        reserved: int | None = 0,
        allocated: int | None = 0,
        available: int | None = 0,
        inventory_item_id: int | None = None,
        location_id: int | None = None,
        received: date | None = None,
        counted: date | None = None,
        moved: date | None = None,
    ) -> "PalletStock":
        return await PalletStockService(
            info.context.session
        ).upsert_pallet_stock(
            PalletStockInput(
                id=id,
                pallet_id=pallet_id,
                product_variant_id=product_variant_id,
                purchase_order_line_item_id=purchase_order_line_item_id,
                inbounded=inbounded,
                forecasted=forecasted,
                reserved=reserved,
                allocated=allocated,
                available=available,
                inventory_item_id=inventory_item_id,
                location_id=location_id,
                received=received,
                counted=counted,
                moved=moved,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_pallet_stock(info, id: int) -> bool:
        return await PalletStockService(
            info.context.session
        ).delete_pallet_stock(PalletStockInput(id=id))

@strawberry.type
class PalletStockSubscriptions:
    @strawberry.subscription
    async def pallet_stock_created(
        self, info
    ) -> AsyncGenerator[PalletStockType, None]:
        yield

    @strawberry.subscription
    async def pallet_stock_updated(
        self, info
    ) -> AsyncGenerator[PalletStockType, None]:
        yield

    @strawberry.subscription
    async def pallet_stock_deleted(self, info) -> AsyncGenerator[int, None]:
        yield