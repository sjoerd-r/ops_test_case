from typing import final
from sqlmodel import Session, select
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader
from core_wms.app.sqlalchemy.models.inventory_levels import InventoryLevel

@final
class InventoryLevelByIdLoader(SQLALoader[int, InventoryLevel]):
    column = InventoryLevel.id
    stmt = select(InventoryLevel)

@final
class InventoryLevelByInventoryItemIdLoader(SQLAListLoader[int, InventoryLevel]):
    column = InventoryLevel.inventory_item_id
    stmt = select(InventoryLevel)

@final
class InventoryLevelByLocationIdLoader(SQLAListLoader[int, InventoryLevel]):
    column = InventoryLevel.location_id
    stmt = select(InventoryLevel)

@final
class InventoryLevelLoaders:
    def __init__(self, session: Session):
        self.by_id = InventoryLevelByIdLoader(session)
        self.by_inventory_item_id = InventoryLevelByInventoryItemIdLoader(session)
        self.by_location_id = InventoryLevelByLocationIdLoader(session)
