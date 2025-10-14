import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select


from core_wms.app.sqlalchemy.models.batches import Batch

logger = logging.getLogger(__name__)

@final
class BatchService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_batches(self) -> List[Batch]:
        try:
            result = await self.session.execute(select(Batch))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_batches failed: {e}")
            raise

    async def upsert_batch(self, args: dict) -> Batch:
        try:
            result = await self.session.execute(select(Batch).where(
                Batch.warehouse_id == args["warehouse_id"],
                Batch.lot == args["lot"]
            ))
            batch = result.scalars().first()
            
            if batch:
                for key, value in args.items():
                    if hasattr(batch, key):
                        setattr(batch, key, value)
            else:
                batch = Batch(**args)
                self.session.add(batch)
                
            await self.session.commit()
            await self.session.refresh(batch)
            return batch
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_batch failed: {e}")
            raise

    async def delete_batch(self, id: int) -> bool:
        try:
            result = await self.session.execute(select(Batch).where(Batch.id == id))
            batch = result.scalars().first()

            if batch:
                await self.session.delete(batch)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_batch failed: {e}")
            raise