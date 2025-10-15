import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator

from ops.app.services.pallet.main import PalletService
from ops.app.services.pallet.dto import (
    PalletInput, PalletFilter
)
from ops.app.api.graphql.types.pallet import Pallet

PalletType: TypeAlias = Annotated[
    "Pallet", strawberry.lazy("ops.app.api.graphql.types.pallet")
]


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
