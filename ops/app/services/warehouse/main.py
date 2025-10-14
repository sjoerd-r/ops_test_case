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

import ops.app.sqlalchemy.models.warehouses as warehouses

from ops.app.services.warehouse.dto import (
    Warehouse,
    WarehouseInput,
    WarehouseFilter,
)

logger = logging.getLogger(__name__)


@final
class WarehouseService(BaseService):
    def __init__(self, session: AsyncSession):
        super().__init__(session)

    async def get_warehouses(self) -> list[Warehouse]:
        async with self.session.begin():
            result = await self.session.execute(select(warehouses.Warehouse))
            stmt = result.scalars().all()

            return validate_list(Warehouse, stmt)

    async def get_warehouse(
        self, warehouse: WarehouseFilter
    ) -> Warehouse | None:
        async with self.session.begin():
            result = await self.session.execute(
                select(warehouses.Warehouse).where(
                    warehouses.Warehouse.id == warehouse.id
                )
            )
            stmt = result.scalar_one_or_none()

            return validate_single(Warehouse, stmt) if stmt else None

    async def upsert_warehouse(self, warehouse: WarehouseInput) -> Warehouse:
        pass

    async def delete_warehouse(self, warehouse: WarehouseInput) -> bool:
        async with self.session.begin():
            result = await self.session.execute(
                delete(warehouses.Warehouse).where(
                    warehouses.Warehouse.id == warehouse.id
                )
            )
            return result.rowcount > 0
