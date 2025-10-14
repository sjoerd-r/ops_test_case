from typing import final
from sqlmodel import Session, select
from core_wms.app.graphql.dataloaders.base import SQLALoader
from core_wms.app.sqlalchemy.models.fulfillment_services import FulfillmentService

@final
class FulfillmentServiceLoader(SQLALoader[int, FulfillmentService]):
    column = FulfillmentService.id
    stmt = select(FulfillmentService)

@final
class FulfillmentServiceLoaders:
    def __init__(self, session: Session):
        self.fulfillment_service = FulfillmentServiceLoader(session)
