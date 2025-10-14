import logging
from typing_extensions import final
from sqlmodel import select, SQLModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

import core_wms.app.sqlalchemy.models.products as products

from core_wms.app.services.base import BaseService

from core_wms.app.services.product.variant import ProductVariantService as ProductVariant
from core_wms.app.services.product.option import ProductOptionService as ProductOption
from core_wms.app.services.product.media import ProductMediaService as ProductMedia

from core_wms.app.services.product.dto import Product, ProductFilter, ProductRelations

logger = logging.getLogger(__name__)

@final
class ProductService(BaseService):
    
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.variant = ProductVariant(session)
        self.option = ProductOption(session)
        self.media = ProductMedia(session)

    async def get_products(self, product: ProductFilter) -> list[Product]:
        async with self.session.begin():
            stmt = await self.session.exec(
                select(products.Product).where(products.Product.store_id == product.store_id)
            ).all()
            
            return Product.model_validate(stmt, many=True)

    async def get_product(self, product: ProductFilter) -> Product | None:
        async with self.session.begin():
            stmt = await self.session.exec(
                select(products.Product).where(products.Product.store_id == product.store_id, products.Product.shopify_product_id == product.shopify_product_id)
            ).one_or_none()

            return Product.model_validate(stmt) if stmt else None

    async def upsert_product(self, product: Product, relations: ProductRelations = None) -> Product:
        async with self.session.begin():
            stmt = await self.session.exec(
                select(products.Product).where(
                    products.Product.store_id == product.store_id, products.Product.shopify_product_id == product.shopify_product_id
                )
            ).one_or_none()
            
            stmt = stmt or products.Product()
            SQLModel.update(stmt, product.model_dump(exclude_unset=True))
            
            if not stmt.id:
                self.session.add(stmt)

            await self.session.flush()

            if relations:
                await self._process_relations(stmt.id, relations)

            return Product.model_validate(stmt)

    async def _process_relations(self, product_id: int, product: ProductRelations) -> None:
        if product.variants:
            for variant in product.variants:
                variant.product_id = product_id
                await self.variant.upsert_product_variant(variant)

        if product.options:
            for option in product.options:
                option.product_id = product_id
                await self.option.upsert_product_option(option)
        
        if product.media:
            for media in product.media:
                media.product_id = product_id
                await self.media.upsert_product_media(media)

    async def delete_product(self, product: Product) -> bool:
        async with self.session.begin():
            statement = await self.session.exec(
                delete(products.Product).where(
                    products.Product.store_id == product.store_id, products.Product.shopify_product_id == product.shopify_product_id
                )
            )
            return statement.rowcount > 0