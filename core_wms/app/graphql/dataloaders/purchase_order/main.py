from typing import List, Optional, final
from sqlmodel import Session, select
from core_wms.app.sqlalchemy.models.purchase_order_line_items import PurchaseOrderLineItem  
from core_wms.app.sqlalchemy.models.stores import Store
from core_wms.app.sqlalchemy.models.warehouses import Warehouse
from core_wms.app.sqlalchemy.models.suppliers import Supplier
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader

@final
class PurchaseOrderLineItemsLoader(SQLAListLoader[int, PurchaseOrderLineItem]):
    column = PurchaseOrderLineItem.purchase_order_id
    stmt = select(PurchaseOrderLineItem)

@final
class StoreLoader(SQLALoader[int, Store]):
    column = Store.id
    stmt = select(Store)

@final
class WarehouseLoader(SQLALoader[int, Warehouse]):
    column = Warehouse.id
    stmt = select(Warehouse)

@final
class SupplierLoader(SQLALoader[int, Supplier]):
    column = Supplier.id
    stmt = select(Supplier)

@final
class PurchaseOrderLoaders:
    def __init__(self, session: Session):
        self.line_items = PurchaseOrderLineItemsLoader(session)
        self.store = StoreLoader(session)
        self.warehouse = WarehouseLoader(session)
        self.supplier = SupplierLoader(session)
