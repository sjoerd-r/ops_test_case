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

import ops.app.sqlalchemy.models.bins as bins

from ops.app.services.bin.position import (
    BinPositionService as BinPosition,
)

from ops.app.services.bin.dto import (
    Bin,
    BinInput,
    BinPositionInput,
    BinFilter,
    BinRelated,
)

logger = logging.getLogger(__name__)


@final
class BinService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)
        self.position = BinPosition(session)

    async def get_bins(self) -> list[Bin]:
        async with self.session.begin():
            result = await self.session.execute(select(bins.Bin))
            stmt = result.scalars().all()

            return validate_list(Bin, stmt)

    async def get_bin(self, bin: BinFilter) -> Bin | None:
        async with self.session.begin():
            result = await self.session.execute(
                select(bins.Bin).where(bins.Bin.id == bin.id)
            )
            stmt = result.scalar_one_or_none()

            return validate_single(Bin, stmt) if stmt else None

    async def upsert_bin(
        self, bin: BinInput, related: BinRelated = None
    ) -> Bin:
        pass

    async def _process_related(self, bin_id: int, related: BinRelated) -> None:
        if related.positions:
            for position in related.positions:
                await self.position.upsert_bin_position(
                    BinPositionInput(**position.model_dump(), bin_id=bin_id)
                )

    async def delete_bin(self, bin: BinInput) -> bool:
        async with self.session.begin():
            result = await self.session.execute(
                delete(bins.Bin).where(bins.Bin.id == bin.id)
            )
            return result.rowcount > 0
