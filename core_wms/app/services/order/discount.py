import logging
from typing import final, List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from core_wms.app.sqlalchemy.models.order_discounts import OrderDiscount

logger = logging.getLogger(__name__)

@final
class OrderDiscountService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_order_discounts(self) -> List[OrderDiscount]:
        result = await self.session.execute(select(OrderDiscount))
        return result.scalars().all()

    async def upsert_order_discount(self, args: dict) -> OrderDiscount:
        try:
            order_discount = None
            if args.get('id'):
                result = await self.session.execute(
                    select(OrderDiscount).where(
                        OrderDiscount.order_id == args.get('order_id'),
                        OrderDiscount.shopify_discount_id == args.get('shopify_discount_id')
                    )
                )
                order_discount = result.scalars().first()

            if order_discount:
                for key, value in args.items():
                    if hasattr(order_discount, key):
                        setattr(order_discount, key, value)
            else:
                order_discount = OrderDiscount(**args)
                self.session.add(order_discount)

            await self.session.commit()
            await self.session.refresh(order_discount)
            return order_discount
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_order_discount failed: {e}")
            raise

    async def delete_order_discount(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(OrderDiscount).where(OrderDiscount.id == id)
            )
            order_discount = result.scalars().first()

            if order_discount:
                await self.session.delete(order_discount)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_order_discount failed: {e}")
            raise