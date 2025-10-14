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

import ops.app.sqlalchemy.models.bin_positions as bin_positions

from ops.app.services.bin.dto import (
    BinPosition,
    BinPositionInput,
    BinPositionFilter,
)

logger = logging.getLogger(__name__)


@final
class BinPositionService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_bin_positions(self) -> list[BinPosition]:
        async with self.session.begin():
            result = await self.session.execute(
                select(bin_positions.BinPosition)
            )
            stmt = result.scalars().all()

            return validate_list(BinPosition, stmt)

    async def get_bin_position(
        self, position: BinPositionFilter
    ) -> BinPosition | None:
        async with self.session.begin():
            result = await self.session.execute(
                select(bin_positions.BinPosition).where(
                    bin_positions.BinPosition.id == position.id
                )
            )
            stmt = result.scalar_one_or_none()

            return validate_single(BinPosition, stmt) if stmt else None

    async def upsert_bin_position(
        self, position: BinPositionInput
    ) -> BinPosition:
        pass

    async def delete_bin_position(self, position: BinPositionInput) -> bool:
        async with self.session.begin():
            result = await self.session.execute(
                delete(bin_positions.BinPosition).where(
                    bin_positions.BinPosition.id == position.id
                )
            )
            return result.rowcount > 0
