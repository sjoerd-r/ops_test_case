from strawberry.fastapi import BaseContext
from starlette.requests import Request
from collections.abc import AsyncGenerator
import logging
from functools import cached_property

from core_wms.app.sqlalchemy.session import db

from core_wms.app.graphql.dataloaders.warehouse.main import (
    WarehouseLoaders,
)
from core_wms.app.graphql.dataloaders.store.main import StoreLoaders
from core_wms.app.graphql.dataloaders.aisle.main import AisleLoaders
from core_wms.app.graphql.dataloaders.batch.main import BatchLoaders
from core_wms.app.graphql.dataloaders.bin.main import BinLoaders
from core_wms.app.graphql.dataloaders.carrier.main import CarrierLoaders
from core_wms.app.graphql.dataloaders.channel.main import ChannelLoaders
from core_wms.app.graphql.dataloaders.customer.main import CustomerLoaders
from core_wms.app.graphql.dataloaders.location.main import LocationLoaders
from core_wms.app.graphql.dataloaders.order.main import OrderLoaders
from core_wms.app.graphql.dataloaders.pallet.main import PalletLoaders
from core_wms.app.graphql.dataloaders.product.main import ProductLoaders
from core_wms.app.graphql.dataloaders.rack.main import RackLoaders
from core_wms.app.graphql.dataloaders.supplier.main import SupplierLoaders
from core_wms.app.graphql.dataloaders.zone.main import ZoneLoaders

from core_wms.app.graphql.dataloaders.purchase_order.main import (
    PurchaseOrderLoaders,
)
from core_wms.app.graphql.dataloaders.shipping_zone.main import (
    ShippingZoneLoaders,
)
from core_wms.app.graphql.dataloaders.inventory_item.main import (
    InventoryItemLoaders,
)
from core_wms.app.graphql.dataloaders.fulfillment_service.main import (
    FulfillmentServiceLoaders,
)
from core_wms.app.graphql.dataloaders.bin_position.main import (
    BinPositionLoaders,
)
from core_wms.app.graphql.dataloaders.inventory_level.main import (
    InventoryLevelLoaders,
)
from core_wms.app.graphql.dataloaders.inventory_adjustment.main import (
    InventoryAdjustmentLoaders,
)
from core_wms.app.graphql.dataloaders.product_variant.main import (
    ProductVariantLoaders,
)
from core_wms.app.graphql.dataloaders.purchase_order_line_item.main import (
    PurchaseOrderLineItemLoaders,
)
from core_wms.app.graphql.dataloaders.pallet_stock.main import (
    PalletStockLoaders,
)

logger = logging.getLogger(__name__)


class Context(BaseContext):
    """General base class for context

    Consider adding even more selective lazy loading for rarely used
    loaders.
    """

    def __init__(self, session):
        self.session = session

    @cached_property
    def loaders(self):
        return LoaderRegistry(
            warehouse=WarehouseLoaders(self.session),
            store=StoreLoaders(self.session),
            aisle=AisleLoaders(self.session),
            batch=BatchLoaders(self.session),
            bin=BinLoaders(self.session),
            carrier=CarrierLoaders(self.session),
            channel=ChannelLoaders(self.session),
            customer=CustomerLoaders(self.session),
            inventory_item=InventoryItemLoaders(self.session),
            location=LocationLoaders(self.session),
            order=OrderLoaders(self.session),
            pallet=PalletLoaders(self.session),
            product=ProductLoaders(self.session),
            purchase_order=PurchaseOrderLoaders(self.session),
            rack=RackLoaders(self.session),
            shipping_zone=ShippingZoneLoaders(self.session),
            supplier=SupplierLoaders(self.session),
            zone=ZoneLoaders(self.session),
            fulfillment_service=FulfillmentServiceLoaders(self.session),
            bin_position=BinPositionLoaders(self.session),
            inventory_level=InventoryLevelLoaders(self.session),
            inventory_adjustment=InventoryAdjustmentLoaders(self.session),
            product_variant=ProductVariantLoaders(self.session),
            purchase_order_line_item=PurchaseOrderLineItemLoaders(
                self.session
            ),
            pallet_stock=PalletStockLoaders(self.session),
        )


class LoaderRegistry:
    def __init__(self, **loaders):
        for name, loader in loaders.items():
            setattr(self, name, loader)


async def get_context(request: Request) -> AsyncGenerator[Context, None]:
    async for session in db.get_async_session():
        try:
            yield Context(session)
        except Exception as e:
            logger.error(f"Context creation failed: {e}")
            await session.rollback()
            raise
        finally:
            try:
                await session.close()
            except Exception as e:
                logger.error(f"Session cleanup failed: {e}")
