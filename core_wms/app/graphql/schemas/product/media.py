import strawberry
from strawberry.field_extensions import InputMutationExtension

from datetime import datetime
from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated

from core_wms.app.services.product.media import ProductMediaService
from core_wms.app.services.product.dto import ProductMedia, ProductMediaFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.product.main import Product

@strawberry.type
class ProductMedia:
    id: int | None = None
    product_id: int | None = None
    shopify_media_id: int | None = None
    media_type: str | None = None
    src: str | None = None
    position: int | None = None
    alt: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def product(self, parent: strawberry.Parent["ProductMedia"], info) -> Annotated["Product", strawberry.lazy("core_wms.app.graphql.schemas.product.main")] | None:
        return await info.context.loaders.product_media.product.load(parent.product_id)

@strawberry.type
class ProductMediaQueries:
    @strawberry.field
    @staticmethod
    async def product_media(info, id: int | None = None, product_id: int | None = None) -> List["ProductMedia"]:
        return await ProductMediaService(info.context.session).get_product_media(
            ProductMediaFilter(id=id, product_id=product_id)
        )
        
    @strawberry.field
    @staticmethod
    async def product_media_item(info, id: int) -> "ProductMedia" | None:
        return await ProductMediaService(info.context.session).get_product_medium(
            ProductMediaFilter(id=id)
        )

@strawberry.type
class ProductMediaMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_product_media(
        info,
        product_id: int,
        shopify_media_id: int,
        id: int | None = None,
        media_type: str | None = None,
        src: str | None = None,
        position: int | None = None,
        alt: str | None = None,
    ) -> "ProductMedia":
        return await ProductMediaService(info.context.session).upsert_product_media(
            ProductMedia(
                id=id,
                product_id=product_id,
                shopify_media_id=shopify_media_id,
                media_type=media_type,
                src=src,
                position=position,
                alt=alt,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_product_media(info, id: int) -> bool:
        return await ProductMediaService(info.context.session).delete_product_media(
            ProductMedia(id=id)
        )

@strawberry.type
class ProductMediaSubscriptions:
    @strawberry.subscription
    async def product_media_created(self, info) -> AsyncGenerator[ProductMedia, None]:
        yield

    @strawberry.subscription
    async def product_media_updated(self, info) -> AsyncGenerator[ProductMedia, None]:
        yield

    @strawberry.subscription
    async def product_media_deleted(self, info) -> AsyncGenerator[int, None]:
        yield