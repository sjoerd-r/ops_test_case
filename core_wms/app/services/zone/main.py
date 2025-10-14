import logging
from typing import Dict, Any, List, Optional, final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.zones import Zone

logger = logging.getLogger(__name__)

@final
class ZoneService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_zones(self) -> List[Zone]:
        try:
            result = await self.session.execute(select(Zone))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_zones failed: {e}")
            raise

    async def upsert_zone(self, args: dict) -> Zone:
        try:
            zone = None
            if args.get('id'):
                result = await self.session.execute(
                    select(Zone).where(Zone.id == args['id'])
                )
                zone = result.scalars().first()

            if zone:
                for key, value in args.items():
                    if hasattr(zone, key) and value is not None:
                        setattr(zone, key, value)
            else:
                zone = Zone(**args)
                self.session.add(zone)
            
            await self.session.commit()
            await self.session.refresh(zone)
            return zone
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_zone failed: {e}")
            raise
    
    async def delete_zone(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(Zone).where(Zone.id == id)
            )
            zone = result.scalars().first()

            if zone:
                await self.session.delete(zone)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_zone failed: {e}")
            raise