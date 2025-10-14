import logging
from typing import Any

import dramatiq

from core_wms.app.sqlalchemy.session import db
from core_wms.app.services.location.main import LocationService
from core_wms.app.services.location.dto import LocationInput

logger = logging.getLogger(__name__)


@dramatiq.actor(max_retries=5, min_backoff=60000)
async def upsert_location(shopify_data: dict[str, Any], store_id: int) -> None:
    """
    Receive raw shopify data and store id, call service method and transform
    with the respective data transfer object (dto).
    """
    try:
        async with db.get_async_session() as session:
            return await LocationService(session).upsert_location(
                LocationInput.from_shopify(shopify_data, store_id)
            )

    except Exception as exc:
        logger.exception(f"Failed to upsert location: {exc}")
        raise


@dramatiq.actor(max_retries=3, min_backoff=30000)
async def delete_location(shopify_location_id: int, store_id: int) -> None:
    try:
        async with db.get_async_session() as session:
            await LocationService(session).delete_location(
                LocationInput(
                    store_id=store_id, shopify_location_id=shopify_location_id
                )
            )

    except Exception as exc:
        logger.exception(f"Failed to delete location: {exc}")
        raise
