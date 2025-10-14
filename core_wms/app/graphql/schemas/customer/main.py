import strawberry
from strawberry.field_extensions import InputMutationExtension
from strawberry.scalars import JSON
from decimal import Decimal
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.customer.main import CustomerService
from core_wms.app.services.customer.dto import Customer, CustomerFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.order.main import Order
    from core_wms.app.graphql.schemas.store.main import Store
    from core_wms.app.graphql.schemas.customer.address import CustomerAddress

@strawberry.type
class Customer:
    id: int | None = None
    store_id: int | None = None
    shopify_customer_id: int | None = None
    email: str | None = None
    first_name: str | None = None
    last_name: str | None = None
    phone: str | None = None
    accepts_marketing: bool | None = None
    accepts_marketing_updated_at: datetime | None = None
    email_marketing_consent: JSON | None = None # type: ignore[misc]
    sms_marketing_consent: JSON | None = None # type: ignore[misc]
    marketing_opt_in_level: str | None = None
    state: str | None = None
    verified_email: bool | None = None
    tax_exempt: bool | None = None
    tags: str | None = None
    note: str | None = None
    currency: str | None = None
    multipass_identifier: str | None = None
    orders_count: int | None = None
    total_spent: Decimal | None = None
    last_order_id: int | None = None
    last_order_name: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def addresses(self, info, parent: strawberry.Parent["Customer"]) -> List[Annotated["CustomerAddress", strawberry.lazy("core_wms.app.graphql.schemas.customer.address")]]:
        return await info.context.loaders.customer.addresses.load(parent.id)

    @strawberry.field
    async def orders(self, info, parent: strawberry.Parent["Customer"]) -> List[Annotated["Order", strawberry.lazy("core_wms.app.graphql.schemas.order.main")]]:
        return await info.context.loaders.customer.orders.load(parent.id)

    @strawberry.field
    async def store(self, info, parent: strawberry.Parent["Customer"]) -> Annotated["Store", strawberry.lazy("core_wms.app.graphql.schemas.store.main")] | None:
        return await info.context.loaders.customer.store.load(parent.store_id)

@strawberry.type
class CustomerQueries:
    @strawberry.field
    @staticmethod
    async def customers(info, store_id: int | None = None) -> List["Customer"]:
        return await CustomerService(info.context.session).get_customers(
            CustomerFilter(store_id=store_id)
        )

    @strawberry.field
    @staticmethod
    async def customer(info, id: int) -> "Customer" | None:
        return await CustomerService(info.context.session).get_customer(
            CustomerFilter(id=id)
        )

@strawberry.type
class CustomerMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_customer(
        info,
        store_id: int | None = None,
        shopify_customer_id: int | None = None,
        email: str | None = None,
        first_name: str | None = None,
        last_name: str | None = None,
        phone: str | None = None,
        accepts_marketing: bool | None = None,
        accepts_marketing_updated_at: datetime | None = None,
        email_marketing_consent: JSON | None = None,
        sms_marketing_consent: JSON | None = None,
        marketing_opt_in_level: str | None = None,
        state: str | None = None,
        verified_email: bool | None = None,
        tax_exempt: bool | None = None,
        tags: str | None = None,
        note: str | None = None,
        currency: str | None = None,
        multipass_identifier: str | None = None,
        orders_count: int | None = None,
        total_spent: Decimal | None = None,
        last_order_id: int | None = None,
        last_order_name: str | None = None,
    ) -> "Customer":
        return await CustomerService(info.context.session).upsert_customer(
            Customer(
                store_id=store_id,
                shopify_customer_id=shopify_customer_id,
                email=email,
                first_name=first_name,
                last_name=last_name,
                phone=phone,
                accepts_marketing=accepts_marketing,
                accepts_marketing_updated_at=accepts_marketing_updated_at,
                email_marketing_consent=email_marketing_consent,
                sms_marketing_consent=sms_marketing_consent,
                marketing_opt_in_level=marketing_opt_in_level,
                state=state,
                verified_email=verified_email,
                tax_exempt=tax_exempt,
                tags=tags,
                note=note,
                currency=currency,
                multipass_identifier=multipass_identifier,
                orders_count=orders_count,
                total_spent=total_spent,
                last_order_id=last_order_id,
                last_order_name=last_order_name,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_customer(info, id: int) -> bool:
        return await CustomerService(info.context.session).delete_customer(
            Customer(id=id)
        )
    

@strawberry.type
class CustomerSubscriptions:
    @strawberry.subscription
    async def customer_created(self, info) -> AsyncGenerator[Customer, None]:
        yield

    @strawberry.subscription
    async def customer_updated(self, info) -> AsyncGenerator[Customer, None]:
        yield

    @strawberry.subscription
    async def customer_deleted(self, info) -> AsyncGenerator[int, None]:
        yield
