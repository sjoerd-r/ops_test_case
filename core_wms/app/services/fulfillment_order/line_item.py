import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.fulfillment_order_line_items import FulfillmentOrderLineItem

logger = logging.getLogger(__name__)

@final
class FulfillmentOrderLineItemService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_fulfillment_order_line_items(self) -> List[FulfillmentOrderLineItem]:
        try:
            result = await self.session.execute(select(FulfillmentOrderLineItem))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_fulfillment_order_line_items failed: {e}")
            raise

    async def upsert_fulfillment_order_line_item(self, args: dict) -> FulfillmentOrderLineItem:
        try:
            fulfillment_order_line_item = None
            if args.get('id'):
                result = await self.session.execute(
                    select(FulfillmentOrderLineItem).where(FulfillmentOrderLineItem.id == args['id'])
                )
                fulfillment_order_line_item = result.scalars().first()

            if fulfillment_order_line_item:
                for key, value in args.items():
                    if hasattr(fulfillment_order_line_item, key) and value is not None:
                        setattr(fulfillment_order_line_item, key, value)
            else:
                fulfillment_order_line_item = FulfillmentOrderLineItem(**args)
                self.session.add(fulfillment_order_line_item)
            
            await self.session.commit()
            await self.session.refresh(fulfillment_order_line_item)
            return fulfillment_order_line_item
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_fulfillment_order_line_item failed: {e}")
            raise
    
    async def delete_fulfillment_order_line_item(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(FulfillmentOrderLineItem).where(FulfillmentOrderLineItem.id == id)
            )
            fulfillment_order_line_item = result.scalars().first()

            if fulfillment_order_line_item:
                await self.session.delete(fulfillment_order_line_item)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_fulfillment_order_line_item failed: {e}")
            raise
