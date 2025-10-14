from typing import final
from sqlmodel import Session, select

from ops.app.sqlalchemy.models.zones import Zone

from ops.app.graphql.dataloaders.base import SQLAListLoader

@final
class WarehouseZonesLoader(SQLAListLoader[int, Zone]):
    column = Zone.warehouse_id
    stmt = select(Zone)

@final
class WarehouseLoaders:
    def __init__(self, session: Session):
        self.zones = WarehouseZonesLoader(session)