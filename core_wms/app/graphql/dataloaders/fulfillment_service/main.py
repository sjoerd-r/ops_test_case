from typing import final
from sqlmodel import Session, select
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader
from core_wms.app.sqlalchemy.models.fulfillment_services import FulfillmentService

@final
class FulfillmentServiceByIdLoader(SQLALoader[int, FulfillmentService]):
    column = FulfillmentService.id
    stmt = select(FulfillmentService)

@final
class FulfillmentServiceByStoreIdLoader(SQLAListLoader[int, FulfillmentService]):
    column = FulfillmentService.store_id
    stmt = select(FulfillmentService)

@final
class FulfillmentServiceLoaders:
    def __init__(self, session: Session):
        self.by_id = FulfillmentServiceByIdLoader(session)
        self.by_store_id = FulfillmentServiceByStoreIdLoader(session)
