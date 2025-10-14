import logging
from typing import List
from typing_extensions import final
from sqlmodel import select, SQLModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

import core_wms.app.sqlalchemy.models.product_media as models
from core_wms.app.services.base import BaseService
from core_wms.app.services.product.dto import ProductMedia, ProductMediaFilter

logger = logging.getLogger(__name__)

@final
class ProductMediaService(BaseService):
    
    def __init__(self, session: AsyncSession):
        super().__init__(session)
    
    async def get_product_media_items(self, media: ProductMediaFilter) -> List[ProductMedia]:
        async with self.session.begin():
            stmt = await self.session.exec(
                select(models.ProductMedia).where(models.ProductMedia.product_id == media.product_id)
            ).all()
            
            return ProductMedia.model_validate(stmt, many=True)
    
    async def get_product_media(self, media: ProductMediaFilter) -> ProductMedia | None:
        async with self.session.begin():
            stmt = await self.session.exec(
                select(models.ProductMedia).where(
                    models.ProductMedia.id == media.id
                )
            ).one_or_none()
            
            return ProductMedia.model_validate(stmt) if stmt else None

    async def upsert_product_media(self, media: ProductMedia) -> ProductMedia:
        async with self.session.begin():
            stmt = await self.session.exec(
                select(models.ProductMedia).where(
                    models.ProductMedia.product_id == media.product_id,
                    models.ProductMedia.shopify_media_id == media.shopify_media_id
                )
            ).one_or_none()
            
            stmt = stmt or models.ProductMedia()
            SQLModel.update(stmt, media.model_dump(exclude_none=True))
            
            if not stmt.id:
                self.session.add(stmt)
            
            await self.session.flush()
            
            return ProductMedia.model_validate(stmt)
    
    async def delete_product_media(self, media: ProductMedia) -> bool:
        async with self.session.begin():
            stmt = await self.session.exec(
                delete(models.ProductMedia).where(
                    models.ProductMedia.product_id == media.product_id,
                    models.ProductMedia.shopify_media_id == media.shopify_media_id
                )
            )
            return stmt.rowcount > 0