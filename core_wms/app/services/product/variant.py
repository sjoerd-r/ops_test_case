import logging
from typing import List
from typing_extensions import final
from sqlmodel import select, SQLModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

import core_wms.app.sqlalchemy.models.product_variants as models
from core_wms.app.services.base import BaseService
from core_wms.app.services.product.dto import ProductVariant, ProductVariantFilter

logger = logging.getLogger(__name__)

@final
class ProductVariantService(BaseService):
    
    def __init__(self, session: AsyncSession):
        super().__init__(session)
    
    async def get_product_variants(self, variant: ProductVariantFilter) -> List[ProductVariant]:
        async with self.session.begin():
            stmt = await self.session.exec(
                select(models.ProductVariant).where(models.ProductVariant.product_id == variant.product_id)
            ).all()
            
            return ProductVariant.model_validate(stmt, many=True)

    async def get_product_variant(self, variant: ProductVariantFilter) -> ProductVariant | None:
        async with self.session.begin():
            stmt = await self.session.exec(
                select(models.ProductVariant).where(
                    models.ProductVariant.id == variant.id
                )
            ).one_or_none()
            
            return ProductVariant.model_validate(stmt) if stmt else None

    async def upsert_product_variant(self, variant: ProductVariant) -> ProductVariant:
        async with self.session.begin():
            stmt = await self.session.exec(
                select(models.ProductVariant).where(
                    models.ProductVariant.product_id == variant.product_id,
                    models.ProductVariant.shopify_variant_id == variant.shopify_variant_id
                )
            ).one_or_none()
            
            stmt = stmt or models.ProductVariant()
            SQLModel.update(stmt, variant.model_dump(exclude_none=True))
            
            if not stmt.id:
                self.session.add(stmt)
            
            await self.session.flush()
            
            return ProductVariant.model_validate(stmt)
    
    async def delete_product_variant(self, variant: ProductVariant) -> bool:
        async with self.session.begin():
            stmt = await self.session.exec(
                delete(models.ProductVariant).where(
                    models.ProductVariant.product_id == variant.product_id,
                    models.ProductVariant.shopify_variant_id == variant.shopify_variant_id
                )
            )
            return stmt.rowcount > 0