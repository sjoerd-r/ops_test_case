import logging
from typing import Any

import dramatiq

from core_wms.app.sqlalchemy.session import db
from core_wms.app.services.purchase_order.main import PurchaseOrderService
from core_wms.app.services.purchase_order.dto import PurchaseOrderInput

logger = logging.getLogger(__name__)


@dramatiq.actor(max_retries=5, min_backoff=60000)
async def upsert_purchase_order(
    shopify_data: dict[str, Any], store_id: int
) -> None:
    """
    Receive raw shopify data and store id, call service method and transform
    with the respective data transfer object (dto).
    """
    try:
        async with db.get_async_session() as session:
            return await PurchaseOrderService(session).upsert_purchase_order(
                PurchaseOrderInput.from_shopify(shopify_data, store_id)
            )

    except Exception as exc:
        logger.exception(f"Failed to upsert purchase order: {exc}")
        raise


@dramatiq.actor(max_retries=3, min_backoff=30000)
async def delete_purchase_order(
    shopify_purchase_order_id: int, store_id: int
) -> None:
    try:
        async with db.get_async_session() as session:
            await PurchaseOrderService(session).delete_purchase_order(
                PurchaseOrderInput(
                    store_id=store_id,
                    shopify_purchase_order_id=shopify_purchase_order_id,
                )
            )

    except Exception as exc:
        logger.exception(f"Failed to delete purchase order: {exc}")
        raise
