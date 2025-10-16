from types import SimpleNamespace
from strawberry.fastapi import BaseContext

from ops.app.core.db import SessionLocal
from ops.app.api.graphql.dataloaders.aisle import AisleLoaders
from ops.app.api.graphql.dataloaders.bin import BinLoaders, BinPositionLoaders
from ops.app.api.graphql.dataloaders.pallet import PalletLoaders, PalletStockLoaders
from ops.app.api.graphql.dataloaders.rack import RackLoaders
from ops.app.api.graphql.dataloaders.warehouse import WarehouseLoaders
from ops.app.api.graphql.dataloaders.zone import ZoneLoaders


class CustomContext(BaseContext):
    def __init__(self, session, loaders):
        self.session = session
        self.loaders = loaders


async def get_context() -> CustomContext:
    if SessionLocal is None:
        raise RuntimeError("Missing database_url environment variable")
    session = SessionLocal()
    loaders = SimpleNamespace(
        aisle=AisleLoaders(session),
        bin=BinLoaders(session),
        bin_position=BinPositionLoaders(session),
        pallet=PalletLoaders(session),
        pallet_stock=PalletStockLoaders(session),
        rack=RackLoaders(session),
        warehouse=WarehouseLoaders(session),
        zone=ZoneLoaders(session),
    )
    return CustomContext(session=session, loaders=loaders)
