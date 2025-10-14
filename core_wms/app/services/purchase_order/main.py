import logging
from typing import List
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.purchase_orders import PurchaseOrder

logger = logging.getLogger(__name__)

@final
class PurchaseOrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_purchase_orders(self) -> List[PurchaseOrder]:
        try:
            result = await self.session.execute(select(PurchaseOrder))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_purchase_orders failed: {e}")
            raise

    async def upsert_purchase_order(self, args: dict) -> PurchaseOrder:
        try:
            purchase_order = None
            if args.get('id'):
                result = await self.session.execute(
                    select(PurchaseOrder).where(PurchaseOrder.id == args['id'])
                )
                purchase_order = result.scalars().first()

            if purchase_order:
                for key, value in args.items():
                    if hasattr(purchase_order, key) and value is not None:
                        setattr(purchase_order, key, value)
            else:
                purchase_order = PurchaseOrder(**args)
                self.session.add(purchase_order)
            
            await self.session.commit()
            await self.session.refresh(purchase_order)
            return purchase_order
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_purchase_order failed: {e}")
            raise
    
    async def delete_purchase_order(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(PurchaseOrder).where(PurchaseOrder.id == id)
            )
            purchase_order = result.scalars().first()

            if purchase_order:
                await self.session.delete(purchase_order)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_purchase_order failed: {e}")
            raise