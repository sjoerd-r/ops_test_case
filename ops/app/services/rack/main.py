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

import ops.app.sqlalchemy.models.racks as racks

from ops.app.services.rack.dto import Rack, RackInput, RackFilter

logger = logging.getLogger(__name__)


@final
class RackService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_racks(self) -> list[Rack]:
        async with self.session.begin():
            result = await self.session.execute(select(racks.Rack))
            stmt = result.scalars().all()

            return validate_list(Rack, stmt)

    async def get_rack(self, rack: RackFilter) -> Rack | None:
        async with self.session.begin():
            result = await self.session.execute(
                select(racks.Rack).where(racks.Rack.id == rack.id)
            )
            stmt = result.scalar_one_or_none()

            return validate_single(Rack, stmt) if stmt else None

    async def upsert_rack(self, rack: RackInput) -> Rack:
        pass

    async def delete_rack(self, rack: RackInput) -> bool:
        async with self.session.begin():
            result = await self.session.execute(
                delete(racks.Rack).where(racks.Rack.id == rack.id)
            )
            return result.rowcount > 0
