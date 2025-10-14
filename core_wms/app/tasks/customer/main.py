import logging
from typing import Any

import dramatiq

from core_wms.app.sqlalchemy.session import db
from core_wms.app.services.customer.main import CustomerService
from core_wms.app.services.customer.dto import CustomerInput

logger = logging.getLogger(__name__)


@dramatiq.actor(max_retries=5, min_backoff=60000)
async def upsert_customer(shopify_data: dict[str, Any], store_id: int) -> None:
    """
    Receive raw shopify data and store id, call service method and transform
    with the respective data transfer object (dto).
    """
    try:
        async with db.get_async_session() as session:
            return await CustomerService(session).upsert_customer(
                CustomerInput.from_shopify(shopify_data, store_id)
            )

    except Exception as exc:
        logger.exception(f"Failed to upsert customer: {exc}")
        raise


@dramatiq.actor(max_retries=3, min_backoff=30000)
async def delete_customer(shopify_customer_id: int, store_id: int) -> None:
    try:
        async with db.get_async_session() as session:
            await CustomerService(session).delete_customer(
                CustomerInput(
                    store_id=store_id, shopify_customer_id=shopify_customer_id
                )
            )

    except Exception as exc:
        logger.exception(f"Failed to delete customer: {exc}")
        raise
