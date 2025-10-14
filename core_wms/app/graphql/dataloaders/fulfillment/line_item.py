from typing import final
from sqlmodel import Session, select
from core_wms.app.graphql.dataloaders.base import SQLALoader
from core_wms.app.sqlalchemy.models.fulfillment_line_items import FulfillmentLineItem
from core_wms.app.sqlalchemy.models.fulfillment_orders import FulfillmentOrder
from core_wms.app.sqlalchemy.models.order_line_items import OrderLineItem

@final
class FulfillmentLineItemLoader(SQLALoader[int, FulfillmentLineItem]):
    column = FulfillmentLineItem.id
    stmt = select(FulfillmentLineItem)

@final
class FulfillmentOrderLoader(SQLALoader[int, FulfillmentOrder]):
    column = FulfillmentOrder.id
    stmt = select(FulfillmentOrder)

@final
class OrderLineItemLoader(SQLALoader[int, OrderLineItem]):
    column = OrderLineItem.id
    stmt = select(OrderLineItem)

@final
class FulfillmentLineItemLoaders:
    def __init__(self, session: Session):
        self.fulfillment_line_item = FulfillmentLineItemLoader(session)
        self.fulfillment_order = FulfillmentOrderLoader(session)
        self.order_line_item = OrderLineItemLoader(session)
