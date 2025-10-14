import logging
from typing import Any

import dramatiq
import asyncio

from core_wms.app.sqlalchemy.session import db
from core_wms.app.services.order.main import OrderService as Order
from core_wms.app.services.order.dto import OrderInput, OrderRelated

logger = logging.getLogger(__name__)


@dramatiq.actor(max_retries=5, min_backoff=60000)
def upsert_order(shopify_data: dict[str, Any], store_id: int) -> None:
    """
    Receive raw shopify data and store id, call service method and transform
    with the respective data transfer object (dto).
    """

    async def _run():
        async with db.get_async_session() as session:
            return await Order(session).upsert_order(
                OrderInput.from_shopify(shopify_data, store_id),
                OrderRelated.from_shopify(shopify_data),
            )

    try:
        asyncio.run(_run())
    except Exception as exc:
        logger.exception("Failed to upsert order")
        raise exc


@dramatiq.actor(max_retries=3, min_backoff=30000)
def delete_order(shopify_order_id: int, store_id: int) -> None:
    """
    Delete order by shopify order id and store id.
    """

    async def _run():
        async with db.get_async_session() as session:
            await Order(session).delete_order(
                OrderInput(
                    store_id=store_id, shopify_order_id=shopify_order_id
                )
            )

    try:
        asyncio.run(_run())
    except Exception as exc:
        logger.exception("Failed to delete order")
        raise exc
