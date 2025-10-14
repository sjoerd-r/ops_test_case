import logging
from typing import Any

import dramatiq

from core_wms.app.sqlalchemy.session import db

from core_wms.app.services.product.main import ProductService as Product

from core_wms.app.services.product.dto import ProductInput, ProductRelated

logger = logging.getLogger(__name__)


@dramatiq.actor(max_retries=5, min_backoff=60000)
async def upsert_product(shopify_data: dict[str, Any], store_id: int) -> None:
    """
    Receive raw shopify data and store id, call service method and transform
    with the respective data transfer object (dto).
    """
    try:
        async with db.get_async_session() as session:
            return await Product(session).upsert_product(
                ProductInput.from_shopify(shopify_data, store_id),
                ProductRelated.from_shopify(shopify_data),
            )

    except Exception as exc:
        logger.exception(f"Failed to upsert product: {exc}")
        raise


@dramatiq.actor(max_retries=3, min_backoff=30000)
async def delete_product(shopify_product_id: int, store_id: int) -> None:
    try:
        async with db.get_async_session() as session:
            await Product(session).delete_product(
                ProductInput(
                    store_id=store_id, shopify_product_id=shopify_product_id
                )
            )

    except Exception as exc:
        logger.exception(f"Failed to delete product: {exc}")
        raise
