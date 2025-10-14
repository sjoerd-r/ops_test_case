import logging
from typing import final, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from core_wms.app.sqlalchemy.models.order_fulfillments import OrderFulfillment

logger = logging.getLogger(__name__)

@final
class OrderFulfillmentService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_order_fulfillments(self) -> List[OrderFulfillment]:
        result = await self.session.execute(select(OrderFulfillment))
        return result.scalars().all()

    async def upsert_order_fulfillment(self, args: dict) -> OrderFulfillment:
        try:
            order_fulfillment = await self.session.execute(select(OrderFulfillment).where(
                OrderFulfillment.order_id == args.get('order_id'),
                OrderFulfillment.fulfillment_id == args.get('fulfillment_id')
            ))
            order_fulfillment = order_fulfillment.first()

            if order_fulfillment:
                for key, value in args.items():
                    if hasattr(order_fulfillment, key):
                        setattr(order_fulfillment, key, value)
            else:
                order_fulfillment = OrderFulfillment(**args)
                self.session.add(order_fulfillment)

            await self.session.commit()
            await self.session.refresh(order_fulfillment)
            return order_fulfillment
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_order_fulfillment failed: {e}")
            raise

    async def delete_order_fulfillment(self, id: int) -> bool:
        try:
            order_fulfillment = await self.session.execute(select(OrderFulfillment).where(OrderFulfillment.id == id))
            order_fulfillment = order_fulfillment.first()

            if order_fulfillment:
                await self.session.delete(order_fulfillment)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_order_fulfillment failed: {e}")
            raise