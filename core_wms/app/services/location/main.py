import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.locations import Location

logger = logging.getLogger(__name__)

@final
class LocationService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_locations(self) -> List[Location]:
        try:
            result = await self.session.execute(select(Location))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_locations failed: {e}")
            raise
    
    async def upsert_location(self, args: dict) -> Location:
        try:
            location = None
            if args.get('id'):
                result = await self.session.execute(
                    select(Location).where(Location.id == args['id'])
                )
                location = result.scalars().first()

            if location:
                for key, value in args.items():
                    if hasattr(location, key) and value is not None:
                        setattr(location, key, value)
            else:
                location = Location(**args)
                self.session.add(location)
            
            await self.session.commit()
            await self.session.refresh(location)
            return location
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_location failed: {e}")
            raise
    
    async def delete_location(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(Location).where(Location.id == id)
            )
            location = result.scalars().first()

            if location:
                await self.session.delete(location)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_location failed: {e}")
            raise