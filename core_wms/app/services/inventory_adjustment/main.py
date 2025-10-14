import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.inventory_adjustments import InventoryAdjustment

logger = logging.getLogger(__name__)

@final
class InventoryAdjustmentService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_inventory_adjustments(self) -> List[InventoryAdjustment]:
        try:
            result = await self.session.execute(select(InventoryAdjustment))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_inventory_adjustments failed: {e}")
            raise
    
    async def upsert_inventory_adjustment(self, args: dict) -> InventoryAdjustment:
        try:
            inventory_adjustment = None
            if args.get('id'):
                result = await self.session.execute(
                    select(InventoryAdjustment).where(InventoryAdjustment.id == args['id'])
                )
                inventory_adjustment = result.scalars().first()

            if inventory_adjustment:
                for key, value in args.items():
                    if hasattr(inventory_adjustment, key) and value is not None:
                        setattr(inventory_adjustment, key, value)
            else:
                inventory_adjustment = InventoryAdjustment(**args)
                self.session.add(inventory_adjustment)
            
            await self.session.commit()
            await self.session.refresh(inventory_adjustment)
            return inventory_adjustment
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_inventory_adjustment failed: {e}")
            raise
    
    async def delete_inventory_adjustment(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(InventoryAdjustment).where(InventoryAdjustment.id == id)
            )
            inventory_adjustment = result.scalars().first()

            if inventory_adjustment:
                await self.session.delete(inventory_adjustment)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_inventory_adjustment failed: {e}")
            raise