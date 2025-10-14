from typing import final
from sqlmodel import Session, select
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader
from core_wms.app.sqlalchemy.models.purchase_order_line_items import PurchaseOrderLineItem
from core_wms.app.sqlalchemy.models.purchase_orders import PurchaseOrder
from core_wms.app.sqlalchemy.models.product_variants import ProductVariant
from core_wms.app.sqlalchemy.models.pallets import Pallet

@final
class PurchaseOrderLineItemByIdLoader(SQLALoader[int, PurchaseOrderLineItem]):
    column = PurchaseOrderLineItem.id
    stmt = select(PurchaseOrderLineItem)

@final
class PurchaseOrderLineItemByPurchaseOrderIdLoader(SQLAListLoader[int, PurchaseOrderLineItem]):
    column = PurchaseOrderLineItem.purchase_order_id
    stmt = select(PurchaseOrderLineItem)

@final
class PurchaseOrderLineItemByProductVariantIdLoader(SQLAListLoader[int, PurchaseOrderLineItem]):
    column = PurchaseOrderLineItem.product_variant_id
    stmt = select(PurchaseOrderLineItem)

@final
class PurchaseOrderLoader(SQLALoader[int, PurchaseOrder]):
    column = PurchaseOrder.id
    stmt = select(PurchaseOrder)

@final
class ProductVariantLoader(SQLALoader[int, ProductVariant]):
    column = ProductVariant.id
    stmt = select(ProductVariant)

@final
class PalletsLoader(SQLAListLoader[int, Pallet]):
    column = Pallet.purchase_order_line_item_id
    stmt = select(Pallet)

@final
class PurchaseOrderLineItemLoaders:
    def __init__(self, session: Session):
        self.by_id = PurchaseOrderLineItemByIdLoader(session)
        self.by_purchase_order_id = PurchaseOrderLineItemByPurchaseOrderIdLoader(session)
        self.by_product_variant_id = PurchaseOrderLineItemByProductVariantIdLoader(session)
        self.purchase_order = PurchaseOrderLoader(session)
        self.product_variant = ProductVariantLoader(session)
        self.pallets = PalletsLoader(session)
