import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated
from datetime import datetime

from core_wms.app.services.rack.main import RackService
from core_wms.app.services.rack.dto import Rack, RackFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.aisle.main import Aisle

from core_wms.app.graphql.schemas.bin.main import Bin

@strawberry.type
class Rack:
    id: int | None = None
    aisle_id: int | None = None
    position: int | None = None
    description: str | None = None
    type: str | None = None
    active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def bins(self, info, parent: strawberry.Parent["Rack"]) -> List[Bin]:
        return await info.context.loaders.rack.bins.load(parent.id)

    @strawberry.field
    async def aisle(self, info, parent: strawberry.Parent["Rack"]) -> Annotated["Aisle", strawberry.lazy("core_wms.app.graphql.schemas.aisle.main")] | None:
        return await info.context.loaders.rack.aisle.load(parent.aisle_id)

@strawberry.type
class RackQueries:
    @strawberry.field
    @staticmethod
    async def racks(info, id: int | None = None, aisle_id: int | None = None) -> List["Rack"]:
        return await RackService(info.context.session).get_racks(
            RackFilter(id=id, aisle_id=aisle_id)
        )
    
    @strawberry.field
    @staticmethod
    async def rack(info, id: int) -> "Rack" | None:
        return await RackService(info.context.session).get_rack(
            RackFilter(id=id)
        )

@strawberry.type
class RackMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_rack(
        info,
        aisle_id: int,
        position: int,
        description: str | None = None,
        type: str | None = "pallet",
        active: bool | None = True,
    ) -> "Rack":
        return await RackService(info.context.session).upsert_rack(
            Rack(
                aisle_id=aisle_id,
                position=position,
                description=description,
                type=type,
                active=active,
            )
        )
    
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_rack(info, id: int) -> bool:
        return await RackService(info.context.session).delete_rack(
            Rack(id=id)
        )

@strawberry.type
class RackSubscriptions:
    @strawberry.subscription
    async def rack_created(self, info) -> AsyncGenerator[Rack, None]:
        yield

    @strawberry.subscription
    async def rack_updated(self, info) -> AsyncGenerator[Rack, None]:
        yield

    @strawberry.subscription
    async def rack_deleted(self, info) -> AsyncGenerator[int, None]:
        yield