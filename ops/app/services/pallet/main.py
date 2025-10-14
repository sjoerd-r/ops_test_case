import logging
from typing import final
from sqlmodel import select, SQLModel
from sqlalchemy import delete
from sqlalchemy.ext.asyncio import AsyncSession

from ops.app.utils.validation import (
    validate_list,
    validate_single,
)

from ops.app.services.base import BaseService

import ops.app.sqlalchemy.models.pallets as pallets

from ops.app.services.pallet.stock import (
    PalletStockService as PalletStock,
)

from ops.app.services.pallet.dto import (
    Pallet,
    PalletInput,
    PalletStockInput,
    PalletFilter,
    PalletRelated,
)

logger = logging.getLogger(__name__)


@final
class PalletService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.stock = PalletStock(session)

    async def get_pallets(self) -> list[Pallet]:
        async with self.session.begin():
            result = await self.session.execute(select(pallets.Pallet))
            stmt = result.scalars().all()

            return validate_list(Pallet, stmt)

    async def get_pallet(self, pallet: PalletFilter) -> Pallet | None:
        async with self.session.begin():
            result = await self.session.execute(
                select(pallets.Pallet).where(pallets.Pallet.id == pallet.id)
            )
            stmt = result.scalar_one_or_none()

            return validate_single(Pallet, stmt) if stmt else None

    async def upsert_pallet(
        self, pallet: PalletInput, related: PalletRelated = None
    ) -> Pallet:
        pass

    async def _process_related(
        self, pallet_id: int, related: PalletRelated
    ) -> None:
        if related.stocks:
            for stock in related.stocks:
                await self.stock.upsert_pallet_stock(
                    PalletStockInput(**stock.model_dump(), pallet_id=pallet_id)
                )

    async def delete_pallet(self, pallet: PalletInput) -> bool:
        async with self.session.begin():
            result = await self.session.execute(
                delete(pallets.Pallet).where(pallets.Pallet.id == pallet.id)
            )
            return result.rowcount > 0
