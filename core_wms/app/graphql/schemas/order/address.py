import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated
from datetime import datetime

from core_wms.app.services.order.address import OrderAddressService
from core_wms.app.services.order.dto import OrderAddress, OrderAddressFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.order.main import Order

@strawberry.type
class OrderAddress:
    id: int | None = None
    order_id: int | None = None
    address_type: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    address1: str | None = None
    address2: str | None = None
    city: str | None = None
    province: str | None = None
    province_code: str | None = None
    country: str | None = None
    country_code: str | None = None
    zip: str | None = None
    phone: str | None = None
    company: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def order(self, parent: strawberry.Parent["OrderAddress"], info) -> Annotated["Order", strawberry.lazy("core_wms.app.graphql.schemas.order.main")] | None:
        return await info.context.loaders.order_address.order.load(parent.order_id)

@strawberry.type
class OrderAddressQueries:
    @strawberry.field
    @staticmethod
    async def order_addresses(info, order_id: int | None = None) -> List["OrderAddress"]:
        return await OrderAddressService(info.context.session).get_order_addresses(
            OrderAddressFilter(order_id=order_id)
        )
    
    @strawberry.field
    @staticmethod
    async def order_address(info, id: int) -> "OrderAddress" | None:
        return await OrderAddressService(info.context.session).get_order_address(
            OrderAddressFilter(id=id)
        )
    
@strawberry.type
class OrderAddressMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_order_address(
        info,
        order_id: int,
        address_type: str,
        id: int | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        address1: str | None = None,
        address2: str | None = None,
        city: str | None = None,
        province: str | None = None,
        province_code: str | None = None,
        country: str | None = None,
        country_code: str | None = None,
        zip: str | None = None,
        phone: str | None = None,
        company: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        name: str | None = None,
    ) -> "OrderAddress":
        return await OrderAddressService(info.context.session).upsert_order_address(
            OrderAddress(
                id=id,
                order_id=order_id,
                address_type=address_type,
                first_name=first_name,
                last_name=last_name,
                address1=address1,
                address2=address2,
                city=city,
                province=province,
                province_code=province_code,
                country=country,
                country_code=country_code,
                zip=zip,
                phone=phone,
                company=company,
                latitude=latitude,
                longitude=longitude,
                name=name,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_order_address(info, id: int) -> bool:
        return await OrderAddressService(info.context.session).delete_order_address(
            OrderAddress(id=id)
        )

@strawberry.type
class OrderAddressSubscriptions:
    @strawberry.subscription
    async def order_address_created(self, info) -> AsyncGenerator[OrderAddress, None]:
        yield

    @strawberry.subscription
    async def order_address_updated(self, info) -> AsyncGenerator[OrderAddress, None]:
        yield

    @strawberry.subscription
    async def order_address_deleted(self, info) -> AsyncGenerator[int, None]:
        yield