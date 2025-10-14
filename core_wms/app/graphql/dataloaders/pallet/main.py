from typing import final
from sqlmodel import Session, select

from core_wms.app.sqlalchemy.models.pallet_stock import PalletStock
from core_wms.app.sqlalchemy.models.bin_positions import BinPosition
from core_wms.app.sqlalchemy.models.batches import Batch
from core_wms.app.sqlalchemy.models.product_variants import ProductVariant
from core_wms.app.sqlalchemy.models.purchase_order_line_items import PurchaseOrderLineItem
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAFilteredLoader

@final
class PalletStockLoader(SQLAFilteredLoader[int, PalletStock]):
    column = PalletStock.pallet_id
    stmt = select(PalletStock)

@final
class BinPositionLoader(SQLALoader[int, BinPosition]):
    column = BinPosition.id
    stmt = select(BinPosition)

@final
class BatchLoader(SQLALoader[int, Batch]):
    column = Batch.id
    stmt = select(Batch)

@final
class ProductVariantLoader(SQLALoader[int, ProductVariant]):
    column = ProductVariant.id
    stmt = select(ProductVariant)

@final
class PurchaseOrderLineItemLoader(SQLALoader[int, PurchaseOrderLineItem]):
    column = PurchaseOrderLineItem.id
    stmt = select(PurchaseOrderLineItem)

@final
class PalletLoaders:
    def __init__(self, session: Session):
        self.stock = PalletStockLoader(session)
        self.bin_position = BinPositionLoader(session)
        self.batch = BatchLoader(session)
        self.product_variant = ProductVariantLoader(session)
        self.purchase_order_line_item = PurchaseOrderLineItemLoader(session)
