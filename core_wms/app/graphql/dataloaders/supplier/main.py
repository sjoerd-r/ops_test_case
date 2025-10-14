from typing import final
from sqlmodel import Session, select
from core_wms.app.sqlalchemy.models.purchase_orders import PurchaseOrder
from core_wms.app.graphql.dataloaders.base import SQLAListLoader

@final
class SupplierPurchaseOrdersLoader(SQLAListLoader[int, PurchaseOrder]):
    column = PurchaseOrder.supplier_id
    stmt = select(PurchaseOrder)

@final
class SupplierLoaders:
    def __init__(self, session: Session):
        self.purchase_orders = SupplierPurchaseOrdersLoader(session)
