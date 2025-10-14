#!/usr/bin/env python

from ops.app.tasks.broker import redis_broker

import ops.app.tasks.product.main
import ops.app.tasks.customer.main
import ops.app.tasks.order.main
import ops.app.tasks.inventory_item.main
import ops.app.tasks.inventory_level.main
import ops.app.tasks.fulfillment_order.main
import ops.app.tasks.location.main

if __name__ == "__main__":
    from dramatiq.cli import main
    main()