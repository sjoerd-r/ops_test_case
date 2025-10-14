import logging
from sqlalchemy.ext.asyncio import AsyncSession
from sqlmodel import select
from typing import List, Dict, Any
from typing_extensions import final

from core_wms.app.sqlalchemy.models.orders import Order

from core_wms.app.services.order.address import OrderAddressService
from core_wms.app.services.order.line_item import OrderLineItemService
from core_wms.app.services.order.shipping_line import OrderShippingLineService
from core_wms.app.services.order.tax import OrderTaxService
from core_wms.app.services.order.discount import OrderDiscountService
from core_wms.app.services.order.fulfillment import OrderFulfillmentService
from core_wms.app.services.order.refund import OrderRefundService
from core_wms.app.services.order.order_return import OrderReturnService

logger = logging.getLogger(__name__)

async def _process_order_related_entities(session: AsyncSession, order_id: int, shopify_data: Dict[str, Any]) -> List[str]:
    processed: List[str] = []

    if shopify_data.get("billing_address"):
        billing_address_args = {
            **shopify_data["billing_address"],
            "order_id": order_id,
            "address_type": "billing",
        }
        await OrderAddressService(session).upsert_order_address(billing_address_args)
        processed.append("billing_address(1)")

    if shopify_data.get("shipping_address"):
        shipping_address_args = {
            **shopify_data["shipping_address"],
            "order_id": order_id,
            "address_type": "shipping",
        }
        await OrderAddressService(session).upsert_order_address(shipping_address_args)
        processed.append("shipping_address(1)")

    if shopify_data.get("line_items"):
        svc = OrderLineItemService(session)
        for line_item in shopify_data["line_items"]:
            args = {**line_item, "order_id": order_id, "shopify_line_item_id": line_item.get("id")}
            await svc.upsert_order_line_item(args)
        processed.append(f"line_items({len(shopify_data['line_items'])})")

    if shopify_data.get("shipping_lines"):
        svc = OrderShippingLineService(session)
        for shipping_line in shopify_data["shipping_lines"]:
            args = {**shipping_line, "order_id": order_id, "shopify_shipping_line_id": shipping_line.get("id")}
            await svc.upsert_order_shipping_line(args)
        processed.append(f"shipping_lines({len(shopify_data['shipping_lines'])})")

    if shopify_data.get("tax_lines"):
        svc = OrderTaxService(session)
        for tax_line in shopify_data["tax_lines"]:
            args = {**tax_line, "order_id": order_id}
            await svc.upsert_order_tax(args)
        processed.append(f"tax_lines({len(shopify_data['tax_lines'])})")

    if shopify_data.get("discount_applications"):
        svc = OrderDiscountService(session)
        for discount in shopify_data["discount_applications"]:
            args = {**discount, "order_id": order_id, "shopify_discount_id": discount.get("id")}
            await svc.upsert_order_discount(args)
        processed.append(f"discounts({len(shopify_data['discount_applications'])})")

    if shopify_data.get("fulfillments"):
        svc = OrderFulfillmentService(session)
        for fulfillment in shopify_data["fulfillments"]:
            args = {
                **fulfillment,
                "order_id": order_id,
                "fulfillment_id": fulfillment.get("id"),
                "shopify_order_id": fulfillment.get("order_id"),
            }
            await svc.upsert_order_fulfillment(args)
        processed.append(f"fulfillments({len(shopify_data['fulfillments'])})")

    if shopify_data.get("refunds"):
        svc = OrderRefundService(session)
        for refund in shopify_data["refunds"]:
            args = {**refund, "order_id": order_id, "shopify_refund_id": refund.get("id")}
            await svc.upsert_order_refund(args)
        processed.append(f"refunds({len(shopify_data['refunds'])})")

    if shopify_data.get("returns"):
        svc = OrderReturnService(session)
        for ret in shopify_data["returns"]:
            args = {**ret, "order_id": order_id, "shopify_return_id": ret.get("id")}
            await svc.upsert_order_return(args)
        processed.append(f"returns({len(shopify_data['returns'])})")

    return processed

@final
class OrderService:
    def __init__(self, session: AsyncSession):
        self.session = session

    async def get_orders(self) -> List[Order]:
        try:
            result = await self.session.execute(select(Order))
            return result.scalars().all()
        except Exception as e:
            logger.exception(f"get_orders failed: {e}")
            raise

    async def upsert_order(self, args: dict) -> Order:
        try:
            order = None
            if args.get('id'):
                result = await self.session.execute(select(Order).where(
                    Order.store_id == args["store_id"],
                    Order.shopify_order_id == args["shopify_order_id"]
                ))
                order = result.scalars().first()

            if order:
                for key, value in args.items():
                    if hasattr(order, key): 
                        setattr(order, key, value)
            else:
                order = Order(**args)
                self.session.add(order)

            await self.session.commit()
            await self.session.refresh(order)
            await _process_order_related_entities(self.session, order.id, args)
            return order
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"upsert_order failed: {e}")
            raise

    async def delete_order(self, id: int) -> bool:
        try:
            order = await self.session.execute(select(Order).where(
                Order.id == id
            ))
            order = order.first()

            if order:
                await self.session.delete(order)
                await self.session.commit()
                return True
            return False
        except Exception as e:
            await self.session.rollback()
            logger.exception(f"delete_order failed: {e}")
            raise