from typing import final
from sqlmodel import Session, select

from core_wms.app.sqlalchemy.models.inventory_levels import InventoryLevel
from core_wms.app.graphql.dataloaders.base import SQLALoader

@final
class InventoryLevelLoader(SQLALoader[int, InventoryLevel]):
    column = InventoryLevel.id
    stmt = select(InventoryLevel)

@final  
class InventoryAdjustmentLoaders:
    def __init__(self, session: Session):
        self.inventory_level = InventoryLevelLoader(session)
