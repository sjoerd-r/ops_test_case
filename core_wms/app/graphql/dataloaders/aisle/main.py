from typing import final
from sqlmodel import Session, select
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader
from core_wms.app.sqlalchemy.models.racks import Rack
from core_wms.app.sqlalchemy.models.zones import Zone

@final
class AisleRacksLoader(SQLAListLoader[int, Rack]):
    column = Rack.aisle_id
    stmt = select(Rack)

@final
class ZoneLoader(SQLALoader[int, Zone]):
    column = Zone.id
    stmt = select(Zone)

@final
class AisleLoaders:
    def __init__(self, session: Session):
        self.racks = AisleRacksLoader(session)
        self.zone = ZoneLoader(session)
