import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.inventory_levels import InventoryLevel

logger = logging.getLogger(__name__)

@final
class InventoryLevelService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_inventory_levels(self) -> List[InventoryLevel]:
        try:
            result = await self.session.execute(select(InventoryLevel))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_inventory_levels failed: {e}")
            raise

    async def upsert_inventory_level(self, args: dict) -> InventoryLevel:
        try:
            inventory_level = None
            if args.get('id'):
                result = await self.session.execute(
                    select(InventoryLevel).where(InventoryLevel.id == args['id'])
                )
                inventory_level = result.scalars().first()

            if inventory_level:
                for key, value in args.items():
                    if hasattr(inventory_level, key) and value is not None:
                        setattr(inventory_level, key, value)
            else:
                inventory_level = InventoryLevel(**args)
                self.session.add(inventory_level)
            
            await self.session.commit()
            await self.session.refresh(inventory_level)
            return inventory_level
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_inventory_level failed: {e}")
            raise
    
    async def delete_inventory_level(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(InventoryLevel).where(InventoryLevel.id == id)
            )
            inventory_level = result.scalars().first()

            if inventory_level:
                await self.session.delete(inventory_level)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_inventory_level failed: {e}")
            raise