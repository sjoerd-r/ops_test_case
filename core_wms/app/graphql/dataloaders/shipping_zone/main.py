from typing import final
from sqlmodel import Session, select
from core_wms.app.sqlalchemy.models.stores import Store
from core_wms.app.graphql.dataloaders.base import SQLALoader

@final
class StoreLoader(SQLALoader[int, Store]):
    column = Store.id
    stmt = select(Store)

@final
class ShippingZoneLoaders:
    def __init__(self, session: Session):
        self.store = StoreLoader(session)
