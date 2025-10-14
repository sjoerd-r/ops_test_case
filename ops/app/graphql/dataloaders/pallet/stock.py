from typing import final
from sqlmodel import Session, select

from ops.app.sqlalchemy.models.pallets import Pallet

from ops.app.graphql.dataloaders.base import SQLALoader

@final
class PalletLoader(SQLALoader[int, Pallet]):
    column = Pallet.id
    stmt = select(Pallet)

@final
class PalletStockLoaders:
    def __init__(self, session: Session):
        self.pallet = PalletLoader(session)