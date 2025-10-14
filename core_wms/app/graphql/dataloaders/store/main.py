from typing import final
from sqlmodel import Session, select
from core_wms.app.sqlalchemy.models.products import Product
from core_wms.app.sqlalchemy.models.orders import Order
from core_wms.app.sqlalchemy.models.customers import Customer
from core_wms.app.sqlalchemy.models.channels import Channel
from core_wms.app.sqlalchemy.models.locations import Location
from core_wms.app.sqlalchemy.models.carriers import Carrier
from core_wms.app.sqlalchemy.models.fulfillment_services import FulfillmentService
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader

@final
class StoreProductsLoader(SQLAListLoader[int, Product]):
    column = Product.store_id
    stmt = select(Product)

@final
class StoreOrdersLoader(SQLAListLoader[int, Order]):
    column = Order.store_id
    stmt = select(Order)

@final
class StoreCustomersLoader(SQLAListLoader[int, Customer]):
    column = Customer.store_id
    stmt = select(Customer)

@final
class StoreChannelsLoader(SQLAListLoader[int, Channel]):
    column = Channel.store_id
    stmt = select(Channel)

@final
class StoreLocationsLoader(SQLAListLoader[int, Location]):
    column = Location.store_id
    stmt = select(Location)

@final
class StoreCarriersLoader(SQLAListLoader[int, Carrier]):
    column = Carrier.store_id
    stmt = select(Carrier)

@final
class StoreFulfillmentServicesLoader(SQLAListLoader[int, FulfillmentService]):
    column = FulfillmentService.store_id
    stmt = select(FulfillmentService)

@final
class StoreLoaders:
    def __init__(self, session: Session):
        self.products = StoreProductsLoader(session)
        self.orders = StoreOrdersLoader(session)
        self.customers = StoreCustomersLoader(session)
        self.channels = StoreChannelsLoader(session)
        self.locations = StoreLocationsLoader(session)
        self.carriers = StoreCarriersLoader(session)
        self.fulfillment_services = StoreFulfillmentServicesLoader(session)
