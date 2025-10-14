import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List
from typing_extensions import final
from core_wms.app.sqlalchemy.models.inventory_items import InventoryItem

logger = logging.getLogger(__name__)

@final
class InventoryItemService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_inventory_items(self) -> List[InventoryItem]:
        try:
            result = await self.session.execute(select(InventoryItem))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_inventory_items failed: {e}")
            raise

    async def upsert_inventory_item(self, args: dict) -> InventoryItem:
        try:
            inventory_item = None
            if args.get('id'):
                result = await self.session.execute(
                    select(InventoryItem).where(InventoryItem.id == args['id'])
                )
                inventory_item = result.scalars().first()

            if inventory_item:
                for key, value in args.items():
                    if hasattr(inventory_item, key):
                        setattr(inventory_item, key, value)
            else:
                inventory_item = InventoryItem(**args)
                self.session.add(inventory_item)
                
            await self.session.commit()
            await self.session.refresh(inventory_item)
            return inventory_item
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_inventory_item failed: {e}")
            raise

    async def delete_inventory_item(self, id: int) -> bool:
        try:
            result = await self.session.execute(select(InventoryItem).where(
                InventoryItem.id == id)
            )
            inventory_item = result.scalars().first()

            if inventory_item:
                await self.session.delete(inventory_item)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_inventory_item failed: {e}")
            raise