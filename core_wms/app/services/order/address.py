import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.order_addresses import OrderAddress

logger = logging.getLogger(__name__)

@final
class OrderAddressService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_order_addresses(self) -> List[OrderAddress]:
        try:
            result = await self.session.execute(select(OrderAddress))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_order_addresses failed: {e}")
            raise
    
    async def upsert_order_address(self, args: dict) -> OrderAddress:
        try:
            order_address = None
            if args.get('id'):
                result = await self.session.execute(
                    select(OrderAddress).where(OrderAddress.id == args['id'])
                )
                order_address = result.scalars().first()
            
            if order_address:
                for key, value in args.items():
                    if hasattr(order_address, key) and value is not None:
                        setattr(order_address, key, value)
            else:
                order_address = OrderAddress(**args)
                self.session.add(order_address)
            
            await self.session.commit()
            await self.session.refresh(order_address)
            return order_address
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_order_address failed: {e}")
            raise
    
    async def delete_order_address(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(OrderAddress).where(OrderAddress.id == id)
            )
            order_address = result.scalars().first()
            
            if order_address:
                await self.session.delete(order_address)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_order_address failed: {e}")
            raise