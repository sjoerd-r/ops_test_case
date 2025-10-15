import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import Annotated, TypeAlias, Optional
from collections.abc import AsyncGenerator
from datetime import date

from ops.app.services.pallet.stock import PalletStockService
from ops.app.services.pallet.dto import (
    PalletStockFilter,
    PalletStockInput,
)
from ops.app.api.graphql.types.pallet_stock import PalletStock

PalletStockType: TypeAlias = Annotated[
    "PalletStock", strawberry.lazy("ops.app.api.graphql.types.pallet_stock")
]


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
    ) -> Optional["PalletStock"]:
        return await PalletStockService(info.context.session).get_pallet_stock(
            PalletStockFilter(
                id=id,
                pallet_id=pallet_id,
            )
        )


@strawberry.type
class PalletStockMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_pallet_stock(
        info,
        pallet_id: int,
        inbounded: int,
        forecasted: int,
        id: int | None = None,
        reserved: int | None = 0,
        allocated: int | None = 0,
        available: int | None = 0,
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
                inbounded=inbounded,
                forecasted=forecasted,
                reserved=reserved,
                allocated=allocated,
                available=available,
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
