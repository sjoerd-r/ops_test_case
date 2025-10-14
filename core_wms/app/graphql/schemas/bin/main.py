import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.bin.main import BinService
from core_wms.app.services.bin.dto import Bin, BinFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.rack.main import Rack
    from core_wms.app.graphql.schemas.bin_position.main import BinPosition

@strawberry.type
class Bin:
    id: int | None = None
    rack_id: int | None = None
    level: str | None = None
    prefix: str | None = None
    accessible: bool | None = None
    status: str | None = None
    type: str | None = None
    notes: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def positions(self, info, parent: strawberry.Parent["Bin"]) -> List[Annotated["BinPosition", strawberry.lazy("core_wms.app.graphql.schemas.bin_position.main")]]:
        return await info.context.loaders.bin.positions.load(parent.id)

    @strawberry.field
    async def rack(self, info, parent: strawberry.Parent["Bin"]) -> Annotated["Rack", strawberry.lazy("core_wms.app.graphql.schemas.rack.main")] | None:
        return await info.context.loaders.bin.rack.load(parent.rack_id)

@strawberry.type
class BinQueries:
    @strawberry.field
    @staticmethod
    async def bins(info, id: int | None = None, rack_id: int | None = None) -> List["Bin"]:
        return await BinService(info.context.session).get_bins(
            BinFilter(id=id, rack_id=rack_id)
        )

    @strawberry.field
    @staticmethod
    async def bin(info, id: int) -> "Bin" | None:
        return await BinService(info.context.session).get_bin(
            BinFilter(id=id)
        )

@strawberry.type
class BinMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_bin(
        info,
        rack_id: int,
        level: str | None = None,
        prefix: str | None = None,
        accessible: bool | None = True,
        status: str | None = "available",
        type: str | None = "standard",
        notes: str | None = None,
    ) -> "Bin":
        return await BinService(info.context.session).upsert_bin(
            Bin(
                rack_id=rack_id,
                level=level,
                prefix=prefix,
                accessible=accessible,
                status=status,
                type=type,
                notes=notes,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_bin(info, id: int) -> bool:
        return await BinService(info.context.session).delete_bin(
            Bin(id=id)
        )

@strawberry.type
class BinSubscriptions:
    @strawberry.subscription
    async def bin_created(self, info) -> AsyncGenerator[Bin, None]:
        yield

    @strawberry.subscription
    async def bin_updated(self, info) -> AsyncGenerator[Bin, None]:
        yield

    @strawberry.subscription
    async def bin_deleted(self, info) -> AsyncGenerator[int, None]:
        yield
