import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.fulfillment_event.main import FulfillmentEventService
from core_wms.app.services.fulfillment_event.dto import FulfillmentEvent, FulfillmentEventFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.order.fulfillment import OrderFulfillment

@strawberry.type
class FulfillmentEvent:
    id: int | None = None
    order_fulfillment_id: int | None = None
    shopify_fulfillment_event_id: int | None = None
    status: str | None = None
    message: str | None = None
    happened_at: datetime | None = None
    city: str | None = None
    province: str | None = None
    country: str | None = None
    zip: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    shop_id: int | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def order_fulfillment(self, info, parent: strawberry.Parent["FulfillmentEvent"]) -> Annotated["OrderFulfillment", strawberry.lazy("core_wms.app.graphql.schemas.order.fulfillment")] | None:
        return await info.context.loaders.fulfillment_event.order_fulfillment.load(parent.order_fulfillment_id)

@strawberry.type
class FulfillmentEventQueries:
    @strawberry.field
    @staticmethod
    async def fulfillment_events(info, order_fulfillment_id: int | None = None) -> List["FulfillmentEvent"]:
        return await FulfillmentEventService(info.context.session).get_fulfillment_events(
            FulfillmentEventFilter(order_fulfillment_id=order_fulfillment_id)
        )

    @strawberry.field
    @staticmethod
    async def fulfillment_event(info, id: int) -> "FulfillmentEvent" | None:
        return await FulfillmentEventService(info.context.session).get_fulfillment_event(
            FulfillmentEventFilter(id=id)
        )

@strawberry.type
class FulfillmentEventMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_fulfillment_event(
        info,
        order_fulfillment_id: int,
        status: str | None = None,
        happened_at: datetime | None = None,
        shopify_fulfillment_event_id: int | None = None,
        message: str | None = None,
        city: str | None = None,
        province: str | None = None,
        country: str | None = None,
        zip: str | None = None,
        latitude: float | None = None,
        longitude: float | None = None,
        shop_id: int | None = None,
    ) -> "FulfillmentEvent":
        return await FulfillmentEventService(info.context.session).upsert_fulfillment_event(
            FulfillmentEvent(
                order_fulfillment_id=order_fulfillment_id,
                status=status,
                happened_at=happened_at,
                shopify_fulfillment_event_id=shopify_fulfillment_event_id,
                message=message,
                city=city,
                province=province,
                country=country,
                zip=zip,
                latitude=latitude,
                longitude=longitude,
                shop_id=shop_id,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_fulfillment_event(info, id: int) -> bool:
        return await FulfillmentEventService(info.context.session).delete_fulfillment_event(
            FulfillmentEvent(id=id)
        )

@strawberry.type
class FulfillmentEventSubscriptions:
    @strawberry.subscription
    async def fulfillment_event_created(self, info) -> AsyncGenerator[FulfillmentEvent, None]:
        yield

    @strawberry.subscription
    async def fulfillment_event_updated(self, info) -> AsyncGenerator[FulfillmentEvent, None]:
        yield

    @strawberry.subscription
    async def fulfillment_event_deleted(self, info) -> AsyncGenerator[int, None]:
        yield