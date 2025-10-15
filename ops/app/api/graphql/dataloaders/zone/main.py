from typing import final
from sqlmodel import Session, select

from ops.app.sqlalchemy.models.aisles import Aisle
from ops.app.sqlalchemy.models.warehouses import Warehouse
from ops.app.api.graphql.dataloaders.base import SQLALoader, SQLAListLoader

@final
class AislesLoader(SQLAListLoader[int, Aisle]):
    column = Aisle.zone_id
    stmt = select(Aisle)

@final
class WarehouseLoader(SQLALoader[int, Warehouse]):
    column = Warehouse.id
    stmt = select(Warehouse)

@final
class ZoneLoaders:
    def __init__(self, session: Session):
        self.aisles = AislesLoader(session)
        self.warehouse = WarehouseLoader(session)
