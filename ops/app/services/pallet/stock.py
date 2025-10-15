import logging
from typing import final
from sqlmodel import select, SQLModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime

from ops.app.services.base import BaseService

from ops.app.utils.validation import (
    validate_list,
    validate_single,
)

import ops.app.sqlalchemy.models.pallet_stock as pallet_stock

from ops.app.services.pallet.dto import (
    PalletStock,
    PalletStockInput,
    PalletStockFilter,
)

logger = logging.getLogger(__name__)


@final
class PalletStockService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_pallet_stocks(
        self, stock: PalletStockFilter = None
    ) -> list[PalletStock]:
        async with self.session.begin():
            query = select(pallet_stock.PalletStock)
            
            if stock and stock.pallet_id:
                query = query.where(pallet_stock.PalletStock.pallet_id == stock.pallet_id)
            
            result = await self.session.execute(query)
            stmt = result.scalars().all()

            return validate_list(PalletStock, stmt)

    async def get_pallet_stock(
        self, stock: PalletStockFilter
    ) -> PalletStock | None:
        async with self.session.begin():
            result = await self.session.execute(
                select(pallet_stock.PalletStock).where(
                    pallet_stock.PalletStock.id == stock.id
                )
            )
            stmt = result.scalar_one_or_none()

            return validate_single(PalletStock, stmt) if stmt else None

    async def upsert_pallet_stock(
        self, stock: PalletStockInput
    ) -> PalletStock:
        async with self.session.begin():
            existing_stock = None
            
            if stock.id is not None:
                existing_stock = await self.session.get(pallet_stock.PalletStock, stock.id)
            elif stock.pallet_id:
                result = await self.session.execute(
                    select(pallet_stock.PalletStock).where(
                        pallet_stock.PalletStock.pallet_id == stock.pallet_id
                    )
                )
                existing_stock = result.scalar_one_or_none()
            
            if existing_stock:
                for key, value in stock.model_dump(
                    exclude_unset=True, exclude_none=True, exclude={'id', 'created_at', 'updated_at'}
                ).items():
                    setattr(existing_stock, key, value)
                existing_stock.updated_at = datetime.utcnow()
                await self.session.flush()
                await self.session.refresh(existing_stock)
                return validate_single(PalletStock, existing_stock)
            else:
                stock_data = stock.model_dump(exclude={'id', 'inventory_item_id', 'product_variant_id', 'purchase_order_line_item_id'})
                new_stock = pallet_stock.PalletStock(**stock_data)
                self.session.add(new_stock)
                await self.session.flush()
                await self.session.refresh(new_stock)
                return validate_single(PalletStock, new_stock)

    async def delete_pallet_stock(self, stock: PalletStockInput) -> bool:
        async with self.session.begin():
            result = await self.session.execute(
                delete(pallet_stock.PalletStock).where(
                    pallet_stock.PalletStock.id == stock.id
                )
            )
            return result.rowcount > 0
