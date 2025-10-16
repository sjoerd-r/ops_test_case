import logging
from typing import final
from datetime import datetime
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
            query = select(pallets.Pallet)
            
            if pallet.id is not None:
                query = query.where(pallets.Pallet.id == pallet.id)
            elif pallet.code is not None:
                query = query.where(pallets.Pallet.code == pallet.code)
            else:
                return None
            
            result = await self.session.execute(query)
            stmt = result.scalar_one_or_none()

            return validate_single(Pallet, stmt) if stmt else None

    async def upsert_pallet(
        self, pallet: PalletInput, related: PalletRelated = None
    ) -> Pallet:
        async with self.session.begin():
            existing_pallet = None
            
            if pallet.id is not None:
                existing_pallet = await self.session.get(pallets.Pallet, pallet.id)
            elif pallet.code:
                result = await self.session.execute(
                    select(pallets.Pallet).where(pallets.Pallet.code == pallet.code)
                )
                existing_pallet = result.scalar_one_or_none()
            
            if existing_pallet:
                for key, value in pallet.model_dump(
                    exclude_unset=True, exclude_none=True, exclude={'id', 'created_at', 'updated_at'}
                ).items():
                    setattr(existing_pallet, key, value)
                existing_pallet.updated_at = datetime.utcnow()
                await self.session.flush()
                await self.session.refresh(existing_pallet)
                
                if related:
                    await self._process_related(existing_pallet.id, related)
                
                return validate_single(Pallet, existing_pallet)
            else:
                pallet_data = pallet.model_dump(exclude={'id', 'batch_id', 'product_variant_id', 'purchase_order_line_item_id'})
                new_pallet = pallets.Pallet(**pallet_data)
                self.session.add(new_pallet)
                await self.session.flush()
                await self.session.refresh(new_pallet)
                
                if related:
                    await self._process_related(new_pallet.id, related)
                
                return validate_single(Pallet, new_pallet)

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
