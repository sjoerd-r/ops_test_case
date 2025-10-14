import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.shipping_zones import ShippingZone

logger = logging.getLogger(__name__)

@final
class ShippingZoneService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_shipping_zones(self) -> List[ShippingZone]:
        try:
            result = await self.session.execute(select(ShippingZone))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_shipping_zones failed: {e}")
            raise
    
    async def upsert_shipping_zone(self, args: dict) -> ShippingZone:
        try:
            shipping_zone = None
            if args.get('id'):
                result = await self.session.execute(
                    select(ShippingZone).where(ShippingZone.id == args['id'])
                )
                shipping_zone = result.scalars().first()

            if shipping_zone:
                for key, value in args.items():
                    if hasattr(shipping_zone, key) and value is not None:
                        setattr(shipping_zone, key, value)
            else:
                shipping_zone = ShippingZone(**args)
                self.session.add(shipping_zone)
            
            await self.session.commit()
            await self.session.refresh(shipping_zone)
            return shipping_zone
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_shipping_zone failed: {e}")
            raise
    
    async def delete_shipping_zone(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(ShippingZone).where(ShippingZone.id == id)
            )
            shipping_zone = result.scalars().first()
            
            if shipping_zone:
                await self.session.delete(shipping_zone)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_shipping_zone failed: {e}")
            raise