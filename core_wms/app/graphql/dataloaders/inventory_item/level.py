from typing import final
from sqlmodel import Session, select

from core_wms.app.sqlalchemy.models.stores import Store
from core_wms.app.sqlalchemy.models.locations import Location
from core_wms.app.sqlalchemy.models.inventory_items import InventoryItem
from core_wms.app.graphql.dataloaders.base import SQLALoader

@final
class StoreLoader(SQLALoader[int, Store]):
    column = Store.id
    stmt = select(Store)

@final
class LocationLoader(SQLALoader[int, Location]):
    column = Location.id
    stmt = select(Location)

@final
class InventoryItemLoader(SQLALoader[int, InventoryItem]):
    column = InventoryItem.id
    stmt = select(InventoryItem)

@final
class InventoryLevelLoaders:
    def __init__(self, session: Session):
        self.store = StoreLoader(session)
        self.location = LocationLoader(session)
        self.inventory_item = InventoryItemLoader(session)
