import logging
from typing import final
from sqlmodel import select, SQLModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

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
        self, stock: PalletStockFilter
    ) -> list[PalletStock]:
        async with self.session.begin():
            result = await self.session.execute(
                select(pallet_stock.PalletStock).where(
                    pallet_stock.PalletStock.pallet_id == stock.pallet_id
                )
            )
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
        pass

    async def delete_pallet_stock(self, stock: PalletStockInput) -> bool:
        async with self.session.begin():
            result = await self.session.execute(
                delete(pallet_stock.PalletStock).where(
                    pallet_stock.PalletStock.id == stock.id
                )
            )
            return result.rowcount > 0
