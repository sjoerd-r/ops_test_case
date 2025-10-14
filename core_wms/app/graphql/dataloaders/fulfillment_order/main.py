from typing import final
from sqlmodel import Session, select
from core_wms.app.sqlalchemy.models.fulfillment_order_line_items import FulfillmentOrderLineItem
from core_wms.app.sqlalchemy.models.orders import Order
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader

@final
class FulfillmentOrderLineItemsLoader(SQLAListLoader[int, FulfillmentOrderLineItem]):
    column = FulfillmentOrderLineItem.fulfillment_order_id
    stmt = select(FulfillmentOrderLineItem)

@final
class OrderLoader(SQLALoader[int, Order]):
    column = Order.id
    stmt = select(Order)

@final
class FulfillmentOrderLoaders:
    def __init__(self, session: Session):
        self.line_items = FulfillmentOrderLineItemsLoader(session)
        self.order = OrderLoader(session)
