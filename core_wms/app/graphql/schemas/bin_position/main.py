import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.bin_position.main import BinPositionService
from core_wms.app.services.bin_position.dto import BinPosition, BinPositionFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.pallet.main import Pallet
    from core_wms.app.graphql.schemas.bin.main import Bin

@strawberry.type
class BinPosition:
    id: int | None = None
    bin_id: int | None = None
    position: str | None = None
    location: str | None = None
    status: str | None = None
    is_available: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def bin(self, info, parent: strawberry.Parent["BinPosition"]) -> Annotated["Bin", strawberry.lazy("core_wms.app.graphql.schemas.bin.main")] | None:
        return await info.context.loaders.bin_position.bin.load(parent.bin_id)

    @strawberry.field
    async def pallets(self, info, parent: strawberry.Parent["BinPosition"]) -> List[Annotated["Pallet", strawberry.lazy("core_wms.app.graphql.schemas.pallet.main")]]:
        return await info.context.loaders.bin_position.pallets.load(parent.id)

@strawberry.type
class BinPositionQueries:
    @strawberry.field
    @staticmethod
    async def bin_positions(info, bin_id: int | None = None) -> List["BinPosition"]:
        return await BinPositionService(info.context.session).get_bin_positions(
            BinPositionFilter(bin_id=bin_id)
        )

    @strawberry.field
    @staticmethod
    async def bin_position(info, id: int) -> "BinPosition" | None:
        return await BinPositionService(info.context.session).get_bin_position(
            BinPositionFilter(id=id)
        )

@strawberry.type
class BinPositionMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_bin_position(
        info,
        bin_id: int,
        position: str | None = None,
        location: str | None = None,
        status: str | None = "available",
        is_available: bool | None = True,
    ) -> "BinPosition":
        return await BinPositionService(info.context.session).upsert_bin_position(
            BinPosition(
                bin_id=bin_id,
                position=position,
                location=location,
                status=status,
                is_available=is_available,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_bin_position(info, id: int) -> bool:
        return await BinPositionService(info.context.session).delete_bin_position(
            BinPosition(id=id)
        )

@strawberry.type
class BinPositionSubscriptions:
    @strawberry.subscription
    async def bin_position_created(self, info) -> AsyncGenerator[BinPosition, None]:
        yield

    @strawberry.subscription
    async def bin_position_updated(self, info) -> AsyncGenerator[BinPosition, None]:
        yield

    @strawberry.subscription
    async def bin_position_deleted(self, info) -> AsyncGenerator[int, None]:
        yield
