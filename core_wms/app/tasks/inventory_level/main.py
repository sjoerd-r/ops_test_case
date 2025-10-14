import logging
from typing import Any

import dramatiq

from core_wms.app.sqlalchemy.session import db
from core_wms.app.services.inventory_level.main import InventoryLevelService
from core_wms.app.services.inventory_level.dto import InventoryLevelInput

logger = logging.getLogger(__name__)


@dramatiq.actor(max_retries=5, min_backoff=60000)
async def upsert_inventory_level(
    shopify_data: dict[str, Any],
    inventory_item_id: int | None = None,
    location_id: int | None = None,
) -> None:
    """
    Receive raw shopify data and related ids, call service method and transform
    with the respective data transfer object (dto).
    """
    try:
        async with db.get_async_session() as session:
            return await InventoryLevelService(session).upsert_inventory_level(
                InventoryLevelInput.from_shopify(
                    shopify_data, inventory_item_id, location_id
                )
            )

    except Exception as exc:
        logger.exception(f"Failed to upsert inventory level: {exc}")
        raise


@dramatiq.actor(max_retries=3, min_backoff=30000)
async def delete_inventory_level(
    shopify_inventory_level_id: int,
    inventory_item_id: int | None = None,
    location_id: int | None = None,
) -> None:
    try:
        async with db.get_async_session() as session:
            await InventoryLevelService(session).delete_inventory_level(
                InventoryLevelInput(
                    shopify_inventory_level_id=shopify_inventory_level_id,
                    inventory_item_id=inventory_item_id,
                    location_id=location_id,
                )
            )

    except Exception as exc:
        logger.exception(f"Failed to delete inventory level: {exc}")
        raise
