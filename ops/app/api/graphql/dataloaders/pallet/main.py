from typing import final
from sqlmodel import Session, select

from ops.app.sqlalchemy.models.pallet_stock import PalletStock
from ops.app.sqlalchemy.models.bin_positions import BinPosition


from ops.app.api.graphql.dataloaders.base import (
    SQLALoader,
    SQLAFilteredLoader,
)

@final
class PalletStockLoader(SQLAFilteredLoader[int, PalletStock]):
    column = PalletStock.pallet_id
    stmt = select(PalletStock)

@final
class BinPositionLoader(SQLALoader[int, BinPosition]):
    column = BinPosition.id
    stmt = select(BinPosition)

@final
class PalletLoaders:
    def __init__(self, session: Session):
        self.stock = PalletStockLoader(session)
        self.bin_position = BinPositionLoader(session)
