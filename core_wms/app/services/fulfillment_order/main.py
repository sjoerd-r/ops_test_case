import logging
from typing import List, Dict, Any
from typing_extensions import final
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select

from core_wms.app.sqlalchemy.models.fulfillment_orders import FulfillmentOrder

from core_wms.app.services.fulfillment_order.line_item import FulfillmentOrderLineItemService

logger = logging.getLogger(__name__)

async def _process_fulfillment_order_related_entities(session: AsyncSession, fulfillment_order_id: int, shopify_data: Dict[str, Any]) -> List[str]:
    processed: List[str] = []
    if shopify_data.get("line_items"):
        svc = FulfillmentOrderLineItemService(session)
        for line_item in shopify_data["line_items"]:
            args = {
                **line_item,
                "fulfillment_order_id": fulfillment_order_id,
                "shopify_fulfillment_order_line_item_id": line_item.get("id"),
            }
            await svc.upsert_fulfillment_order_line_item(args)
        processed.append(f"line_items({len(shopify_data['line_items'])})")
    return processed

@final
class FulfillmentOrderService:
    def __init__(self, session: AsyncSession):
        self.session = session
    
    async def get_fulfillment_orders(self) -> List[FulfillmentOrder]:
        try:
            result = await self.session.execute(select(FulfillmentOrder))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_fulfillment_orders failed: {e}")
            raise

    async def upsert_fulfillment_order(self, args: dict) -> FulfillmentOrder:
        try:
            fulfillment_order = None
            if args.get('id'):
                result = await self.session.execute(
                    select(FulfillmentOrder).where(FulfillmentOrder.id == args['id'])
                )
                fulfillment_order = result.scalars().first()

            if fulfillment_order:
                for key, value in args.items():
                    if hasattr(fulfillment_order, key) and value is not None:
                        setattr(fulfillment_order, key, value)
            else:
                fulfillment_order = FulfillmentOrder(**args)
                self.session.add(fulfillment_order)
            
            await self.session.commit()
            await self.session.refresh(fulfillment_order)
            await _process_fulfillment_order_related_entities(self.session, fulfillment_order.id, args)
            return fulfillment_order
            
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_fulfillment_order failed: {e}")
            raise
    
    async def delete_fulfillment_order(self, id: int) -> bool:
        try:
            result = await self.session.execute(
                select(FulfillmentOrder).where(FulfillmentOrder.id == id)
            )
            fulfillment_order = result.scalars().first()

            if fulfillment_order:
                await self.session.delete(fulfillment_order)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_fulfillment_order failed: {e}")
            raise