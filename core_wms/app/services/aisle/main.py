import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.aisles import Aisle

logger = logging.getLogger(__name__)

@final
class AisleService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_aisles(self) -> List[Aisle]:
        try:
            result = await self.session.execute(select(Aisle))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_aisles failed: {e}")
            raise

    async def upsert_aisle(self, args: dict) -> Aisle:
        try:
            aisle = None
            if args.get('id'):
                result = await self.session.execute(
                    select(Aisle).where(Aisle.id == args['id'])
                )
                aisle = result.scalars().first()
            
            if aisle:
                for key, value in args.items():
                    if hasattr(aisle, key) and value is not None:
                        setattr(aisle, key, value)
            else:
                aisle = Aisle(**args)
                self.session.add(aisle)
            
            await self.session.commit()
            await self.session.refresh(aisle)
            return aisle
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_aisle failed: {e}")
            raise
    
    async def delete_aisle(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(Aisle).where(Aisle.id == id)
            )
            aisle = result.scalars().first()

            if aisle:
                await self.session.delete(aisle)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_aisle failed: {e}")
            raise