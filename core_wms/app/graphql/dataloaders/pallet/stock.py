from typing import final
from sqlmodel import Session, select

from core_wms.app.sqlalchemy.models.pallets import Pallet
from core_wms.app.sqlalchemy.models.product_variants import ProductVariant
from core_wms.app.sqlalchemy.models.purchase_order_line_items import PurchaseOrderLineItem
from core_wms.app.graphql.dataloaders.base import SQLALoader

@final
class PalletLoader(SQLALoader[int, Pallet]):
    column = Pallet.id
    stmt = select(Pallet)

@final
class ProductVariantLoader(SQLALoader[int, ProductVariant]):
    column = ProductVariant.id
    stmt = select(ProductVariant)

@final
class PurchaseOrderLineItemLoader(SQLALoader[int, PurchaseOrderLineItem]):
    column = PurchaseOrderLineItem.id
    stmt = select(PurchaseOrderLineItem)

@final
class PalletStockLoaders:
    def __init__(self, session: Session):
        self.pallet = PalletLoader(session)
        self.product_variant = ProductVariantLoader(session)
        self.purchase_order_line_item = PurchaseOrderLineItemLoader(session)
