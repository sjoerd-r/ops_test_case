import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.order_taxes import OrderTax

logger = logging.getLogger(__name__)

@final
class OrderTaxService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_order_taxes(self) -> List[OrderTax]:
        try:
            result = await self.session.execute(select(OrderTax))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_order_taxes failed: {e}")
            raise

    async def upsert_order_tax(self, args: dict) -> OrderTax:
        try:
            order_tax = None
            if args.get('id'):
                result = await self.session.execute(
                    select(OrderTax).where(OrderTax.id == args['id'])
                )
                order_tax = result.scalars().first()

            if order_tax:
                for key, value in args.items():
                    if hasattr(order_tax, key) and value is not None:
                        setattr(order_tax, key, value)
            else:
                order_tax = OrderTax(**args)
                self.session.add(order_tax)

            await self.session.commit()
            await self.session.refresh(order_tax)
            return order_tax
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_order_tax failed: {e}")
            raise
    
    async def delete_order_tax(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(OrderTax).where(OrderTax.id == id)
            )
            order_tax = result.scalars().first()

            if order_tax:
                await self.session.delete(order_tax)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_order_tax failed: {e}")
            raise