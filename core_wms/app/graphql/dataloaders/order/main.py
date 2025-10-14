from typing import final
from sqlmodel import Session, select

from core_wms.app.sqlalchemy.models.order_line_items import OrderLineItem
from core_wms.app.sqlalchemy.models.order_addresses import OrderAddress
from core_wms.app.sqlalchemy.models.order_fulfillments import OrderFulfillment
from core_wms.app.sqlalchemy.models.order_refunds import OrderRefund
from core_wms.app.sqlalchemy.models.order_returns import OrderReturn
from core_wms.app.sqlalchemy.models.order_taxes import OrderTax
from core_wms.app.sqlalchemy.models.order_discounts import OrderDiscount
from core_wms.app.sqlalchemy.models.order_shipping_lines import OrderShippingLine
from core_wms.app.sqlalchemy.models.customers import Customer
from core_wms.app.sqlalchemy.models.stores import Store

from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader, SQLAFilteredLoader

@final
class OrderLineItemsLoader(SQLAListLoader[int, OrderLineItem]):
    column = OrderLineItem.order_id
    stmt = select(OrderLineItem)

@final
class OrderFulfillmentsLoader(SQLAListLoader[int, OrderFulfillment]):
    column = OrderFulfillment.order_id
    stmt = select(OrderFulfillment)

@final
class OrderRefundsLoader(SQLAListLoader[int, OrderRefund]):
    column = OrderRefund.order_id
    stmt = select(OrderRefund)

@final
class OrderReturnsLoader(SQLAListLoader[int, OrderReturn]):
    column = OrderReturn.order_id
    stmt = select(OrderReturn)

@final
class OrderTaxesLoader(SQLAListLoader[int, OrderTax]):
    column = OrderTax.order_id
    stmt = select(OrderTax)

@final
class OrderDiscountsLoader(SQLAListLoader[int, OrderDiscount]):
    column = OrderDiscount.order_id
    stmt = select(OrderDiscount)

@final
class OrderShippingLinesLoader(SQLAListLoader[int, OrderShippingLine]):
    column = OrderShippingLine.order_id
    stmt = select(OrderShippingLine)

@final
class OrderBillingAddressLoader(SQLAFilteredLoader[int, OrderAddress]):
    column = OrderAddress.order_id
    stmt = select(OrderAddress)
    filter_column = OrderAddress.address_type
    filter_value = 'billing'

@final
class OrderShippingAddressLoader(SQLAFilteredLoader[int, OrderAddress]):
    column = OrderAddress.order_id
    stmt = select(OrderAddress)
    filter_column = OrderAddress.address_type
    filter_value = 'shipping'

@final
class CustomerLoader(SQLALoader[int, Customer]):
    column = Customer.id
    stmt = select(Customer)

@final
class StoreLoader(SQLALoader[int, Store]):
    column = Store.id
    stmt = select(Store)

class OrderLoaders:
    def __init__(self, session: Session):
        self.line_items = OrderLineItemsLoader(session)
        self.billing_address = OrderBillingAddressLoader(session)
        self.shipping_address = OrderShippingAddressLoader(session)
        self.fulfillments = OrderFulfillmentsLoader(session)
        self.refunds = OrderRefundsLoader(session)
        self.returns = OrderReturnsLoader(session)
        self.taxes = OrderTaxesLoader(session)
        self.discounts = OrderDiscountsLoader(session)
        self.shipping_lines = OrderShippingLinesLoader(session)
        self.customer = CustomerLoader(session)
        self.store = StoreLoader(session)