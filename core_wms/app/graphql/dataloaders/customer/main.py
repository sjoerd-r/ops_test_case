from typing import final
from sqlmodel import Session, select
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader
from core_wms.app.sqlalchemy.models.customer_addresses import CustomerAddress
from core_wms.app.sqlalchemy.models.orders import Order
from core_wms.app.sqlalchemy.models.stores import Store

@final
class CustomerAddressesLoader(SQLAListLoader[int, CustomerAddress]):
    column = CustomerAddress.customer_id
    stmt = select(CustomerAddress)

@final
class CustomerOrdersLoader(SQLAListLoader[int, Order]):
    column = Order.customer_id
    stmt = select(Order)

@final
class StoreLoader(SQLALoader[int, Store]):
    column = Store.id
    stmt = select(Store)

@final
class CustomerLoaders:
    def __init__(self, session: Session):
        self.addresses = CustomerAddressesLoader(session)
        self.orders = CustomerOrdersLoader(session)
        self.store = StoreLoader(session)
