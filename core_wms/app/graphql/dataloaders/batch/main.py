from typing import final
from sqlmodel import Session, select
from core_wms.app.sqlalchemy.models.pallets import Pallet
from core_wms.app.sqlalchemy.models.warehouses import Warehouse
from core_wms.app.sqlalchemy.models.suppliers import Supplier
from core_wms.app.sqlalchemy.models.product_variants import ProductVariant
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader

@final
class BatchPalletsLoader(SQLAListLoader[int, Pallet]):
    column = Pallet.batch_id
    stmt = select(Pallet)

@final
class WarehouseLoader(SQLALoader[int, Warehouse]):
    column = Warehouse.id
    stmt = select(Warehouse)

@final
class SupplierLoader(SQLALoader[int, Supplier]):
    column = Supplier.id
    stmt = select(Supplier)

@final
class ProductVariantLoader(SQLALoader[int, ProductVariant]):
    column = ProductVariant.id
    stmt = select(ProductVariant)

@final
class BatchLoaders:
    def __init__(self, session: Session):
        self.pallets = BatchPalletsLoader(session)
        self.warehouse = WarehouseLoader(session)
        self.supplier = SupplierLoader(session)
        self.product_variant = ProductVariantLoader(session)
