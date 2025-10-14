from typing import final
from sqlmodel import Session, select

from core_wms.app.sqlalchemy.models.product_variants import ProductVariant
from core_wms.app.sqlalchemy.models.product_options import ProductOption
from core_wms.app.sqlalchemy.models.product_media import ProductMedia
from core_wms.app.sqlalchemy.models.stores import Store
from core_wms.app.graphql.dataloaders.base import SQLALoader, SQLAListLoader

@final
class ProductVariantsLoader(SQLAListLoader[int, ProductVariant]):
    column = ProductVariant.product_id
    stmt = select(ProductVariant)

@final
class ProductOptionsLoader(SQLAListLoader[int, ProductOption]):
    column = ProductOption.product_id
    stmt = select(ProductOption)

@final
class ProductMediaLoader(SQLAListLoader[int, ProductMedia]):
    column = ProductMedia.product_id
    stmt = select(ProductMedia)

@final
class StoreLoader(SQLALoader[int, Store]):
    column = Store.id
    stmt = select(Store)

@final
class ProductLoaders:
    def __init__(self, session: Session):
        self.variants = ProductVariantsLoader(session)
        self.options = ProductOptionsLoader(session)
        self.media = ProductMediaLoader(session)
        self.store = StoreLoader(session)
