from typing import final
from sqlmodel import Session, select

from core_wms.app.sqlalchemy.models.inventory_levels import InventoryLevel
from core_wms.app.sqlalchemy.models.products import Product
from core_wms.app.sqlalchemy.models.locations import Location
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader

@final
class InventoryLevelsLoader(SQLAListLoader[int, InventoryLevel]):
    column = InventoryLevel.inventory_item_id
    stmt = select(InventoryLevel)

@final
class ProductLoader(SQLALoader[int, Product]):
    column = Product.id
    stmt = select(Product)

@final
class LocationLoader(SQLALoader[int, Location]):
    column = Location.id
    stmt = select(Location)

@final
class InventoryItemLoaders:
    def __init__(self, session: Session):
        self.inventory_levels = InventoryLevelsLoader(session)
        self.product = ProductLoader(session)
        self.location = LocationLoader(session)
