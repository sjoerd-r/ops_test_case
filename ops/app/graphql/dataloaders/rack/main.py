from typing import final
from sqlmodel import Session, select

from ops.app.sqlalchemy.models.bins import Bin
from ops.app.sqlalchemy.models.aisles import Aisle
from ops.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader

@final
class BinsLoader(SQLAListLoader[int, Bin]):
    column = Bin.rack_id
    stmt = select(Bin)

@final
class AisleLoader(SQLALoader[int, Aisle]):
    column = Aisle.id
    stmt = select(Aisle)

@final
class RackLoaders:
    def __init__(self, session: Session):
        self.bins = BinsLoader(session)
        self.aisle = AisleLoader(session)