from typing import final
from sqlmodel import Session, select
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader
from core_wms.app.sqlalchemy.models.bin_positions import BinPosition

@final
class BinPositionByIdLoader(SQLALoader[int, BinPosition]):
    column = BinPosition.id
    stmt = select(BinPosition)

@final
class BinPositionByBinIdLoader(SQLAListLoader[int, BinPosition]):
    column = BinPosition.bin_id
    stmt = select(BinPosition)

@final
class BinPositionLoaders:
    def __init__(self, session: Session):
        self.by_id = BinPositionByIdLoader(session)
        self.by_bin_id = BinPositionByBinIdLoader(session)
