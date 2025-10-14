from typing import final
from sqlmodel import Session, select

from core_wms.app.sqlalchemy.models.zones import Zone
from core_wms.app.sqlalchemy.models.purchase_orders import PurchaseOrder
from core_wms.app.sqlalchemy.models.batches import Batch
from core_wms.app.sqlalchemy.models.locations import Location
from core_wms.app.sqlalchemy.models.fulfillment_services import FulfillmentService
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader

@final
class WarehouseZonesLoader(SQLAListLoader[int, Zone]):
    column = Zone.warehouse_id
    stmt = select(Zone)

@final
class WarehousePurchaseOrdersLoader(SQLAListLoader[int, PurchaseOrder]):
    column = PurchaseOrder.warehouse_id
    stmt = select(PurchaseOrder)

@final
class WarehouseBatchesLoader(SQLAListLoader[int, Batch]):
    column = Batch.warehouse_id
    stmt = select(Batch)

@final
class LocationLoader(SQLALoader[int, Location]):
    column = Location.id
    stmt = select(Location)

@final
class FulfillmentServiceLoader(SQLALoader[int, FulfillmentService]):
    column = FulfillmentService.id
    stmt = select(FulfillmentService)

@final
class WarehouseLoaders:
    def __init__(self, session: Session):
        self.zones = WarehouseZonesLoader(session)
        self.purchase_orders = WarehousePurchaseOrdersLoader(session)
        self.batches = WarehouseBatchesLoader(session)
        self.location = LocationLoader(session)
        self.fulfillment_service = FulfillmentServiceLoader(session)
