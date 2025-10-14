import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List
from typing_extensions import final

from core_wms.app.sqlalchemy.models.stores import Store

logger = logging.getLogger(__name__)

@final
class StoreService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_stores(self) -> List[Store]:
        try:
            result = await self.session.execute(select(Store))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_stores failed: {e}")
            raise

    async def upsert_store(self, args: dict) -> Store:
        try:
            store = None
            if args.get('id'):
                result = await self.session.execute(
                    select(Store).where(Store.id == args['id'])
                )
                store = result.scalars().first()

            if store:
                for key, value in args.items():
                    if hasattr(store, key) and value is not None:
                        setattr(store, key, value)
            else:
                store = Store(**args)
                self.session.add(store)
            
            await self.session.commit()
            await self.session.refresh(store)
            return store
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_store failed: {e}")
            raise

    async def delete_store(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(Store).where(Store.id == id)
            )
            store = result.scalars().first()

            if store:
                await self.session.delete(store)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_store failed: {e}")
            raise