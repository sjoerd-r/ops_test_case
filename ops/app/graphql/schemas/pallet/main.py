import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import TYPE_CHECKING, Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator

from ops.app.services.pallet.main import PalletService
from ops.app.services.pallet.dto import (
    PalletInput, PalletFilter
)

if TYPE_CHECKING:
    from ops.app.graphql.schemas.pallet.stock import PalletStock
    from ops.app.graphql.schemas.bin.position import BinPosition

PalletStockType: TypeAlias = Annotated[
    "PalletStock", strawberry.lazy("ops.app.graphql.schemas.pallet.stock")
]
BinPositionType: TypeAlias = Annotated[
    "BinPosition", strawberry.lazy("ops.app.graphql.schemas.bin.position")
]
PalletType: TypeAlias = Annotated[
    "Pallet", strawberry.lazy("ops.app.graphql.schemas.pallet.main")
]

@strawberry.federation.type(keys=["id"])
class Pallet:
    id: strawberry.ID
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
    async def stock(
        self, info, parent: strawberry.Parent["Pallet"]
    ) -> PalletStockType | None:
        if not parent.id:
            return None
        return await info.context.loaders.pallet.stock.load(parent.id)

    @strawberry.field
    async def bin_position(
        self, info, parent: strawberry.Parent["Pallet"]
    ) -> BinPositionType | None:
        if not parent.bin_position_id:
            return None
        return await info.context.loaders.pallet.bin_position.load(
            parent.bin_position_id
        )


@strawberry.type
class PalletQueries:
    @strawberry.field
    @staticmethod
    async def pallets(info) -> list["Pallet"]:
        return await PalletService(info.context.session).get_pallets()

    @strawberry.field
    @staticmethod
    async def pallet(info, code: str) -> Optional["Pallet"]:
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
            PalletInput(
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
            PalletInput(code=code)
        )


@strawberry.type
class PalletSubscriptions:
    @strawberry.subscription
    async def pallet_created(self, info) -> AsyncGenerator[PalletType, None]:
        yield

    @strawberry.subscription
    async def pallet_updated(self, info) -> AsyncGenerator[PalletType, None]:
        yield

    @strawberry.subscription
    async def pallet_deleted(self, info) -> AsyncGenerator[str, None]:
        yield