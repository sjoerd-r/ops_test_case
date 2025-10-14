import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import List, TYPE_CHECKING, Annotated, AsyncGenerator

from core_wms.app.services.channel.main import ChannelService
from core_wms.app.services.channel.dto import Channel, ChannelFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.store.main import Store

@strawberry.type
class Channel:
    id: int | None = None
    store_id: int | None = None
    shopify_channel_id: int | None = None
    name: str | None = None
    channel_type: str | None = None
    handle: str | None = None
    platform: str | None = None
    app_id: int | None = None
    active: bool | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def store(self, info, parent: strawberry.Parent["Channel"]) -> Annotated["Store", strawberry.lazy("core_wms.app.graphql.schemas.store")] | None:
        return await info.context.loaders.channel.store.load(parent.store_id)

@strawberry.type
class ChannelQueries:
    @strawberry.field
    @staticmethod
    async def channels(info, store_id: int | None = None) -> List["Channel"]:
        return await ChannelService(info.context.session).get_channels(
            ChannelFilter(store_id=store_id)
        )

    @strawberry.field
    @staticmethod
    async def channel(info, id: int) -> "Channel" | None:
        return await ChannelService(info.context.session).get_channel(
            ChannelFilter(id=id)
        )

@strawberry.type
class ChannelMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_channel(
        info,
        store_id: int,
        name: str | None = None,
        shopify_channel_id: int | None = None,
        channel_type: str | None = None,
        handle: str | None = None,
        platform: str | None = None,
        app_id: int | None = None,
        active: bool | None = True,
    ) -> "Channel":
        return await ChannelService(info.context.session).upsert_channel(
            Channel(
                store_id=store_id,
                name=name,
                shopify_channel_id=shopify_channel_id,
                channel_type=channel_type,
                handle=handle,
                platform=platform,
                app_id=app_id,
                active=active,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_channel(info, id: int) -> bool:
        return await ChannelService(info.context.session).delete_channel(
            Channel(id=id)
        )

@strawberry.type
class ChannelSubscriptions:
    @strawberry.subscription
    async def channel_created(self, info) -> AsyncGenerator[Channel, None]:
        yield

    @strawberry.subscription
    async def channel_updated(self, info) -> AsyncGenerator[Channel, None]:
        yield

    @strawberry.subscription
    async def channel_deleted(self, info) -> AsyncGenerator[int, None]:
        yield
