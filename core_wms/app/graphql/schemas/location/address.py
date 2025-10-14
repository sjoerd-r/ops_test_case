import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated

from core_wms.app.services.location.address import LocationAddressService
from core_wms.app.services.location.dto import LocationAddress, LocationAddressFilter 

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.location.main import Location

@strawberry.type
class LocationAddress:
    id: int | None = None
    address1: str | None = None
    address2: str | None = None
    city: str | None = None
    province: str | None = None
    province_code: str | None = None
    country: str | None = None
    country_code: str | None = None
    zip: str | None = None
    phone: str | None = None

    @strawberry.field
    async def location(self, info, parent: strawberry.Parent["LocationAddress"]) -> Annotated["Location", strawberry.lazy("core_wms.app.graphql.schemas.location.main")] | None:
        return await info.context.loaders.location_address.location.load(parent.id)
    
@strawberry.type
class LocationAddressQueries:
    @strawberry.field
    @staticmethod
    async def location_addresses(info, id: int | None = None, location_id: int | None = None) -> List["LocationAddress"]:
        return await LocationAddressService(info.context.session).get_location_addresses(
            LocationAddressFilter(id=id, location_id=location_id)
        )
    
    @strawberry.field
    @staticmethod
    async def location_address(info, id: int | None = None, location_id: int | None = None) -> "LocationAddress" | None:
        return await LocationAddressService(info.context.session).get_location_address(
            LocationAddressFilter(id=id, location_id=location_id)
        )

@strawberry.type
class LocationAddressMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_location_address(
        info,
        id: int | None = None,
        address1: str | None = None,
        address2: str | None = None,
        city: str | None = None,
        province: str | None = None,
        province_code: str | None = None,
        country: str | None = None,
        country_code: str | None = None,
        zip: str | None = None,
        phone: str | None = None,
    ) -> "LocationAddress":
        return await LocationAddressService(info.context.session).upsert_location_address(
            LocationAddress(
                id=id,
                address1=address1,
                address2=address2,
                city=city,
                province=province,
                province_code=province_code,
                country=country,
                country_code=country_code,
                zip=zip,
                phone=phone,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_location_address(info, id: int) -> bool:
        return await LocationAddressService(info.context.session).delete_location_address(
            LocationAddress(id=id)
        )

@strawberry.type
class LocationAddressSubscriptions:
    @strawberry.subscription
    async def location_address_created(self, info) -> AsyncGenerator[LocationAddress, None]:
        yield

    @strawberry.subscription
    async def location_address_updated(self, info) -> AsyncGenerator[LocationAddress, None]:
        yield

    @strawberry.subscription
    async def location_address_deleted(self, info) -> AsyncGenerator[int, None]:
        yield