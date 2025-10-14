import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.fulfillment_services import FulfillmentService

logger = logging.getLogger(__name__)

@final
class FulfillmentServiceService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_fulfillment_services(self) -> List[FulfillmentService]:
        try:
            result = await self.session.execute(select(FulfillmentService))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_fulfillment_services failed: {e}")
            raise
    
    async def upsert_fulfillment_service(self, args: dict) -> FulfillmentService:
        try:
            fulfillment_service = None
            if args.get('id'):
                result = await self.session.execute(
                    select(FulfillmentService).where(FulfillmentService.id == args['id'])
                )
                fulfillment_service = result.scalars().first()

            if fulfillment_service:
                for key, value in args.items():
                    if hasattr(fulfillment_service, key) and value is not None:
                        setattr(fulfillment_service, key, value)
            else:
                fulfillment_service = FulfillmentService(**args)
                self.session.add(fulfillment_service)
            
            await self.session.commit()
            await self.session.refresh(fulfillment_service)
            return fulfillment_service
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_fulfillment_service failed: {e}")
            raise
    
    async def delete_fulfillment_service(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(FulfillmentService).where(FulfillmentService.id == id)
            )
            fulfillment_service = result.scalars().first()

            if fulfillment_service:
                await self.session.delete(fulfillment_service)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_fulfillment_service failed: {e}")
            raise