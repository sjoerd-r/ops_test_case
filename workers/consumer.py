#!/usr/bin/env python

from core_wms.app.tasks.broker import redis_broker

import core_wms.app.tasks.product.main
import core_wms.app.tasks.customer.main
import core_wms.app.tasks.order.main
import core_wms.app.tasks.inventory_item.main
import core_wms.app.tasks.inventory_level.main
import core_wms.app.tasks.fulfillment_order.main
import core_wms.app.tasks.location.main

if __name__ == "__main__":
    from dramatiq.cli import main
    main()