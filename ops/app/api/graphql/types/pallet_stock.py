import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime, date
from typing import Annotated, TypeAlias

PalletType: TypeAlias = Annotated[
    "Pallet", strawberry.lazy("ops.app.api.graphql.types.pallet")
]
PalletStockType: TypeAlias = Annotated[
    "PalletStock", strawberry.lazy("ops.app.api.graphql.types.pallet_stock")
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
