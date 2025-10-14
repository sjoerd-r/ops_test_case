import logging
from typing import List
from typing_extensions import final
from sqlmodel import select, SQLModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

import core_wms.app.sqlalchemy.models.product_options as models
from core_wms.app.services.base import BaseService
from core_wms.app.services.product.dto import ProductOption, ProductOptionFilter

logger = logging.getLogger(__name__)

@final
class ProductOptionService(BaseService):
    
    def __init__(self, session: AsyncSession):
        super().__init__(session)
    
    async def get_product_options(self, option: ProductOptionFilter) -> List[ProductOption]:
        async with self.session.begin():
            stmt = await self.session.exec(
                select(models.ProductOption).where(models.ProductOption.product_id == option.product_id)
            ).all()
            
            return ProductOption.model_validate(stmt, many=True)

    async def get_product_option(self, option: ProductOptionFilter) -> ProductOption | None:
        async with self.session.begin():
            stmt = await self.session.exec(
                select(models.ProductOption).where(
                    models.ProductOption.id == option.id
                )
            ).one_or_none()
            
            return ProductOption.model_validate(stmt) if stmt else None

    async def upsert_product_option(self, option: ProductOption) -> ProductOption:
        async with self.session.begin():
            stmt = await self.session.exec(
                select(models.ProductOption).where(
                    models.ProductOption.product_id == option.product_id,
                    models.ProductOption.shopify_option_id == option.shopify_option_id
                )
            ).one_or_none()
            
            stmt = stmt or models.ProductOption()
            SQLModel.update(stmt, option.model_dump(exclude_none=True))
            
            if not stmt.id:
                self.session.add(stmt)
            
            await self.session.flush()
            
            return ProductOption.model_validate(stmt)
    
    async def delete_product_option(self, option: ProductOption) -> bool:
        async with self.session.begin():
            stmt = await self.session.exec(
                delete(models.ProductOption).where(
                    models.ProductOption.product_id == option.product_id,
                    models.ProductOption.shopify_option_id == option.shopify_option_id
                )
            )
            return stmt.rowcount > 0