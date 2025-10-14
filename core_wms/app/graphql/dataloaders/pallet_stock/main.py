from typing import final
from sqlmodel import Session, select
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader
from core_wms.app.sqlalchemy.models.pallet_stock import PalletStock

@final
class PalletStockByIdLoader(SQLALoader[int, PalletStock]):
    column = PalletStock.id
    stmt = select(PalletStock)

@final
class PalletStockByPalletIdLoader(SQLAListLoader[int, PalletStock]):
    column = PalletStock.pallet_id
    stmt = select(PalletStock)

@final
class PalletStockByInventoryItemIdLoader(SQLAListLoader[int, PalletStock]):
    column = PalletStock.inventory_item_id
    stmt = select(PalletStock)

@final
class PalletStockLoaders:
    def __init__(self, session: Session):
        self.by_id = PalletStockByIdLoader(session)
        self.by_pallet_id = PalletStockByPalletIdLoader(session)
        self.by_inventory_item_id = PalletStockByInventoryItemIdLoader(session)
