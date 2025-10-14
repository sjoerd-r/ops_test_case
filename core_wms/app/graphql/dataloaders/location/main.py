from typing import final
from sqlmodel import Session, select

from core_wms.app.sqlalchemy.models.inventory_levels import InventoryLevel
from core_wms.app.sqlalchemy.models.stores import Store
from core_wms.app.sqlalchemy.models.fulfillment_orders import FulfillmentOrder
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader

@final
class InventoryLevelsLoader(SQLAListLoader[int, InventoryLevel]):
    column = InventoryLevel.location_id
    stmt = select(InventoryLevel)

@final
class FulfillmentOrdersLoader(SQLAListLoader[int, FulfillmentOrder]):
    column = FulfillmentOrder.assigned_location_id
    stmt = select(FulfillmentOrder)

@final
class StoreLoader(SQLALoader[int, Store]):
    column = Store.id
    stmt = select(Store)

@final
class LocationLoaders:
    def __init__(self, session: Session):
        self.inventory_levels = InventoryLevelsLoader(session)
        self.fulfillment_orders = FulfillmentOrdersLoader(session)
        self.store = StoreLoader(session)
