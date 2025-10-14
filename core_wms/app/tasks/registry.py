# isort: skip_file
# ruff: noqa: F401

from core_wms.app.tasks.product.main import upsert_product, delete_product
from core_wms.app.tasks.customer.main import upsert_customer, delete_customer
from core_wms.app.tasks.order.main import upsert_order, delete_order
from core_wms.app.tasks.inventory_item.main import upsert_inventory_item
from core_wms.app.tasks.inventory_level.main import upsert_inventory_level
from core_wms.app.tasks.fulfillment_order.main import upsert_fulfillment_order
from core_wms.app.tasks.location.main import upsert_location

MAP = {
    "products/create": "upsert_product",
    "products/update": "upsert_product",
    "products/delete": "delete_product",
    "customers/create": "upsert_customer",
    "customers/update": "upsert_customer",
    "customers/delete": "delete_customer",
    "orders/create": "upsert_order",
    "orders/updated": "upsert_order",
    "orders/cancelled": "upsert_order",
    "orders/delete": "delete_order",
    "inventory_items/create": "upsert_inventory_item",
    "inventory_items/update": "upsert_inventory_item",
    "inventory_levels/update": "upsert_inventory_level",
    "fulfillment_orders/create": "upsert_fulfillment_order",
    "fulfillment_orders/updated": "upsert_fulfillment_order",
    "locations/create": "upsert_location",
    "locations/update": "upsert_location",
}
