import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.bins import Bin

logger = logging.getLogger(__name__)

@final
class BinService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_bins(self) -> List[Bin]:
        try:
            result = await self.session.execute(select(Bin))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_bins failed: {e}")
            raise

    async def upsert_bin(self, args: dict) -> Bin:
        try:
            bin = None
            if args.get('id'):
                result = await self.session.execute(
                    select(Bin).where(Bin.id == args["id"])
                )
                bin = result.scalars().first()
            
            if bin:
                for key, value in args.items():
                    if hasattr(bin, key) and value is not None:
                        setattr(bin, key, value)
            else:
                bin = Bin(**args)
                self.session.add(bin)
            
            await self.session.commit()
            await self.session.refresh(bin)
            return bin
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_bin failed: {e}")
            raise
    
    async def delete_bin(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(Bin).where(Bin.id == id)
            )
            bin = result.scalars().first()
            
            if bin:
                await self.session.delete(bin)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_bin failed: {e}")
            raise