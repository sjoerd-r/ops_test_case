import strawberry
from strawberry.field_extensions import InputMutationExtension
from typing import AsyncGenerator, List, TYPE_CHECKING, Annotated
from datetime import datetime

from core_wms.app.services.product.option import ProductOptionService
from core_wms.app.services.product.dto import ProductOption, ProductOptionFilter

if TYPE_CHECKING:
    from core_wms.app.graphql.schemas.product.main import Product

@strawberry.type
class ProductOption:
    id: int | None = None
    product_id: int | None = None
    shopify_option_id: int | None = None
    name: str | None = None
    position: int | None = None
    values: List[str] | None = None
    created_at: datetime | None = None
    updated_at: datetime | None = None

    @strawberry.field
    async def product(self, parent: strawberry.Parent["ProductOption"], info) -> Annotated["Product", strawberry.lazy("core_wms.app.graphql.schemas.product.main")] | None:
        return await info.context.loaders.product_option.product.load(parent.product_id)

@strawberry.type
class ProductOptionQueries:
    @strawberry.field
    @staticmethod
    async def product_options(info, id: int | None = None, product_id: int | None = None, shopify_option_id: int | None = None) -> List["ProductOption"]:
        return await ProductOptionService(info.context.session).get_product_options(
            ProductOptionFilter(id=id, product_id=product_id, shopify_option_id=shopify_option_id)
        )
        
    @strawberry.field
    @staticmethod
    async def product_option(info, id: int) -> "ProductOption" | None:
        return await ProductOptionService(info.context.session).get_product_option(
            ProductOptionFilter(id=id)
        )

@strawberry.type
class ProductOptionMutations:
    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def upsert_product_option(
        info,
        product_id: int,
        shopify_option_id: int,
        id: int | None = None,
        name: str | None = None,
        position: int | None = None,
        values: List[str] | None = None,
    ) -> "ProductOption":
        return await ProductOptionService(info.context.session).upsert_product_option(
            ProductOption(
                id=id,
                product_id=product_id,
                shopify_option_id=shopify_option_id,
                name=name,
                position=position,
                values=values,
            )
        )

    @strawberry.mutation(extensions=[InputMutationExtension()])
    @staticmethod
    async def delete_product_option(info, id: int) -> bool:
        return await ProductOptionService(info.context.session).delete_product_option(
            ProductOption(id=id)
        )

@strawberry.type
class ProductOptionSubscriptions:
    @strawberry.subscription
    async def product_option_created(self, info) -> AsyncGenerator[ProductOption, None]:
        yield

    @strawberry.subscription
    async def product_option_updated(self, info) -> AsyncGenerator[ProductOption, None]:
        yield

    @strawberry.subscription
    async def product_option_deleted(self, info) -> AsyncGenerator[int, None]:
        yield