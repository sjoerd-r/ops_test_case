from typing import final
from sqlmodel import Session, select
from core_wms.app.graphql.dataloaders.base import SQLALoader
from core_wms.app.sqlalchemy.models.orders import Order
from core_wms.app.sqlalchemy.models.products import Product
from core_wms.app.sqlalchemy.models.product_variants import ProductVariant

@final
class OrderLoader(SQLALoader[int, Order]):
    column = Order.id
    stmt = select(Order)

@final
class ProductLoader(SQLALoader[int, Product]):
    column = Product.id
    stmt = select(Product)

@final
class ProductVariantLoader(SQLALoader[int, ProductVariant]):
    column = ProductVariant.id
    stmt = select(ProductVariant)

@final
class OrderLineItemLoaders:
    def __init__(self, session: Session):
        self.order = OrderLoader(session)
        self.product = ProductLoader(session)
        self.variant = ProductVariantLoader(session)
