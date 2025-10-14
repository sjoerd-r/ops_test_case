import logging
from typing import final, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from core_wms.app.sqlalchemy.models.order_refunds import OrderRefund

logger = logging.getLogger(__name__)

@final
class OrderRefundService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_order_refunds(self) -> List[OrderRefund]:
        try:
            result = await self.session.execute(select(OrderRefund))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_order_refunds failed: {e}")
            raise

    async def upsert_order_refund(self, args: dict) -> OrderRefund:
        try:
            order_refund = await self.session.execute(select(OrderRefund).where(
                OrderRefund.order_id == args.get('order_id'),
                OrderRefund.shopify_refund_id == args.get('shopify_refund_id')
            ))
            order_refund = order_refund.first()

            if order_refund:
                for key, value in args.items():
                    if hasattr(order_refund, key):
                        setattr(order_refund, key, value)
            else:
                order_refund = OrderRefund(**args)
                self.session.add(order_refund)

            await self.session.commit()
            await self.session.refresh(order_refund)
            return order_refund
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_order_refund failed: {e}")
            raise

    async def delete_order_refund(self, id: int) -> bool:
        try:
            order_refund = await self.session.execute(select(OrderRefund).where(
                OrderRefund.id == id
            ))
            order_refund = order_refund.first()

            if order_refund:
                await self.session.delete(order_refund)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_order_refund failed: {e}")
            raise