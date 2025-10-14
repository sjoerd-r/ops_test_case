from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
import logging

from core_wms.app.sqlalchemy.models.warehouses import Warehouse

logger = logging.getLogger(__name__)

@final
class WarehouseService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_warehouses(self) -> List[Warehouse]:
        try:
            result = await self.session.execute(select(Warehouse))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_warehouses failed: {e}")
            raise
    
    async def upsert_warehouse(self, args: dict) -> Warehouse:
        try:
            warehouse = None
            if args.get('id'):
                result = await self.session.execute(
                    select(Warehouse).where(Warehouse.id == args['id'])
                )
                warehouse = result.scalars().first()

            if warehouse:
                for key, value in args.items():
                    if hasattr(warehouse, key) and value is not None:
                        setattr(warehouse, key, value)
            else:
                warehouse = Warehouse(**args)
                self.session.add(warehouse)
            
            await self.session.commit()
            await self.session.refresh(warehouse)
            return warehouse
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_warehouse failed: {e}")
            raise
    
    async def delete_warehouse(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(Warehouse).where(Warehouse.id == id)
            )
            warehouse = result.scalars().first()

            if warehouse:
                await self.session.delete(warehouse)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_warehouse failed: {e}")
            raise