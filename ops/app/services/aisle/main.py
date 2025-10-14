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

import ops.app.sqlalchemy.models.aisles as aisles

from ops.app.services.aisle.dto import (
    Aisle,
    AisleInput,
    AisleFilter,
)

logger = logging.getLogger(__name__)


@final
class AisleService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_aisles(self) -> list[Aisle]:
        async with self.session.begin():
            result = await self.session.execute(select(aisles.Aisle))
            stmt = result.scalars().all()

            return validate_list(Aisle, stmt)

    async def get_aisle(self, aisle: AisleFilter) -> Aisle | None:
        pass

    async def upsert_aisle(self, aisle: AisleInput) -> Aisle:
        pass

    async def delete_aisle(self, aisle: AisleInput) -> bool:
        async with self.session.begin():
            result = await self.session.execute(
                delete(aisles.Aisle).where(aisles.Aisle.id == aisle.id)
            )
            return result.rowcount > 0
