import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.racks import Rack

logger = logging.getLogger(__name__)

@final
class RackService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_racks(self) -> List[Rack]:
        try:
            result = await self.session.execute(select(Rack))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_racks failed: {e}")
            raise
    
    async def upsert_rack(self, args: dict) -> Rack:
        try:
            rack = None
            if args.get('id'):
                result = await self.session.execute(
                    select(Rack).where(Rack.id == args['id'])
                )
                rack = result.scalars().first()
            
            if rack:
                for key, value in args.items():
                    if hasattr(rack, key) and value is not None:
                        setattr(rack, key, value)
            else:
                rack = Rack(**args)
                self.session.add(rack)
            
            await self.session.commit()
            await self.session.refresh(rack)
            return rack
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_rack failed: {e}")
            raise
    
    async def delete_rack(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(Rack).where(Rack.id == id)
            )
            rack = result.scalars().first()
            
            if rack:
                await self.session.delete(rack)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_rack failed: {e}")
            raise