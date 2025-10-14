from typing import final
from sqlmodel import Session, select
from core_wms.app.sqlalchemy.models.orders import Order
from core_wms.app.graphql.dataloaders.base import SQLALoader

@final
class OrderLoader(SQLALoader[int, Order]):
    column = Order.id
    stmt = select(Order)

@final
class OrderReturnLoaders:
    def __init__(self, session: Session):
        self.order = OrderLoader(session)
