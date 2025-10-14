from typing import final
from sqlmodel import Session, select
from core_wms.app.sqlalchemy.models.fulfillment_orders import FulfillmentOrder
from core_wms.app.sqlalchemy.models.order_line_items import OrderLineItem
from core_wms.app.graphql.dataloaders.base import SQLALoader

@final
class FulfillmentOrderLoader(SQLALoader[int, FulfillmentOrder]):
    column = FulfillmentOrder.id
    stmt = select(FulfillmentOrder)

@final
class OrderLineItemLoader(SQLALoader[int, OrderLineItem]):
    column = OrderLineItem.id
    stmt = select(OrderLineItem)

@final
class FulfillmentOrderLineItemLoaders:
    def __init__(self, session: Session):
        self.fulfillment_order = FulfillmentOrderLoader(session)
        self.order_line_item = OrderLineItemLoader(session)
