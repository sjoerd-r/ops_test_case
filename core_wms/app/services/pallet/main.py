import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.pallets import Pallet

logger = logging.getLogger(__name__)

@final
class PalletService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_pallets(self) -> List[Pallet]:
        try:
            result = await self.session.execute(select(Pallet))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_pallets failed: {e}")
            raise

    async def upsert_pallet(self, args: dict) -> Pallet:
        try:
            pallet = None
            if args.get('id'):
                result = await self.session.execute(
                    select(Pallet).where(Pallet.id == args['id'])
                )
                pallet = result.scalars().first()

            if pallet:
                for key, value in args.items():
                    if hasattr(pallet, key) and value is not None:
                        setattr(pallet, key, value)
            else:
                pallet = Pallet(**args)
                self.session.add(pallet)
            
            await self.session.commit()
            await self.session.refresh(pallet)
            return pallet
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_pallet failed: {e}")
            raise
    
    async def delete_pallet(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(Pallet).where(Pallet.id == id)
            )
            pallet = result.scalars().first()

            if pallet:
                await self.session.delete(pallet)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_pallet failed: {e}")
            raise