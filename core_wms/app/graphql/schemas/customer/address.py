import strawberry
from strawberry.field_extensions import InputMutationExtension

from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated
from datetime import datetime

from core_wms.app.services.customer.address import CustomerAddressService
from core_wms.app.services.customer.dto import CustomerAddress, CustomerAddressFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.customer.main import Customer

@strawberry.type
class CustomerAddress:
    id: int | None = None
    customer_id: int | None = None
    shopify_address_id: int | None = None
    shopify_customer_id: int | None = None
    first_name: str | None = None
    last_name: str | None = None
    company: str | None = None
    address1: str | None = None
    address2: str | None = None
    city: str | None = None
    province: str | None = None
    province_code: str | None = None
    country: str | None = None
    country_code: str | None = None
    zip: str | None = None
    phone: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    default: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def customer(self, info, parent: strawberry.Parent["CustomerAddress"]) -> Annotated["Customer", strawberry.lazy("core_wms.app.graphql.schemas.customer.main")] | None:
        return await info.context.loaders.customer.addresses.load(parent.customer_id)
    
@strawberry.type
class CustomerAddressQueries:
    @strawberry.field
    @staticmethod
    async def customer_addresses(info, id: int | None = None, customer_id: int | None = None) -> List["CustomerAddress"]:
        return await CustomerAddressService(info.context.session).get_customer_addresses(
            CustomerAddressFilter(id=id, customer_id=customer_id)
        )
    
    @strawberry.field
    @staticmethod
    async def customer_address(info, id: int | None = None, customer_id: int | None = None) -> "CustomerAddress" | None:
        return await CustomerAddressService(info.context.session).get_customer_address(
            CustomerAddressFilter(id=id, customer_id=customer_id)
        )
    
@strawberry.type
class CustomerAddressMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_customer_address(
        info,
        customer_id: int,
        shopify_address_id: int,
        id: int | None = None,
        shopify_customer_id: int | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        company: str | None = None,
        address1: str | None = None,
        address2: str | None = None,
        city: str | None = None,
        province: str | None = None,
        province_code: str | None = None,
        country: str | None = None,
        country_code: str | None = None,
        zip: str | None = None,
        phone: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        default: bool | None = False,
    ) -> "CustomerAddress":
        return await CustomerAddressService(info.context.session).upsert_customer_address(
            CustomerAddress(
                id=id,
                customer_id=customer_id,
                shopify_address_id=shopify_address_id,
                shopify_customer_id=shopify_customer_id,
                first_name=first_name,
                last_name=last_name,
                company=company,
                address1=address1,
                address2=address2,
                city=city,
                province=province,
                province_code=province_code,
                country=country,
                country_code=country_code,
                zip=zip,
                phone=phone,
                latitude=latitude,
                longitude=longitude,
                default=default,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_customer_address(info, id: int) -> bool:
        return await CustomerAddressService(info.context.session).delete_customer_address(
            CustomerAddress(id=id)
        )

@strawberry.type
class CustomerAddressSubscriptions:
    @strawberry.subscription
    async def customer_address_created(self, info) -> AsyncGenerator[CustomerAddress, None]:
        yield

    @strawberry.subscription
    async def customer_address_updated(self, info) -> AsyncGenerator[CustomerAddress, None]:
        yield

    @strawberry.subscription
    async def customer_address_deleted(self, info) -> AsyncGenerator[int, None]:
        yield