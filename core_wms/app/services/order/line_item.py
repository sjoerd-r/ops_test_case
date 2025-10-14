import logging
from typing import final, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from core_wms.app.sqlalchemy.models.order_line_items import OrderLineItem

logger = logging.getLogger(__name__)

@final
class OrderLineItemService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_order_line_items(self) -> List[OrderLineItem]:
        try:
            result = await self.session.execute(select(OrderLineItem))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_order_line_items failed: {e}")
            raise

    async def upsert_order_line_item(self, args: dict) -> OrderLineItem:
        try:
            order_line_item = await self.session.execute(select(OrderLineItem).where(
                OrderLineItem.order_id == args.get('order_id'),
                OrderLineItem.shopify_line_item_id == args.get('shopify_line_item_id')
            ))
            order_line_item = order_line_item.first()

            if order_line_item:
                for key, value in args.items():
                    if hasattr(order_line_item, key):
                        setattr(order_line_item, key, value)
            else:
                order_line_item = OrderLineItem(**args)
                self.session.add(order_line_item)

            await self.session.commit()
            await self.session.refresh(order_line_item)
            return order_line_item
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_order_line_item failed: {e}")
            raise

    async def delete_order_line_item(self, id: int) -> bool:
        try:
            order_line_item = await self.session.execute(
                select(OrderLineItem).where(OrderLineItem.id == id)
            )
            order_line_item = order_line_item.first()

            if order_line_item:
                await self.session.delete(order_line_item)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_order_line_item failed: {e}")
            raise