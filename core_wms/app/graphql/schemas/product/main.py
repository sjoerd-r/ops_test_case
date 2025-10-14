import strawberry
from strawberry.field_extensions import InputMutationExtension
from datetime import datetime
from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated

from core_wms.app.services.product.main import ProductService
from core_wms.app.services.product.dto import Product, ProductFilter 

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.product.variant import ProductVariant
    from core_wms.app.graphql.schemas.product.option import ProductOption
    from core_wms.app.graphql.schemas.product.media import ProductMedia
    from core_wms.app.graphql.schemas.store.main import Store

@strawberry.type
class Product:
    id: int | None = None
    store_id: int | None = None
    shopify_product_id: int | None = None
    title: str | None = None
    body_html: str | None = None
    vendor: str | None = None
    product_type: str | None = None
    handle: str | None = None
    tags: str | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def store(self, info, parent: strawberry.Parent["Product"]) -> Annotated["Store", strawberry.lazy("core_wms.app.graphql.schemas.store")] | None:
        return await info.context.loaders.product.store.load(parent.store_id)

    @strawberry.field
    async def variants(self, info, parent: strawberry.Parent["Product"]) -> Annotated["ProductVariant", strawberry.lazy("core_wms.app.graphql.schemas.product.variant")] | None:
        return await info.context.loaders.product.variants.load(parent.id)

    @strawberry.field
    async def options(self, info, parent: strawberry.Parent["Product"]) -> Annotated["ProductOption", strawberry.lazy("core_wms.app.graphql.schemas.product.option")] | None:
        return await info.context.loaders.product.options.load(parent.id)

    @strawberry.field
    async def media(self, info, parent: strawberry.Parent["Product"]) -> Annotated["ProductMedia", strawberry.lazy("core_wms.app.graphql.schemas.product.media")] | None:
        return await info.context.loaders.product.media.load(parent.id)

@strawberry.type
class ProductQueries:
    @strawberry.field
    @staticmethod
    async def products(info, store_id: int, id: int | None = None) -> List["Product"]:
        return await ProductService(info.context.session).get_products(
            ProductFilter(store_id=store_id, id=id)
        )

    @strawberry.field
    @staticmethod
    async def product(info, id: int | None = None, store_id: int | None = None, shopify_product_id: int | None = None) -> "Product" | None:
        return await ProductService(info.context.session).get_product(
            ProductFilter(id=id, store_id=store_id, shopify_product_id=shopify_product_id)
        )

@strawberry.type
class ProductMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_product(
        info,
        store_id: int,
        shopify_product_id: int,
        title: str | None = None,
        body_html: str | None = None,
        vendor: str | None = None,
        product_type: str | None = None,
        handle: str | None = None,
        tags: str | None = None,
    ) -> "Product":
        return await ProductService(info.context.session).upsert_product(
            Product(
                store_id=store_id,
                shopify_product_id=shopify_product_id,
                title=title,
                body_html=body_html,
                vendor=vendor,
                product_type=product_type,
                handle=handle,
                tags=tags,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_product(info, store_id: int, shopify_product_id: int) -> bool:
        return await ProductService(info.context.session).delete_product(
            Product(store_id=store_id, shopify_product_id=shopify_product_id)
        )

@strawberry.type
class ProductSubscriptions:
    @strawberry.subscription
    async def product_created(self, info) -> AsyncGenerator[Product, None]:
        yield

    @strawberry.subscription
    async def product_updated(self, info) -> AsyncGenerator[Product, None]:
        yield

    @strawberry.subscription
    async def product_deleted(self, info) -> AsyncGenerator[int, None]:
        yield