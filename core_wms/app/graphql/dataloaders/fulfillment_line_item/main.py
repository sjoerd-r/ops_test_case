from typing import final
from sqlmodel import Session, select
from core_wms.app.sqlalchemy.models.order_fulfillments import OrderFulfillment
from core_wms.app.sqlalchemy.models.order_line_items import OrderLineItem
from core_wms.app.sqlalchemy.models.fulfillment_line_items import FulfillmentLineItem
from core_wms.app.graphql.dataloaders.base import SQLALoader

@final
class OrderFulfillmentLoader(SQLALoader[int, OrderFulfillment]):
    column = OrderFulfillment.id
    stmt = select(OrderFulfillment)

@final
class OrderLineItemLoader(SQLALoader[int, OrderLineItem]):
    column = OrderLineItem.id
    stmt = select(OrderLineItem)

@final
class FulfillmentLineItemByIdLoader(SQLALoader[int, FulfillmentLineItem]):
    column = FulfillmentLineItem.id
    stmt = select(FulfillmentLineItem)

@final
class FulfillmentLineItemLoaders:
    def __init__(self, session: Session):
        self.order_fulfillment = OrderFulfillmentLoader(session)
        self.order_line_item = OrderLineItemLoader(session)
        self.load = FulfillmentLineItemByIdLoader(session)
