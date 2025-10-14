from typing import final
from sqlmodel import Session, select
from core_wms.app.sqlalchemy.models.purchase_orders import PurchaseOrder
from core_wms.app.sqlalchemy.models.product_variants import ProductVariant
from core_wms.app.graphql.dataloaders.base import SQLALoader

@final
class PurchaseOrderLoader(SQLALoader[int, PurchaseOrder]):
    column = PurchaseOrder.id
    stmt = select(PurchaseOrder)

@final
class ProductVariantLoader(SQLALoader[int, ProductVariant]):
    column = ProductVariant.id
    stmt = select(ProductVariant)

@final
class PurchaseOrderLineItemLoaders:
    def __init__(self, session: Session):
        self.purchase_order = PurchaseOrderLoader(session)
        self.product_variant = ProductVariantLoader(session)
