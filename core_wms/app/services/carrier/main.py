import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.carriers import Carrier

logger = logging.getLogger(__name__)

@final
class CarrierService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_carriers(self) -> List[Carrier]:
        try:
            result = await self.session.execute(select(Carrier))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_carriers failed: {e}")
            raise

    async def upsert_carrier(self, args: dict) -> Carrier:
        try:
            carrier = None
            if args.get('id'):
                result = await self.session.execute(
                    select(Carrier).where(Carrier.id == args['id'])
                )
                carrier = result.scalars().first()
            
            if carrier:
                for key, value in args.items():
                    if hasattr(carrier, key) and value is not None:
                        setattr(carrier, key, value)
            else:
                carrier = Carrier(**args)
                self.session.add(carrier)
            
            await self.session.commit()
            await self.session.refresh(carrier)
            return carrier
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_carrier failed: {e}")
            raise
    
    async def delete_carrier(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(Carrier).where(Carrier.id == id)
            )
            carrier = result.scalars().first()
            
            if carrier:
                await self.session.delete(carrier)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_carrier failed: {e}")
            raise