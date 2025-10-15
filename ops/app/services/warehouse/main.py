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
        async with self.session.begin():
            if warehouse.id is not None:
                existing_warehouse = await self.session.get(warehouses.Warehouse, warehouse.id)
            else:
                existing_warehouse = None
            
            if existing_warehouse:
                for key, value in warehouse.model_dump(
                    exclude_unset=True, exclude_none=True, exclude={'id'}
                ).items():
                    setattr(existing_warehouse, key, value)
                existing_warehouse.updated_at = datetime.utcnow()
                await self.session.flush()
                await self.session.refresh(existing_warehouse)
                return validate_single(Warehouse, existing_warehouse)
            else:
                new_warehouse = warehouses.Warehouse(**warehouse.model_dump())
                self.session.add(new_warehouse)
                await self.session.flush()
                await self.session.refresh(new_warehouse)
                return validate_single(Warehouse, new_warehouse)

    async def delete_warehouse(self, warehouse: WarehouseInput) -> bool:
        async with self.session.begin():
            result = await self.session.execute(
                delete(warehouses.Warehouse).where(
                    warehouses.Warehouse.id == warehouse.id
                )
            )
            return result.rowcount > 0
