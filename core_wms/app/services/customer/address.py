import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.customer_addresses import CustomerAddress

logger = logging.getLogger(__name__)

@final
class CustomerAddressService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_customer_addresses(self) -> List[CustomerAddress]:
        try:
            result = await self.session.execute(select(CustomerAddress))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_customer_addresses failed: {e}")
            raise
    
    async def upsert_customer_address(self, args: dict) -> CustomerAddress:
        try:
            customer_address = None
            if args.get('id'):
                result = await self.session.execute(
                    select(CustomerAddress).where(CustomerAddress.id == args['id'])
                )
                customer_address = result.scalars().first()
            
            if customer_address:
                for key, value in args.items():
                    if hasattr(customer_address, key) and value is not None:
                        setattr(customer_address, key, value)
            else:
                customer_address = CustomerAddress(**args)
                self.session.add(customer_address)
            
            await self.session.commit()
            await self.session.refresh(customer_address)
            return customer_address
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_customer_address failed: {e}")
            raise
    
    async def delete_customer_address(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(CustomerAddress).where(CustomerAddress.id == id)
            )
            customer_address = result.scalars().first()

            if customer_address:
                await self.session.delete(customer_address)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_customer_address failed: {e}")
            raise