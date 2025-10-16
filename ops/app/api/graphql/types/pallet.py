import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import Annotated, TypeAlias

PalletStockType: TypeAlias = Annotated[
    "PalletStock", strawberry.lazy("ops.app.api.graphql.types.pallet_stock")
]
BinPositionType: TypeAlias = Annotated[
    "BinPosition", strawberry.lazy("ops.app.api.graphql.types.bin_position")
]
PalletType: TypeAlias = Annotated[
    "Pallet", strawberry.lazy("ops.app.api.graphql.types.pallet")
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
