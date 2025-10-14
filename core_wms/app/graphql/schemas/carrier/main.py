import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.carrier.main import CarrierService
from core_wms.app.services.carrier.dto import Carrier, CarrierFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.store.main import Store

@strawberry.type
class Carrier:
    id: int | None = None
    store_id: int | None = None
    name: str | None = None
    code: str | None = None
    tracking_url_template: str | None = None
    active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def store(self, info, parent: strawberry.Parent["Carrier"]) -> Annotated["Store", strawberry.lazy("core_wms.app.graphql.schemas.store")] | None:
        return await info.context.loaders.carrier.store.load(parent.store_id)

@strawberry.type
class CarrierQueries:
    @strawberry.field
    @staticmethod
    async def carriers(info, store_id: int | None = None) -> List["Carrier"]:
        return await CarrierService(info.context.session).get_carriers(
            CarrierFilter(store_id=store_id)
        )

    @strawberry.field
    @staticmethod
    async def carrier(info, id: int) -> "Carrier" | None:
        return await CarrierService(info.context.session).get_carrier(
            CarrierFilter(id=id)
        )

@strawberry.type
class CarrierMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_carrier(
        info,
        store_id: int | None = None,
        name: str | None = None,
        code: str | None = None,
        tracking_url_template: str | None = None,
        active: bool | None = None,
    ) -> "Carrier":
        return await CarrierService(info.context.session).upsert_carrier(
            Carrier(
                store_id=store_id,
                name=name,
                code=code,
                tracking_url_template=tracking_url_template,
                active=active,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_carrier(info, id: int) -> bool:
        return await CarrierService(info.context.session).delete_carrier(
            Carrier(id=id)
        )

@strawberry.type
class CarrierSubscriptions:
    @strawberry.subscription
    async def carrier_created(self, info) -> AsyncGenerator[Carrier, None]:
        yield

    @strawberry.subscription
    async def carrier_updated(self, info) -> AsyncGenerator[Carrier, None]:
        yield

    @strawberry.subscription
    async def carrier_deleted(self, info) -> AsyncGenerator[int, None]:
        yield