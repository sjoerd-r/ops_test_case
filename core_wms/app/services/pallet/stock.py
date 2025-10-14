import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.pallet_stock import PalletStock

logger = logging.getLogger(__name__)

@final
class PalletStockService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_pallet_stocks(self) -> List[PalletStock]:
        try:
            result = await self.session.execute(select(PalletStock))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_pallet_stocks failed: {e}")
            raise

    async def upsert_pallet_stock(self, args: dict) -> PalletStock:
        try:
            pallet_stock = None
            if args.get('id'):
                result = await self.session.execute(
                    select(PalletStock).where(PalletStock.id == args['id'])
                )
                pallet_stock = result.scalars().first()

            if pallet_stock:
                for key, value in args.items():
                    if hasattr(pallet_stock, key) and value is not None:
                        setattr(pallet_stock, key, value)
            else:
                pallet_stock = PalletStock(**args)
                self.session.add(pallet_stock)
            
            await self.session.commit()
            await self.session.refresh(pallet_stock)
            return pallet_stock
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_pallet_stock failed: {e}")
            raise
    
    async def delete_pallet_stock(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(PalletStock).where(PalletStock.id == id)
            )
            pallet_stock = result.scalars().first()

            if pallet_stock:
                await self.session.delete(pallet_stock)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_pallet_stock failed: {e}")
            raise