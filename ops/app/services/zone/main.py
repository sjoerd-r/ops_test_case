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

import ops.app.sqlalchemy.models.zones as zones

from ops.app.services.zone.dto import Zone, ZoneInput, ZoneFilter

logger = logging.getLogger(__name__)


@final
class ZoneService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_zones(self) -> list[Zone]:
        async with self.session.begin():
            result = await self.session.execute(select(zones.Zone))
            stmt = result.scalars().all()

            return validate_list(Zone, stmt)

    async def get_zone(self, zone: ZoneFilter) -> Zone | None:
        async with self.session.begin():
            result = await self.session.execute(
                select(zones.Zone).where(zones.Zone.id == zone.id)
            )
            stmt = result.scalar_one_or_none()

            return validate_single(Zone, stmt) if stmt else None

    async def upsert_zone(self, zone: ZoneInput) -> Zone:
        async with self.session.begin():
            existing_zone = await self.session.get(zones.Zone, zone.id)
            if existing_zone:
                for key, value in zone.dict(
                    exclude_unset=True, exclude_none=True, exclude={'id'}
                ).items():
                    setattr(existing_zone, key, value)
                return validate_single(Zone, existing_zone)
            else:
                new_zone = zones.Zone(**zone.dict())
                self.session.add(new_zone)
                return validate_single(Zone, new_zone)

    async def delete_zone(self, zone: ZoneInput) -> bool: 
        async with self.session.begin():
            result = await self.session.execute(
                delete(zones.Zone).where(zones.Zone.id == zone.id)
            )
            return result.rowcount > 0
