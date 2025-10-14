import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.fulfillment_events import FulfillmentEvent

logger = logging.getLogger(__name__)

@final
class FulfillmentEventService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_fulfillment_events(self) -> List[FulfillmentEvent]:
        try:
            result = await self.session.execute(select(FulfillmentEvent))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_fulfillment_events failed: {e}")
            raise

    async def upsert_fulfillment_event(self, args: dict) -> FulfillmentEvent:
        try:
            fulfillment_event = None
            if args.get('id'):
                result = await self.session.execute(
                    select(FulfillmentEvent).where(FulfillmentEvent.id == args['id'])
                )
                fulfillment_event = result.scalars().first()
            
            if fulfillment_event:
                for key, value in args.items():
                    if hasattr(fulfillment_event, key) and value is not None:
                        setattr(fulfillment_event, key, value)
            else:
                fulfillment_event = FulfillmentEvent(**args)
                self.session.add(fulfillment_event)
            
            await self.session.commit()
            await self.session.refresh(fulfillment_event)
            return fulfillment_event
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_fulfillment_event failed: {e}")
            raise
    
    async def delete_fulfillment_event(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(FulfillmentEvent).where(FulfillmentEvent.id == id)
            )
            fulfillment_event = result.scalars().first()

            if fulfillment_event:
                await self.session.delete(fulfillment_event)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_fulfillment_event failed: {e}")
            raise