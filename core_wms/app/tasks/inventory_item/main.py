import logging
from typing import Any

import dramatiq

from core_wms.app.sqlalchemy.session import db
from core_wms.app.services.inventory_item.main import InventoryItemService
from core_wms.app.services.inventory_item.dto import InventoryItemInput

logger = logging.getLogger(__name__)


@dramatiq.actor(max_retries=5, min_backoff=60000)
async def upsert_inventory_item(
    shopify_data: dict[str, Any], variant_id: int | None = None
) -> None:
    """
    Receive raw shopify data and variant id, call service method and transform
    with the respective data transfer object (dto).
    """
    try:
        async with db.get_async_session() as session:
            return await InventoryItemService(session).upsert_inventory_item(
                InventoryItemInput.from_shopify(shopify_data, variant_id)
            )

    except Exception as exc:
        logger.exception(f"Failed to upsert inventory item: {exc}")
        raise


@dramatiq.actor(max_retries=3, min_backoff=30000)
async def delete_inventory_item(
    shopify_inventory_item_id: int, variant_id: int | None = None
) -> None:
    try:
        async with db.get_async_session() as session:
            await InventoryItemService(session).delete_inventory_item(
                InventoryItemInput(
                    shopify_inventory_item_id=shopify_inventory_item_id,
                    variant_id=variant_id,
                )
            )

    except Exception as exc:
        logger.exception(f"Failed to delete inventory item: {exc}")
        raise
