from typing import final
from sqlmodel import Session, select
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader
from core_wms.app.sqlalchemy.models.product_variants import ProductVariant

@final
class ProductVariantByIdLoader(SQLALoader[int, ProductVariant]):
    column = ProductVariant.id
    stmt = select(ProductVariant)

@final
class ProductVariantByProductIdLoader(SQLAListLoader[int, ProductVariant]):
    column = ProductVariant.product_id
    stmt = select(ProductVariant)

@final
class ProductVariantByShopifyIdLoader(SQLALoader[int, ProductVariant]):
    column = ProductVariant.shopify_variant_id
    stmt = select(ProductVariant)

@final
class ProductVariantLoaders:
    def __init__(self, session: Session):
        self.by_id = ProductVariantByIdLoader(session)
        self.by_product_id = ProductVariantByProductIdLoader(session)
        self.by_shopify_id = ProductVariantByShopifyIdLoader(session)
