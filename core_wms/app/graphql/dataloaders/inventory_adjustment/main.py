from typing import final
from sqlmodel import Session, select
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader
from core_wms.app.sqlalchemy.models.inventory_adjustments import InventoryAdjustment

@final
class InventoryAdjustmentByIdLoader(SQLALoader[int, InventoryAdjustment]):
    column = InventoryAdjustment.id
    stmt = select(InventoryAdjustment)

@final
class InventoryAdjustmentByInventoryItemIdLoader(SQLAListLoader[int, InventoryAdjustment]):
    column = InventoryAdjustment.inventory_level_id
    stmt = select(InventoryAdjustment)

@final
class InventoryAdjustmentByInventoryLevelIdLoader(SQLAListLoader[int, InventoryAdjustment]):
    column = InventoryAdjustment.inventory_level_id
    stmt = select(InventoryAdjustment)

@final
class InventoryAdjustmentByUserIdLoader(SQLAListLoader[int, InventoryAdjustment]):
    column = InventoryAdjustment.user_id
    stmt = select(InventoryAdjustment)

@final
class InventoryAdjustmentLoaders:
    def __init__(self, session: Session):
        self.by_id = InventoryAdjustmentByIdLoader(session)
        self.by_inventory_item_id = InventoryAdjustmentByInventoryItemIdLoader(session)
        self.by_inventory_level_id = InventoryAdjustmentByInventoryLevelIdLoader(session)
        self.by_user_id = InventoryAdjustmentByUserIdLoader(session)
