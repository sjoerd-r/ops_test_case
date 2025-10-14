from typing import final
from sqlmodel import Session, select
from ops.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader
from ops.app.sqlalchemy.models.bin_positions import BinPosition
from ops.app.sqlalchemy.models.racks import Rack

@final
class BinPositionsLoader(SQLAListLoader[int, BinPosition]):
    column = BinPosition.bin_id
    stmt = select(BinPosition)

@final
class RackLoader(SQLALoader[int, Rack]):
    column = Rack.id
    stmt = select(Rack)

@final
class BinLoaders:
    def __init__(self, session: Session):
        self.positions = BinPositionsLoader(session)
        self.rack = RackLoader(session)