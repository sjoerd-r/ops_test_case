import logging
from typing import final, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from core_wms.app.sqlalchemy.models.order_shipping_lines import OrderShippingLine

logger = logging.getLogger(__name__)

@final
class OrderShippingLineService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_order_shipping_lines(self) -> List[OrderShippingLine]:
        result = await self.session.execute(select(OrderShippingLine))
        return result.scalars().all()
    
    async def upsert_order_shipping_line(self, args: dict) -> OrderShippingLine:
        try:
            order_shipping_line = None
            if args.get('id'):
                result = await self.session.execute(
                    select(OrderShippingLine).where(OrderShippingLine.id == args['id'])
                )
                order_shipping_line = result.scalars().first()

            if order_shipping_line:
                for key, value in args.items():
                    if hasattr(order_shipping_line, key):
                        setattr(order_shipping_line, key, value)
            else:
                order_shipping_line = OrderShippingLine(**args)
                self.session.add(order_shipping_line)

            await self.session.commit()
            await self.session.refresh(order_shipping_line)
            return order_shipping_line
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_order_shipping_line failed: {e}")
            raise

    async def delete_order_shipping_line(self, id: int) -> bool:
        try:
            order_shipping_line = await self.session.execute(
                select(OrderShippingLine).where(OrderShippingLine.id == id)
            )
            order_shipping_line = order_shipping_line.first()

            if order_shipping_line:
                await self.session.delete(order_shipping_line)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_order_shipping_line failed: {e}")
            raise