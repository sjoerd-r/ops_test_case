import strawberry
from strawberry.extensions import ParserCache, ValidationCache

from core_wms.app.graphql.schemas.store.main import StoreQueries, StoreMutations, StoreSubscriptions
from core_wms.app.graphql.schemas.warehouse.main import WarehouseQueries, WarehouseMutations, WarehouseSubscriptions
from core_wms.app.graphql.schemas.order.main import OrderQueries, OrderMutations, OrderSubscriptions
from core_wms.app.graphql.schemas.batch.main import BatchQueries, BatchMutations, BatchSubscriptions
from core_wms.app.graphql.schemas.pallet.main import PalletQueries, PalletMutations, PalletSubscriptions
from core_wms.app.graphql.schemas.zone.main import ZoneQueries, ZoneMutations, ZoneSubscriptions
from core_wms.app.graphql.schemas.aisle.main import AisleQueries, AisleMutations, AisleSubscriptions
from core_wms.app.graphql.schemas.rack.main import RackQueries, RackMutations, RackSubscriptions
from core_wms.app.graphql.schemas.supplier.main import SupplierQueries, SupplierMutations, SupplierSubscriptions
from core_wms.app.graphql.schemas.channel.main import ChannelQueries, ChannelMutations, ChannelSubscriptions
from core_wms.app.graphql.schemas.location.main import LocationQueries, LocationMutations, LocationSubscriptions
from core_wms.app.graphql.schemas.product.main import ProductQueries, ProductMutations, ProductSubscriptions
from core_wms.app.graphql.schemas.bin.main import BinQueries, BinMutations, BinSubscriptions
from core_wms.app.graphql.schemas.inventory_item.main import InventoryItemQueries, InventoryItemMutations, InventoryItemSubscriptions
from core_wms.app.graphql.schemas.inventory_level.main import InventoryLevelQueries, InventoryLevelMutations, InventoryLevelSubscriptions
from core_wms.app.graphql.schemas.customer.main import CustomerQueries, CustomerMutations, CustomerSubscriptions
from core_wms.app.graphql.schemas.carrier.main import CarrierQueries, CarrierMutations, CarrierSubscriptions
from core_wms.app.graphql.schemas.bin_position.main import BinPositionQueries, BinPositionMutations, BinPositionSubscriptions
from core_wms.app.graphql.schemas.fulfillment_order.main import FulfillmentOrderQueries, FulfillmentOrderMutations, FulfillmentOrderSubscriptions
from core_wms.app.graphql.schemas.fulfillment_service.main import FulfillmentServiceQueries, FulfillmentServiceMutations, FulfillmentServiceSubscriptions
from core_wms.app.graphql.schemas.fulfillment_line_item.main import FulfillmentLineItemQueries, FulfillmentLineItemMutations, FulfillmentLineItemSubscriptions
from core_wms.app.graphql.schemas.product.variant import ProductVariantQueries, ProductVariantMutations, ProductVariantSubscriptions
from core_wms.app.graphql.schemas.product.option import ProductOptionQueries, ProductOptionMutations, ProductOptionSubscriptions
from core_wms.app.graphql.schemas.product.media import ProductMediaQueries, ProductMediaMutations, ProductMediaSubscriptions
from core_wms.app.graphql.schemas.pallet.stock import PalletStockQueries, PalletStockMutations, PalletStockSubscriptions
from core_wms.app.graphql.schemas.shipping_zone.main import ShippingZoneQueries, ShippingZoneMutations, ShippingZoneSubscriptions
from core_wms.app.graphql.schemas.inventory_adjustment.main import InventoryAdjustmentQueries, InventoryAdjustmentMutations, InventoryAdjustmentSubscriptions
from core_wms.app.graphql.schemas.purchase_order.main import PurchaseOrderQueries, PurchaseOrderMutations, PurchaseOrderSubscriptions
from core_wms.app.graphql.schemas.purchase_order.line_item import PurchaseOrderLineItemQueries, PurchaseOrderLineItemMutations, PurchaseOrderLineItemSubscriptions
from core_wms.app.graphql.schemas.fulfillment_event.main import FulfillmentEventQueries, FulfillmentEventMutations, FulfillmentEventSubscriptions
from core_wms.app.graphql.schemas.customer.address import CustomerAddressQueries
from core_wms.app.graphql.schemas.location.address import LocationAddressQueries
from core_wms.app.graphql.schemas.fulfillment_order_line_item.main import FulfillmentOrderLineItemQueries, FulfillmentOrderLineItemMutations, FulfillmentOrderLineItemSubscriptions
from core_wms.app.graphql.schemas.order.address import OrderAddressQueries, OrderAddressMutations, OrderAddressSubscriptions
from core_wms.app.graphql.schemas.order.discount import OrderDiscountQueries, OrderDiscountMutations, OrderDiscountSubscriptions
from core_wms.app.graphql.schemas.order.fulfillment import OrderFulfillmentQueries, OrderFulfillmentMutations, OrderFulfillmentSubscriptions
from core_wms.app.graphql.schemas.order.line_item import OrderLineItemQueries, OrderLineItemMutations, OrderLineItemSubscriptions
from core_wms.app.graphql.schemas.order.order_return import OrderReturnQueries, OrderReturnMutations, OrderReturnSubscriptions
from core_wms.app.graphql.schemas.order.refund import OrderRefundQueries, OrderRefundMutations, OrderRefundSubscriptions
from core_wms.app.graphql.schemas.order.shipping_line import OrderShippingLineQueries, OrderShippingLineMutations, OrderShippingLineSubscriptions
from core_wms.app.graphql.schemas.order.tax import OrderTaxQueries, OrderTaxMutations, OrderTaxSubscriptions

from core_wms.app.graphql.extensions import AddValidationRules, EnumValidationRule

@strawberry.type
class Query(
    StoreQueries,
    WarehouseQueries,
    ZoneQueries,
    AisleQueries,
    RackQueries,
    BatchQueries,
    PalletQueries,
    OrderQueries,
    SupplierQueries,
    ChannelQueries,
    LocationQueries,
    ProductQueries,
    BinQueries,
    InventoryItemQueries,
    InventoryLevelQueries,
    CustomerQueries,
    CarrierQueries,
    BinPositionQueries,
    FulfillmentOrderQueries,
    FulfillmentServiceQueries,
    FulfillmentLineItemQueries,
    ProductVariantQueries,
    ProductOptionQueries,
    ProductMediaQueries,
    PalletStockQueries,
    ShippingZoneQueries,
    InventoryAdjustmentQueries,
    PurchaseOrderQueries,
    PurchaseOrderLineItemQueries,
    FulfillmentEventQueries,
    CustomerAddressQueries,
    LocationAddressQueries,
    FulfillmentOrderLineItemQueries,
    OrderAddressQueries,
    OrderDiscountQueries,
    OrderFulfillmentQueries,
    OrderLineItemQueries,
    OrderReturnQueries,
    OrderRefundQueries,
    OrderShippingLineQueries,
    OrderTaxQueries,
):
    @strawberry.field
    async def health_check(self) -> str:
        return "OK"

@strawberry.type
class Mutation(
    StoreMutations,
    WarehouseMutations,
    ZoneMutations,
    AisleMutations,
    RackMutations,
    BatchMutations,
    PalletMutations,
    OrderMutations,
    SupplierMutations,
    ChannelMutations,
    LocationMutations,
    ProductMutations,
    BinMutations,
    InventoryItemMutations,
    InventoryLevelMutations,
    CustomerMutations,
    CarrierMutations,
    BinPositionMutations,
    FulfillmentOrderMutations,
    FulfillmentServiceMutations,
    FulfillmentLineItemMutations,
    ProductVariantMutations,
    ProductOptionMutations,
    ProductMediaMutations,
    PalletStockMutations,
    ShippingZoneMutations,
    InventoryAdjustmentMutations,
    PurchaseOrderMutations,
    PurchaseOrderLineItemMutations,
    FulfillmentEventMutations,
    FulfillmentOrderLineItemMutations,
    OrderAddressMutations,
    OrderDiscountMutations,
    OrderFulfillmentMutations,
    OrderLineItemMutations,
    OrderReturnMutations,
    OrderRefundMutations,
    OrderShippingLineMutations,
    OrderTaxMutations,
):
    pass

@strawberry.type
class Subscription(
    StoreSubscriptions,
    WarehouseSubscriptions,
    ZoneSubscriptions,
    AisleSubscriptions,
    RackSubscriptions,
    BatchSubscriptions,
    PalletSubscriptions,
    OrderSubscriptions,
    SupplierSubscriptions,
    ChannelSubscriptions,
    LocationSubscriptions,
    ProductSubscriptions,
    BinSubscriptions,
    InventoryItemSubscriptions,
    InventoryLevelSubscriptions,
    CustomerSubscriptions,
    CarrierSubscriptions,
    BinPositionSubscriptions,
    FulfillmentOrderSubscriptions,
    FulfillmentServiceSubscriptions,
    FulfillmentLineItemSubscriptions,
    ProductVariantSubscriptions,
    ProductOptionSubscriptions,
    ProductMediaSubscriptions,
    PalletStockSubscriptions,
    ShippingZoneSubscriptions,
    InventoryAdjustmentSubscriptions,
    PurchaseOrderSubscriptions,
    PurchaseOrderLineItemSubscriptions,
    FulfillmentEventSubscriptions,
    FulfillmentOrderLineItemSubscriptions,
    OrderAddressSubscriptions,
    OrderDiscountSubscriptions,
    OrderFulfillmentSubscriptions,
    OrderLineItemSubscriptions,
    OrderReturnSubscriptions,
    OrderRefundSubscriptions,
    OrderShippingLineSubscriptions,
    OrderTaxSubscriptions,
):
    pass

class GraphQLSchema:
    schema = strawberry.federation.Schema(
        query=Query,
        mutation=Mutation,
        subscription=Subscription,
        enable_federation_2=True, 
        extensions=[
            ParserCache(maxsize=1000),
            ValidationCache(maxsize=1000),
            AddValidationRules([EnumValidationRule]),
        ]
    )