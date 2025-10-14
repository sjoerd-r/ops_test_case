from typing import final
from sqlmodel import Session, select
from ops.app.sqlalchemy.models.bins import Bin
from ops.app.graphql.dataloaders.base import SQLALoader

@final
class BinLoader(SQLALoader[int, Bin]):
    column = Bin.id
    stmt = select(Bin)

@final
class BinPositionLoaders:
    def __init__(self, session: Session):
        self.bin = BinLoader(session)