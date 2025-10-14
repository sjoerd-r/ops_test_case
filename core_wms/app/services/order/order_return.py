import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.order_returns import OrderReturn

logger = logging.getLogger(__name__)

@final
class OrderReturnService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_order_returns(self) -> List[OrderReturn]:
        try:
            result = await self.session.execute(select(OrderReturn))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_order_returns failed: {e}")
            raise

    async def upsert_order_return(self, args: dict) -> OrderReturn:
        try:
            order_return = None
            if args.get('id'):
                result = await self.session.execute(
                    select(OrderReturn).where(OrderReturn.id == args['id'])
                )
                order_return = result.scalars().first()
            
            if order_return:
                for key, value in args.items():
                    if hasattr(order_return, key) and value is not None:
                        setattr(order_return, key, value)
            else:
                order_return = OrderReturn(**args)
                self.session.add(order_return)
            
            await self.session.commit()
            await self.session.refresh(order_return)
            return order_return
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_order_return failed: {e}")
            raise
    
    async def delete_order_return(self, id: int) -> bool:
        try:
            order_return = await self.session.execute(
                select(OrderReturn).where(OrderReturn.id == id)
            )
            order_return = order_return.first()

            if order_return:
                await self.session.delete(order_return)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_order_return failed: {e}")
            raise