import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.bin_positions import BinPosition

logger = logging.getLogger(__name__)

@final
class BinPositionService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_bin_positions(self) -> List[BinPosition]:
        try:
            result = await self.session.execute(select(BinPosition))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_bin_positions failed: {e}")
            raise

    async def upsert_bin_position(self, args: dict) -> BinPosition:
        try:
            bin_position = None
            if args.get('id'):
                result = await self.session.execute(
                    select(BinPosition).where(BinPosition.id == args['id'])
                )
                bin_position = result.scalars().first()
            
            if bin_position:
                for key, value in args.items():
                    if hasattr(bin_position, key) and value is not None:
                        setattr(bin_position, key, value)
            else:
                bin_position = BinPosition(**args)
                self.session.add(bin_position)
            
            await self.session.commit()
            await self.session.refresh(bin_position)
            return bin_position
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_bin_position failed: {e}")
            raise
    
    async def delete_bin_position(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(BinPosition).where(BinPosition.id == id)
            )
            bin_position = result.scalars().first()
            
            if bin_position:
                await self.session.delete(bin_position)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_bin_position failed: {e}")
            raise