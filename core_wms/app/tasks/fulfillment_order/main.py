import logging
from typing import Any

import dramatiq

from core_wms.app.sqlalchemy.session import db
from core_wms.app.services.fulfillment_order.main import (
    FulfillmentOrderService,
)
from core_wms.app.services.fulfillment_order.dto import FulfillmentOrderInput
from core_wms.app.services.fulfillment_line_item.main import (
    FulfillmentLineItemService,
)
from core_wms.app.services.fulfillment_line_item.dto import (
    FulfillmentLineItemInput,
)

logger = logging.getLogger(__name__)


async def _process_fulfillment_order_related_entities(
    session, fulfillment_order, shopify_data
):
    if shopify_data.get("line_items"):
        for line_item in shopify_data["line_items"]:
            await FulfillmentLineItemService(
                session
            ).upsert_fulfillment_line_item(
                FulfillmentLineItemInput.from_shopify(
                    line_item,
                    fulfillment_order_id=fulfillment_order.id,
                    order_line_item_id=line_item.get("order_line_item_id"),
                )
            )


@dramatiq.actor(max_retries=5, min_backoff=60000)
async def upsert_fulfillment_order(
    shopify_data: dict[str, Any],
    order_id: int,
    assigned_location_id: int | None = None,
    channel_id: int | None = None,
) -> None:
    """
    Receive raw shopify data and related ids, call service method and transform
    with the respective data transfer object (dto).
    """
    try:
        async with db.get_async_session() as session:
            fulfillment_order = await FulfillmentOrderService(
                session
            ).upsert_fulfillment_order(
                FulfillmentOrderInput.from_shopify(
                    shopify_data, order_id, assigned_location_id, channel_id
                )
            )

            await _process_fulfillment_order_related_entities(
                session, fulfillment_order, shopify_data
            )
            return fulfillment_order

    except Exception as exc:
        logger.exception(f"Failed to upsert fulfillment order: {exc}")
        raise


@dramatiq.actor(max_retries=3, min_backoff=30000)
async def delete_fulfillment_order(
    shopify_fulfillment_order_id: int, order_id: int
) -> None:
    try:
        async with db.get_async_session() as session:
            await FulfillmentOrderService(session).delete_fulfillment_order(
                FulfillmentOrderInput(
                    shopify_fulfillment_order_id=shopify_fulfillment_order_id,
                    order_id=order_id,
                )
            )

    except Exception as exc:
        logger.exception(f"Failed to delete fulfillment order: {exc}")
        raise
