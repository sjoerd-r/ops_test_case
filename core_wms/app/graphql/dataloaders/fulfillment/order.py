from typing import final
from sqlmodel import Session, select
from core_wms.app.graphql.dataloaders.base import SQLALoader
from core_wms.app.sqlalchemy.models.fulfillment_orders import FulfillmentOrder
from core_wms.app.sqlalchemy.models.orders import Order
from core_wms.app.sqlalchemy.models.fulfillment_services import FulfillmentService

@final
class FulfillmentOrderLoader(SQLALoader[int, FulfillmentOrder]):
    column = FulfillmentOrder.id
    stmt = select(FulfillmentOrder)

@final
class OrderLoader(SQLALoader[int, Order]):
    column = Order.id
    stmt = select(Order)

@final
class FulfillmentServiceLoader(SQLALoader[int, FulfillmentService]):
    column = FulfillmentService.id
    stmt = select(FulfillmentService)

@final
class FulfillmentOrderLoaders:
    def __init__(self, session: Session):
        self.fulfillment_order = FulfillmentOrderLoader(session)
        self.order = OrderLoader(session)
        self.fulfillment_service = FulfillmentServiceLoader(session)
